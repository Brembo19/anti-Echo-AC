import os
import platform
import webbrowser
import subprocess
import glob
import ctypes
import sys
import re
from pathlib import Path
from colorama import init

init(autoreset=True)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass

def delete_files(pattern):
    for file in glob.glob(pattern):
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error removing {file}: {e}")

def delete_registry_keys(keys):
    for key in keys:
        run_command(f'reg delete "{key}" /f')

def clear_logs():
    event_logs = ['Application', 'Security', 'Setup', 'System', 'ForwardedEvents']
    for log in event_logs:
        run_command(f'wevtutil cl {log}')
    run_command('del /F /Q %APPDATA%\\Microsoft\\Windows\\Recent\\*')
    run_command('del /F /Q %APPDATA%\\Microsoft\\Windows\\Recent\\AutomaticDestinations\\*')
    run_command('del /F /Q %APPDATA%\\Microsoft\\Windows\\Recent\\CustomDestinations\\*')
    run_command('del /F /Q %APPDATA%\\Roaming\\Microsoft\\Windows\\Recent\\*')
    run_command('del /F /Q %LOCALAPPDATA%\\Microsoft\\Windows\\Explorer\\RecentDocs')
    run_command('del /F /S /Q C:\\Windows\\Prefetch\\*')
    run_command('del /F /Q %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\*')
    run_command('del /F /Q %LOCALAPPDATA%\\Microsoft\\Windows\\History\\*')

def clean_system():
    temp_folders = [
        os.getenv('TEMP', ''),
        r'C:\Windows\Temp',
        r'C:\Windows\Prefetch',
        os.path.join(os.getenv('APPDATA', ''), r'Microsoft\Windows\Recent')
    ]

    for folder in temp_folders:
        if folder:
            run_command(f'rd /s /q "{folder}"')

    delete_files(r'C:\Windows\System32\winevt\Logs\*.evtx')

    tzproject_files = [
        r'C:\Path\To\Search\*api.tzproject.com*',
        r'C:\Another\Path\*api.tzproject.com*'
    ]
    for pattern in tzproject_files:
        delete_files(pattern)

    run_command(r'RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 255')

    clear_logs()

def perform_deletion_tasks():
    files_to_delete = [
        r'C:\Windows\Temp\*.*',
        os.path.join(os.getenv('TEMP', ''), '*.*'),
        r'C:\Program Files (x86)\Steam\steamapps\common\Driver Booster for Steam\loader.cfg',
        r'C:\Program Files (x86)\Steam\steamapps\common\Driver Booster for Steam\loader.dll',
        r'C:\Program Files (x86)\Steam\steamapps\common\Driver Booster for Steam\DriverBooster.cfg',
        r'C:\Program Files (x86)\Steam\steamapps\common\Driver Booster for Steam\DriverBooster.dll'
    ]
    for pattern in files_to_delete:
        delete_files(pattern)

    registry_keys = [
        r'HKLM\SYSTEM\CurrentControlSet\Control\CI\Config /v VulnerableDriverBlocklistEnable',
        r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery',
        r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RunMRU',
        r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage',
        r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs',
        r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectInput',
        r'HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\AppCompatCache',
        r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU',
        r'HKEY_CURRENT_USER\SOFTWARE\WinRAR\ArcHistory',
        r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\UserAssist',
        r'HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\bam\State\UserSettings'
    ]
    delete_registry_keys(registry_keys)

def main():
    os.system('title brembo.py')
    hostname = platform.node()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Welcome to brembo.py on {hostname}")
        print("1. Reseller")
        print("2. Ovix")
        print("3. Clean")
        print("4. Perform Deletion Tasks")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            webbrowser.open('https://lmarket.fr/')
        elif choice == '2':
            webbrowser.open('https://ovix.one/')
            webbrowser.open('https://discord.gg/kCgfnxXAzD')
        elif choice == '3':
            clean_system()
        elif choice == '4':
            perform_deletion_tasks()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == '__main__':
    main()
