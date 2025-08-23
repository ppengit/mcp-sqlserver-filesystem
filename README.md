# MCP SQL Server Filesystem

🚀 **增强的 MCP 服务器**，支持 SQL Server 数据库和文件系统访问，具有双界面支持（Web UI + 桌面应用）。

## 🌟 核心特性

### 🗄️ SQL Server 数据库操作
- ✅ **完整SQL支持** - 执行所有SQL命令（SELECT, INSERT, UPDATE, DELETE, CREATE, DROP等）
- ✅ **增强连接参数** - 支持 `TrustServerCertificate=true`, `Encrypt=false`, `MultipleActiveResultSets=true`
- ✅ **UI结果展示** - 查询结果在专用Web UI窗口中显示
- ✅ **表结构查询** - 获取详细的表结构和元数据信息
- ✅ **智能错误处理** - 友好的错误消息和调试信息

### 📁 文件系统操作
- ✅ **完全访问模式** - 默认允许读写所有指定目录的文件
- ✅ **大文件支持** - 支持最大1GB文件操作
- ✅ **交互确认** - 文件写入和删除操作的确认对话框
- ✅ **目录浏览** - 递归目录列表和文件信息展示
- ✅ **多格式支持** - 支持所有文件扩展名（可配置限制）

### 🌐 双界面支持
- ✅ **Web UI界面** - 基于FastAPI的现代Web界面
- ✅ **桌面应用** - 跨平台原生桌面应用（基于Tauri）
- ✅ **实时通信** - WebSocket实时数据更新
- ✅ **智能环境检测** - 自动适配SSH Remote、WSL、本地环境

### 🛡️ 安全与监控
- ✅ **灵活权限控制** - 可配置的安全策略（默认完全访问）
- ✅ **操作日志记录** - 详细的操作日志和审计跟踪
- ✅ **内存监控** - 自动内存管理和资源清理
- ✅ **错误追踪** - 统一的错误处理和问题诊断

## 🚀 快速开始

### 📋 系统要求

#### Windows 11 新电脑必需组件：
1. **Python 3.11+** 
   ```bash
   # 检查Python版本
   python --version
   
   # 如果未安装，推荐使用winget安装
   winget install Python.Python.3.12
   ```

2. **ODBC Driver for SQL Server** ⭐ **重要！**
   ```bash
   # 检查现有驱动
   python -c "import pyodbc; print([d for d in pyodbc.drivers() if 'SQL Server' in d])"
   
   # 如果没有，安装最新驱动
   winget install Microsoft.ODBCDriverforSQLServer
   ```

3. **Python ODBC模块**
   ```bash
   pip install pyodbc
   ```

### 📦 安装步骤

#### 第1步：克隆项目
```bash
git clone https://github.com/ppengit/mcp-sqlserver-filesystem.git
cd mcp-sqlserver-filesystem
```

#### 第2步：安装依赖
```bash
# 使用pip安装（推荐开发模式）
pip install -e .

# 或使用uv（如果已安装）
uv sync
```

#### 第3步：配置数据库连接
```bash
# 复制配置模板
copy .env.example .env

# 编辑配置文件（使用记事本或您喜欢的编辑器）
notepad .env
```

**基本配置示例：**
```env
# SQL Server 配置
DB_SERVER=localhost
DB_DATABASE=master
DB_USE_WINDOWS_AUTH=true

# 增强连接参数（已集成您要求的参数）
DB_TRUST_SERVER_CERTIFICATE=true
DB_ENCRYPT=false
DB_MULTIPLE_ACTIVE_RESULT_SETS=true

# Web UI 配置
MCP_WEB_HOST=127.0.0.1
MCP_WEB_PORT=8765
MCP_DEBUG=true
```

#### 第4步：测试安装
```bash
# 测试基本功能
python -m mcp_sqlserver_filesystem version

# 测试Web UI（会自动打开浏览器）
python -m mcp_sqlserver_filesystem test --web

# 测试桌面应用（如果支持）
python -m mcp_sqlserver_filesystem test --desktop
```

### 🔧 配置到 Augment Code

