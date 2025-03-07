"""
FastAPI /chat 接口测试模块。

该模块用于测试 FastAPI 后端的 `/chat` 接口，验证不同用户输入下后端是否返回正确的响应。使用 `pytest` 和 `httpx` 库进行异步测试，模拟与后端进行交互，确保接口处理正常，能够根据不同的输入返回期望的聊天机器人回复。

主要功能：
- 测试机器人对常见输入（如 "Hikari", "damn", "bye" 和 "?" 等）的响应是否正确。
- 验证机器人能否处理各种不同类型的请求，并返回相应的正确消息。
- 通过接口返回的 JSON 数据验证每个响应的正确性。

测试流程：
1. 使用 `httpx.AsyncClient` 配合 `ASGITransport` 连接 FastAPI 应用，模拟请求和响应。
2. 向 `/chat` 接口发送包含不同文本的 POST 请求，检查响应的状态码和返回的 JSON 内容。
3. 使用 `assert` 语句确认响应是否符合预期，若不符合则触发错误。

测试用例：
- 测试输入 "Hikari" 时，机器人应该返回欢迎消息。
- 测试输入脏话 "damn" 时，机器人应该返回封禁提示。
- 测试输入 "bye" 时，机器人应该回复断开连接消息。
- 测试输入问号 "?" 时，机器人应该提示使用界内文字。

异常处理：
- 每个测试用例都会检查返回的响应状态码和内容，确保接口能够稳定、准确地处理各种用户输入。

使用示例：
- 执行该测试模块，能够确保聊天接口正确处理不同输入，并在每种情况下返回符合预期的回复。

注意：
- 测试前确保 FastAPI 应用已启动，并且可以通过 `http://localhost:3000` 访问。
"""



import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
API_URL = "http://localhost:3000"

@pytest.mark.asyncio
async def test_chat_end():
    """Test the /chat end."""

    transport = ASGITransport(app=app)  # 使用 ASGITransport 替代 app 参数
    async with AsyncClient(transport=transport, base_url=API_URL) as client:
        
        response = await client.post("/chat", json={"text": "Hikari"})
        assert response.status_code == 200
        assert response.json() == {"reply": "Hello! I am Hikari! How can I assist you?"}

        response = await client.post("/chat", json={"text": "damn"})
        assert response.status_code == 200
        assert response.json() == {"reply": "You Are Banned!给我爬！"}

        
        response = await client.post("/chat", json={"text": "bye"})
        assert response.status_code == 200
        assert response.json() == {"reply": "生物链接断开，回归休眠！"}

        response = await client.post("/chat", json={"text": "?"})
        assert response.status_code == 200
        assert response.json() == {"reply": "请使用界内文字！光是理解不了的(TAT)"}

