from setuptools import setup, find_packages

setup(
    name='KeyFileCleaner',  # Updated project name
    version='0.1',  # Initial version of your project
    author='GEYulong',  # Replace with your name
    author_email='geyulong@weilanauto.com',  # Replace with your email
    description='A utility to remove specific pre-processor information and files in directories for ls-dyna projects',  # Updated description to specify functionality
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Specifies that the long description is in Markdown
    url='https://github.com/weliteauto/KEYFILECLEANER',  # Updated URL to match project name
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        # List any dependencies your project needs here.
        # Example: 'numpy', 'pandas' if your project uses these packages
    ],
    classifiers=[
        'Development Status :: 4 - Beta',  # Indicates the project is in beta stage
        'Intended Audience :: Developers',  # Target audience
        'License :: OSI Approved :: MIT License',  # License type
        'Programming Language :: Python :: 3',  # Supported Python versions
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Minimum required Python version
    entry_points={
        'console_scripts': [
            'keyfilecleaner=KeYFILECLEANER.main:main',  # Ensure 'KeYFILECLEANER' matches your package structure
        ],
    },
    include_package_data=True,  # Include any non-code files specified in MANIFEST.in
)
