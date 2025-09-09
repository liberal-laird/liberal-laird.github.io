#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-OSS-20B模型配置文件
针对openai/gpt-oss-20b模型优化的翻译参数
"""

# LM Studio配置
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "openai/gpt-oss-20b"

# API参数配置（针对GPT-OSS-20B优化）
API_CONFIG = {
    "temperature": 0.2,        # 稍微提高温度以获得更好的翻译质量
    "max_tokens": 6000,        # 增加token限制以处理更长的内容
    "top_p": 0.9,             # 核采样参数
    "frequency_penalty": 0.0,  # 频率惩罚
    "presence_penalty": 0.0,   # 存在惩罚
    "stream": False,           # 非流式输出
}

# 翻译配置
TRANSLATION_CONFIG = {
    "max_chunk_size": 3000,    # 针对GPT-OSS-20B优化的块大小
    "max_retries": 3,          # 最大重试次数
    "retry_delay": 2,          # 重试延迟（秒）
    "chunk_delay": 1,          # 块间延迟（秒）
}

# 针对GPT-OSS-20B优化的翻译提示词模板
TRANSLATION_PROMPT_TEMPLATE = """You are a professional medical and nutritional translation expert. Please translate the following English content to {target_language} with these requirements:

1. Keep all Markdown formatting exactly the same (including headers, tables, lists, links, etc.)
2. Keep the frontmatter YAML structure unchanged, only translate text content
3. Medical terms must be accurately translated with professional terminology
4. Maintain the original logical structure and paragraph divisions
5. Do not add any explanations or comments
6. For tables, keep the table structure and only translate the content
7. Keep numbers, dates, and citation formats unchanged
8. Use proper {target_language} medical terminology and maintain academic rigor
9. Ensure consistency in medical terminology throughout the document
10. For {target_language}, use appropriate cultural and linguistic conventions

Please output only the translation result without any prefix or suffix explanations."""

# 默认中文翻译提示词（向后兼容）
TRANSLATION_PROMPT = TRANSLATION_PROMPT_TEMPLATE.format(target_language="中文")

# 需要翻译的frontmatter字段
FRONTMATTER_FIELDS_TO_TRANSLATE = [
    'title',
    'description',
    'keywords',
    'categories',
    'tags'
]

# 不需要翻译的frontmatter字段（保持原样）
FRONTMATTER_FIELDS_TO_PRESERVE = [
    'date',
    'draft', 
    'url',
    'tags',
    'categories',
    'keywords',
    'weight',
    'menu',
    'layout',
    'type',
    'author',
    'slug',
    'aliases',
    'series',
    'lastmod',
    'publishdate',
    'expirydate',
    'images',
    'featured_image',
    'featured_image_path',
    'featured_image_alt',
    'featured_image_caption',
    'gallery',
    'video',
    'audio',
    'link',
    'external_link',
    'external_link_name',
    'external_link_description',
    'external_link_icon',
    'external_link_target',
    'external_link_rel',
    'external_link_class',
    'external_link_style',
    'external_link_title',
    'external_link_aria_label',
    'external_link_aria_describedby',
    'external_link_aria_expanded',
    'external_link_aria_haspopup',
    'external_link_aria_controls',
    'external_link_aria_labelledby',
    'external_link_aria_owns',
    'external_link_aria_flowto',
    'external_link_aria_describedby',
    'external_link_aria_expanded',
    'external_link_aria_haspopup',
    'external_link_aria_controls',
    'external_link_aria_labelledby',
    'external_link_aria_owns',
    'external_link_aria_flowto'
]

# 系统要求
SYSTEM_REQUIREMENTS = {
    "min_memory_gb": 8,        # 最小内存要求（GB）
    "recommended_memory_gb": 16, # 推荐内存（GB）
    "model_size_gb": 20,       # 模型大小（GB）
}

# 性能优化设置
PERFORMANCE_CONFIG = {
    "enable_batch_processing": True,  # 启用批处理
    "max_concurrent_requests": 1,     # 最大并发请求数（建议为1以避免内存问题）
    "timeout_seconds": 120,           # 请求超时时间
}

# 语言特定配置
LANGUAGE_CONFIGS = {
    "chinese": {
        "name": "中文",
        "chunk_size": 3000,
        "temperature": 0.2,
        "special_instructions": "使用简体中文，保持医学术语的准确性"
    },
    "french": {
        "name": "法语",
        "chunk_size": 2800,
        "temperature": 0.3,
        "special_instructions": "使用标准法语，注意法语语法和医学术语"
    },
    "japanese": {
        "name": "日语",
        "chunk_size": 2500,
        "temperature": 0.2,
        "special_instructions": "使用敬语形式，保持日语的礼貌表达"
    },
    "spanish": {
        "name": "西班牙语",
        "chunk_size": 3000,
        "temperature": 0.3,
        "special_instructions": "使用标准西班牙语，注意语法和医学术语"
    },
    "german": {
        "name": "德语",
        "chunk_size": 2800,
        "temperature": 0.2,
        "special_instructions": "使用标准德语，注意复合词和医学术语"
    },
    "korean": {
        "name": "韩语",
        "chunk_size": 2500,
        "temperature": 0.2,
        "special_instructions": "使用标准韩语，保持敬语形式"
    },
    "italian": {
        "name": "意大利语",
        "chunk_size": 2800,
        "temperature": 0.3,
        "special_instructions": "使用标准意大利语，注意语法和医学术语"
    },
    "portuguese": {
        "name": "葡萄牙语",
        "chunk_size": 3000,
        "temperature": 0.3,
        "special_instructions": "使用标准葡萄牙语，注意语法和医学术语"
    },
    "russian": {
        "name": "俄语",
        "chunk_size": 2800,
        "temperature": 0.2,
        "special_instructions": "使用标准俄语，注意语法和医学术语"
    }
}
