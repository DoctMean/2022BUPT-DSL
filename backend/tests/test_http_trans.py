"""
FastAPI Chatbot 测试模块。

该模块用于测试 FastAPI 后端的 `/chat` 接口，特别是与 ptt 相关的交互逻辑。使用 `pytest` 和 `httpx` 库进行异步测试，模拟前端与后端的通信，确保正确处理用户输入并返回预期响应。

主要功能：
- 测试发送 "ptt"、"高"、"low"、"你好" 等消息时，后端是否返回正确的响应。
- 验证后端对于不同类型的查询（有效或无效）是否能够做出正确回应。
- 测试当输入为特定的字符串（如 "在吗"）时，是否返回预期的聊天机器人响应。

测试流程：
1. 使用 `httpx.AsyncClient` 通过 ASGITransport 连接 FastAPI 应用，模拟与后端进行聊天交互。
2. 发送不同的消息（如 "ptt", "高", "low", "你好" 等），检查后端返回的状态码和 JSON 响应。
3. 确保每个响应与预期值一致，确保后端逻辑的正确性。

异常处理：
- 每个测试用例中都会通过 `assert` 语句验证返回的响应状态码和内容，若不符合预期，则会抛出 `AssertionError`。

使用示例：
- 运行该测试模块可以确保聊天接口在处理与 ptt 相关的输入时的稳定性和正确性。

注意：
- 需要在测试环境中启动 FastAPI 应用，确保 `http://localhost:3000` 可访问。
"""



import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
API_URL = "http://localhost:3000"

@pytest.mark.asyncio
async def test_chat_ptt():
    """Test ptt-related interactions via /chat end."""

    transport = ASGITransport(app=app)  # 使用 ASGITransport 替代 app 参数
    async with AsyncClient(transport=transport, base_url=API_URL) as client:
        # Test ptt response
        response = await client.post("/chat", json={"text": "ptt"})
        assert response.status_code == 200
        assert response.json() == {"reply": "接下来我会根据master的提示给出回应哦~"}

        # Test query response
        response = await client.post("/chat", json={"text": "高"})
        assert response.status_code == 200
        assert response.json() == {"reply": "目前ptt最高值为13.12哟~你差得远呢"}

        # Test invalid query
        response = await client.post("/chat", json={"text": "low"})
        assert response.status_code == 200
        assert response.json() == {"reply": "目前ptt最低值为0.00哟~你差得不远呢！加油"}

        # Test valid query
        response = await client.post("/chat", json={"text": "你好"})
        assert response.status_code == 200
        assert response.json() == {"reply": "链接失效，尝试重连至Arcaea..."}

        
        response = await client.post("/chat", json={"text": "在吗"})
        assert response.status_code == 200
        assert response.json() == {"reply": "好！我是光！需要什么助力呢？"}