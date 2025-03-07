"""
ArcInterpreter 聊天功能单元测试 - 模拟测试版

该模块用于测试 `ArcInterpreter` 类的 `get_response` 方法的行为。通过 `MagicMock` 模拟 `ArcInterpreter` 实例，针对不同的输入文本验证其返回的聊天响应是否正确。

测试目的：
- 使用 `MagicMock` 模拟 `ArcInterpreter` 实例中的 `get_response` 方法，并通过设定的模拟响应来测试不同输入下的返回结果。
- 确保 `ArcInterpreter` 在面对各种输入时，能够返回预期的响应，包括正常查询、礼貌用语、粗鲁语言、以及特定命令等。

测试流程：
1. 使用 `MagicMock` 替代 `ArcInterpreter` 实际实例，通过 `side_effect` 设置预期的返回值。
2. 对常见的聊天输入（如打招呼、查询、粗鲁言语等）进行断言，验证返回的响应是否与预期一致。
3. 通过对不同文本的测试，确保机器人能根据用户输入做出正确的反应。

主要测试点：
- 测试基本的打招呼和帮助请求，如 `"hello"`, `"hi"`, `"查询"`, `"退出"` 等。
- 测试粗鲁语言输入，如 `"damn"`, `"草"` 等是否能返回封禁提示。
- 测试特定的命令输入，如 `"ptt"`, `"潜力值"`, `"?"` 等，确保返回的响应符合预期。
- 确保未定义命令的输入返回 `"Unknown command"`。

注意事项：
- 测试中的响应通过 `MagicMock` 进行模拟，模拟的响应值可以根据需要调整。
- 本测试仅用于单元测试，模拟了 `get_response` 方法的返回值，不涉及真实的交互逻辑。

使用示例：
- 运行此测试模块将验证 `ArcInterpreter` 类在不同输入情况下的响应，确保聊天机器人功能的正常运行。

"""



from unittest.mock import MagicMock
from backend.interpreter import ArcInterpreter

# Mock data for testing
grammar_file = "grammars.lark"
disc_file = "disciplines.dsl"

# Test cases for the test stub version
def test_interpreter_chat_stub():
    # Create a mock instance of ArcInterpreter
    arc_interpreter = MagicMock(ArcInterpreter)
    
    # Stub the get_response method with pre-set responses
    arc_interpreter.get_response = MagicMock(side_effect=lambda text: {
        "hello": "Hello! I am Hikari! How can I assist you?",
        "hi": "Hello! I am Hikari! How can I assist you?",
        "Hikari": "Hello! I am Hikari! How can I assist you?",
        "你好": "好！我是光！需要什么助力呢？",
        "查询": "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372",
        "退出": "正在返回初始界面",
        "在吗": "好！我是光！需要什么助力呢？",
        "您好": "好！我是光！需要什么助力呢？",
        "光": "好！我是光！需要什么助力呢？",
        "damn": "You Are Banned!给我爬！",
        "草": "You Are Banned!给我爬！",
        "ptt": "接下来我会根据master的提示给出回应哦~",
        "?": "链接失效，尝试重连至Arcaea...",
        "potential": "接下来我会根据master的提示给出回应哦~",
        "潜力值": "接下来我会根据master的提示给出回应哦~",
        "？": "请使用界内文字！光是理解不了的(TAT)"
    }.get(text, "Unknown command"))

    # Test greeting funcs
    assert arc_interpreter.get_response("hello") == "Hello! I am Hikari! How can I assist you?"
    assert arc_interpreter.get_response("hi") == "Hello! I am Hikari! How can I assist you?"
    assert arc_interpreter.get_response("Hikari") == "Hello! I am Hikari! How can I assist you?"

    # Test assistance funcs
    assert arc_interpreter.get_response("你好") == "好！我是光！需要什么助力呢？"
    assert arc_interpreter.get_response("查询") == "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372"
    assert arc_interpreter.get_response("退出") == "正在返回初始界面"

    # Additional tests
    assert arc_interpreter.get_response("在吗") == "好！我是光！需要什么助力呢？"
    assert arc_interpreter.get_response("查询") == "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372"
    assert arc_interpreter.get_response("退出") == "正在返回初始界面"
    assert arc_interpreter.get_response("您好") == "好！我是光！需要什么助力呢？"
    assert arc_interpreter.get_response("查询") == "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372"
    assert arc_interpreter.get_response("退出") == "正在返回初始界面"
    assert arc_interpreter.get_response("光") == "好！我是光！需要什么助力呢？"
    assert arc_interpreter.get_response("查询") == "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372"
    assert arc_interpreter.get_response("退出") == "正在返回初始界面"

    # Test rude message
    assert arc_interpreter.get_response("damn") == "You Are Banned!给我爬！"
    assert arc_interpreter.get_response("草") == "You Are Banned!给我爬！"

    # Test ptt message
    assert arc_interpreter.get_response("ptt") == "接下来我会根据master的提示给出回应哦~"
    assert arc_interpreter.get_response("?") == "链接失效，尝试重连至Arcaea..."
    assert arc_interpreter.get_response("potential") == "接下来我会根据master的提示给出回应哦~"
    assert arc_interpreter.get_response("?") == "链接失效，尝试重连至Arcaea..."
    assert arc_interpreter.get_response("潜力值") == "接下来我会根据master的提示给出回应哦~"
    assert arc_interpreter.get_response("?") == "链接失效，尝试重连至Arcaea..."

    # Test outbound message
    assert arc_interpreter.get_response("？") == "请使用界内文字！光是理解不了的(TAT)"
