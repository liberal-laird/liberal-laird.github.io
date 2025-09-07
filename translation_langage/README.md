# Hugo文章翻译工具

这个Python脚本可以将Hugo网站中的英文文章自动翻译成中文，使用本地LM Studio API进行翻译。

## 功能特点

- 🔄 自动读取`content/english`目录下的所有Markdown文件
- 🤖 使用本地LM Studio API进行翻译
- 🌍 支持多语言翻译（中文、法语、西班牙语、德语、日语、韩语等）
- 📝 保持Markdown格式和结构完全不变
- 🏷️ 智能处理frontmatter：只翻译`title`、`description`、`tags`、`categories`、`keywords`，保持其他结构字段不变
- 📊 支持表格、列表、链接等复杂格式
- 💾 自动保存翻译结果到指定语言目录

## 安装依赖

### 方法1：使用uv（推荐）
```bash
cd translation_langage
uv sync  # 或者 uv pip install -r requirements.txt
```

### 方法2：使用pip
```bash
cd translation_langage
pip install -r requirements.txt
```

## 支持的语言

脚本支持以下目标语言：

- `chinese` - 中文（默认）
- `french` - 法语
- `spanish` - 西班牙语
- `german` - 德语
- `japanese` - 日语
- `korean` - 韩语
- `italian` - 意大利语
- `portuguese` - 葡萄牙语
- `russian` - 俄语

## 使用前准备

1. **启动LM Studio**
   - 下载并安装[LM Studio](https://lmstudio.ai/)
   - 加载 `openai/gpt-oss-20b` 模型（推荐用于翻译）
   - 启动本地服务器（默认端口1234）
   - 确保模型已完全加载并准备就绪

2. **确认目录结构**
   ```
   health-hugo/
   ├── content/
   │   ├── english/     # 英文文章目录
   │   └── chinese/     # 中文文章目录（自动创建）
   └── translation_langage/
       ├── translate_articles.py
       ├── requirements.txt
       └── README.md
   ```

## 运行翻译

### 方法1：使用uv便捷脚本（推荐）
```bash
cd translation_langage

# 翻译到中文（默认）
./run_translation_uv.sh

# 翻译到法语
./run_translation_uv.sh french

# 翻译到西班牙语
./run_translation_uv.sh spanish
```

### 方法2：使用传统便捷脚本
```bash
cd translation_langage
./run_translation.sh
```

### 方法3：使用uv直接运行（推荐）
```bash
cd translation_langage

# 翻译到中文（默认）
uv run translate_articles.py

# 翻译到法语
uv run translate_articles.py french

# 翻译到西班牙语
uv run translate_articles.py spanish
```

### 方法4：直接运行Python脚本
```bash
cd translation_langage
python translate_articles.py
```

### 方法5：测试配置（首次使用建议）
```bash
cd translation_langage
uv run test_config.py
```

### 方法6：测试frontmatter处理规则
```bash
cd translation_langage
uv run test_frontmatter.py
```

## 脚本特性

### 智能内容分割
- 自动将长文章分割成适合翻译的块
- 保持Markdown结构完整性
- 避免API限制和超时

### 格式保持
- ✅ 保持所有Markdown格式（标题、表格、列表等）
- ✅ 智能处理frontmatter字段
- ✅ 保持数字、日期、引用格式
- ✅ 保持链接和图片引用

### Frontmatter处理规则
**会被翻译的字段：**
- `title` - 文章标题
- `description` - 文章描述
- `tags` - 标签
- `categories` - 分类
- `keywords` - 关键词（数组格式）

**保持不变的字段：**
- `date` - 发布日期
- `draft` - 草稿状态
- `url` - 文章URL
- `weight` - 权重
- `menu` - 菜单配置
- `layout` - 布局
- `type` - 类型
- `author` - 作者
- `slug` - 别名
- 其他所有结构性和配置性字段

### 错误处理
- 自动重试失败的翻译请求
- 连接测试和错误提示
- 详细的进度显示

## 配置选项

可以在脚本中修改以下配置：

```python
# LM Studio API地址
lm_studio_url = "http://localhost:1234/v1/chat/completions"

# 模型名称（已配置为openai/gpt-oss-20b）
model_name = "openai/gpt-oss-20b"

# 翻译块大小（针对GPT-OSS-20B优化）
max_chunk_size = 3000

# 重试次数
max_retries = 3

# API参数（针对GPT-OSS-20B优化）
temperature = 0.2
max_tokens = 6000
top_p = 0.9
```

## 注意事项

1. **LM Studio设置**
   - 使用 `openai/gpt-oss-20b` 模型（已针对此模型优化）
   - 确保模型完全加载（可能需要几分钟）
   - 保持服务器稳定运行
   - 建议至少8GB可用内存用于模型运行

2. **翻译质量**
   - 脚本会保持原文结构，但翻译质量取决于模型
   - 建议翻译后人工检查医学术语准确性

3. **文件处理**
   - 已存在的翻译文件会被覆盖
   - 建议先备份重要文件

## 故障排除

### 连接问题
```
❌ LM Studio连接失败
```
- 检查LM Studio是否正在运行
- 确认端口1234是否可用
- 检查防火墙设置

### 翻译质量问题
- 尝试更换更好的翻译模型
- 调整temperature参数（当前为0.1）
- 检查模型的中文能力

### 内存不足
- 减小`max_chunk_size`参数
- 关闭其他占用内存的程序
- 使用更小的模型

## GPT-OSS-20B模型优化

本脚本已针对`openai/gpt-oss-20b`模型进行了专门优化：

### 模型特性
- **模型大小**: 20GB
- **内存要求**: 最少8GB，推荐16GB
- **翻译质量**: 优秀的医学和营养学翻译能力
- **上下文长度**: 支持长文档翻译

### 优化配置
- **温度参数**: 0.2（平衡创造性和准确性）
- **最大Token**: 6000（处理长内容）
- **块大小**: 3000字符（优化处理效率）
- **Top-p**: 0.9（提高翻译质量）

### 性能建议
1. **内存管理**: 确保有足够内存运行20GB模型
2. **批处理**: 建议一次处理一个文件以避免内存问题
3. **监控**: 注意系统资源使用情况

## 扩展功能

可以轻松扩展脚本以支持：
- 其他语言翻译（法语、西班牙语等）
- 批量处理多个语言
- 自定义翻译提示词
- 翻译进度保存和恢复
- 其他大语言模型（如Llama、Mistral等）
