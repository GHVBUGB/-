#!/usr/bin/env python3
"""
测试脚本：验证项目中的FFmpeg路径配置是否正确
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ffmpeg_paths():
    """测试各个模块中的FFmpeg路径配置"""
    print("🔍 测试FFmpeg路径配置...")
    
    # 测试 subtitle_burner 模块
    try:
        from app.utils.subtitle_burner import get_ffmpeg_path
        ffmpeg_path = get_ffmpeg_path()
        print(f"✅ subtitle_burner.get_ffmpeg_path(): {ffmpeg_path}")
        
        # 检查路径是否存在
        if Path(ffmpeg_path).exists():
            print(f"   ✅ 文件存在")
        else:
            print(f"   ❌ 文件不存在")
    except Exception as e:
        print(f"❌ subtitle_burner 测试失败: {e}")
    
    # 测试项目内bin目录
    bin_ffmpeg = project_root / "bin" / "ffmpeg.exe"
    print(f"\n📁 项目内FFmpeg路径: {bin_ffmpeg}")
    if bin_ffmpeg.exists():
        print("   ✅ 项目内FFmpeg存在")
    else:
        print("   ❌ 项目内FFmpeg不存在")
        print("   💡 请将ffmpeg.exe复制到bin目录中")
    
    # 测试系统FFmpeg
    import shutil
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        print(f"🖥️  系统FFmpeg路径: {system_ffmpeg}")
    else:
        print("🖥️  系统中未找到FFmpeg")
    
    # 测试Windows默认路径
    win_default = Path(r"C:\ffmpeg\bin\ffmpeg.exe")
    if win_default.exists():
        print(f"🪟 Windows默认FFmpeg存在: {win_default}")
    else:
        print("🪟 Windows默认FFmpeg不存在")

def test_import_modules():
    """测试导入修改后的模块"""
    print("\n🔧 测试模块导入...")
    
    modules_to_test = [
        "app.utils.subtitle_burner",
        "app.services.xunfei_asr_service", 
        "app.services.tencent_video_service",
        "app.services.video_processor",
        "app.utils.beautify_basic",
        "app.utils.quality_enhancer",
        "app.pipeline.v2_pipeline",
        "app.services.tencent_asr_sdk"
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {module_name}")
        except Exception as e:
            print(f"   ❌ {module_name}: {e}")

if __name__ == "__main__":
    print("🚀 开始测试FFmpeg路径配置...\n")
    test_ffmpeg_paths()
    test_import_modules()
    print("\n✨ 测试完成！")