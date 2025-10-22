#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外教视频处理系统 - 部署工具
一键部署和启动系统
"""

import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path
import time
import signal
import threading

def print_header():
    """打印部署工具标题"""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   部署工具                                   ║
    ║                                                              ║
    ║   一键部署和启动外教视频处理系统                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)

def check_system():
    """检查系统环境"""
    print("🔍 检查系统环境...")
    
    # 检查Python版本
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    
    # 检查操作系统
    system = platform.system()
    print(f"✅ 操作系统: {system}")
    
    return True

def check_dependencies():
    """检查依赖是否安装"""
    print("📦 检查依赖...")
    
    try:
        import fastapi
        import uvicorn
        print("✅ 核心依赖已安装")
        return True
    except ImportError:
        print("❌ 缺少核心依赖")
        return False

def install_dependencies():
    """安装依赖"""
    print("📥 安装依赖...")
    
    try:
        # 运行依赖安装脚本
        if Path("install_dependencies.py").exists():
            result = subprocess.run([sys.executable, "install_dependencies.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 依赖安装成功")
                return True
            else:
                print("❌ 依赖安装失败")
                print(result.stderr)
                return False
        else:
            # 直接安装requirements.txt
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 依赖安装成功")
                return True
            else:
                print("❌ 依赖安装失败")
                return False
    
    except Exception as e:
        print(f"❌ 安装依赖时出错: {e}")
        return False

def check_configuration():
    """检查配置"""
    print("⚙️  检查配置...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env文件不存在")
        return False
    
    # 检查关键配置
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY', '')
    tencent_id = os.getenv('TENCENT_SECRET_ID', '')
    
    if openai_key.startswith('sk-your-') or not openai_key:
        print("⚠️  OpenAI API Key未配置")
    else:
        print("✅ OpenAI API Key已配置")
    
    if tencent_id.startswith('your-') or not tencent_id:
        print("⚠️  腾讯云API Keys未配置")
    else:
        print("✅ 腾讯云API Keys已配置")
    
    return True

def setup_configuration():
    """设置配置"""
    print("🔧 设置配置...")
    
    if Path("setup_api_keys.py").exists():
        try:
            result = subprocess.run([sys.executable, "setup_api_keys.py"], 
                                  input="y\n", text=True, timeout=300)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("⏰ 配置超时")
            return False
        except Exception as e:
            print(f"❌ 配置失败: {e}")
            return False
    else:
        print("❌ 配置脚本不存在")
        return False

def create_directories():
    """创建必要的目录"""
    print("📁 创建目录...")
    
    directories = [
        "temp",
        "output", 
        "uploads",
        "logs"
    ]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"✅ {dir_name}/")
    
    return True

def start_server():
    """启动服务器"""
    print("🚀 启动服务器...")
    
    try:
        # 启动FastAPI应用
        cmd = [sys.executable, "-m", "app.main"]
        
        print("正在启动服务器...")
        print("按Ctrl+C停止服务器")
        
        # 启动服务器进程
        process = subprocess.Popen(cmd, cwd=Path.cwd())
        
        # 等待服务器启动
        time.sleep(3)
        
        # 打开浏览器
        url = "http://localhost:8000"
        print(f"🌐 服务器已启动: {url}")
        
        try:
            webbrowser.open(url)
            print("✅ 已在浏览器中打开")
        except Exception:
            print("⚠️  请手动在浏览器中打开上述地址")
        
        # 等待进程结束
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 正在停止服务器...")
            process.terminate()
            process.wait()
            print("✅ 服务器已停止")
        
        return True
    
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")
        return False

def run_tests():
    """运行测试"""
    print("🧪 运行系统测试...")
    
    if Path("test_system.py").exists():
        try:
            result = subprocess.run([sys.executable, "test_system.py"], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ 系统测试通过")
                return True
            else:
                print("❌ 系统测试失败")
                print(result.stdout)
                return False
        
        except subprocess.TimeoutExpired:
            print("⏰ 测试超时")
            return False
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
    else:
        print("⚠️  测试脚本不存在，跳过测试")
        return True

def show_menu():
    """显示菜单"""
    menu = """
    请选择操作:
    
    1. 🚀 快速启动 (推荐)
    2. 📦 安装依赖
    3. ⚙️  配置API Keys
    4. 🧪 运行测试
    5. 🌐 启动服务器
    6. ❌ 退出
    
    """
    print(menu)

def quick_deploy():
    """快速部署"""
    print("🚀 开始快速部署...")
    
    steps = [
        ("检查系统环境", check_system),
        ("创建目录", create_directories),
        ("检查依赖", check_dependencies),
        ("检查配置", check_configuration),
        ("运行测试", run_tests),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ {step_name}失败")
            
            # 尝试自动修复
            if step_name == "检查依赖":
                if install_dependencies():
                    continue
            elif step_name == "检查配置":
                print("请手动运行: python setup_api_keys.py")
            
            return False
    
    print("\n🎉 部署完成！")
    return True

def main():
    """主函数"""
    print_header()
    
    try:
        while True:
            show_menu()
            choice = input("请输入选项 (1-6): ").strip()
            
            if choice == "1":
                if quick_deploy():
                    start_server()
                break
            
            elif choice == "2":
                install_dependencies()
            
            elif choice == "3":
                setup_configuration()
            
            elif choice == "4":
                run_tests()
            
            elif choice == "5":
                start_server()
                break
            
            elif choice == "6":
                print("👋 再见！")
                break
            
            else:
                print("❌ 无效选项，请重新选择")
            
            input("\n按回车键继续...")
    
    except KeyboardInterrupt:
        print("\n\n👋 部署已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 部署过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()