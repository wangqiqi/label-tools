# 工具健康检查脚本使用指南

## 功能说明

`check_tools.py` 是一个综合的健康检查脚本，提供以下功能：

1. **链接有效性检查**：检查 README.md 中所有超链接是否可访问
2. **GitHub 仓库状态检查**：获取仓库的 Stars、Forks、最后更新时间、最新版本、开源协议等信息
3. **生成详细报告**：生成 HTML 和 Markdown 格式的检查报告

## 安装依赖

```bash
pip install -r requirements.txt
```

## 基本使用

### 1. 完整检查（推荐）

检查所有链接和 GitHub 仓库状态：

```bash
python check_tools.py
```

生成的报告：
- `health_report.html` - 综合 HTML 报告（包含链接和仓库状态）
- `link_check_report.md` - 链接检查 Markdown 报告

### 2. 仅检查链接

```bash
python check_tools.py --links-only
```

### 3. 仅检查 GitHub 仓库

```bash
python check_tools.py --repos-only
```

### 4. 指定输入文件

```bash
python check_tools.py --input path/to/your/README.md
```

### 5. 使用 GitHub Token（推荐）

为避免 GitHub API 限制，建议使用 Personal Access Token：

```bash
python check_tools.py --token YOUR_GITHUB_TOKEN
```

如何获取 GitHub Token：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 `public_repo` 权限
4. 生成并复制 token

## 输出说明

### 终端输出

脚本会实时显示检查进度，使用彩色标记：
- ✅ 绿色：成功/活跃
- ⚠️ 黄色：警告/不活跃
- ❌ 红色：失败/归档/错误

### HTML 报告 (health_report.html)

包含以下内容：
- **链接检查统计**：成功、警告、失败的链接数量
- **GitHub 仓库健康状态**：活跃、不活跃、归档、错误的仓库数量
- **详细表格**：
  - 工具名称
  - 状态（活跃/不活跃/归档）
  - Stars 和 Forks 数
  - 最后更新时间
  - 最新版本
  - 开源协议
- **失败的链接列表**：显示所有无法访问的链接

### Markdown 报告 (link_check_report.md)

包含链接检查的详细结果：
- 统计信息
- 失败的链接（优先显示）
- 警告的链接
- 成功的链接

## 状态说明

### 链接状态

- **success**：链接可正常访问（HTTP 200）
- **warning**：链接重定向（HTTP 3xx）
- **error**：链接无法访问（HTTP 4xx/5xx、超时、连接失败等）

### GitHub 仓库状态

- **active**：仓库活跃（180 天内有更新）
- **inactive**：仓库不活跃（超过 180 天未更新）
- **archived**：仓库已归档（只读状态）
- **not_found**：仓库不存在或已删除
- **error**：检查出错（网络问题、API 限制等）

## 配置选项

可以在脚本中修改以下配置：

```python
GITHUB_TOKEN = None  # GitHub API Token
TIMEOUT = 10         # 请求超时时间（秒）
MAX_WORKERS = 10     # 并发线程数
```

## 常见问题

### 1. GitHub API 限制

**问题**：出现 "API 限制" 错误

**解决**：
- 使用 `--token` 参数提供 GitHub Token
- 未认证：60 次/小时
- 已认证：5000 次/小时

### 2. 请求超时

**问题**：某些链接检查超时

**解决**：
- 增加 `TIMEOUT` 配置值
- 检查网络连接
- 某些网站可能屏蔽自动化请求

### 3. 连接失败

**问题**：无法连接到某些网站

**可能原因**：
- 网站暂时不可用
- 防火墙或代理设置
- 网站屏蔽了脚本的 User-Agent

## 定期检查建议

建议定期运行此脚本以维护文档质量：

1. **每周检查**：确保链接有效性
2. **每月检查**：更新 Stars/Forks 数据
3. **发布前检查**：确保所有信息准确

## 示例输出

```
================================================================================
开始检查链接有效性...
================================================================================

找到 150 个链接
去重后: 120 个唯一链接

[1/120] ✓ https://github.com/HumanSignal/label-studio
[2/120] ✓ https://github.com/cvat-ai/cvat
[3/120] ✗ https://example.com/broken-link
...

✓ 链接检查报告已保存: link_check_report.md

================================================================================
开始检查 GitHub 仓库状态...
================================================================================

找到 67 个 GitHub 仓库

[1/67] 检查 Label Studio (HumanSignal/label-studio)...
  ✓ 活跃 - 20000 stars, 最后更新: 2026-02-25
[2/67] 检查 CVAT (cvat-ai/cvat)...
  ✓ 活跃 - 14000 stars, 最后更新: 2026-02-24
...

⚠️ 发现 5 个需要关注的工具：
  - VoTT: archived - 仓库已归档
  - Dataturks: not_found - 仓库不存在或已删除
  ...

✓ 综合健康报告已生成: health_report.html
```

## 许可证

本脚本遵循 MIT 许可证。
