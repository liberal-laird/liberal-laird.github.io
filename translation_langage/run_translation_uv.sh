#!/bin/bash

# Hugo文章翻译脚本启动器 (使用uv)
# 使用方法: ./run_translation_uv.sh

echo "🚀 启动Hugo文章翻译工具 (uv版本)"
echo "================================"

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: 未找到uv，请先安装uv"
    echo "💡 安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "translate_articles.py" ]; then
    echo "❌ 错误: 请在translation_langage目录下运行此脚本"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖..."
uv run python -c "import requests, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ 依赖未安装，正在安装..."
    uv pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 检查LM Studio连接
echo "🔗 检查LM Studio连接..."
uv run python -c "
import requests
import json
try:
    response = requests.get('http://localhost:1234/v1/models', timeout=5)
    if response.status_code == 200:
        models = response.json()
        if 'data' in models and len(models['data']) > 0:
            model_name = models['data'][0].get('id', 'unknown')
            print(f'✅ LM Studio连接正常，当前模型: {model_name}')
            if 'openai/gpt-oss-20b' in model_name.lower() or 'gpt-oss-20b' in model_name.lower():
                print('✅ 检测到GPT-OSS-20B模型，配置正确')
            else:
                print('⚠️ 建议使用openai/gpt-oss-20b模型以获得最佳翻译效果')
        else:
            print('✅ LM Studio连接正常')
    else:
        print('⚠️ LM Studio响应异常，但可能仍在运行')
except Exception as e:
    print('❌ 无法连接到LM Studio')
    print('请确保LM Studio正在运行并监听端口1234')
    print('建议加载openai/gpt-oss-20b模型')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "💡 提示:"
    echo "1. 启动LM Studio"
    echo "2. 加载 openai/gpt-oss-20b 模型"
    echo "3. 启动本地服务器"
    echo "4. 重新运行此脚本"
    exit 1
fi

echo ""
echo "🎯 开始翻译..."

# 检查是否有目标语言参数
if [ $# -eq 0 ]; then
    echo "🌍 使用默认目标语言: chinese"
    echo "💡 使用方法: $0 [目标语言]"
    echo "💡 支持的语言: chinese, french, spanish, german, japanese, korean, italian, portuguese, russian"
    uv run translate_articles.py
else
    echo "🌍 指定目标语言: $1"
    uv run translate_articles.py "$1"
fi

echo ""
echo "✨ 翻译完成！"
