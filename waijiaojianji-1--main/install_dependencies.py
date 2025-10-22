#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外教视频处理系统 - 依赖安装工具
自动检测和安装所需的Python依赖包
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import importlib.util

def print_header():
    """打印安装工具标题"""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   依赖安装工具                               ║
    ║                                                              ║
    ║   自动检测和安装外教视频处理系统所需的Python依赖包           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """检查pip是否可用"""
    print("📦 检查pip...")
    
    try:
        import pip
        print("✅ pip已安装")
        return True
    except ImportError:
        print("❌ pip未安装")
        return False

def get_system_info():
    """获取系统信息"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    print(f"💻 系统信息: {platform.system()} {platform.release()} ({arch})")
    
    return system, arch

def check_package_installed(package_name, import_name=None):
    """检查包是否已安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        return spec is not None
    except (ImportError, ValueError, ModuleNotFoundError):
        return False

def install_package(package_name, extra_args=None):
    """安装单个包"""
    cmd = [sys.executable, "-m", "pip", "install", package_name]
    
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        print(f"📥 安装 {package_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package_name} 安装成功")
            return True
        else:
            print(f"❌ {package_name} 安装失败:")
            print(result.stderr)
            return False
    
    except subprocess.TimeoutExpired:
        print(f"⏰ {package_name} 安装超时")
        return False
    except Exception as e:
        print(f"❌ 安装 {package_name} 时出错: {e}")
        return False

def install_requirements():
    """从requirements.txt安装依赖"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt文件不存在")
        return False
    
    print("📋 从requirements.txt安装依赖...")
    
    try:
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ 所有依赖安装成功")
            return True
        else:
            print("❌ 依赖安装失败:")
            print(result.stderr)
            return False
    
    except subprocess.TimeoutExpired:
        print("⏰ 依赖安装超时")
        return False
    except Exception as e:
        print(f"❌ 安装依赖时出错: {e}")
        return False

def check_critical_packages():
    """检查关键包是否正确安装"""
    print("\n🔍 检查关键包...")
    
    critical_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("opencv-python", "cv2"),
        ("Pillow", "PIL"),
        ("numpy", "numpy"),
        ("requests", "requests"),
        ("python-dotenv", "dotenv"),
        ("tencentcloud-sdk-python", "tencentcloud"),
        ("cos-python-sdk-v5", "qcloud_cos"),
        ("pydub", "pydub"),
        ("redis", "redis")
    ]
    
    failed_packages = []
    
    for package_name, import_name in critical_packages:
        if check_package_installed(package_name, import_name):
            print(f"✅ {package_name}")
        else:
            print(f"❌ {package_name}")
            failed_packages.append(package_name)
    
    return failed_packages

def install_system_dependencies():
    """安装系统级依赖"""
    system, arch = get_system_info()
    
    print("\n🔧 检查系统依赖...")
    
    if system == "windows":
        print("💡 Windows系统提示:")
        print("   - 确保已安装Microsoft Visual C++ Redistributable")
        print("   - 如果OpenCV安装失败，请安装Visual Studio Build Tools")
    
    elif system == "linux":
        print("💡 Linux系统提示:")
        print("   - 可能需要安装: sudo apt-get install python3-dev libffi-dev")
        print("   - OpenCV依赖: sudo apt-get install libopencv-dev")
    
    elif system == "darwin":  # macOS
        print("💡 macOS系统提示:")
        print("   - 确保已安装Xcode Command Line Tools")
        print("   - 可使用Homebrew安装依赖: brew install opencv")

def upgrade_pip():
    """升级pip到最新版本"""
    print("⬆️  升级pip...")
    
    try:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ pip升级成功")
            return True
        else:
            print("⚠️  pip升级失败，继续使用当前版本")
            return False
    
    except Exception as e:
        print(f"⚠️  pip升级出错: {e}")
        return False

def create_virtual_env_hint():
    """提示创建虚拟环境"""
    print("\n💡 建议使用虚拟环境:")
    print("   python -m venv venv")
    print("   # Windows:")
    print("   venv\\Scripts\\activate")
    print("   # Linux/macOS:")
    print("   source venv/bin/activate")

def main():
    """主函数"""
    print_header()
    
    # 检查基础环境
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        print("请先安装pip")
        sys.exit(1)
    
    # 获取系统信息
    get_system_info()
    
    # 提示虚拟环境
    create_virtual_env_hint()
    
    try:
        # 升级pip
        upgrade_pip()
        
        # 安装系统依赖提示
        install_system_dependencies()
        
        # 安装Python依赖
        print("\n" + "="*60)
        print("📦 开始安装Python依赖包...")
        print("="*60)
        
        if install_requirements():
            print("\n🎉 依赖安装完成！")
        else:
            print("\n❌ 依赖安装失败")
            sys.exit(1)
        
        # 检查关键包
        failed_packages = check_critical_packages()
        
        if failed_packages:
            print(f"\n⚠️  以下包安装失败: {', '.join(failed_packages)}")
            print("请手动安装这些包或检查错误信息")
        
        print("\n" + "="*60)
        print("🚀 安装完成！现在可以运行:")
        print("   python setup_api_keys.py  # 配置API Keys")
        print("   python quick_start.py     # 启动系统")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n👋 安装已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 安装过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()