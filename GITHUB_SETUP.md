# GitHub 仓库设置指南

## 🚀 推送到 GitHub

### 第1步：创建 GitHub 仓库

1. **访问 GitHub**: https://github.com
2. **点击 "New repository"** 或访问 https://github.com/new
3. **填写仓库信息**:
   - Repository name: `mcp-sqlserver-filesystem`
   - Description: `Enhanced MCP server for SQL Server and filesystem access with dual interface support`
   - 选择 **Public** (推荐) 或 **Private**
   - **不要**勾选 "Add a README file" (我们已经有了)
   - **不要**勾选 "Add .gitignore" (我们已经有了)
   - **不要**选择 License (我们已经在 pyproject.toml 中指定了 MIT)

4. **点击 "Create repository"**

### 第2步：添加远程仓库并推送

创建仓库后，GitHub 会显示推送现有仓库的命令。在项目目录中执行：

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/mcp-sqlserver-filesystem.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 第3步：验证推送成功

推送完成后，您可以：

1. **访问仓库页面**: https://github.com/YOUR_USERNAME/mcp-sqlserver-filesystem
2. **检查文件**: 确认所有文件都已上传
3. **查看 README**: GitHub 会自动显示 README.md 内容

## 📋 推送后的 README 安装步骤

推送到 GitHub 后，用户可以按照以下步骤安装：

### 方法1：直接从 GitHub 安装
```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/mcp-sqlserver-filesystem.git
cd mcp-sqlserver-filesystem

# 安装依赖
pip install -e .

# 配置数据库连接
copy .env.example .env
notepad .env

# 测试安装
python -m mcp_sqlserver_filesystem version
python -m mcp_sqlserver_filesystem test --web
```

### 方法2：使用 pip 直接安装（如果发布到 PyPI）
```bash
pip install git+https://github.com/YOUR_USERNAME/mcp-sqlserver-filesystem.git
```

## 🔧 Augment Code 配置

用户需要在 Augment Code 配置文件中添加：

```json
{
  "mcpServers": {
    "mcp-sqlserver-filesystem": {
      "command": "python",
      "args": ["-m", "mcp_sqlserver_filesystem"],
      "cwd": "C:/path/to/mcp-sqlserver-filesystem",
      "timeout": 600,
      "env": {
        "PYTHONPATH": "C:/path/to/mcp-sqlserver-filesystem/src",
        "DB_SERVER": "localhost",
        "DB_DATABASE": "master",
        "DB_USE_WINDOWS_AUTH": "true",
        "DB_TRUST_SERVER_CERTIFICATE": "true",
        "DB_ENCRYPT": "false",
        "DB_MULTIPLE_ACTIVE_RESULT_SETS": "true",
        "MCP_DEBUG": "true"
      },
      "autoApprove": [
        "sql_query",
        "sql_execute", 
        "list_tables",
        "get_table_schema",
        "read_file",
        "write_file",
        "list_directory"
      ]
    }
  }
}
```

## 📝 后续步骤

1. **创建 Release**: 在 GitHub 上创建第一个 release (v0.1.0)
2. **添加 Issues 模板**: 创建 bug 报告和功能请求模板
3. **设置 CI/CD**: 添加 GitHub Actions 进行自动测试
4. **发布到 PyPI**: 让用户可以通过 `pip install mcp-sqlserver-filesystem` 安装

## 🎉 完成！

推送完成后，您的 MCP SQL Server Filesystem 项目就可以供其他人使用了！

用户可以按照 README.md 中的详细步骤进行安装和配置。
