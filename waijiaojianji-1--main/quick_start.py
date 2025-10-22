#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外教视频处理系统 - 一键启动脚本
自动检查环境、配置API Keys、启动服务
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   外教视频处理系统                           ║
    ║                   一键启动配置工具                           ║
    ║                                                              ║
    ║   🎥 视频背景移除  🎤 语音转文字  📝 自动字幕               ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python版本过低，需要Python 3.9+")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")
    try:
        import fastapi
        import uvicorn
        import opencv_python
        print("✅ 核心依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("正在安装依赖包...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ 依赖包安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖包安装失败")
            return False

def check_ffmpeg():
    """检查FFmpeg"""
    print("\n🔍 检查FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg已安装")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg未安装或不在PATH中")
    print("请安装FFmpeg: https://ffmpeg.org/download.html")
    return False

def setup_env_file():
    """设置环境变量文件"""
    print("\n⚙️ 配置环境变量...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env文件已存在")
        load_dotenv()
        return True
    
    if env_example.exists():
        # 复制示例文件
        with open(env_example, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 已创建.env文件（基于.env.example）")
        print("⚠️  请编辑.env文件，配置您的API Keys")
        return True
    else:
        print("❌ 未找到.env.example文件")
        return False

def test_api_keys():
    """测试API Keys配置"""
    print("\n🔑 测试API Keys...")
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    tencent_id = os.getenv('TENCENT_SECRET_ID')
    
    if not openai_key or openai_key.startswith('sk-your-'):
        print("⚠️  OpenAI API Key未配置")
        return False
    
    if not tencent_id or tencent_id.startswith('your-'):
        print("⚠️  腾讯云API Keys未配置")
        return False
    
    print("✅ API Keys配置检查通过")
    return True

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建必要目录...")
    
    directories = ['uploads', 'outputs', 'temp', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ 目录创建完成")

def start_server():
    """启动服务器"""
    print("\n🚀 启动服务器...")
    print("服务地址: http://localhost:8000")
    print("按 Ctrl+C 停止服务")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

def main():
    """主函数"""
    print_banner()
    
    # 检查系统环境
    if not check_python_version():
        return False
    
    if not check_dependencies():
        return False
    
    if not check_ffmpeg():
        print("⚠️  FFmpeg未安装，部分功能可能无法使用")
    
    # 配置环境
    if not setup_env_file():
        return False
    
    create_directories()
    
    # 测试配置
    if not test_api_keys():
        print("\n⚠️  API Keys未正确配置，请编辑.env文件后重新运行")
        print("配置完成后，运行: python quick_start.py")
        return False
    
    # 启动服务
    start_server()
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)