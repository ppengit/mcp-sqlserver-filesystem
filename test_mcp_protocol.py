#!/usr/bin/env python3
"""
测试MCP协议实现是否正确
"""

import asyncio
import json
import sys
import subprocess
from pathlib import Path

async def test_mcp_server():
    """测试MCP服务器的基本协议实现"""
    print("🧪 测试MCP服务器协议实现...")
    
    # 设置环境变量
    env = {
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
    }
    
    try:
        # 启动MCP服务器进程
        print("🚀 启动MCP服务器...")
        process = await asyncio.create_subprocess_exec(
            "uvx", "mcp-sqlserver-filesystem@latest",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**env}
        )
        
        # 发送初始化请求
        print("📡 发送初始化请求...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # 发送请求
        request_data = json.dumps(init_request) + "\n"
        process.stdin.write(request_data.encode())
        await process.stdin.drain()
        
        # 读取响应
        print("📥 等待初始化响应...")
        response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        
        if response_line:
            response = json.loads(response_line.decode().strip())
            print(f"✅ 收到初始化响应: {response}")
            
            # 发送tools/list请求
            print("📡 请求工具列表...")
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            request_data = json.dumps(tools_request) + "\n"
            process.stdin.write(request_data.encode())
            await process.stdin.drain()
            
            # 读取工具列表响应
            tools_response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
            if tools_response_line:
                tools_response = json.loads(tools_response_line.decode().strip())
                print(f"✅ 收到工具列表: {len(tools_response.get('result', {}).get('tools', []))} 个工具")
                
                # 显示工具名称
                tools = tools_response.get('result', {}).get('tools', [])
                for tool in tools:
                    print(f"  - {tool.get('name')}: {tool.get('description')}")
                
                print("✅ MCP协议测试成功！")
                return True
            else:
                print("❌ 未收到工具列表响应")
                return False
        else:
            print("❌ 未收到初始化响应")
            return False
            
    except asyncio.TimeoutError:
        print("❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        # 清理进程
        if process:
            try:
                process.terminate()
                await process.wait()
            except:
                pass

async def test_simple_connection():
    """测试简单的连接"""
    print("🔌 测试简单连接...")
    
    try:
        # 尝试启动服务器并立即检查
        result = subprocess.run([
            "uvx", "mcp-sqlserver-filesystem@latest", "--help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 服务器可以正常启动")
            print(f"输出: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ 服务器启动失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 服务器启动超时")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 MCP SQL Server Filesystem 协议测试")
    print("=" * 60)
    
    # 测试1: 简单连接
    success1 = await test_simple_connection()
    print()
    
    # 测试2: MCP协议
    success2 = await test_mcp_protocol()
    print()
    
    if success1 and success2:
        print("🎉 所有测试通过！MCP服务器协议实现正确。")
        print("💡 如果AugmentCode仍显示橙色，可能是:")
        print("   1. AugmentCode的MCP客户端实现问题")
        print("   2. 网络或权限问题")
        print("   3. 环境变量配置问题")
    else:
        print("❌ 测试失败，MCP服务器可能有问题")
        
    return success1 and success2

if __name__ == "__main__":
    asyncio.run(main())
