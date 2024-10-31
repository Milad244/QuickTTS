import os
import shutil
import subprocess

download_folder = 'C:\\All Milad Coding\\Pycharm\\Python Projects\\QuickTTS\\download'
script_filename = 'quick_tts.py'


def clean_download_folder():
    if os.path.exists(download_folder):
        for item in os.listdir(download_folder):
            if item == ".git":
                continue
            item_path = os.path.join(download_folder, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print("Download folder cleaned.")
    else:
        print("Download folder does not exist.")


def build_application():
    try:
        subprocess.run(['pyinstaller', '--onefile', script_filename, '--distpath', download_folder], check=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while building: {e}")


def clean_main_folder():
    build_folder = 'build'
    spec_file = f'{script_filename}.spec'

    for item in [build_folder, spec_file]:
        item_path = os.path.join(os.getcwd(), item)
        if os.path.exists(item_path):
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")
            else:
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
    print("Main folder cleaned.")


def main():
    clean_download_folder()
    build_application()
    clean_main_folder()


if __name__ == "__main__":
    main()
