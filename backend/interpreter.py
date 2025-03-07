"""
Arc 解释器模块。

该模块包含了用于解析和处理自定义 DSL 语法的类和方法，包括以下配置：
- 自定义 Transformer，用于将 DSL 文本转换为结构化的字典格式。
- ArcInterpreter 类，用于解析 DSL 文件并根据用户输入生成响应。
- 支持条件语句和默认语句，能够根据不同条件生成相应的回复。

主要功能：
- 定义 `ArcTransformer` 类，用于转换 DSL 语法树。
- 定义 `ArcInterpreter` 类，用于加载和解析 DSL 文件，生成聊天机器人响应。
- 处理条件语句和默认语句，支持根据输入更新状态和生成动态响应。
- 通过 `get_statistics` 方法替换文本中的占位符，生成带有动态数据的回复。

异常处理：
- 对文件加载、语法解析和数据处理等关键步骤进行了错误捕获，保证程序的健壮性。
- 若遇到错误会记录详细日志，并在必要时终止程序。

示例数据：
- 该模块使用了一个示例数据 `ware`，包含了一些商品的 ID 和 PTT 值，可以用于响应生成时的数据替换。
"""



import logging
import pprint
import sys
import unittest

from pathlib import Path
from lark import Lark, Transformer
try:
    from config import get_logging_config
except ImportError:
    from backend.config import get_logging_config

# 示例数据，包含不同 id 和对应的 ptt 值
ware = [
    {"id": 500, "ptt": 13.12},
    {"id": 307, "ptt": 13.11},
    {"id": 364, "ptt": 12.71},
    {"id": 372, "ptt": 10.89},
]

# 尝试加载日志配置，捕获异常以保证程序的稳定性
try:
    get_logging_config()
    logger = logging.getLogger("exampleLogger")
except Exception as e:
    print(f"日志配置加载失败: {e}")
    sys.exit(1)  # 如果日志配置失败，退出程序


class ArcTransformer(Transformer):
    """自定义 Transformer,用于解析 DSL 语法定义的 discipline。"""

    def start(self, children):
        """转换语法的开始部分,返回语法定义与表达式块的字典映射。"""
        return {statement['state_definition']: statement['expression_block'] for statement in children}

    def statement(self, children):
        """转换语法中的一个语句，返回包含 state_definition 和 expression_block 的字典。"""
        return {'state_definition': children[0], 'expression_block': children[1]}

    def state_definition(self, children):
        """提取状态定义名称，返回字符串类型的状态名称。"""
        return str(children[0])

    def expression_block(self, children):
        """返回表达式块的列表，包括条件语句和默认语句。"""
        return children

    def othercons(self, children):
        """提取 'or' 条件，返回一个包含 'or' 条件的字典。"""
        return {'other_condition': children[0]}  # children[0] is 'or', children[1] is condition

    def condition(self, children):
        """提取条件字符串，去掉引号后返回。"""
        return children[0][1:-1]  # Remove quotes

    def action_block(self, children):
        """解析动作块，包含响应动作。"""
        # 'respond' keyword is at children[0]
        response = children[0]  # children[1] is the response
        return {'action_block': {'response': response}}

    def response(self, children):
        """提取响应字符串，去掉引号后返回。"""
        return children[0][1:-1]  # Remove quotes

    def state_transition(self, children):
        """提取状态转换名称，返回状态名称的字符串。"""
        return str(children[0])

    def conditional_statement(self, children):
        """解析条件语句，包含条件、动作和状态转换。"""
        # Index to keep track of position in children
        index = 0 
        conditions = [children[index]]  # 第一个条件
        index += 1

        # 用or逻辑聚集所有条件
        while index < len(children) and isinstance(children[index], dict) and 'other_condition' in children[index]:
            conditions.append(children[index]['other_condition'])
            index += 1

        # 提取动作块
        action_block = None
        if index < len(children) and isinstance(children[index], dict) and 'action_block' in children[index]:
            action_block = children[index]['action_block']
            index += 1

        # 可选的状态转换
        state_transition = None
        if index < len(children) :
            state_transition = children[index]
            

        return {
            'type': 'conditional',
            'conditions': conditions,
            'actions': action_block,
            'transition': state_transition if state_transition else 'INIT'
        }

    def default_statement(self, children):
        """解析默认语句，包含动作和可选的状态转换。"""
        # 'otherwise' is at children[0]
        index = 0
        action_block = None
        if index < len(children) and isinstance(children[index], dict) and 'action_block' in children[index]:
            action_block = children[index]['action_block']
            index += 1

        # 可选的状态转换
        state_transition = None
        if index < len(children):
            state_transition = children[index]

        return {
            'type': 'default',
            'actions': action_block,
            'transition': state_transition if state_transition else 'INIT'
        }


