import argparse
import sys
from pathlib import Path
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    print("""
╔══════════════════════════════════╗
║        Weilan Auto Toolkit       ║
╠══════════════════════════════════╣
║                                  ║
║  1. Key File Cleaner            ║
║  2. Video Generator             ║
║  0. Exit                        ║
║                                  ║
╚══════════════════════════════════╝
    """)
    return input("Please select a tool (0-2): ")

def run_key_file_cleaner():
    try:
        from key_file_cleaner import main as key_cleaner_main
        key_cleaner_main()
    except ImportError:
        print("Error: Could not import key_file_cleaner module")
        sys.exit(1)

def run_video_generator():
    try:
        from generate_video import main as video_generator_main
        video_generator_main()
    except ImportError:
        print("Error: Could not import generate_video module")
        sys.exit(1)

def interactive_mode():
    while True:
        choice = show_menu()
        if choice == '1':
            print("\nRunning Key File Cleaner...")
            run_key_file_cleaner()
            input("\nPress Enter to continue...")
        elif choice == '2':
            print("\nRunning Video Generator...")
            run_video_generator()
            input("\nPress Enter to continue...")
        elif choice == '0':
            print("\nExiting...")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

def main():
    # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Weilan Auto Toolkit - A collection of commonly used tools')
        parser.add_argument('tool', choices=['clean', 'video'],
                          help='Choose which tool to run: "clean" for Key File Cleaner, "video" for Video Generator')
        
        args = parser.parse_args()

        if args.tool == 'clean':
            print("Running Key File Cleaner...")
            run_key_file_cleaner()
        elif args.tool == 'video':
            print("Running Video Generator...")
            run_video_generator()
    else:
        # No arguments provided, run in interactive mode
        interactive_mode()

if __name__ == "__main__":
    main() 