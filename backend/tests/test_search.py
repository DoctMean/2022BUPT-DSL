"""
ArcInterpreter 搜索功能测试

该测试用例用于验证 `ArcInterpreter` 类在处理与玩家搜索相关的请求时，是否能够返回正确的响应。具体来说，测试了如何处理帮助信息、查询命令以及根据玩家编号返回成绩。

测试目的：
- 确保 `ArcInterpreter` 在接收到与搜索相关的输入时，能够根据预设的规则返回准确的信息。
- 包括帮助命令、查询命令以及基于玩家编号的成绩查询。

测试流程：
1. 初始化 `ArcInterpreter` 实例，并使用模拟数据加载相关文件（`grammars.lark` 和 `disciplines.dsl`）。
2. 调用 `get_response` 方法，对不同的输入进行断言，验证返回的结果是否符合预期。

主要测试点：
- 测试输入 `"帮助"` 时，确保返回正确的帮助信息。
- 测试输入 `"查询"` 时，确保能够返回查询提示信息，并列出玩家选择。
- 测试输入具体玩家编号（如 `"500"`）时，确保能够返回该玩家的成绩。

注意事项：
- 测试假设 `ArcInterpreter` 类能够正确地解析和处理传入的命令。
- 本测试主要针对查询命令和返回值进行验证，不涉及外部数据的依赖。

使用示例：
- 运行此测试时，`ArcInterpreter` 应该能够返回预定义的响应，确保与搜索相关的功能按预期工作。
"""



from backend.interpreter import ArcInterpreter

# Mock data for testing
grammar_file = "grammars.lark"
disc_file = "disciplines.dsl"


# Test cases
def test_interpreter_search():
    arc_interpreter = ArcInterpreter(disc_file_path=disc_file, grammar_file_path=grammar_file)

    assert arc_interpreter.get_response("帮助") == "生物链接！启动！需要什么帮助？"
    assert "请问需要查询哪位玩家的potential呢？" in arc_interpreter.get_response("查询")
    assert arc_interpreter.get_response("500") == "玩家500的成绩为13.12"
