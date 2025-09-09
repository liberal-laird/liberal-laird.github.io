#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单文件多语言翻译脚本
用于翻译指定的单个文件到多个目标语言
使用方法: python translate_single_file.py <文件名> <语言1> <语言2> ...
例如: python translate_single_file.py Zinc.md chinese french japanese spanish
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict
from translate_articles import ArticleTranslator
from config import LANGUAGE_CONFIGS

class SingleFileMultiLanguageTranslator:
    def __init__(self, target_languages: List[str]):
        """
        初始化单文件多语言翻译器
        
        Args:
            target_languages: 目标语言列表
        """
        self.target_languages = target_languages
        self.supported_languages = {lang: config['name'] for lang, config in LANGUAGE_CONFIGS.items()}
        
        # 验证目标语言
        self._validate_languages()
        
        self.base_dir = Path(__file__).parent.parent
        self.english_dir = self.base_dir / "content" / "english"
        
        print(f"🌍 目标语言: {', '.join([self.supported_languages[lang] for lang in self.target_languages])}")
        print(f"📁 源目录: {self.english_dir}")
        
    def _validate_languages(self):
        """验证目标语言是否支持"""
        invalid_languages = []
        for lang in self.target_languages:
            if lang not in self.supported_languages:
                invalid_languages.append(lang)
        
        if invalid_languages:
            print(f"❌ 不支持的语言: {', '.join(invalid_languages)}")
            print(f"✅ 支持的语言: {', '.join(self.supported_languages.keys())}")
            sys.exit(1)
    
    def translate_file_to_languages(self, filename: str):
        """
        翻译指定文件到多个语言
        
        Args:
            filename: 要翻译的文件名
        """
        print("🚀 启动单文件多语言翻译工具")
        print("=" * 60)
        
        # 检查文件是否存在
        file_path = self.english_dir / filename
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            print(f"📁 请确保文件在目录中: {self.english_dir}")
            return
        
        print(f"📖 将翻译文件: {filename}")
        print(f"🌍 目标语言: {', '.join([self.supported_languages[lang] for lang in self.target_languages])}")
        
        # 统计结果
        results = {}
        
        # 逐个语言翻译
        for i, target_language in enumerate(self.target_languages, 1):
            print(f"\n{'='*60}")
            print(f"🌍 [{i}/{len(self.target_languages)}] 开始翻译到: {self.supported_languages[target_language]}")
            print(f"{'='*60}")
            
            try:
                # 创建翻译器实例
                translator = ArticleTranslator(target_language=target_language)
                
                # 测试连接
                if not translator.test_lm_studio_connection():
                    print(f"❌ 无法连接到LM Studio，跳过 {target_language} 翻译")
                    results[target_language] = {"success": False, "error": "连接失败"}
                    continue
                
                # 翻译文件
                success = translator.translate_article(file_path)
                results[target_language] = {"success": success, "error": None}
                
                if success:
                    print(f"✅ {self.supported_languages[target_language]} 翻译完成!")
                else:
                    print(f"❌ {self.supported_languages[target_language]} 翻译失败!")
                
                # 语言间延迟
                if i < len(self.target_languages):
                    print(f"\n⏳ 等待 2 秒后开始下一个语言...")
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                print(f"\n⚠️ 用户中断翻译，已停止")
                break
            except Exception as e:
                print(f"\n❌ 翻译 {target_language} 时发生错误: {e}")
                results[target_language] = {"success": False, "error": str(e)}
        
        # 显示结果摘要
        self._print_summary(results, filename)
    
    def _print_summary(self, results: Dict[str, Dict], filename: str):
        """打印翻译结果摘要"""
        print(f"\n{'='*60}")
        print(f"📊 翻译结果摘要 - {filename}")
        print(f"{'='*60}")
        
        success_count = 0
        failed_count = 0
        
        for language, result in results.items():
            lang_name = self.supported_languages[language]
            if result["success"]:
                success_count += 1
                print(f"✅ {lang_name:8} | 翻译成功")
            else:
                failed_count += 1
                error_msg = result.get("error", "未知错误")
                print(f"❌ {lang_name:8} | 翻译失败 - {error_msg}")
        
        print(f"{'='*60}")
        print(f"📈 总计: 成功 {success_count}/{len(self.target_languages)} 个翻译")
        
        if failed_count > 0:
            print(f"⚠️ 有 {failed_count} 个翻译失败，请检查日志")
        else:
            print("🎉 所有翻译都成功完成!")
        
        # 显示输出文件位置
        print(f"\n📁 翻译结果保存在:")
        for language in self.target_languages:
            if results[language]["success"]:
                output_dir = self.base_dir / "content" / language
                print(f"   {output_dir}")

def main():
    """主函数"""
    print("🚀 Hugo单文件多语言翻译工具")
    print("=" * 60)
    
    # 检查参数
    if len(sys.argv) < 3:
        print("❌ 参数不足")
        print("💡 使用方法:")
        print("   python translate_single_file.py <文件名> <语言1> <语言2> ...")
        print("   python translate_single_file.py Zinc.md chinese french japanese spanish")
        print("")
        print("🌍 支持的语言: chinese, french, spanish, german, japanese, korean, italian, portuguese, russian")
        sys.exit(1)
    
    # 解析参数
    filename = sys.argv[1]
    target_languages = sys.argv[2:]
    
    # 验证文件名
    if not filename.endswith('.md'):
        print(f"⚠️ 警告: 文件名 '{filename}' 不是 .md 文件")
    
    # 创建翻译器
    translator = SingleFileMultiLanguageTranslator(target_languages=target_languages)
    
    # 开始翻译
    try:
        translator.translate_file_to_languages(filename)
    except KeyboardInterrupt:
        print(f"\n⚠️ 用户中断翻译")
    except Exception as e:
        print(f"\n❌ 翻译过程中发生错误: {e}")

if __name__ == "__main__":
    main()