class ArcInterpreter:
    """DSL 解释器，用于处理自定义定义的 discipline。"""

    def __init__(self,disc_file_path: str, grammar_file_path: str) -> None:
        """初始化 Arc 解释器，加载并解析 DSL 文本和语法文件。"""
        try:
            # 读取语法文件
            with Path(grammar_file_path).open(encoding="utf-8") as f:
                grammar = f.read()

            # 使用 Lark 解析器初始化语法树
            self.parser = Lark(grammar, start="start", parser="lalr", transformer=ArcTransformer())
        except FileNotFoundError as e:
            logger.error("Grammar files not found: %s", e)
            raise  # 重新抛出异常以便后续处理
        except Exception as e:
            logger.error("Grammar logged fault: %s", e)
            raise

        try:
            # 读取并解析 DSL 文件
            with Path(disc_file_path).open(encoding="utf-8") as f:
                dsl_text = f.read()

            # 解析 DSL 文本
            self.tree = self.parser.parse(dsl_text)
        except FileNotFoundError as e:
            logger.error("DSL file not found: %s", e)
            raise
        except Exception as e:
            logger.error("Analyse DSL file fault: %s", e)
            raise

        try:
            # 使用 ArcTransformer 转换解析树为字典形式的 disciplines
            self.demand = ArcTransformer().transform(self.tree)
        except Exception as e:
            logger.error("Convert DSL tree error: %s", e)
            raise

        # 初始化默认状态为 INIT
        self.id = None
        self.current_state = "INIT"

        # 获取默认动作
        self.defaultact = self.demand.get("DEFAULT", [{"actions": {"response": "Default response"}}])[0]["actions"]["response"]
        
        # 输出解析树的日志信息
        logger.info(pprint.pp(self.tree))

    def get_statistics(self, text: str) -> str:
        """将文本中的占位符替换为实际值。"""
        try:
            ids = "\n" + "\n".join(str(data["id"]) for data in ware)
            text = text.replace("{ids}", ids)

            # 如果 id 已经被设置，替换 {id} 占位符
            if self.id:
                text = text.replace("{id}", str(self.id))

            # 如果 ware 中有与 id 匹配的条目，替换 {id.ptt} 占位符
            for data in ware:
                if self.id and data["id"] == self.id:
                    text = text.replace("{id.ptt}", str(data["ptt"]))

        except Exception as e:
            logger.error("替换统计信息时发生错误: %s", e)
            raise

        return text

    def process_conditional_statement(self, statement: dict, user_input: str) -> str:
        """处理条件语句，生成相应的回复。"""
        try:
            if statement["type"] == "conditional":
                # 如果任何条件匹配用户输入，生成响应
                if any(condition in user_input for condition in statement["conditions"]):
                    self.current_state = statement.get("transition", "INIT")
                    response_text = statement["actions"]["response"]
                    return self.get_statistics(response_text)
            elif statement["type"] == "default":
                # 默认动作，如果没有条件匹配
                self.current_state = statement.get("transition", "INIT")
                response_text = statement["actions"]["response"]
                return self.get_statistics(response_text)
        except KeyError as e:
            logger.error("ConStates dealing key error: %s", e)
        except Exception as e:
            logger.error("ConStates dealing another fault: %s", e)

        return "No valid response."

    def get_response(self, user_input: str) -> str:
        """Generate a response based on user input and update state."""
        try:
            if not self.current_state:
                self.current_state = "INIT"

            # 输出当前状态的日志信息
            logger.info("Current Status: %s", self.current_state)

            # 获取当前状态对应的 discipline
            disciplines_for_state = self.demand.get(self.current_state, [])

            # 如果当前状态为 'SEARCH' ,并且用户输入是数字，更新 id
            if self.current_state.startswith("SEARCH") and user_input.isdigit():
                self.id = int(user_input)

                # 如果输入的 id 在 ware 中存在，替换输入
                logger.info("Object ID: %d", self.id)
                if any(data["id"] == self.id for data in ware):
                    user_input = "{id}"

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
            logger.error("Response Error: %s", e)
            return "An error occurred while processing your request."