import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path

class SetupError(Exception):
    pass

def check_command_exists(command):
    """Check if a command exists in the system."""
    return shutil.which(command) is not None

def create_nekon_config():
    """Create the .nekon configuration file in the nekon directory with placeholders for sensitive information."""
    config_content = """
# Django Configuration
SECRET_KEY=your_django_project_secret_key

# Database Configuration
RDS_HOST=your_rds_postgres_database_endpoint
RDS_PORT=your_rds_postgres_database_port
RDS_DBNAME=your_rds_postgres_database_name
RDS_USER=your_rds_postgres_database_masterusername
RDS_PASSWORD=your_rds_postgres_database_password

# OAuth Configurations
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret_key
GITHUB_CLIENT_ID=your_github_oauth_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_client_secret_key

# Other Configurations
DEBUG=True
    """.strip()

    with open(".nekon", "w") as config_file:
        config_file.write(config_content)
    print("✓ .nekon configuration file created with placeholder values.")

def run_command(command, error_msg=None, shell=True):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {result.stdout.strip()}" if result.stdout else f"✓ Successfully ran: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running command: {command}")
        if error_msg:
            print(f"✗ {error_msg}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if all required software is installed."""
    required_commands = {
        'git': "Git is not installed. Please install it from https://git-scm.com/downloads",
        'code': "VSCode is not installed. Please install it from https://code.visualstudio.com/download",
        'python': "Python is not installed. Please install it from https://www.python.org/downloads/",
        'node': "Node.js is not installed. Please install it from https://nodejs.org/",
        'npm': "npm is not installed. Please reinstall Node.js from https://nodejs.org/"
    }

    for command, error_msg in required_commands.items():
        if not check_command_exists(command):
            if command == 'python' and check_command_exists('python3'):
                continue
            print(f"✗ {error_msg}")
            sys.exit(1)

def setup_windows_execution_policy():
    """Set execution policy for PowerShell if restricted."""
    if platform.system().lower() == 'windows':
        try:
            # Check current execution policy
            check_policy = subprocess.run(
                ['powershell', 'Get-ExecutionPolicy'],
                capture_output=True,
                text=True
            )
            current_policy = check_policy.stdout.strip().lower()
            
            if current_policy == 'restricted':
                print("⚠️ PowerShell execution policy is Restricted. Changing to RemoteSigned...")
                subprocess.run(
                    ['powershell', 'Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser'],
                    check=True
                )
                print("✓ Execution policy updated to RemoteSigned")
        except subprocess.CalledProcessError:
            print("⚠️ Failed to check/set PowerShell execution policy")
            raise SetupError("PowerShell execution policy configuration failed")

def setup_project():
    """Main setup function."""
    check_prerequisites()

    # Change to the nekon directory
    if not os.path.exists('nekon'):
        raise SetupError("Directory 'nekon' does not exist")
    os.chdir('nekon')

    # Determine OS and shell
    system = platform.system().lower()
    is_windows = system == 'windows'
    shell_type = os.environ.get('SHELL', '').lower() if not is_windows else (
        'powershell' if os.environ.get('PSModulePath') else 'cmd')

    # Set execution policy if on Windows
    if is_windows:
        setup_windows_execution_policy()

    # Frontend setup
    print("\n📦 Setting up Frontend...")
    frontend_commands = [
        "npm install",
        "npm fund"
    ]

    if not os.path.exists('frontend'):
        raise SetupError("Directory 'frontend' does not exist")

    # Change to frontend directory
    os.chdir('frontend')

    for cmd in frontend_commands:
        if not run_command(cmd):
            raise SetupError("Frontend setup failed")

    # Go back to nekon root directory
    os.chdir('..')

    # Backend setup
    print("\n🐍 Setting up Backend...")

    # Create and activate virtual environment
    if is_windows:
        venv_commands = [
            "py -m venv dpr",
            ".\\dpr\\Scripts\\Activate.ps1"  # Use PowerShell activation script
        ]
    else:
        venv_commands = [
            "python3 -m venv dpr",
            'ln -s "$(pwd)/nekon/dpr/bin/python3" "$(pwd)/nekon/dpr/bin/py"',
            "source dpr/bin/activate"
        ]

    for cmd in venv_commands:
        if is_windows:
            # For Windows, use PowerShell to run the activation script
            if "Activate.ps1" in cmd:
                activate_cmd = f"powershell -ExecutionPolicy Bypass -File {cmd}"
                if not run_command(activate_cmd, shell=True):
                    raise SetupError("Virtual environment activation failed")
            else:
                if not run_command(cmd):
                    raise SetupError("Virtual environment setup failed")
        else:
            if not run_command(cmd):
                raise SetupError("Virtual environment setup failed")

    # Install Python packages
    pip_commands = [
        "py -m pip install --upgrade pip",
        "py -m pip install -r requirements.txt"
    ]

    for cmd in pip_commands:
        if not run_command(cmd):
            raise SetupError("Python package installation failed")

    # Setup VSCode path and open project in VSCode
    if is_windows:
        if shell_type == 'powershell':
            vscode_path_command = r'''
            $vscodePath = Get-ChildItem "$env:LOCALAPPDATA\\Programs\\Microsoft VS Code\\bin" -Recurse -Filter "code.cmd" | 
            Select-Object -ExpandProperty DirectoryName; 
            if ($vscodePath) { 
                if ($env:Path -notlike "*$vscodePath*") {
                    [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$vscodePath", [System.EnvironmentVariableTarget]::User)
                }
            }
            '''
            run_command(vscode_path_command)
        elif shell_type == 'cmd':
            vscode_path_command = r'''
            @echo off
            for /f "tokens=*" %%i in ('dir /s /b "%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\bin\\code.cmd"') do (
                set "vscodePath=%%~dpi"
            )
            if defined vscodePath (
                echo %PATH% | find /i "%vscodePath%" > nul
                if errorlevel 1 (
                    setx PATH "%PATH%;%vscodePath%"
                )
            )
            '''
            # Write the batch script to a temporary file and execute it
            with open('temp_vscode_path.bat', 'w') as f:
                f.write(vscode_path_command)
            run_command('temp_vscode_path.bat')
            os.remove('temp_vscode_path.bat')

    create_nekon_config()
    run_command("code . -n")

    print("\n✅ Setup completed successfully!")
    print("\n⚠️  Remember to:")
    print("1. Set up the .nekon configuration file in the project root")
    print("2. Configure your Git credentials if you haven't already")

if __name__ == "__main__":
    try:
        setup_project()
    except SetupError as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
