"""
ArcInterpreter 聊天功能测试模块。

该模块用于测试 `ArcInterpreter` 类的聊天功能，包括对不同用户输入的响应，验证其在处理问候、请求帮助、违规输入、以及查询等功能时的表现。测试涵盖了多种输入情景，确保解释器根据 DSL 语法正确响应。

主要功能：
- 测试用户输入的问候语（如 "hello", "hi", "Hikari"）是否正确响应为问候信息。
- 测试用户请求帮助时，解释器是否能正确返回查询信息和帮助指引。
- 测试在接收到违反规则的输入（如 "damn" 和 "草"）时，是否正确返回禁用消息。
- 测试针对 `ptt` 和潜力值查询的输入是否正确生成响应。
- 测试不符合界内文字的输入是否能返回提示信息。

异常处理：
- 对每个测试用例进行了断言检查，确保返回的响应符合预期。如果有任何测试失败，程序将抛出 `AssertionError`。

测试数据：
- 使用模拟的 `grammars.lark` 和 `disciplines.dsl` 文件进行测试，确保解释器根据这些文件中的定义生成正确的响应。

使用示例：
- 通过运行该测试模块，可以验证 `ArcInterpreter` 在处理不同用户输入时是否能够正确生成响应，确保聊天功能的准确性和稳定性。
"""



from backend.interpreter import ArcInterpreter

# Mock data for testing
grammar_file = "grammars.lark"
disc_file = "disciplines.dsl"

# Test cases
def test_interpreter_chat():
    arc_interpreter = ArcInterpreter(disc_file_path=disc_file, grammar_file_path=grammar_file)

    # Test greeting funcs
    assert arc_interpreter.get_response("hello") == "Hello! I am Hikari! How can I assist you?"
    assert arc_interpreter.get_response("hi") == "Hello! I am Hikari! How can I assist you?"
    assert arc_interpreter.get_response("Hikari") == "Hello! I am Hikari! How can I assist you?"

    # Test assistance funcs
    assert arc_interpreter.get_response("你好") == "好！我是光！需要什么助力呢？"
    assert arc_interpreter.get_response("查询") == "请问需要查询哪位玩家的potential呢？\n500\n307\n364\n372"
    assert arc_interpreter.get_response("退出") == "正在返回初始界面"

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
    assert arc_interpreter.get_response("?") == "请使用界内文字！光是理解不了的(TAT)"
    assert arc_interpreter.get_response("？") == "请使用界内文字！光是理解不了的(TAT)"