#!/usr/bin/env python3
"""
InstaReelTranscriber - One-Click Installer
Cross-platform setup script that handles all dependencies and configuration.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def supports_color():
    """Check if terminal supports color."""
    if platform.system() == 'Windows':
        return os.environ.get('TERM') or os.environ.get('WT_SESSION')
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

USE_COLOR = supports_color()

def cprint(text, color=''):
    """Print with optional color."""
    if USE_COLOR and color:
        print(f"{color}{text}{Colors.END}")
    else:
        print(text)

def print_banner():
    """Print installation banner."""
    banner = """
============================================================
     InstaReelTranscriber - One-Click Installer
============================================================
"""
    cprint(banner, Colors.HEADER)

def print_step(step_num, total, message):
    """Print step progress."""
    cprint(f"\n[{step_num}/{total}] {message}", Colors.BLUE)

def print_success(message):
    """Print success message."""
    cprint(f"✓ {message}", Colors.GREEN)

def print_warning(message):
    """Print warning message."""
    cprint(f"⚠ {message}", Colors.YELLOW)

def print_error(message):
    """Print error message."""
    cprint(f"✗ {message}", Colors.RED)

def get_os_info():
    """Get operating system information."""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    return system

def run_command(cmd, capture=False, cwd=None):
    """Run a shell command."""
    try:
        if capture:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, cwd=cwd
            )
            return result.returncode == 0, result.stdout.strip()
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            return result.returncode == 0, None
    except Exception as e:
        return False, str(e)

def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    print_error(f"Python 3.8+ required, found {version.major}.{version.minor}")
    return False

def check_node():
    """Check Node.js installation."""
    success, output = run_command("node --version", capture=True)
    if success and output:
        version = output.strip().lstrip('v')
        major = int(version.split('.')[0])
        if major >= 18:
            print_success(f"Node.js {output} detected")
            return True
        print_warning(f"Node.js 18+ recommended, found {output}")
        return True
    print_warning("Node.js not found - required for web interface")
    print("  Install from: https://nodejs.org/")
    return False

def check_ffmpeg():
    """Check FFmpeg installation."""
    success, output = run_command("ffmpeg -version", capture=True)
    if success:
        print_success("FFmpeg detected")
        return True
    
    os_type = get_os_info()
    print_warning("FFmpeg not found - required for audio processing")
    
    if os_type == 'windows':
        print("  Install via: winget install ffmpeg")
        print("  Or download from: https://ffmpeg.org/download.html")
    elif os_type == 'macos':
        print("  Install via: brew install ffmpeg")
    else:
        print("  Install via: sudo apt install ffmpeg")
    
    return False

def create_venv(project_root):
    """Create virtual environment if it doesn't exist."""
    venv_path = project_root / "venv"
    
    if venv_path.exists():
        print_success("Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    success, _ = run_command(f'"{sys.executable}" -m venv venv', cwd=project_root)
    
    if success:
        print_success("Virtual environment created")
        return True
    
    print_error("Failed to create virtual environment")
    return False

def get_venv_python(project_root):
    """Get the path to the virtual environment's Python executable."""
    os_type = get_os_info()
    if os_type == 'windows':
        return project_root / "venv" / "Scripts" / "python.exe"
    return project_root / "venv" / "bin" / "python"

def get_venv_pip(project_root):
    """Get the path to the virtual environment's pip executable."""
    os_type = get_os_info()
    if os_type == 'windows':
        return project_root / "venv" / "Scripts" / "pip.exe"
    return project_root / "venv" / "bin" / "pip"

def install_backend_deps(project_root):
    """Install backend Python dependencies."""
    pip_path = get_venv_pip(project_root)
    
    print("Upgrading pip...")
    run_command(f'"{pip_path}" install --upgrade pip', cwd=project_root)
    
    print("Installing backend dependencies...")
    success, _ = run_command(
        f'"{pip_path}" install -r requirements.txt',
        cwd=project_root
    )
    
    if success:
        print_success("Backend dependencies installed")
        return True
    
    print_error("Failed to install backend dependencies")
    return False

def install_frontend_deps(project_root):
    """Install frontend Node.js dependencies."""
    frontend_path = project_root / "frontend"
    
    if not frontend_path.exists():
        print_warning("Frontend directory not found, skipping...")
        return True
    
    node_modules = frontend_path / "node_modules"
    if node_modules.exists():
        print_success("Frontend dependencies already installed")
        return True
    
    print("Installing frontend dependencies (this may take a minute)...")
    success, _ = run_command("npm install", cwd=frontend_path)
    
    if success:
        print_success("Frontend dependencies installed")
        return True
    
    print_error("Failed to install frontend dependencies")
    print("  Make sure Node.js is installed and try: cd frontend && npm install")
    return False

def download_whisper_model(project_root, model="base"):
    """Pre-download the Whisper model."""
    python_path = get_venv_python(project_root)
    model_downloader = project_root / "src" / "model_downloader.py"
    
    if not model_downloader.exists():
        print_warning("Model downloader not found, skipping pre-download")
        return True
    
    print(f"Downloading Whisper '{model}' model (this may take a few minutes)...")
    success, _ = run_command(
        f'"{python_path}" src/model_downloader.py --model {model}',
        cwd=project_root
    )
    
    if success:
        print_success(f"Whisper '{model}' model downloaded")
        return True
    
    print_warning("Model download failed - will retry on first use")
    return True

def create_env_file(project_root):
    """Create .env file from template if it doesn't exist."""
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if env_file.exists():
        print_success(".env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print_success(".env file created from template")
        return True
    
    # Create default .env
    default_env = """# InstaReelTranscriber Configuration

# Backend Configuration
WHISPER_MODEL=base
API_PORT=8000
LOG_LEVEL=INFO

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# CORS Configuration
CORS_ORIGIN=http://localhost:3000
"""
    env_file.write_text(default_env)
    print_success(".env file created with defaults")
    return True

def main():
    """Main installation process."""
    print_banner()
    
    # Determine project root
    project_root = Path(__file__).parent.resolve()
    os_type = get_os_info()
    
    cprint(f"Operating System: {platform.system()} ({os_type})", Colors.BLUE)
    cprint(f"Project Directory: {project_root}", Colors.BLUE)
    
    total_steps = 7
    all_success = True
    warnings = []
    
    # Step 1: Check Python
    print_step(1, total_steps, "Checking Python installation")
    if not check_python():
        print_error("Python 3.8+ is required. Please install it and try again.")
        sys.exit(1)
    
    # Step 2: Check Node.js
    print_step(2, total_steps, "Checking Node.js installation")
    if not check_node():
        warnings.append("Node.js not found - web interface will not work")
    
    # Step 3: Check FFmpeg
    print_step(3, total_steps, "Checking FFmpeg installation")
    if not check_ffmpeg():
        warnings.append("FFmpeg not found - audio processing will fail")
    
    # Step 4: Create virtual environment
    print_step(4, total_steps, "Setting up Python virtual environment")
    if not create_venv(project_root):
        print_error("Failed to create virtual environment")
        sys.exit(1)
    
    # Step 5: Install backend dependencies
    print_step(5, total_steps, "Installing backend dependencies")
    if not install_backend_deps(project_root):
        all_success = False
    
    # Step 6: Install frontend dependencies
    print_step(6, total_steps, "Installing frontend dependencies")
    if not install_frontend_deps(project_root):
        warnings.append("Frontend dependencies not installed")
    
    # Step 7: Download Whisper model
    print_step(7, total_steps, "Downloading AI model")
    download_whisper_model(project_root)
    
    # Create environment file
    create_env_file(project_root)
    
    # Summary
    print("\n" + "=" * 60)
    
    if all_success and not warnings:
        cprint("  ✓ Setup Complete! All components ready.", Colors.GREEN)
    elif all_success:
        cprint("  ✓ Setup Complete with warnings.", Colors.YELLOW)
    else:
        cprint("  ✗ Setup completed with errors.", Colors.RED)
    
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print_warning(f"  - {w}")
    
    print("\n" + "=" * 60)
    cprint("\nTo start the application:", Colors.BOLD)
    
    if os_type == 'windows':
        print("  Run: start.bat")
        print("  Or manually:")
        print("    Backend:  venv\\Scripts\\uvicorn src.api:app --reload")
        print("    Frontend: cd frontend && npm run dev")
    else:
        print("  Run: ./start.sh")
        print("  Or manually:")
        print("    Backend:  source venv/bin/activate && uvicorn src.api:app --reload")
        print("    Frontend: cd frontend && npm run dev")
    
    print("\nThen open: http://localhost:3000")
    print("=" * 60 + "\n")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
