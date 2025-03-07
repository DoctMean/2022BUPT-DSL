"""
ArcInterpreter 状态转换测试模块。

该模块包含了针对 `ArcInterpreter` 类的状态转换功能的单元测试。测试主要验证在处理不同用户输入时，解释器是否能够根据定义正确返回响应，包括对 "ptt"、"高"、"low" 等相关输入的处理。

主要功能：
- 测试 `ArcInterpreter` 类的 `get_response` 方法，确保解释器能够根据用户输入正确返回响应。
- 测试包含状态转换和数据更新的复杂情景，如查询 `ptt` 值和其他状态相关的输入。
- 验证 DSL 语法定义是否能正确地影响状态转换和响应内容。

异常处理：
- 对每个输入场景进行了断言检查，确保返回的响应符合预期，如果任何测试失败，程序将抛出 `AssertionError`。

测试数据：
- 使用了模拟的 `grammars.lark` 和 `disciplines.dsl` 文件作为输入数据进行测试，确保解释器根据这些文件中的定义生成正确的响应。

使用示例：
- 通过运行该测试模块，可以验证 `ArcInterpreter` 是否能正确地解析并响应各种用户输入，确保其稳定性和准确性。
"""



from backend.interpreter import ArcInterpreter

# Mock data for testing
grammar_file = "grammars.lark"
disc_file = "disciplines.dsl"

# Test cases
def test_interpreter_trans():
    arc_interpreter = ArcInterpreter(disc_file_path=disc_file, grammar_file_path=grammar_file)
    # Test ptt
    assert arc_interpreter.get_response("ptt") == "接下来我会根据master的提示给出回应哦~"
    assert arc_interpreter.get_response("高") == "目前ptt最高值为13.12哟~你差得远呢"
    assert arc_interpreter.get_response("low") == "目前ptt最低值为0.00哟~你差得不远呢！加油"
    assert arc_interpreter.get_response("你好") == "链接失效，尝试重连至Arcaea..."
    assert arc_interpreter.get_response("在吗") == "好！我是光！需要什么助力呢？"