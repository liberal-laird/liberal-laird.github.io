#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo文章多语言翻译脚本
支持从英文翻译到多种语言：中文、法语、日语、西班牙语
使用LM Studio本地API进行翻译
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict
from translate_articles import ArticleTranslator
from config import LANGUAGE_CONFIGS

class MultiLanguageTranslator:
    def __init__(self, target_languages: List[str] = None):
        """
        初始化多语言翻译器
        
        Args:
            target_languages: 目标语言列表，默认为 ['chinese', 'french', 'japanese', 'spanish']
        """
        if target_languages is None:
            target_languages = ['chinese', 'french', 'japanese', 'spanish']
        
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
    
    def get_english_files(self) -> List[Path]:
        """获取所有英文markdown文件"""
        if not self.english_dir.exists():
            print(f"❌ 英文目录不存在: {self.english_dir}")
            return []
        
        md_files = list(self.english_dir.glob("*.md"))
        if not md_files:
            print("❌ 未找到任何markdown文件")
            return []
        
        print(f"📚 找到 {len(md_files)} 个英文文件")
        return md_files
    
    def translate_to_language(self, target_language: str, english_files: List[Path]) -> Dict[str, int]:
        """
        翻译到指定语言
        
        Args:
            target_language: 目标语言
            english_files: 英文文件列表
            
        Returns:
            Dict[str, int]: 翻译结果统计
        """
        print(f"\n{'='*60}")
        print(f"🌍 开始翻译到: {self.supported_languages[target_language]}")
        print(f"{'='*60}")
        
        # 创建翻译器实例
        translator = ArticleTranslator(target_language=target_language)
        
        # 测试连接
        if not translator.test_lm_studio_connection():
            print(f"❌ 无法连接到LM Studio，跳过 {target_language} 翻译")
            return {"success": 0, "failed": len(english_files), "skipped": 0}
        
        success_count = 0
        failed_count = 0
        
        for i, md_file in enumerate(english_files, 1):
            print(f"\n📖 [{i}/{len(english_files)}] 翻译: {md_file.name}")
            if translator.translate_article(md_file):
                success_count += 1
            else:
                failed_count += 1
            
            # 添加文件间延迟
            if i < len(english_files):
                time.sleep(1)
        
        print(f"\n✅ {self.supported_languages[target_language]} 翻译完成!")
        print(f"   成功: {success_count}, 失败: {failed_count}")
        
        return {"success": success_count, "failed": failed_count, "skipped": 0}
    
    def translate_all_languages(self, specific_files: List[str] = None):
        """
        翻译所有目标语言
        
        Args:
            specific_files: 指定要翻译的文件名列表，如果为None则翻译所有文件
        """
        print("🚀 启动多语言翻译工具")
        print("=" * 60)
        
        # 获取英文文件
        all_english_files = self.get_english_files()
        if not all_english_files:
            return
        
        # 如果指定了特定文件，则过滤
        if specific_files:
            english_files = []
            for file_name in specific_files:
                file_path = self.english_dir / file_name
                if file_path.exists():
                    english_files.append(file_path)
                else:
                    print(f"⚠️ 文件不存在: {file_name}")
            
            if not english_files:
                print("❌ 没有找到指定的文件")
                return
        else:
            english_files = all_english_files
        
        print(f"📝 将翻译 {len(english_files)} 个文件到 {len(self.target_languages)} 种语言")
        
        # 统计总体结果
        total_results = {}
        
        # 逐个语言翻译
        for target_language in self.target_languages:
            try:
                results = self.translate_to_language(target_language, english_files)
                total_results[target_language] = results
                
                # 语言间延迟
                if target_language != self.target_languages[-1]:
                    print(f"\n⏳ 等待 3 秒后开始下一个语言...")
                    time.sleep(3)
                    
            except KeyboardInterrupt:
                print(f"\n⚠️ 用户中断翻译，已停止")
                break
            except Exception as e:
                print(f"\n❌ 翻译 {target_language} 时发生错误: {e}")
                total_results[target_language] = {"success": 0, "failed": len(english_files), "skipped": 0}
        
        # 显示总体结果
        self._print_summary(total_results, len(english_files))
    
    def _print_summary(self, results: Dict[str, Dict], total_files: int):
        """打印翻译结果摘要"""
        print(f"\n{'='*60}")
        print("📊 翻译结果摘要")
        print(f"{'='*60}")
        
        total_success = 0
        total_failed = 0
        
        for language, result in results.items():
            lang_name = self.supported_languages[language]
            success = result["success"]
            failed = result["failed"]
            total_success += success
            total_failed += failed
            
            print(f"🌍 {lang_name:8} | 成功: {success:2}/{total_files} | 失败: {failed:2}")
        
        print(f"{'='*60}")
        print(f"📈 总计: 成功 {total_success}/{total_files * len(self.target_languages)} 个翻译")
        
        if total_failed > 0:
            print(f"⚠️ 有 {total_failed} 个翻译失败，请检查日志")
        else:
            print("🎉 所有翻译都成功完成!")

def main():
    """主函数"""
    print("🚀 Hugo文章多语言翻译工具")
    print("=" * 60)
    
    # 解析命令行参数
    target_languages = None
    specific_files = None
    
    if len(sys.argv) > 1:
        # 检查是否是语言参数
        if sys.argv[1] in ['chinese', 'french', 'japanese', 'spanish', 'german', 'korean', 'italian', 'portuguese', 'russian']:
            target_languages = sys.argv[1:]
        else:
            # 假设是文件名参数
            specific_files = sys.argv[1:]
    
    # 创建多语言翻译器
    translator = MultiLanguageTranslator(target_languages=target_languages)
    
    # 显示使用说明
    if not target_languages and not specific_files:
        print("💡 使用方法:")
        print("   python translate_multi_languages.py                    # 翻译所有文件到所有语言")
        print("   python translate_multi_languages.py chinese french     # 只翻译到指定语言")
        print("   python translate_multi_languages.py file1.md file2.md  # 只翻译指定文件")
        print("   python translate_multi_languages.py chinese file1.md   # 翻译指定文件到指定语言")
        print("")
        print("🌍 支持的语言: chinese, french, spanish, german, japanese, korean, italian, portuguese, russian")
        print("")
    
    # 开始翻译
    try:
        translator.translate_all_languages(specific_files=specific_files)
    except KeyboardInterrupt:
        print(f"\n⚠️ 用户中断翻译")
    except Exception as e:
        print(f"\n❌ 翻译过程中发生错误: {e}")

if __name__ == "__main__":
    main()
