#!/bin/bash

# Hugo文章多语言翻译脚本启动器
# 支持翻译到中文、法语、日语、西班牙语
# 使用方法: ./run_multi_translation.sh [选项] [参数]

echo "🚀 启动Hugo文章多语言翻译工具"
echo "================================"

# 检查是否在正确的目录
if [ ! -f "translate_multi_languages.py" ]; then
    echo "❌ 错误: 请在translation_langage目录下运行此脚本"
    exit 1
fi

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: 未找到uv，请先安装uv"
    echo "💡 安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh"
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
echo "🎯 开始多语言翻译..."

# 显示使用说明
show_usage() {
    echo ""
    echo "💡 使用方法:"
    echo "  $0                                    # 翻译所有文件到所有语言 (chinese, french, japanese, spanish)"
    echo "  $0 chinese french                     # 只翻译到指定语言"
    echo "  $0 file1.md file2.md                 # 只翻译指定文件到所有语言"
    echo "  $0 chinese file1.md file2.md         # 翻译指定文件到指定语言"
    echo ""
    echo "🌍 支持的语言: chinese, french, spanish, german, japanese, korean, italian, portuguese, russian"
    echo ""
}

# 检查参数
if [ $# -eq 0 ]; then
    echo "🌍 将翻译所有文件到所有语言: chinese, french, japanese, spanish"
    show_usage
    uv run translate_multi_languages.py
else
    # 检查第一个参数是否是语言
    first_arg="$1"
    case "$first_arg" in
        chinese|french|spanish|german|japanese|korean|italian|portuguese|russian)
            echo "🌍 指定目标语言: $*"
            ;;
        *.md)
            echo "📝 指定文件: $*"
            ;;
        *)
            echo "❌ 未知参数: $first_arg"
            show_usage
            exit 1
            ;;
    esac
    
    uv run translate_multi_languages.py "$@"
fi

echo ""
echo "✨ 多语言翻译完成！"
echo ""
echo "📁 翻译结果保存在以下目录:"
echo "   ../content/chinese/     - 中文版本"
echo "   ../content/french/      - 法语版本"
echo "   ../content/japanese/    - 日语版本"
echo "   ../content/spanish/     - 西班牙语版本"
