# MCP SQL Server Filesystem

English | [中文](README.md)

A simple and efficient MCP (Model Context Protocol) server providing SQL Server database access and filesystem operations.

## ✨ Key Features

### 🗄️ Database Functions
- **SQL Query Execution** - Support for SELECT queries
- **SQL Command Execution** - Support for INSERT/UPDATE/DELETE operations
- **Table Schema Query** - Get detailed table structure information and field descriptions
- **Table Listing** - List all tables in the database

### 📁 Filesystem Functions
- **File Reading** - Read file contents
- **File Writing** - Write content to files
- **Directory Listing** - List directory contents

### 🔒 Security Features
- SQL injection protection
- Filesystem access control
- Environment variable configuration
- Permission validation

## 🚀 Quick Start

### 📋 Prerequisites

#### 1. Install ODBC Driver for SQL Server

**Windows:**
```bash
# Download and install Microsoft ODBC Driver 17 for SQL Server
# Visit: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
# Or use winget to install
winget install Microsoft.ODBCDriverforSQLServer
```

**macOS:**
```bash
# Install using Homebrew
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql17 mssql-tools
```

**Linux (Ubuntu/Debian):**
```bash
# Add Microsoft repository
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list

# Install driver
sudo apt-get update
sudo apt-get install msodbcsql17
```

#### 2. Verify ODBC Installation

```bash
# Windows
odbcad32.exe

# macOS/Linux
odbcinst -j
```

### 📦 Zero-Installation Usage (Recommended)

```bash
# Install uv (if not already installed)
pip install uv

# Run directly - no need to clone repository!
uvx mcp-sqlserver-filesystem@latest
```

### 🔧 Configuration

Add the following configuration to your MCP client (such as Claude Desktop, AugmentCode):

```json
{
  "mcpServers": {
    "mcp-sqlserver-filesystem": {
      "command": "uvx",
      "args": ["mcp-sqlserver-filesystem@latest"],
      "env": {
        "DB_SERVER": "localhost",
        "DB_DATABASE": "your_database",
        "DB_USERNAME": "your_username",
        "DB_PASSWORD": "your_password",
        "DB_USE_WINDOWS_AUTH": "false",
        "DB_TRUST_SERVER_CERTIFICATE": "true",
        "DB_ENCRYPT": "false",
        "FS_ALLOWED_PATHS": "*",
        "FS_ALLOWED_EXTENSIONS": "*.*",
        "FS_IGNORE_FILE_LOCKS": "true"
      }
    }
  }
}
```

## 🛠️ Available Tools

### Database Tools

- `sql_query` - Execute SQL SELECT queries
- `sql_execute` - Execute SQL INSERT/UPDATE/DELETE commands
- `list_tables` - List all tables in the database
- `get_table_schema` - Get table structure information

### Filesystem Tools

- `read_file` - Read file contents
- `write_file` - Write file contents
- `list_directory` - List directory contents

## 📋 Environment Variables

### Database Configuration
- `DB_SERVER` - SQL Server address
- `DB_DATABASE` - Database name
- `DB_USERNAME` - Username
- `DB_PASSWORD` - Password
- `DB_USE_WINDOWS_AUTH` - Whether to use Windows authentication
- `DB_TRUST_SERVER_CERTIFICATE` - Whether to trust server certificate
- `DB_ENCRYPT` - Whether to encrypt connection

### Filesystem Configuration
- `FS_ALLOWED_PATHS` - Allowed access paths (`*` means all paths)
- `FS_ALLOWED_EXTENSIONS` - Allowed file extensions (`*.*` means all files)
- `FS_IGNORE_FILE_LOCKS` - Whether to ignore file locks

## 🔧 Development

### Local Development

```bash
# Clone repository
git clone https://github.com/ppengit/mcp-sqlserver-filesystem.git
cd mcp-sqlserver-filesystem

# Install dependencies
uv sync

# Run server
uv run python -m mcp_sqlserver_filesystem server
```

### Testing

```bash
# Run tests
uv run pytest

# Run specific tests
uv run pytest tests/test_database.py
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please submit Issues or Pull Requests.

## ❓ FAQ

### Q: Getting "No module named 'pyodbc'" error
A: Please ensure ODBC Driver for SQL Server is installed, see Prerequisites section above.

### Q: Getting "Data source name not found" error
A: Check if `DB_SERVER` configuration is correct and ensure SQL Server service is running.

### Q: Connection timeout or connection refused
A:
1. Check if SQL Server has TCP/IP protocol enabled
2. Verify firewall settings allow connections to SQL Server port (default 1433)
3. Confirm username and password are correct

### Q: Filesystem operations denied
A: Check `FS_ALLOWED_PATHS` and `FS_ALLOWED_EXTENSIONS` configuration to ensure paths and file types are allowed.

## 📞 Support

- GitHub Issues: [https://github.com/ppengit/mcp-sqlserver-filesystem/issues](https://github.com/ppengit/mcp-sqlserver-filesystem/issues)

## 🔄 Changelog

### v1.0.1
- 🎉 First stable release
- ✨ Complete SQL Server database support
- 📁 Comprehensive filesystem operations
- 🔒 Enhanced security features
- 📝 Improved error handling and logging
- 🚀 Simplified architecture focused on core functionality

---

**Note**: This version focuses on core functionality stability and reliability, providing a simple and efficient MCP server experience.
