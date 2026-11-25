"""Test registracije alata na MCP serveru — samo javni list_tools(), bez baze."""

import asyncio

from app.mcp.server import server


def test_registers_exactly_three_tools():
    tools = asyncio.run(server.list_tools())
    names = {tool.name for tool in tools}
    assert names == {"search_books", "ask_question", "list_books"}
