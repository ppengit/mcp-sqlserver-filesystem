#!/usr/bin/env python3
"""
简单测试MCP服务器是否能正常启动
"""

import subprocess
import sys
import os

def test_mcp_server():
    """测试MCP服务器启动"""
    print("🧪 测试MCP服务器启动...")
    
    # 设置环境变量
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
        print("🚀 启动MCP服务器...")
        process = subprocess.Popen([
            sys.executable, "-m", "mcp_sqlserver_filesystem", "server"
        ], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True
        )
        
        # 发送简单的JSON-RPC请求
        print("📡 发送初始化请求...")
        init_request = '''{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
'''
        
        # 发送请求
        stdout, stderr = process.communicate(input=init_request, timeout=10)
        
        print(f"📥 标准输出: {stdout[:200]}...")
        print(f"📥 错误输出: {stderr[:200]}...")
        
        if process.returncode == 0:
            print("✅ MCP服务器正常退出")
            return True
        else:
            print(f"❌ MCP服务器异常退出，返回码: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 请求超时")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_server()
    if success:
        print("🎉 MCP服务器测试通过！")
        print("💡 现在可以在AugmentCode中重新配置并测试")
    else:
        print("❌ MCP服务器测试失败")
    
    sys.exit(0 if success else 1)
