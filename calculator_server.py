from mcp.server.fastmcp import FastMCP

# FastMCPを使って簡単にMCPサーバーを作成します
mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数値を足し算します"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """2つの数値を掛け算します"""
    return a * b

if __name__ == "__main__":
    # サーバーを標準入出力(stdio)モードで起動します
    mcp.run()
