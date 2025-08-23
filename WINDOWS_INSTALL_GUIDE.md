# Windows 11 新电脑完整安装指南

## 🎯 概述

在全新的Windows 11电脑上安装和配置MCP SQL Server Filesystem的完整步骤。

## ✅ 系统检查结果

根据您的系统检查，您已经具备：
- ✅ **ODBC Driver 17 for SQL Server** (32-bit & 64-bit)
- ✅ **SQL Server** ODBC驱动程序
- ❌ **pyodbc** Python模块（需要安装）

## 📋 完整安装步骤

### 第1步：安装Python（如果尚未安装）

```bash
# 方法1: 从官网下载
# 访问 https://www.python.org/downloads/
# 下载Python 3.11或3.12版本
# ⚠️ 安装时务必勾选 "Add Python to PATH"

# 方法2: 使用winget
winget install Python.Python.3.12

# 方法3: 使用Microsoft Store
# 搜索并安装 "Python 3.12"
```

### 第2步：安装必要的Python包

```bash
# 安装pyodbc（SQL Server连接必需）
pip install pyodbc

# 安装其他依赖
pip install pydantic python-dotenv fastapi uvicorn aiofiles sqlalchemy
```

### 第3步：升级ODBC驱动程序（可选但推荐）

虽然您已有ODBC Driver 17，但建议升级到最新的Driver 18：

```bash
# 方法1: 使用winget（推荐）
winget install Microsoft.ODBCDriverforSQLServer

# 方法2: 手动下载
# 访问: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
# 下载并安装 "Microsoft ODBC Driver 18 for SQL Server"
```

### 第4步：克隆和安装MCP项目

```bash
# 克隆项目
git clone https://github.com/ppengit/mcp-sqlserver-filesystem.git
cd mcp-sqlserver-filesystem

# 安装项目依赖
pip install -e .

# 或使用uv（如果已安装）
uv sync
```

### 第5步：配置数据库连接

```bash
# 复制配置模板
copy .env.example .env

# 编辑.env文件，设置您的数据库连接
notepad .env
```

基本配置示例：
```env
# 使用您现有的ODBC Driver 17
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=localhost
DB_DATABASE=master
DB_USE_WINDOWS_AUTH=true

# 重要的连接参数
DB_TRUST_SERVER_CERTIFICATE=true
DB_ENCRYPT=false
DB_MULTIPLE_ACTIVE_RESULT_SETS=true

# Web UI配置
MCP_WEB_HOST=127.0.0.1
MCP_WEB_PORT=8765
MCP_DEBUG=true
```

### 第6步：测试安装

```bash
# 测试基本功能
python -m mcp_sqlserver_filesystem version

# 测试Web UI
python -m mcp_sqlserver_filesystem test --web

# 检查ODBC连接
python check_odbc_drivers.py
```

### 第7步：配置到Augment Code

#### 找到配置文件位置：
```
%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
```

#### 添加MCP配置：
```json
{
  "mcpServers": {
    "mcp-sqlserver-filesystem": {
      "command": "python",
      "args": ["-m", "mcp_sqlserver_filesystem"],
      "cwd": "C:/path/to/your/mcp-sqlserver-filesystem",
      "timeout": 600,
      "env": {
        "PYTHONPATH": "C:/path/to/your/mcp-sqlserver-filesystem/src",
        "DB_DRIVER": "ODBC Driver 17 for SQL Server",
        "DB_SERVER": "localhost",
        "DB_DATABASE": "master",
        "DB_USE_WINDOWS_AUTH": "true",
        "DB_TRUST_SERVER_CERTIFICATE": "true",
        "DB_ENCRYPT": "false",
        "DB_MULTIPLE_ACTIVE_RESULT_SETS": "true",
        "MCP_DEBUG": "true",
        "MCP_WEB_HOST": "127.0.0.1",
        "MCP_WEB_PORT": "8765"
      },
      "autoApprove": [
        "sql_query",
        "list_tables",
        "get_table_schema",
        "read_file",
        "list_directory"
      ]
    }
  }
}
```

### 第8步：重启并测试

1. **重启Augment Code/Cursor**
2. **测试MCP连接**：
   - 在Augment Code中输入："list tables in database"
   - 或："show me the schema of table users"

## 🔧 常见问题解决

### 问题1：pyodbc安装失败

```bash
# 如果pip安装失败，尝试：
pip install --upgrade pip
pip install pyodbc --no-cache-dir

# 或者安装预编译版本：
pip install pyodbc --only-binary=all
```

### 问题2：ODBC驱动程序未找到

```bash
# 重新安装ODBC驱动程序
winget uninstall Microsoft.ODBCDriverforSQLServer
winget install Microsoft.ODBCDriverforSQLServer

# 重启PowerShell后重新检查
python check_odbc_drivers.py
```

### 问题3：数据库连接失败

检查以下配置：
```env
# 确保SQL Server服务正在运行
# 确保防火墙允许连接
# 确保用户有数据库访问权限

# 对于本地SQL Server Express：
DB_SERVER=localhost\SQLEXPRESS
DB_DATABASE=master
DB_USE_WINDOWS_AUTH=true
```

### 问题4：Web UI无法访问

```bash
# 检查端口是否被占用
netstat -an | findstr :8765

# 尝试不同端口
set MCP_WEB_PORT=9765
python -m mcp_sqlserver_filesystem test --web
```

## 🎉 验证安装成功

安装成功后，您应该能够：

1. ✅ **运行版本检查**：`python -m mcp_sqlserver_filesystem version`
2. ✅ **启动Web UI**：访问 http://127.0.0.1:8765
3. ✅ **在Augment Code中使用**：
   - "list all tables in the database"
   - "read the file config.json"
   - "show me the schema of the users table"

## 📞 获取帮助

如果遇到问题：

1. **检查日志**：设置 `MCP_DEBUG=true` 查看详细日志
2. **运行诊断**：`python check_odbc_drivers.py`
3. **查看配置**：确认 `.env` 文件配置正确
4. **重启服务**：重启Augment Code和相关服务

## 🔄 升级指南

定期更新到最新版本：

```bash
# 更新项目代码
git pull origin main

# 更新依赖
pip install -e . --upgrade

# 重启Augment Code
```

---

**恭喜！** 您现在已经在Windows 11上成功安装了MCP SQL Server Filesystem！🎉
