#!/usr/bin/env python3
"""
诊断MCP服务器问题
"""

import subprocess
import sys
import os
import time
import json

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    
    env = os.environ.copy()
    env.update({
        "DB_SERVER": "localhost",
        "DB_DATABASE": "CYSF_Dev", 
        "DB_USERNAME": "sa",
        "DB_PASSWORD": "Pass@word1",
        "DB_USE_WINDOWS_AUTH": "false",
        "DB_TRUST_SERVER_CERTIFICATE": "true",
        "DB_ENCRYPT": "false",
    })
    
    try:
        # 测试数据库连接
        result = subprocess.run([
            sys.executable, "-c", """
import sys
sys.path.insert(0, 'src')
from mcp_sqlserver_filesystem.database import db_manager
try:
    db_manager.test_connection()
    print('✅ 数据库连接成功')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
"""
        ], env=env, capture_output=True, text=True, timeout=30)
        
        print(f"数据库测试输出: {result.stdout}")
        if result.stderr:
            print(f"数据库测试错误: {result.stderr}")
            
        return "✅ 数据库连接成功" in result.stdout
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False

def test_mcp_server_startup():
    """测试MCP服务器启动"""
    print("🚀 测试MCP服务器启动...")
    
    env = os.environ.copy()
    env.update({
        "DB_SERVER": "localhost",
        "DB_DATABASE": "CYSF_Dev", 
        "DB_USERNAME": "sa",
        "DB_PASSWORD": "Pass@word1",
        "DB_USE_WINDOWS_AUTH": "false",
        "DB_TRUST_SERVER_CERTIFICATE": "true",
        "DB_ENCRYPT": "false",
        "FS_ALLOWED_PATHS": "*",
        "FS_ALLOWED_EXTENSIONS": "*.*",
        "FS_IGNORE_FILE_LOCKS": "true"
    })
    
    try:
        # 启动MCP服务器进程
        process = subprocess.Popen([
            sys.executable, "-m", "mcp_sqlserver_filesystem", "server"
        ], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True
        )
        
        # 等待一下让服务器启动
        time.sleep(2)
        
        # 检查进程是否还在运行
        if process.poll() is None:
            print("✅ MCP服务器进程正在运行")
            
            # 发送初始化请求
            init_request = '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}\n'
            
            try:
                process.stdin.write(init_request)
                process.stdin.flush()
                
                # 等待响应
                time.sleep(1)
                
                # 检查是否有输出
                process.stdin.close()
                stdout, stderr = process.communicate(timeout=5)
                
                print(f"📥 服务器输出: {stdout[:500]}...")
                if stderr:
                    print(f"📥 服务器错误: {stderr[:500]}...")
                
                # 检查是否有JSON响应
                if stdout and "{" in stdout:
                    print("✅ 服务器返回了JSON响应")
                    return True
                else:
                    print("❌ 服务器没有返回预期的JSON响应")
                    return False
                    
            except subprocess.TimeoutExpired:
                print("❌ 服务器响应超时")
                process.kill()
                return False
                
        else:
            # 进程已经退出
            stdout, stderr = process.communicate()
            print(f"❌ MCP服务器进程已退出，返回码: {process.returncode}")
            print(f"输出: {stdout}")
            print(f"错误: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ MCP服务器启动测试失败: {e}")
        return False

def test_uvx_installation():
    """测试uvx安装"""
    print("📦 测试uvx安装...")
    
    try:
        result = subprocess.run(["uvx", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ uvx版本: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ uvx不可用: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ uvx测试失败: {e}")
        return False

def test_package_installation():
    """测试包安装"""
    print("📦 测试包安装...")
    
    try:
        result = subprocess.run([
            "uvx", "mcp-sqlserver-filesystem@0.2.5", "version"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ 包安装成功: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ 包安装失败: {result.stderr[:200]}...")
            return False
    except Exception as e:
        print(f"❌ 包安装测试失败: {e}")
        return False

def main():
    """主诊断函数"""
    print("=" * 60)
    print("🔧 MCP SQL Server Filesystem 问题诊断")
    print("=" * 60)
    
    tests = [
        ("uvx安装", test_uvx_installation),
        ("包安装", test_package_installation),
        ("数据库连接", test_database_connection),
        ("MCP服务器启动", test_mcp_server_startup),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试:")
        results[test_name] = test_func()
        print()
    
    print("=" * 60)
    print("📊 诊断结果汇总:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有测试通过！MCP服务器应该可以正常工作。")
        print("💡 如果AugmentCode仍显示橙色，可能是AugmentCode的问题。")
    else:
        print("❌ 发现问题，需要修复失败的测试项。")
        
        if not results.get("数据库连接", False):
            print("\n💡 数据库连接失败的可能原因:")
            print("   1. SQL Server服务未启动")
            print("   2. sa账户被禁用或密码错误")
            print("   3. 数据库CYSF_Dev不存在")
            print("   4. 防火墙阻止连接")
        
        if not results.get("MCP服务器启动", False):
            print("\n💡 MCP服务器启动失败的可能原因:")
            print("   1. 数据库连接问题导致服务器无法启动")
            print("   2. 环境变量配置错误")
            print("   3. 依赖包版本冲突")

if __name__ == "__main__":
    main()
