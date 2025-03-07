"""
ArcInterpreter 测试模块。

该模块包含了针对 `ArcInterpreter` 类的单元测试，用于验证其在处理用户输入时的正确性和稳定性。测试涵盖了不同输入的响应生成，并确保解释器根据 DSL 文件中的定义返回预期的结果。

主要功能：
- 测试 `ArcInterpreter` 类的 `get_response` 方法，验证其对不同用户输入的响应。
- 模拟真实的输入场景，如查询 "潜力值"、"高"、"帮助" 等，确保解释器正确生成回复。
- 验证状态转换和输入解析的正确性，确保解释器根据 DSL 语法正确更新当前状态并返回适当的响应。

异常处理：
- 对每个测试用例进行了断言检查，确保返回值符合预期，如果有不符合预期的情况，测试将失败并抛出 AssertionError。

使用示例：
- 通过运行该测试模块，验证 `ArcInterpreter` 在实际应用中的表现，确保所有功能按设计正常运行。

测试数据：
- 使用了模拟的 `grammars.lark` 和 `disciplines.dsl` 文件作为输入数据进行测试。
"""



from backend.interpreter import ArcInterpreter

# Mock data for testing
grammar_file = "grammars.lark"
disc_file = "disciplines.dsl"


# Test cases
def test_interpreter_defualt():
    arc_interpreter = ArcInterpreter(disc_file_path=disc_file, grammar_file_path=grammar_file)

    assert arc_interpreter.get_response("潜力值") == "接下来我会根据master的提示给出回应哦~"
    assert arc_interpreter.get_response("高") == "目前ptt最高值为13.12哟~你差得远呢"
    assert arc_interpreter.get_response("帮助") == "链接失效，尝试重连至Arcaea..."

    assert arc_interpreter.get_response("潜力值") == "接下来我会根据master的提示给出回应哦~"
    assert arc_interpreter.get_response("高") == "目前ptt最高值为13.12哟~你差得远呢"
    assert arc_interpreter.get_response("退出") == "正在返回初始界面"
    assert arc_interpreter.get_response("是我") == "请使用界内文字！光是理解不了的(TAT)"
