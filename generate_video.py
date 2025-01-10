import os
import shutil
import cv2
import numpy as np
import time
import logging
import sys
if os.name == 'nt':  # Windows
    import msvcrt
else:  # macOS and Linux
    import tty
    import termios

# Setup basic configuration for logging
logging.basicConfig(filename='VideoGenerator.log', filemode='a', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def is_leaf_folder(folder_path):
    """
    判断是否是叶子文件夹：
    如果该文件夹下没有子文件夹，则认为是叶子文件夹
    """
    for item in os.scandir(folder_path):
        if item.is_dir():
            return False
    return True

def rename_images_in_folder(folder_path):
    """
    将文件夹下的所有图片按文件名排序，并重命名为统一前缀 + 序号的形式
    image_0001.jpg, image_0002.jpg ...
    返回重命名后的文件列表
    """
    exts = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif")
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(exts)]
    if not files:
        return []

    # 排序
    files.sort()
    
    # 新建一个用于存放重命名后图片的临时文件夹
    tmp_folder = os.path.join(folder_path, "tmp_img_seq")
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    new_file_list = []
    for idx, file_name in enumerate(files, start=1):
        # 扩展名保持一致
        ext = os.path.splitext(file_name)[1]
        new_name = f"image_{idx:04d}{ext}"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(tmp_folder, new_name)
        shutil.copy2(old_path, new_path)  # 保留文件元数据复制

        new_file_list.append(new_path)

    return new_file_list

def generate_mp4_from_images(folder_path, frame_rate=30, output_name="output.mp4"):
    """
    使用OpenCV将指定folder_path中的序列帧合成为MP4
    output_name 为输出视频文件名
    """
    tmp_folder = os.path.join(folder_path, "tmp_img_seq")
    if not os.path.exists(tmp_folder):
        return
    
    # 获取第一张图片来确定视频尺寸
    image_files = sorted([f for f in os.listdir(tmp_folder) if f.startswith("image_")])
    if not image_files:
        return
        
    first_image = cv2.imread(os.path.join(tmp_folder, image_files[0]))
    height, width = first_image.shape[:2]
    
    # Convert Windows path to forward slashes to avoid GStreamer issues
    out_path = os.path.join(folder_path, output_name).replace('\\', '/')
    
    # Try different codecs in order of preference
    codecs = [
        ('mp4v', True),   # Try MPEG-4 first (more widely supported)
        ('XVID', True),   # Then try XVID
        ('MJPG', True),   # Then Motion JPEG
        ('avc1', True),   # H.264 as last resort
    ]
    
    out = None
    for codec, is_color in codecs:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(out_path, fourcc, frame_rate, (width, height), is_color)
            if out is not None and out.isOpened():
                print(f"Successfully initialized VideoWriter with codec: {codec}")
                break
            else:
                print(f"Failed to initialize VideoWriter with codec: {codec}")
        except Exception as e:
            print(f"Error with codec {codec}: {str(e)}")
            if out is not None:
                out.release()
    
    if out is None or not out.isOpened():
        raise RuntimeError(f"Error: Could not create video writer for {output_name}. No compatible codec found.")
    
    print(f"正在生成视频：{folder_path} -> {output_name}")
    
    # 添加时间统计
    start_time = time.time()
    total_frames = len(image_files)
    
    # 逐帧写入视频
    for idx, image_file in enumerate(image_files, 1):
        image_path = os.path.join(tmp_folder, image_file)
        frame = cv2.imread(image_path)
        
        # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        lab = cv2.merge((l,a,b))
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        out.write(frame)
        
        # 打印进度
        if idx % 10 == 0 or idx == total_frames:
            progress = (idx / total_frames) * 100
            elapsed_time = time.time() - start_time
            print(f"进度: {progress:.1f}% ({idx}/{total_frames}) - 已用时: {elapsed_time:.1f}秒", end='\r')
    
    # 完成后打印总用时
    total_time = time.time() - start_time
    print(f"\n视频生成完成！总用时: {total_time:.1f}秒")
    
    # 释放资源
    out.release()
    
    # 生成完毕后，删除临时图片文件夹
    shutil.rmtree(tmp_folder, ignore_errors=True)

def check_keyboard_interrupt():
    if os.name == 'nt':  # Windows
        if msvcrt.kbhit():
            msvcrt.getch()
            return True
    else:  # macOS and Linux
        try:
            # Save the terminal settings
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                # Set the terminal to raw mode
                tty.setraw(sys.stdin.fileno())
                # Check if there's input waiting
                if sys.stdin.read(1):
                    return True
            finally:
                # Restore the terminal settings
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            pass
    return False

def wait_key():
    print("\nPress any key to exit...")
    if getattr(sys, 'frozen', False):
        while True:
            if msvcrt.kbhit():
                msvcrt.getch()
                break
            time.sleep(0.1)

def main():
    """
    The main entry point for the video generator.
    Processes image sequences in leaf folders and converts them to MP4 videos.
    """
    start_time = time.time()  # Add start time tracking
    try:
        print("Welcome to the Video Generator Tool")
        # print(cv2.file) 
        input_path = input("Please enter the directory path to process (Enter for Current Directory): ").strip()
        
        # Use script directory as default if no input provided
        if not input_path:
            root_folder = os.getcwd()
        else:
            # Convert relative path to absolute path
            root_folder = os.path.abspath(input_path)
        
        # Validate directory exists
        if not os.path.exists(root_folder):
            raise FileNotFoundError(f"Directory does not exist: {root_folder}")
        if not os.path.isdir(root_folder):
            raise NotADirectoryError(f"Path is not a directory: {root_folder}")

        processed_folders = 0
        for current_folder, dirs, files in os.walk(root_folder):
            if is_leaf_folder(current_folder):
                try:
                    new_files = rename_images_in_folder(current_folder)
                    if len(new_files) > 0:
                        folder_name = os.path.basename(current_folder)
                        output_name = f"{folder_name}.mp4"
                        generate_mp4_from_images(current_folder, frame_rate=30, output_name=output_name)
                        processed_folders += 1
                        logging.info(f"Successfully processed folder: {current_folder}")
                    else:
                        logging.info(f"Skipped folder (no images): {current_folder}")
                except Exception as e:
                    logging.error(f"Error processing folder {current_folder}: {str(e)}")
                    print(f"\nError processing folder {current_folder}: {str(e)}")

        if processed_folders > 0:
            total_time = time.time() - start_time
            print(f"\nSuccessfully processed {processed_folders} folders.")
            print(f"Total processing time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        else:
            print("\nNo image sequences found to process.")

    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"\nError: {str(e)}")
        logging.error(str(e))
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        logging.error(f"Unhandled exception: {str(e)}")
    finally:
        # Add total run time even if there were errors
        total_run_time = time.time() - start_time
        print(f"\nTotal run time: {total_run_time:.1f} seconds ({total_run_time/60:.1f} minutes)")
        wait_key()

if __name__ == "__main__":
    main()