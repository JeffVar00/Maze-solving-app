import os
import subprocess

def generate_executable(script_name):
    script_name = os.path.join(os.getcwd(), script_name)
    print(f"Generating executable for {script_name}...")
    subprocess.run(['pyinstaller', '--onefile', script_name])

if __name__ == "__main__":
    script_name = "main.py" 
    generate_executable(script_name)
    print("Executable generated successfully.")