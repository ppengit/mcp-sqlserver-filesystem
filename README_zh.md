# MCP SQL Server 文件系统

🚀 **增强的 MCP 服务器**，支持 SQL Server 数据库和文件系统访问，具有双界面支持。

*其他语言版本: [English](README.md)*

## ✨ 核心特性

- **完整 SQL Server 支持** - 执行所有 SQL 命令，支持增强连接参数
- **完全文件系统访问** - 读写文件，带确认对话框
- **Web UI 界面** - 实时查询结果显示
- **桌面应用程序** - 跨平台原生桌面应用 (v0.1.1 新功能)
- **智能环境检测** - 自动适配 SSH Remote、WSL、本地环境
- **增强连接参数** - 内置支持 `TrustServerCertificate=true`、`Encrypt=false`、`MultipleActiveResultSets=true`

## 🚀 快速开始

### 📦 简单安装

```bash
# 安装 uv（如果尚未安装）
pip install uv

# 直接运行（无需克隆仓库）
uvx mcp-sqlserver-filesystem@latest
```

### 🧪 安装与测试

```bash
# 测试 Web UI
uvx mcp-sqlserver-filesystem@latest --test-web

# 测试桌面应用程序 (v0.1.1 新功能)
uvx mcp-sqlserver-filesystem@latest --test-desktop

# 或使用传统方式
uvx mcp-sqlserver-filesystem@latest test --web
uvx mcp-sqlserver-filesystem@latest test --desktop
```

### 📋 系统要求

**Windows 11 用户请确保已安装：**

1. **Python 3.11+** 
   ```bash
   python --version  # 检查版本
   # 如果未安装：winget install Python.Python.3.12
   ```

2. **ODBC Driver for SQL Server** ⭐ **重要！**
   ```bash
   # 检查驱动：python -c "import pyodbc; print([d for d in pyodbc.drivers() if 'SQL Server' in d])"
   # 如果没有：winget install Microsoft.ODBCDriverforSQLServer
   ```

## 🔧 Augment Code 配置

添加到您的 Augment Code MCP 设置：

```json
{
  "mcpServers": {
    "mcp-sqlserver-filesystem": {
      "command": "uvx",
      "args": ["mcp-sqlserver-filesystem@latest"],
      "timeout": 600,
      "env": {
        "DB_SERVER": "localhost",
        "DB_DATABASE": "master",
        "DB_USE_WINDOWS_AUTH": "true",
        "DB_TRUST_SERVER_CERTIFICATE": "true",
        "DB_ENCRYPT": "false",
        "DB_MULTIPLE_ACTIVE_RESULT_SETS": "true"
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

## 🛠️ 可用工具

### 数据库工具
- `sql_query` - 执行 SQL 查询，结果在 UI 中显示
- `sql_execute` - 执行 INSERT/UPDATE/DELETE 操作
- `get_table_schema` - 获取表结构信息
- `list_tables` - 列出数据库中的所有表

### 文件系统工具
- `read_file` - 读取文件内容
- `write_file` - 写入文件内容（带确认对话框）
- `list_directory` - 列出目录内容

## 📝 使用示例

在 Augment Code 中尝试：

```
"执行 SQL 查询：SELECT TOP 10 * FROM Users"
"显示 Users 表的结构"
"列出数据库中的所有表"
"读取文件 config.json"
"将配置写入 settings.json"
```

## 🔒 配置选项

设置环境变量或创建 `.env` 文件：

```env
# SQL Server 配置
DB_SERVER=localhost
DB_DATABASE=master
DB_USE_WINDOWS_AUTH=true

# 增强连接参数
DB_TRUST_SERVER_CERTIFICATE=true
DB_ENCRYPT=false
DB_MULTIPLE_ACTIVE_RESULT_SETS=true

# Web UI 配置
MCP_WEB_HOST=127.0.0.1
MCP_WEB_PORT=8765
```

## 🆕 v0.1.1 新功能

- ✅ **桌面应用程序支持** - 跨平台原生桌面应用
- ✅ **快速测试命令** - `--test-web` 和 `--test-desktop`
- ✅ **增强连接参数** - 完整支持 SQL Server 连接选项
- ✅ **完全访问模式** - 默认允许所有 SQL 命令和文件操作

## 📋 系统要求

- Python 3.11+
- ODBC Driver for SQL Server
- Windows/macOS/Linux 支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

**🎉 在 Augment Code 中享受强大的 SQL Server 和文件系统访问功能！**
