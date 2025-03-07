"""FastAPI 聊天机器人后端应用模块。

该模块设置了 FastAPI 应用，包括以下配置：
- CORS 配置，允许前端跨域访问。
- 日志配置，用于跟踪事件和错误。
- 使用 DSL 解释器处理用户消息的接口，生成聊天机器人回复。

主要功能：
- 配置 CORS,允许来自前端(如 React)的请求。
- 定义 `Message` 模型，处理用户输入。
- 通过 `ArcInterpreter` 解释 DSL 生成回复。
- `/chat` POST 接口处理用户输入并返回响应。
"""



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import sys

# 尝试从配置文件导入日志设置函数和日志对象
try:
    from config import get_logging_config, logging
except ImportError:
    from backend.config import get_logging_config, logging


# 尝试从解释器模块导入 ArcInterpreter 类
try:
    from interpreter import ArcInterpreter
except ImportError:
    from backend.interpreter import ArcInterpreter


# 配置日志
try:
    get_logging_config()  # 尝试加载日志配置
    logger = logging.getLogger("exampleLogger")  # 获取日志记录器
    logger.info("Config Info")  # 记录配置信息，确认日志系统已启动
except Exception as e:
    # 如果加载日志配置失败，记录异常并输出到标准错误
    print(f"日志配置失败: {e}")
    # 可以选择在这里终止程序或继续执行
    sys.exit(1)  # 退出程序，提示日志系统未正确配置


app = FastAPI()

# 添加 CORS 中间件，以允许来自指定源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_methods = ["*"],  # 允许所有 HTTP 方法，如 GET、POST、PUT 等
    allow_headers = ["*"],  # 允许所有的请求头
    allow_origins = ["http://localhost:3000"],  # 仅允许来自本地 React 前端的请求

)


# 定义一个 Pydantic 模型，用于描述用户消息的结构
class Message(BaseModel):
    """用户消息的 Schema。

    该类定义了发送到聊天接口的消息结构，包含一个字段：
    - text: 用户输入的消息。
    """
    
    # 用户输入的文本消息
    text: str


# 初始化 DSL 解释器，传入定义好的 DSL 文件路径和语法文件路径
interpreter = ArcInterpreter(
    disc_file_path="./disciplines.dsl",
    grammar_file_path="./grammars.lark",
)

# 创建一个 POST 请求的聊天接口
@app.post("/chat")
async def chat_end(message: Message) -> dict:
    """处理用户聊天请求并返回回复。

    该接口接受一个包含用户消息的 POST 请求，使用 ArcInterpreter 处理消息，并返回相应的回复。

    参数：
        message: 用户发送的消息。

    返回值：
        dict: 包含回复的字典。

    示例：
        输入: {"text": "Ciao!"}
        输出: {"reply": "Hello! May I help you?"}
    """

    # 获取用户消息并去掉两端的空白字符
    user_message = message.text.strip() 

    # 如果用户没有输入消息，则返回 400 错误
    if not user_message:
        raise HTTPException(status_code=400, detail="你好?需要什么帮助嘛?")
    
    try:
        # 使用 DSL 解释器生成响应
        response = interpreter.get_response(user_message)
        return {"reply": response}
    except Exception as e:
        # 捕获可能的异常，记录详细错误信息，并返回 500 错误

        # 记录异常的堆栈跟踪
        logger.exception("Error processing message")   
        raise HTTPException(status_code=500, detail="处理请求时发生错误，请稍后再试。")
    