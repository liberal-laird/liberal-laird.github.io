#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frontmatter处理测试脚本
测试哪些字段会被翻译，哪些会保持不变
"""

from config import FRONTMATTER_FIELDS_TO_TRANSLATE, FRONTMATTER_FIELDS_TO_PRESERVE

def test_frontmatter_config():
    """测试frontmatter配置"""
    print("🧪 Frontmatter处理规则测试")
    print("=" * 50)
    
    # 示例frontmatter
    sample_frontmatter = {
        'date': '2025-08-20',
        'draft': False,
        'title': 'Vitamin C - Biological Functions',
        'url': 'post/Vitamin_C.html',
        'tags': 'vitamin',
        'categories': 'Nutrients',
        'description': 'Vitamin C is a water-soluble micronutrient essential for human health.',
        'keywords': ['Vitamin C', 'Ascorbic acid', 'Antioxidant', 'Immune support'],
        'weight': 10,
        'author': 'Health Expert',
        'layout': 'post'
    }
    
    print("📋 示例frontmatter字段:")
    for key, value in sample_frontmatter.items():
        print(f"  {key}: {value}")
    
    print("\n🔄 处理结果:")
    print("-" * 30)
    
    for field, value in sample_frontmatter.items():
        if field in FRONTMATTER_FIELDS_TO_TRANSLATE and field not in FRONTMATTER_FIELDS_TO_PRESERVE:
            print(f"✅ {field}: 会被翻译")
        elif field in FRONTMATTER_FIELDS_TO_PRESERVE:
            print(f"🔒 {field}: 保持不变")
        else:
            print(f"❓ {field}: 未定义 (将保持不变)")
    
    print("\n📊 统计信息:")
    print(f"  总字段数: {len(sample_frontmatter)}")
    print(f"  会被翻译: {len([f for f in sample_frontmatter.keys() if f in FRONTMATTER_FIELDS_TO_TRANSLATE and f not in FRONTMATTER_FIELDS_TO_PRESERVE])}")
    print(f"  保持不变: {len([f for f in sample_frontmatter.keys() if f in FRONTMATTER_FIELDS_TO_PRESERVE or f not in FRONTMATTER_FIELDS_TO_TRANSLATE])}")
    
    print("\n🎯 配置验证:")
    print(f"  翻译字段列表: {FRONTMATTER_FIELDS_TO_TRANSLATE}")
    print(f"  保持字段数量: {len(FRONTMATTER_FIELDS_TO_PRESERVE)}")

def show_field_examples():
    """显示字段处理示例"""
    print("\n📝 字段处理示例:")
    print("=" * 50)
    
    examples = [
        ("title", "Vitamin C - Biological Functions", "维生素C - 生物学功能"),
        ("description", "Essential for human health", "对人体健康至关重要"),
        ("tags", "vitamin", "vitamin (保持不变)"),
        ("categories", "Nutrients", "Nutrients (保持不变)"),
        ("keywords", "['Vitamin C', 'Antioxidant']", "['Vitamin C', 'Antioxidant'] (保持不变)"),
        ("url", "post/Vitamin_C.html", "post/Vitamin_C.html (保持不变)"),
        ("date", "2025-08-20", "2025-08-20 (保持不变)")
    ]
    
    for field, original, result in examples:
        print(f"  {field}:")
        print(f"    原文: {original}")
        print(f"    结果: {result}")
        print()

def main():
    """主函数"""
    test_frontmatter_config()
    show_field_examples()
    
    print("✅ Frontmatter处理规则测试完成！")
    print("💡 这样可以确保Hugo网站的结构和SEO信息保持不变")

if __name__ == "__main__":
    main()
