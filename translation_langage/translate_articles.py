#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo文章翻译脚本
使用LM Studio本地API翻译英文文章到中文
保持Markdown格式和frontmatter结构不变
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Tuple
import yaml
from config import (
    LM_STUDIO_URL, MODEL_NAME, API_CONFIG, TRANSLATION_CONFIG,
    TRANSLATION_PROMPT, FRONTMATTER_FIELDS_TO_TRANSLATE,
    FRONTMATTER_FIELDS_TO_PRESERVE, SYSTEM_REQUIREMENTS, PERFORMANCE_CONFIG
)

class ArticleTranslator:
    def __init__(self, target_language: str = "chinese", lm_studio_url: str = LM_STUDIO_URL):
        """
        初始化翻译器
        
        Args:
            target_language: 目标语言 (chinese, french, spanish等)
            lm_studio_url: LM Studio API地址
        """
        self.lm_studio_url = lm_studio_url
        self.model_name = MODEL_NAME
        self.api_config = API_CONFIG
        self.translation_config = TRANSLATION_CONFIG
        # 根据目标语言调整翻译提示词
        self.translation_prompt = self._get_translation_prompt(target_language)
        self.frontmatter_fields_to_translate = FRONTMATTER_FIELDS_TO_TRANSLATE
        self.frontmatter_fields_to_preserve = FRONTMATTER_FIELDS_TO_PRESERVE
        self.target_language = target_language
        
        self.base_dir = Path(__file__).parent.parent
        self.english_dir = self.base_dir / "content" / "english"
        self.target_dir = self.base_dir / "content" / target_language
        
        # 确保目标语言目录存在
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # 显示配置信息
        print(f"🤖 使用模型: {self.model_name}")
        print(f"🌍 目标语言: {target_language}")
        print(f"📁 输出目录: {self.target_dir}")
        print(f"📊 块大小: {self.translation_config['max_chunk_size']} 字符")
        print(f"🔄 最大重试: {self.translation_config['max_retries']} 次")

    def _get_translation_prompt(self, target_language: str) -> str:
        """根据目标语言获取翻译提示词"""
        language_map = {
            "chinese": "中文",
            "french": "法语", 
            "spanish": "西班牙语",
            "german": "德语",
            "japanese": "日语",
            "korean": "韩语",
            "italian": "意大利语",
            "portuguese": "葡萄牙语",
            "russian": "俄语"
        }
        
        target_lang_name = language_map.get(target_language, target_language)
        
        return f"""You are a professional medical and nutritional translation expert. Please translate the following English content to {target_lang_name} with these requirements:

1. Keep all Markdown formatting exactly the same (including headers, tables, lists, links, etc.)
2. Keep the frontmatter YAML structure unchanged, only translate text content
3. Medical terms must be accurately translated with professional terminology
4. Maintain the original logical structure and paragraph divisions
5. Do not add any explanations or comments
6. For tables, keep the table structure and only translate the content
7. Keep numbers, dates, and citation formats unchanged
8. Use proper {target_lang_name} medical terminology and maintain academic rigor
9. Ensure consistency in medical terminology throughout the document

Please output only the translation result without any prefix or suffix explanations."""

    def test_lm_studio_connection(self) -> bool:
        """测试LM Studio连接"""
        try:
            test_payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": "Hello, please respond with 'OK'"}
                ],
                **{k: v for k, v in self.api_config.items() if k != "max_tokens"},
                "max_tokens": 10
            }
            
            response = requests.post(
                self.lm_studio_url,
                json=test_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ LM Studio连接成功")
                return True
            else:
                print(f"❌ LM Studio连接失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ LM Studio连接错误: {e}")
            return False

    def parse_markdown_file(self, file_path: Path) -> Tuple[Dict, str, str]:
        """
        解析Markdown文件，分离frontmatter和内容
        
        Returns:
            Tuple[Dict, str, str]: (frontmatter_dict, markdown_content, original_frontmatter_str)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有frontmatter
        if content.startswith('+++'):
            # 找到frontmatter结束位置
            end_pos = content.find('+++', 3)
            if end_pos != -1:
                frontmatter_str = content[3:end_pos]
                markdown_content = content[end_pos + 3:].strip()
                
                # 解析frontmatter
                try:
                    frontmatter = yaml.safe_load(frontmatter_str)
                    # 确保返回的是字典类型
                    if not isinstance(frontmatter, dict):
                        print(f"⚠️ frontmatter解析结果不是字典: {type(frontmatter)}")
                        return {}, markdown_content, frontmatter_str
                    return frontmatter, markdown_content, frontmatter_str
                except yaml.YAMLError as e:
                    print(f"⚠️ 解析frontmatter失败: {e}")
                    return {}, markdown_content, frontmatter_str
            else:
                print("⚠️ 未找到frontmatter结束标记")
                return {}, content, ""
        else:
            return {}, content, ""

    def translate_text(self, text: str, max_retries: int = None) -> str:
        """
        使用LM Studio翻译文本
        
        Args:
            text: 要翻译的文本
            max_retries: 最大重试次数
            
        Returns:
            str: 翻译后的文本
        """
        if not text.strip():
            return text
            
        if max_retries is None:
            max_retries = self.translation_config['max_retries']
            
        for attempt in range(max_retries):
            try:
                payload = {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": self.translation_prompt},
                        {"role": "user", "content": text}
                    ],
                    **self.api_config
                }
                
                response = requests.post(
                    self.lm_studio_url,
                    json=payload,
                    timeout=PERFORMANCE_CONFIG['timeout_seconds']
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        translated_text = result['choices'][0]['message']['content'].strip()
                        return translated_text
                    else:
                        print(f"⚠️ API响应格式异常: {result}")
                else:
                    print(f"⚠️ API请求失败: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"⚠️ 翻译请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(self.translation_config['retry_delay'])
                    
        print(f"❌ 翻译失败，已重试{max_retries}次")
        return text  # 返回原文

    def translate_frontmatter(self, frontmatter: Dict) -> Dict:
        """翻译frontmatter中的文本字段，保持结构字段不变"""
        # 确保frontmatter是字典类型
        if not isinstance(frontmatter, dict):
            print(f"  ⚠️ frontmatter不是字典类型: {type(frontmatter)}")
            return frontmatter
            
        translated = frontmatter.copy()
        
        print("  处理frontmatter字段...")
        for field, value in translated.items():
            # 只翻译指定的字段，且必须是字符串类型
            if (field in self.frontmatter_fields_to_translate and 
                isinstance(value, str) and 
                field not in self.frontmatter_fields_to_preserve):
                print(f"    翻译字段: {field}")
                translated[field] = self.translate_text(value)
            else:
                print(f"    保持字段: {field} (不翻译)")
                
        return translated

    def split_content_for_translation(self, content: str, max_chunk_size: int = None) -> List[str]:
        """
        将内容分割成适合翻译的块
        保持Markdown结构完整性
        针对GPT-OSS-20B模型优化
        """
        if max_chunk_size is None:
            max_chunk_size = self.translation_config['max_chunk_size']
        chunks = []
        current_chunk = ""
        
        # 按段落分割
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            # 如果当前块加上新段落不会超过限制
            if len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:
                if current_chunk:
                    current_chunk += '\n\n' + paragraph
                else:
                    current_chunk = paragraph
            else:
                # 保存当前块
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph
                
        # 添加最后一个块
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    def translate_markdown_content(self, content: str) -> str:
        """翻译Markdown内容"""
        if not content.strip():
            return content
            
        # 分割内容
        chunks = self.split_content_for_translation(content)
        translated_chunks = []
        
        for i, chunk in enumerate(chunks):
            print(f"  翻译块 {i + 1}/{len(chunks)}...")
            translated_chunk = self.translate_text(chunk)
            translated_chunks.append(translated_chunk)
            
            # 添加延迟避免API限制
            if i < len(chunks) - 1:
                time.sleep(self.translation_config['chunk_delay'])
                
        return '\n\n'.join(translated_chunks)

    def translate_frontmatter_string(self, frontmatter_str: str) -> str:
        """翻译frontmatter字符串中的特定字段值"""
        lines = frontmatter_str.split('\n')
        translated_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            should_translate = False
            field_name = ""
            
            # 检查需要翻译的字段
            for field in self.frontmatter_fields_to_translate:
                if line_stripped.startswith(f'{field} =') or line_stripped.startswith(f'{field}='):
                    should_translate = True
                    field_name = field
                    break
            
            if should_translate and '=' in line:
                # 提取字段名和值
                key, value = line.split('=', 1)
                value = value.strip()
                
                # 处理不同类型的值
                if value.startswith('[') and value.endswith(']'):
                    # 处理数组类型（如keywords）
                    print(f"    翻译字段: {field_name} (数组)")
                    # 提取数组内容
                    array_content = value[1:-1]
                    if array_content.strip():
                        # 翻译数组中的每个元素
                        items = [item.strip().strip('"\'') for item in array_content.split(',')]
                        translated_items = []
                        for item in items:
                            if item.strip():
                                translated_item = self.translate_text(item)
                                translated_items.append(f'"{translated_item}"')
                            else:
                                translated_items.append(f'"{item}"')
                        translated_value = f"[{', '.join(translated_items)}]"
                        translated_line = f"{key}= {translated_value}"
                        translated_lines.append(translated_line)
                    else:
                        translated_lines.append(line)
                else:
                    # 处理字符串类型
                    # 移除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # 翻译值
                    if value.strip():
                        print(f"    翻译字段: {field_name}")
                        translated_value = self.translate_text(value)
                        # 重新添加引号
                        translated_line = f"{key}= \"{translated_value}\""
                        translated_lines.append(translated_line)
                    else:
                        translated_lines.append(line)
            else:
                # 其他字段保持不变
                translated_lines.append(line)
        
        return '\n'.join(translated_lines)

    def save_translated_file(self, frontmatter: Dict, content: str, output_path: Path, original_frontmatter_str: str = ""):
        """保存翻译后的文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            if frontmatter:
                f.write('+++\n')
                yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
                f.write('+++\n\n')
            elif original_frontmatter_str:
                # 如果frontmatter解析失败，尝试翻译特定字段
                print("  尝试翻译frontmatter中的特定字段...")
                translated_frontmatter_str = self.translate_frontmatter_string(original_frontmatter_str)
                f.write('+++')
                f.write(translated_frontmatter_str)
                f.write('+++\n\n')
            f.write(content)

    def translate_article(self, english_file: Path) -> bool:
        """
        翻译单个文章
        
        Args:
            english_file: 英文文章文件路径
            
        Returns:
            bool: 翻译是否成功
        """
        print(f"\n📖 开始翻译: {english_file.name}")
        
        try:
            # 解析文件
            frontmatter, content, original_frontmatter_str = self.parse_markdown_file(english_file)
            
            # 翻译frontmatter
            if frontmatter:
                print("  翻译frontmatter...")
                translated_frontmatter = self.translate_frontmatter(frontmatter)
            else:
                translated_frontmatter = {}
                
            # 翻译内容
            if content.strip():
                print("  翻译文章内容...")
                translated_content = self.translate_markdown_content(content)
            else:
                translated_content = content
                
            # 保存翻译后的文件
            output_path = self.target_dir / english_file.name
            self.save_translated_file(translated_frontmatter, translated_content, output_path, original_frontmatter_str)
            
            print(f"✅ 翻译完成: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 翻译失败 {english_file.name}: {e}")
            return False

    def translate_all_articles(self):
        """翻译所有英文文章"""
        if not self.english_dir.exists():
            print(f"❌ 英文目录不存在: {self.english_dir}")
            return
            
        # 测试连接
        if not self.test_lm_studio_connection():
            print("❌ 无法连接到LM Studio，请确保LM Studio正在运行")
            return
            
        # 获取所有markdown文件
        md_files = list(self.english_dir.glob("*.md"))
        
        if not md_files:
            print("❌ 未找到任何markdown文件")
            return
            
        print(f"📚 找到 {len(md_files)} 个文件需要翻译到 {self.target_language}")
        print(f"📁 输出目录: {self.target_dir}")
        
        success_count = 0
        for md_file in md_files:
            if self.translate_article(md_file):
                success_count += 1
                
        print(f"\n🎉 翻译完成! 成功翻译 {success_count}/{len(md_files)} 个文件到 {self.target_language}")

def main():
    """主函数"""
    import sys
    
    print("🚀 Hugo文章翻译工具启动")
    print("=" * 50)
    
    # 获取目标语言参数
    target_language = "chinese"  # 默认目标语言
    if len(sys.argv) > 1:
        target_language = sys.argv[1]
        print(f"🌍 指定目标语言: {target_language}")
    else:
        print(f"🌍 使用默认目标语言: {target_language}")
        print("💡 使用方法: python translate_articles.py [目标语言]")
        print("💡 支持的语言: chinese, french, spanish, german, japanese, korean, italian, portuguese, russian")
    
    # 创建翻译器实例
    translator = ArticleTranslator(target_language=target_language)
    
    # 开始翻译
    translator.translate_all_articles()

if __name__ == "__main__":
    main()
