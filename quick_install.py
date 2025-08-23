#!/usr/bin/env python3
"""
MCP SQL Server Filesystem 快速安装脚本
====================================

此脚本帮助用户快速安装和配置 MCP SQL Server Filesystem。
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("💡 请安装Python 3.11或更高版本")
        print("   下载地址: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_odbc_driver():
    """检查ODBC驱动"""
    print("\n🔍 检查ODBC驱动...")
    try:
        import pyodbc
        drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
        if drivers:
            print("✅ 找到SQL Server ODBC驱动:")
            for driver in drivers:
                print(f"   - {driver}")
            return True
        else:
            print("❌ 未找到SQL Server ODBC驱动")
            print("💡 请安装ODBC Driver for SQL Server:")
            print("   winget install Microsoft.ODBCDriverforSQLServer")
            return False
    except ImportError:
        print("❌ pyodbc模块未安装")
        print("💡 正在安装pyodbc...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyodbc"], check=True)
            print("✅ pyodbc安装成功")
            return check_odbc_driver()  # 递归检查
        except subprocess.CalledProcessError:
            print("❌ pyodbc安装失败")
            return False


def install_dependencies():
    """安装项目依赖"""
    print("\n📦 安装项目依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def create_env_file():
    """创建.env配置文件"""
    print("\n📝 创建配置文件...")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env文件已存在")
        return True
    
    if not env_example_path.exists():
        print("❌ .env.example文件不存在")
        return False
    
    # 复制示例文件
    import shutil
    shutil.copy2(env_example_path, env_path)
    print("✅ 已创建.env配置文件")
    
    # 提示用户编辑
    print("💡 请编辑.env文件设置您的数据库连接信息:")
    print(f"   notepad {env_path}")
    
    return True


def test_installation():
    """测试安装"""
    print("\n🧪 测试安装...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "mcp_sqlserver_filesystem", "version"
        ], capture_output=True, text=True, check=True)
        
        print("✅ 安装测试成功")
        print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装测试失败: {e}")
        print(f"   错误输出: {e.stderr}")
        return False


def generate_augment_config():
    """生成Augment Code配置"""
    print("\n🔧 生成Augment Code配置...")
    
    current_dir = Path.cwd().resolve()
    
    config = {
        "mcpServers": {
            "mcp-sqlserver-filesystem": {
                "command": "python",
                "args": ["-m", "mcp_sqlserver_filesystem"],
                "cwd": str(current_dir),
                "timeout": 600,
                "env": {
                    "PYTHONPATH": str(current_dir / "src"),
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
    
    # 保存配置到文件
    config_file = Path("augment_code_config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置已保存到: {config_file}")
    print("\n📋 请将以下配置添加到Augment Code:")
    print("   配置文件位置:")
    print("   Windows: %APPDATA%\\Cursor\\User\\globalStorage\\rooveterinaryinc.roo-cline\\settings\\cline_mcp_settings.json")
    print(f"\n   或直接复制 {config_file} 中的内容")
    
    return True


def main():
    """主函数"""
    print("🚀 MCP SQL Server Filesystem 快速安装")
    print("=" * 50)
    
    # 检查系统要求
    if not check_python():
        return False
    
    if not check_odbc_driver():
        print("\n⚠️  ODBC驱动检查失败，但可以继续安装")
        print("   请稍后手动安装ODBC驱动")
    
    # 安装依赖
    if not install_dependencies():
        return False
    
    # 创建配置文件
    if not create_env_file():
        return False
    
    # 测试安装
    if not test_installation():
        return False
    
    # 生成Augment Code配置
    if not generate_augment_config():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 安装完成！")
    print("\n📋 下一步:")
    print("1. 编辑.env文件设置数据库连接")
    print("2. 将augment_code_config.json中的配置添加到Augment Code")
    print("3. 重启Augment Code/Cursor")
    print("4. 测试MCP连接:")
    print("   - 'list all tables in database'")
    print("   - 'show me the schema of users table'")
    print("   - 'read the file config.json'")
    
    print("\n🌐 Web UI测试:")
    print("   python -m mcp_sqlserver_filesystem test --web")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ 安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
