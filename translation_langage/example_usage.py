#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言翻译脚本使用示例
演示如何使用translate_multi_languages.py进行批量翻译
"""

from translate_multi_languages import MultiLanguageTranslator

def example_translate_all_languages():
    """示例：翻译所有文件到所有语言"""
    print("示例1: 翻译所有文件到所有语言")
    print("=" * 50)
    
    # 创建翻译器，使用默认语言列表
    translator = MultiLanguageTranslator()
    
    # 开始翻译
    translator.translate_all_languages()

def example_translate_specific_languages():
    """示例：只翻译到指定语言"""
    print("示例2: 只翻译到中文和法语")
    print("=" * 50)
    
    # 创建翻译器，指定目标语言
    translator = MultiLanguageTranslator(target_languages=['chinese', 'french'])
    
    # 开始翻译
    translator.translate_all_languages()

def example_translate_specific_files():
    """示例：只翻译指定文件"""
    print("示例3: 只翻译指定文件")
    print("=" * 50)
    
    # 创建翻译器
    translator = MultiLanguageTranslator()
    
    # 指定要翻译的文件
    specific_files = ['example.md', 'another_file.md']
    
    # 开始翻译
    translator.translate_all_languages(specific_files=specific_files)

def example_translate_specific_files_to_specific_languages():
    """示例：翻译指定文件到指定语言"""
    print("示例4: 翻译指定文件到指定语言")
    print("=" * 50)
    
    # 创建翻译器，指定目标语言
    translator = MultiLanguageTranslator(target_languages=['japanese', 'spanish'])
    
    # 指定要翻译的文件
    specific_files = ['example.md']
    
    # 开始翻译
    translator.translate_all_languages(specific_files=specific_files)

if __name__ == "__main__":
    print("🚀 多语言翻译脚本使用示例")
    print("=" * 60)
    print()
    
    # 运行示例（注释掉不需要的示例）
    
    # 示例1: 翻译所有文件到所有语言
    # example_translate_all_languages()
    
    # 示例2: 只翻译到指定语言
    # example_translate_specific_languages()
    
    # 示例3: 只翻译指定文件
    # example_translate_specific_files()
    
    # 示例4: 翻译指定文件到指定语言
    # example_translate_specific_files_to_specific_languages()
    
    print("💡 要运行示例，请取消注释相应的函数调用")
    print("💡 或者直接使用命令行:")
    print("   python translate_multi_languages.py")
    print("   python translate_multi_languages.py chinese french")
    print("   python translate_multi_languages.py file1.md file2.md")
