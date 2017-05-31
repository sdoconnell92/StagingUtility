#!/bin/bash
pyinstaller -F -w --distpath StagingUtility\PyInstaller_Files\dist --workpath StagingUtility\PyInstaller_Files\build guiapp.py

pyinstaller -F -w --distpath C:\Users\sean\WorthSaving\repos\StagingUtility\PyInstaller_Files\dist --workpath C:\Users\sean\WorthSaving\repos\StagingUtility\PyInstaller_Files\build C:\Users\sean\WorthSaving\repos\StagingUtility\nsp_staging_utility\guiapp.py