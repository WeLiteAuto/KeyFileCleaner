# WeilanToolkit
A toolkit commonly used tools for Weilan Auto

## Features

### Key File Cleaner
- Remove lines from `.key` files that start with a specified character or pattern
- Delete files with the extensions `.ansa`, `.hm`, `.mvw`, and `.catpart`

### Video Generator
- Generate videos from LS-DYNA simulation results
- Customize video output parameters
- Support for various video formats

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

You can run the toolkit in two ways:

### 1. Interactive Mode
Simply run the script without any arguments to open the interactive menu:
```bash
python main.py
```

### 2. Command Line Mode
Directly specify which tool to run using command-line arguments:
```bash
python main.py [tool]
```

Available tools:
- `clean`: Run the Key File Cleaner
- `video`: Run the Video Generator

### Examples:

1. To use the Key File Cleaner:
```bash
python main.py clean
```

2. To use the Video Generator:
```bash
python main.py video
```

For help:
```bash
python main.py --help
```

## Dependencies

The project requires several Python packages which are listed in `requirements.txt`:
- pandas
- numpy
- opencv-python
- moviepy
- matplotlib
- seaborn
- pathlib
- python-dotenv

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

