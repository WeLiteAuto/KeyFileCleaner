import os
import shutil
import cv2
import numpy as np
import time

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
        ('avc1', True),   # H.264 codec
        ('mp4v', True),   # MPEG-4 codec
        ('XVID', True),   # XVID codec
        ('MJPG', True),   # Motion JPEG codec
    ]
    
    out = None
    for codec, is_color in codecs:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(out_path, fourcc, frame_rate, (width, height), is_color)
            if out.isOpened():
                break
        except Exception as e:
            print(f"Codec {codec} failed, trying next...")
            if out is not None:
                out.release()
    
    if out is None or not out.isOpened():
        print(f"Error: Could not create video writer for {output_name}")
        return
    
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

def main():
    # Get input path from user
    input_path = input("请输入要处理的文件夹路径（直接回车则使用脚本所在目录）：").strip()
    
    # Use script directory as default if no input provided
    if not input_path:
        root_folder = os.path.dirname(os.path.abspath(__file__))
    else:
        root_folder = os.path.abspath(input_path)
    
    if not os.path.exists(root_folder):
        print(f"错误：路径 '{root_folder}' 不存在")
        return

    for current_folder, dirs, files in os.walk(root_folder):
        # 跳过类似 .git、__pycache__ 等非必要目录
        # 或根据需要排除与脚本同级的一些其他文件夹
        # if current_folder == root_folder:
        #     continue

        # 判断是否是叶子文件夹
        if is_leaf_folder(current_folder):
            # 收集并重命名图片
            new_files = rename_images_in_folder(current_folder)
            if len(new_files) > 0:
                # Use folder name as the output video filename
                folder_name = os.path.basename(current_folder)
                output_name = f"{folder_name}.mp4"
                # Generate video with the folder name
                generate_mp4_from_images(current_folder, frame_rate=30, output_name=output_name)
            else:
                print(f"跳过：{current_folder}（无图片）")

if __name__ == "__main__":
    main()