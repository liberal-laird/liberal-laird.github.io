#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置测试脚本
测试GPT-OSS-20B模型配置和连接
"""

import requests
import json
from config import (
    LM_STUDIO_URL, MODEL_NAME, API_CONFIG, TRANSLATION_CONFIG,
    SYSTEM_REQUIREMENTS, PERFORMANCE_CONFIG
)

def test_lm_studio_connection():
    """测试LM Studio连接和模型"""
    print("🔗 测试LM Studio连接...")
    print(f"📍 API地址: {LM_STUDIO_URL}")
    print(f"🤖 模型名称: {MODEL_NAME}")
    print("-" * 50)
    
    try:
        # 测试基本连接
        response = requests.get(f"{LM_STUDIO_URL.replace('/v1/chat/completions', '/v1/models')}", timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ LM Studio连接成功")
            
            if 'data' in models and len(models['data']) > 0:
                current_model = models['data'][0].get('id', 'unknown')
                print(f"📋 当前模型: {current_model}")
                
                if MODEL_NAME.lower() in current_model.lower() or 'gpt-oss-20b' in current_model.lower():
                    print("✅ 检测到正确的GPT-OSS-20B模型")
                else:
                    print("⚠️ 当前模型与配置不匹配")
                    print(f"   配置模型: {MODEL_NAME}")
                    print(f"   当前模型: {current_model}")
            else:
                print("⚠️ 未检测到加载的模型")
        else:
            print(f"❌ LM Studio响应异常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False
    
    # 测试翻译功能
    print("\n🧪 测试翻译功能...")
    test_text = "Hello, this is a test translation."
    
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a translator. Translate the following text to Chinese."},
                {"role": "user", "content": test_text}
            ],
            **API_CONFIG
        }
        
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                translation = result['choices'][0]['message']['content']
                print(f"✅ 翻译测试成功")
                print(f"   原文: {test_text}")
                print(f"   译文: {translation}")
                return True
            else:
                print("❌ 翻译响应格式异常")
                return False
        else:
            print(f"❌ 翻译请求失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 翻译测试失败: {e}")
        return False

def show_configuration():
    """显示当前配置"""
    print("⚙️ 当前配置信息")
    print("=" * 50)
    print(f"🌐 API地址: {LM_STUDIO_URL}")
    print(f"🤖 模型名称: {MODEL_NAME}")
    print(f"📊 块大小: {TRANSLATION_CONFIG['max_chunk_size']} 字符")
    print(f"🔄 最大重试: {TRANSLATION_CONFIG['max_retries']} 次")
    print(f"⏱️ 重试延迟: {TRANSLATION_CONFIG['retry_delay']} 秒")
    print(f"⏳ 块间延迟: {TRANSLATION_CONFIG['chunk_delay']} 秒")
    print(f"⏰ 请求超时: {PERFORMANCE_CONFIG['timeout_seconds']} 秒")
    print(f"💾 最小内存要求: {SYSTEM_REQUIREMENTS['min_memory_gb']} GB")
    print(f"💾 推荐内存: {SYSTEM_REQUIREMENTS['recommended_memory_gb']} GB")
    print(f"📦 模型大小: {SYSTEM_REQUIREMENTS['model_size_gb']} GB")
    print()
    print("🔧 API参数:")
    for key, value in API_CONFIG.items():
        print(f"   {key}: {value}")

def main():
    """主函数"""
    print("🚀 GPT-OSS-20B配置测试工具")
    print("=" * 50)
    
    show_configuration()
    print()
    
    if test_lm_studio_connection():
        print("\n🎉 所有测试通过！可以开始翻译了。")
        print("💡 运行命令: python translate_articles.py")
    else:
        print("\n❌ 测试失败，请检查配置和LM Studio设置。")
        print("💡 确保:")
        print("   1. LM Studio正在运行")
        print("   2. 已加载openai/gpt-oss-20b模型")
        print("   3. 本地服务器在端口1234上运行")

if __name__ == "__main__":
    main()
