# WeilanToolkit
A toolkit commonly used tools for Weilan Auto

## Features

### Key File Cleaner
- Clean and process key files for simulation data
- Automated file processing and cleaning capabilities
- Handles multiple file formats and cleaning patterns

### Video Generator
- Generate videos from LS-DYNA simulation results
- Customizable video output parameters
- Support for various video formats

## Installation

1. Clone this repository:
```bash
git clone https://github.com/weilan-auto/WeilanToolkit.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The toolkit can be used in two modes:

### 1. Interactive Mode
Run the script without any arguments to use the interactive menu:
```bash
python main.py
```

This will display a user-friendly menu where you can select:
1. Key File Cleaner
2. Video Generator
0. Exit

### 2. Command Line Mode
Run specific tools directly using command-line arguments:
```bash
python main.py [tool]
```

Available commands:
- `clean`: Run the Key File Cleaner
- `video`: Run the Video Generator

Examples:
```bash
python main.py clean  # Run Key File Cleaner
python main.py video  # Run Video Generator
```

For help with command-line options:
```bash
python main.py --help
```

## Dependencies

Required Python packages:
- pandas (>=1.5.0,<2.0.0)
- numpy (==1.24.3)
- opencv-python (==4.8.1.78)
- moviepy (==1.0.3)
- python-dotenv (>=1.0.0)
- pyinstaller (>=6.4.0) - for building executables

All dependencies are listed in `requirements.txt` and will be installed automatically during setup.

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## Contact

For any questions or support, please email: drivelytics@weilanauto.com