#### 找到配置文件
Augment Code 的 MCP 配置文件位置：
```
Windows: %APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
macOS: ~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
Linux: ~/.config/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

#### 添加MCP配置
在配置文件中添加以下内容：

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

**⚠️ 重要：** 请将 `C:/path/to/your/mcp-sqlserver-filesystem` 替换为您实际的项目路径！

#### 第5步：重启并测试
1. **重启 Augment Code/Cursor**
2. **测试MCP连接**，在Augment Code中尝试：
   - "list all tables in the database"
   - "show me the schema of the users table"
   - "read the file config.json"
   - "execute SQL: SELECT TOP 10 * FROM your_table"

## 🛠️ 可用工具

### 数据库工具
| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `sql_query` | 执行SQL查询，结果在UI中显示 | `query`, `parameters`, `show_ui` |
| `sql_execute` | 执行INSERT/UPDATE/DELETE操作 | `query`, `parameters`, `confirm` |
| `get_table_schema` | 获取表结构信息 | `table_name`, `schema_name`, `show_ui` |
| `list_tables` | 列出数据库中的所有表 | `schema_name`, `show_ui` |

### 文件系统工具
| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `read_file` | 读取文件内容 | `file_path`, `encoding`, `show_ui` |
| `write_file` | 写入文件内容（带确认） | `file_path`, `content`, `encoding`, `confirm` |
| `list_directory` | 列出目录内容 | `dir_path`, `recursive`, `show_ui` |

## 📝 使用示例

### 在 Augment Code 中的使用方式：

```
# 数据库操作示例
"执行SQL查询：SELECT TOP 100 * FROM Users WHERE Status = 'Active'"
"显示表结构：Users表的详细结构信息"
"列出数据库中的所有表"
"执行更新操作：UPDATE Users SET LastLogin = GETDATE() WHERE ID = 1"

# 文件操作示例  
"读取配置文件：appsettings.json的完整内容"
"写入日志文件：将错误信息保存到error.log"
"浏览项目目录：显示src文件夹的所有文件"
"创建新文件：在docs目录下创建README.md"
```

### SQL连接字符串示例：
```
# Windows认证 + 开发环境
DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1433;DATABASE=TestDB;Trusted_Connection=yes;TrustServerCertificate=yes;Encrypt=no;MultipleActiveResultSets=yes;Application Name=MCP-SQLServer-Filesystem;

# SQL Server认证 + 生产环境
DRIVER={ODBC Driver 17 for SQL Server};SERVER=prod-server,1433;DATABASE=ProductionDB;UID=username;PWD=password;TrustServerCertificate=no;Encrypt=yes;MultipleActiveResultSets=yes;Application Name=MCP-SQLServer-Filesystem;
```

## 🔒 安全配置

### 默认设置（完全访问模式）
```env
# SQL安全（默认禁用保护，允许所有SQL命令）
SEC_ENABLE_SQL_PROTECTION=false
SEC_MAX_QUERY_LENGTH=100000

# 文件系统安全（默认完全访问）
FS_MAX_FILE_SIZE=1073741824  # 1GB
FS_ENABLE_WRITE=true
FS_ENABLE_DELETE=true
```

### 生产环境安全配置
```env
# 启用SQL保护
SEC_ENABLE_SQL_PROTECTION=true
SEC_MAX_QUERY_LENGTH=10000

# 限制文件系统访问
FS_ALLOWED_PATHS=/home/user/documents,/home/user/projects
FS_BLOCKED_PATHS=/etc,/var,/usr
FS_ENABLE_DELETE=false
```

## 🐛 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 检查连接字符串
python -c "from mcp_sqlserver_filesystem.config import config; print(config.database.connection_string)"

# 测试ODBC驱动
python -c "import pyodbc; print([d for d in pyodbc.drivers() if 'SQL Server' in d])"
```

#### 2. Web UI 无法访问
```bash
# 检查端口占用
netstat -an | findstr :8765

# 尝试不同端口
set MCP_WEB_PORT=9765
python -m mcp_sqlserver_filesystem test --web
```

#### 3. 权限问题
```bash
# 检查文件系统权限
# 确保有足够的权限访问指定目录

# 检查SQL Server权限
# 确保数据库用户有足够的权限执行操作
```

### 调试模式
```bash
# 启用详细日志
set MCP_DEBUG=true
python -m mcp_sqlserver_filesystem

# 查看配置信息
python -c "from mcp_sqlserver_filesystem.config import config; print(config.dict())"
```

## 📚 更多信息

- **配置参考**: [.env.example](.env.example) - 完整的配置选项说明
- **Windows安装指南**: [WINDOWS_INSTALL_GUIDE.md](WINDOWS_INSTALL_GUIDE.md) - Windows 11详细安装步骤
- **项目架构**: 基于FastMCP框架，支持异步操作和实时UI交互

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

**🎉 现在您可以在 Augment Code 中享受强大的 SQL Server 和文件系统访问功能！**
