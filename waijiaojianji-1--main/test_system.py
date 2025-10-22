#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外教视频处理系统 - 系统测试工具
测试各个功能模块是否正常工作
"""

import os
import sys
import asyncio
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import requests
import time

def print_header():
    """打印测试工具标题"""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   系统测试工具                               ║
    ║                                                              ║
    ║   测试外教视频处理系统各个功能模块                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)

def test_environment():
    """测试环境配置"""
    print("🔧 测试环境配置...")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查关键环境变量
    required_vars = [
        'OPENAI_API_KEY',
        'TENCENT_SECRET_ID',
        'TENCENT_SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your-') or value.startswith('sk-your-'):
            missing_vars.append(var)
        else:
            print(f"✅ {var}: 已配置")
    
    if missing_vars:
        print(f"⚠️  缺少配置: {', '.join(missing_vars)}")
        print("   请运行: python setup_api_keys.py")
        return False
    
    return True

def test_imports():
    """测试关键模块导入"""
    print("\n📦 测试模块导入...")
    
    modules = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests'),
        ('dotenv', 'python-dotenv'),
        ('tencentcloud', '腾讯云SDK'),
        ('qcloud_cos', '腾讯云COS'),
        ('pydub', 'PyDub'),
        ('redis', 'Redis')
    ]
    
    failed_imports = []
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  导入失败: {', '.join(failed_imports)}")
        print("   请运行: python install_dependencies.py")
        return False
    
    return True

def test_app_structure():
    """测试应用结构"""
    print("\n📁 测试应用结构...")
    
    required_files = [
        'app/main.py',
        'app/config/settings.py',
        'app/api/routes/video.py',
        'app/services/video_processor.py',
        'app/services/speech_service.py',
        'app/static/index.html',
        'app/static/js/main.js',
        'requirements.txt',
        '.env'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  缺少文件: {', '.join(missing_files)}")
        return False
    
    return True

def test_config_loading():
    """测试配置加载"""
    print("\n⚙️  测试配置加载...")
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        from app.config.settings import get_settings
        
        settings = get_settings()
        print(f"✅ 配置加载成功")
        print(f"   - 应用名称: {settings.app_name}")
        print(f"   - 调试模式: {settings.debug}")
        print(f"   - 语音服务: {settings.speech_service}")
        print(f"   - 视频服务: {settings.video_service}")
        
        return True
    
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_services():
    """测试服务模块"""
    print("\n🔧 测试服务模块...")
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        
        # 测试语音服务
        print("  🎤 测试语音服务...")
        from app.services.speech_service import SpeechService
        speech_service = SpeechService()
        print("  ✅ 语音服务初始化成功")
        
        # 测试视频处理服务
        print("  🎬 测试视频处理服务...")
        from app.services.video_processor import VideoProcessor
        video_processor = VideoProcessor()
        print("  ✅ 视频处理服务初始化成功")
        
        # 测试名称叠加服务
        print("  📝 测试名称叠加服务...")
        from app.services.name_overlay import NameOverlayService
        name_service = NameOverlayService()
        print("  ✅ 名称叠加服务初始化成功")
        
        return True
    
    except Exception as e:
        print(f"  ❌ 服务模块测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 测试API端点...")
    
    # 启动应用进行测试
    import subprocess
    import threading
    import time
    
    def start_server():
        """启动测试服务器"""
        try:
            subprocess.run([
                sys.executable, "-m", "app.main"
            ], cwd=Path.cwd(), timeout=5)
        except subprocess.TimeoutExpired:
            pass  # 预期的超时
        except Exception as e:
            print(f"  ⚠️  服务器启动错误: {e}")
    
    # 在后台启动服务器
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动
    time.sleep(3)
    
    # 测试端点
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "主页"),
        ("/docs", "API文档"),
        ("/health", "健康检查"),
        ("/static/index.html", "静态文件")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {name} ({endpoint})")
            else:
                print(f"  ⚠️  {name} ({endpoint}): HTTP {response.status_code}")
        except requests.RequestException as e:
            print(f"  ❌ {name} ({endpoint}): {e}")
    
    return True

def test_file_operations():
    """测试文件操作"""
    print("\n📄 测试文件操作...")
    
    try:
        # 测试临时目录创建
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        print("  ✅ 临时目录创建")
        
        # 测试文件写入
        test_file = temp_dir / "test.txt"
        test_file.write_text("测试内容", encoding='utf-8')
        print("  ✅ 文件写入")
        
        # 测试文件读取
        content = test_file.read_text(encoding='utf-8')
        if content == "测试内容":
            print("  ✅ 文件读取")
        else:
            print("  ❌ 文件读取内容不匹配")
        
        # 清理测试文件
        test_file.unlink()
        print("  ✅ 文件清理")
        
        return True
    
    except Exception as e:
        print(f"  ❌ 文件操作测试失败: {e}")
        return False

def generate_test_report(results):
    """生成测试报告"""
    print("\n" + "="*60)
    print("📊 测试报告")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"总测试数: {total_tests}")
    print(f"通过: {passed_tests}")
    print(f"失败: {failed_tests}")
    print(f"成功率: {passed_tests/total_tests*100:.1f}%")
    
    print("\n详细结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    if failed_tests == 0:
        print("\n🎉 所有测试通过！系统运行正常")
        print("\n可以运行以下命令启动系统:")
        print("  python quick_start.py")
        print("  或访问: http://localhost:8000")
    else:
        print(f"\n⚠️  有 {failed_tests} 个测试失败，请检查相关配置")

def main():
    """主函数"""
    print_header()
    
    print("开始系统测试...")
    print("提示: 按Ctrl+C可随时退出")
    
    try:
        # 执行各项测试
        results = {}
        
        results["环境配置"] = test_environment()
        results["模块导入"] = test_imports()
        results["应用结构"] = test_app_structure()
        results["配置加载"] = test_config_loading()
        results["服务模块"] = test_services()
        results["文件操作"] = test_file_operations()
        results["API端点"] = test_api_endpoints()
        
        # 生成测试报告
        generate_test_report(results)
        
    except KeyboardInterrupt:
        print("\n\n👋 测试已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()