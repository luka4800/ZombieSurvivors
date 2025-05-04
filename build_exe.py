import PyInstaller.__main__
import os

# Get the absolute path to the assets directory
assets_path = os.path.abspath('assets')

# Define the PyInstaller arguments
pyinstaller_args = [
    'zombie_survivors.py',  # Your main script
    '--name=ZombieSurvivors',  # Name of the executable
    '--onefile',  # Create a single executable file
    '--windowed',  # Don't show console window
    '--icon=assets/icon.ico',  # Icon for the executable (if you have one)
    '--add-data=assets;assets',  # Include the assets folder
    '--clean',  # Clean PyInstaller cache
    '--noconfirm',  # Replace existing build without asking
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args) 