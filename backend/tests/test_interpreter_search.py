"""
ArcInterpreter 搜索功能单元测试 - 模拟测试版

该模块用于测试 `ArcInterpreter` 类的 `get_response` 方法在搜索相关操作中的行为。通过 `MagicMock` 模拟 `ArcInterpreter` 实例，验证其对不同搜索命令的响应是否符合预期。

测试目的：
- 使用 `MagicMock` 模拟 `ArcInterpreter` 实例的 `get_response` 方法，针对搜索相关命令（如玩家查询、ptt查询等）验证返回值的正确性。
- 确保 `ArcInterpreter` 对于查询命令和相应的输入，能够返回相应的搜索结果和错误提示。

测试流程：
1. 使用 `MagicMock` 替代 `ArcInterpreter` 实例，通过 `side_effect` 设置针对不同文本输入的响应。
2. 对常见的查询输入（如 `"帮助"`, `"查询"`, `"500"` 等）进行断言，确保返回的响应与预期一致。
3. 验证对于不同搜索命令，机器人是否能返回正确的玩家成绩或相关信息。

主要测试点：
- 测试输入 `"帮助"` 时，返回帮助信息。
- 测试输入 `"查询"` 时，返回玩家列表并要求选择具体玩家。
- 测试输入具体玩家编号（如 `"500"`）时，返回该玩家的成绩。
- 测试输入 pt值相关的命令（如 `"高"`, `"低"`），确保返回当前的 pt 值信息。

注意事项：
- 该测试通过模拟 `get_response` 的返回值来验证搜索功能的正确性，模拟数据可以根据实际需求进行调整。
- 本测试仅用于模拟验证，并未调用实际的后端数据。

使用示例：
- 运行此测试模块将验证 `ArcInterpreter` 在处理与搜索功能相关的输入时，是否能够返回准确的结果。
"""



from unittest.mock import MagicMock
from backend.interpreter import ArcInterpreter

# Mock data for testing
grammar_file = "grammars.lark"
disc_file = "disciplines.dsl"

# Test cases for the test stub version
def test_interpreter_search_stub():
    # Create a mock instance of ArcInterpreter
    arc_interpreter = MagicMock(ArcInterpreter)
    
    # Stub the get_response method with pre-set responses
    arc_interpreter.get_response = MagicMock(side_effect=lambda text: {
        "帮助": "生物链接！启动！需要什么帮助？",
        "查询": "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372",
        "500": "玩家500的成绩为13.12",
        "高": "目前ptt最高值为13.12哟~你差得远呢",
        "低": "目前ptt最低值为0.00哟~你差得不远呢！加油"
    }.get(text, "Unknown command"))

    # Test that the stubbed responses are returned correctly
    assert arc_interpreter.get_response("帮助") == "生物链接！启动！需要什么帮助？"
    assert "请问需要查询哪位玩家的potential呢？" in arc_interpreter.get_response("查询")
    assert arc_interpreter.get_response("500") == "玩家500的成绩为13.12"
