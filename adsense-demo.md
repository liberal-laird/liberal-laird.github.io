---
title: "AdSense 广告功能演示"
date: 2024-01-15
description: "演示如何在 Hugo 网站中集成 Google AdSense 广告"
tags: ["AdSense", "广告", "Hugo"]
categories: ["技术"]
---

# AdSense 广告功能演示

这篇文章演示了如何在 Hugo 网站中集成 Google AdSense 广告。

## 自动插入的广告

在文章内容下方会自动插入一个广告区块。

## 手动插入广告

您也可以在文章内容中使用 shortcode 手动插入广告：

```markdown
{{< adsense >}}
```

或者使用特定的广告单元：

```markdown
{{< adsense-slot "article_middle" >}}
{{< adsense-slot "article_top" >}}
```

{{< adsense-slot "article_middle" >}}

## 配置说明

在 `hugo.toml` 中配置了以下参数：

```toml
[params.adsense]
  publisher_id = "pub-4522670236044605"
  enable_ads = true
  article_ads_only = true            # 只在文章页显示广告
  
  # 文章页广告单元ID配置
  [params.adsense.slots]
    article_top = "1234567890"        # 文章顶部广告单元ID
    article_middle = "2345678901"     # 文章中间广告单元ID
    article_bottom = "3456789012"     # 文章底部广告单元ID
```

## 功能特点

1. **仅文章页广告**：只在文章阅读页显示广告，不影响其他页面
2. **多位置投放**：文章顶部、中间、底部可灵活配置
3. **手动控制**：可以使用 shortcode 手动插入广告
4. **响应式设计**：广告会根据屏幕大小自动调整
5. **配置简洁**：通过配置文件集中管理广告设置

## 注意事项

- 确保您的 AdSense 账户已获得批准
- 广告需要时间才能开始显示
- 请遵守 AdSense 的政策和规定
