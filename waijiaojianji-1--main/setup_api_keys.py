#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外教视频处理系统 - API Keys 配置工具
交互式配置OpenAI和腾讯云API Keys
"""

import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv, set_key

def print_header():
    """打印配置工具标题"""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   API Keys 配置工具                          ║
    ║                                                              ║
    ║   配置OpenAI和腾讯云API Keys以启用完整功能                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)

def get_user_input(prompt, default="", required=True):
    """获取用户输入"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if user_input or not required:
            return user_input
        
        print("❌ 此项为必填项，请输入有效值")

def test_openai_api(api_key):
    """测试OpenAI API Key"""
    print("🔍 测试OpenAI API Key...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            'https://api.openai.com/v1/models',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ OpenAI API Key 验证成功")
            return True
        else:
            print(f"❌ OpenAI API Key 验证失败: {response.status_code}")
            return False
    
    except requests.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False

def test_tencent_api(secret_id, secret_key):
    """测试腾讯云API Keys"""
    print("🔍 测试腾讯云API Keys...")
    
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.asr.v20190614 import asr_client
        
        cred = credential.Credential(secret_id, secret_key)
        client_profile = ClientProfile()
        client = asr_client.AsrClient(cred, "ap-beijing", client_profile)
        
        print("✅ 腾讯云API Keys 格式验证成功")
        return True
    
    except Exception as e:
        print(f"❌ 腾讯云API Keys 验证失败: {e}")
        return False

def configure_openai():
    """配置OpenAI API Key"""
    print("\n" + "="*60)
    print("🤖 配置 OpenAI API Key")
    print("="*60)
    print("用于语音转文字功能")
    print("获取地址: https://platform.openai.com/api-keys")
    print()
    
    current_key = os.getenv('OPENAI_API_KEY', '')
    if current_key and not current_key.startswith('sk-your-'):
        print(f"当前配置: {current_key[:10]}...{current_key[-4:]}")
        if get_user_input("是否保持当前配置？(y/n)", "y").lower() == 'y':
            return current_key
    
    while True:
        api_key = get_user_input("请输入OpenAI API Key (sk-...)")
        
        if not api_key.startswith('sk-'):
            print("❌ OpenAI API Key应该以'sk-'开头")
            continue
        
        if test_openai_api(api_key):
            return api_key
        
        retry = get_user_input("是否重新输入？(y/n)", "y").lower()
        if retry != 'y':
            return None

def configure_tencent():
    """配置腾讯云API Keys"""
    print("\n" + "="*60)
    print("☁️  配置 腾讯云 API Keys")
    print("="*60)
    print("用于视频背景移除和语音识别功能")
    print("获取地址: https://console.cloud.tencent.com/cam/capi")
    print()
    
    current_id = os.getenv('TENCENT_SECRET_ID', '')
    current_key = os.getenv('TENCENT_SECRET_KEY', '')
    
    if current_id and not current_id.startswith('your-'):
        print(f"当前Secret ID: {current_id[:8]}...{current_id[-4:]}")
        if get_user_input("是否保持当前配置？(y/n)", "y").lower() == 'y':
            return current_id, current_key
    
    while True:
        secret_id = get_user_input("请输入腾讯云 Secret ID")
        secret_key = get_user_input("请输入腾讯云 Secret Key")
        
        if test_tencent_api(secret_id, secret_key):
            return secret_id, secret_key
        
        retry = get_user_input("是否重新输入？(y/n)", "y").lower()
        if retry != 'y':
            return None, None

def configure_optional_settings():
    """配置可选设置"""
    print("\n" + "="*60)
    print("⚙️  可选配置")
    print("="*60)
    
    settings = {}
    
    # 服务选择
    print("\n语音识别服务选择:")
    print("1. OpenAI Whisper (推荐，准确度高)")
    print("2. 讯飞ASR (速度快)")
    print("3. 腾讯云ASR")
    
    choice = get_user_input("请选择语音识别服务 (1-3)", "1", False)
    service_map = {"1": "openai", "2": "xunfei", "3": "tencent"}
    settings['SPEECH_SERVICE'] = service_map.get(choice, "openai")
    
    # 视频处理服务
    print("\n视频背景移除服务:")
    print("1. 腾讯云 (推荐)")
    print("2. 本地处理")
    
    choice = get_user_input("请选择视频处理服务 (1-2)", "1", False)
    video_service_map = {"1": "tencent", "2": "local"}
    settings['VIDEO_SERVICE'] = video_service_map.get(choice, "tencent")
    
    return settings

def save_configuration(openai_key, tencent_id, tencent_key, optional_settings):
    """保存配置到.env文件"""
    print("\n💾 保存配置...")
    
    env_file = Path(".env")
    
    # 确保.env文件存在
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    # 保存API Keys
    if openai_key:
        set_key(env_file, 'OPENAI_API_KEY', openai_key)
    
    if tencent_id and tencent_key:
        set_key(env_file, 'TENCENT_SECRET_ID', tencent_id)
        set_key(env_file, 'TENCENT_SECRET_KEY', tencent_key)
        set_key(env_file, 'TENCENT_ASR_SECRET_ID', tencent_id)
        set_key(env_file, 'TENCENT_ASR_SECRET_KEY', tencent_key)
        set_key(env_file, 'TENCENT_TMT_SECRET_ID', tencent_id)
        set_key(env_file, 'TENCENT_TMT_SECRET_KEY', tencent_key)
    
    # 保存可选设置
    for key, value in optional_settings.items():
        set_key(env_file, key, value)
    
    print("✅ 配置已保存到.env文件")

def main():
    """主函数"""
    print_header()
    
    # 加载现有配置
    load_dotenv()
    
    print("开始配置API Keys...")
    print("提示: 按Ctrl+C可随时退出")
    
    try:
        # 配置OpenAI
        openai_key = configure_openai()
        if not openai_key:
            print("⚠️  跳过OpenAI配置，语音转文字功能将不可用")
        
        # 配置腾讯云
        tencent_id, tencent_key = configure_tencent()
        if not tencent_id or not tencent_key:
            print("⚠️  跳过腾讯云配置，视频背景移除功能将不可用")
        
        # 可选配置
        optional_settings = configure_optional_settings()
        
        # 保存配置
        save_configuration(openai_key, tencent_id, tencent_key, optional_settings)
        
        print("\n" + "="*60)
        print("🎉 配置完成！")
        print("="*60)
        print("现在可以运行以下命令启动系统:")
        print("  python quick_start.py")
        print("或者:")
        print("  python -m app.main")
        
    except KeyboardInterrupt:
        print("\n\n👋 配置已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 配置过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()