"""
ArcInterpreter 模拟测试模块。

该模块用于测试 `MockArcInterpreter` 类的 `get_response` 方法，通过模拟不同的输入来验证聊天解释器在不同状态下的响应行为。此测试模拟了默认状态与条件语句状态下的返回结果，并验证了输入无法匹配任何条件时的默认响应。

主要功能：
- 测试默认状态下，当用户输入问候语时，解释器是否能返回正确的欢迎消息。
- 测试在条件语句状态（如 "SEARCH"）下，当用户输入特定的查询 ID（如 "500"）时，是否返回正确的搜索响应。
- 测试在输入无法匹配任何条件时，解释器是否返回预设的默认响应。

测试数据：
- 模拟了一个简化版本的 `ArcInterpreter` 类，设定了默认状态（"INIT"）与一个条件语句状态（"SEARCH"）。
- `get_response` 方法会根据当前状态和用户输入返回相应的响应信息。

使用示例：
- 运行该测试模块可以确保 `get_response` 方法在模拟的环境下正确处理不同用户输入，并返回符合预期的响应。

异常处理：
- 若任何测试失败，将通过断言抛出 `AssertionError`。
"""



from unittest.mock import MagicMock
import pytest

# 假设 get_response 是你正在测试的函数
class MockArcInterpreter:
    def __init__(self):
        self.current_state = "INIT"  # 默认状态
        self.demand = {
            "INIT": [
                {"type": "default", "response": "Hello! I am Hikari! How can I assist you?"}
            ],
            "SEARCH": [
                {"type": "conditional", "conditions": ["500", "307"], "response": "Searching for player..."}
            ]
        }
        self.id = None
        self.defaultact = "Sorry, I don't understand your request."

    def process_conditional_statement(self, discipline, user_input):
        # 简化版的条件处理函数，直接返回模拟响应
        return discipline["response"]

    def get_response(self, user_input: str) -> str:
        """Generate a response based on user input and update state."""
        try:
            if not self.current_state:
                self.current_state = "INIT"

            # 获取当前状态对应的 discipline
            disciplines_for_state = self.demand.get(self.current_state, [])

            # 如果当前状态为 'SEARCH' ,并且用户输入是数字，更新 id
            if self.current_state.startswith("SEARCH") and user_input.isdigit():
                self.id = int(user_input)

                # 判断 user input 是否属于当前状态的条件
                for discipline in disciplines_for_state:
                    if discipline["type"] == "conditional":
                        # Check if the input matches any of the conditions
                        if user_input in discipline["conditions"]:
                            return self.process_conditional_statement(discipline, user_input)

            # 遍历所有符合当前状态的 discipline，处理条件语句和默认语句
            for discipline in disciplines_for_state:
                if discipline["type"] == "conditional":
                    if any(condition in user_input for condition in discipline["conditions"]):
                        return self.process_conditional_statement(discipline, user_input)
                elif discipline["type"] == "default":
                    return self.process_conditional_statement(discipline, user_input)

            # 如果没有匹配的条件或默认语句，返回默认的响应
            self.current_state = "INIT"
            return self.defaultact
        except Exception as e:
            return "An error occurred while processing your request."


# 测试桩版本的测试
def test_get_response_stub():
    mock_interpreter = MockArcInterpreter()

    # 测试默认状态返回值
    response = mock_interpreter.get_response("hello")
    assert response == "Hello! I am Hikari! How can I assist you?"

    # 测试条件语句状态下的响应
    mock_interpreter.current_state = "SEARCH"
    response = mock_interpreter.get_response("500")
    assert response == "Searching for player..."  # 输入 "500" 时返回 "Searching for player..."

    # 测试输入无法匹配任何条件时返回的默认响应
    response = mock_interpreter.get_response("unknown command")
    assert response == "Sorry, I don't understand your request."
