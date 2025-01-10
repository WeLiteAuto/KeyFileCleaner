from setuptools import setup, find_packages

setup(
    name='WeilanToolkit',  # Project name
    version='0.2',  # Updated version
    author='weilanauto',
    author_email='drivelytics@weilanauto.com',  # Updated email from README
    description='A toolkit containing commonly used tools for Weilan Auto',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/weilan-auto/WeilanToolkit',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.0,<2.0.0',
        'numpy==1.24.3',
        'opencv-python==4.8.1.78',
        'moviepy==1.0.3',
        'python-dotenv>=1.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'weilan-toolkit=main:main',
            'key-cleaner=key_file_cleaner:main',
            'video-generator=generate_video:main',
        ],
    },
    include_package_data=True,
)
