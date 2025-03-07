"""
日志配置模块。

该模块定义了 `get_logging_config` 函数，用于从配置文件中加载和设置日志记录系统。该函数通过读取 `logging.conf` 文件中的配置信息来初始化日志系统，并为后续的日志记录提供配置好的记录器、处理器和格式。

主要功能：
- 从 `logging.conf` 文件中加载日志配置，配置日志记录器。
- 设置日志的输出格式、级别和处理器等参数。
- 在加载配置过程中，如果遇到错误，记录错误信息并抛出异常。

异常处理：
- 如果配置文件加载或解析失败，会捕获异常并记录错误日志，同时抛出异常以保证系统的健壮性。

使用示例：
- 调用 `get_logging_config` 函数后，系统将根据 `logging.conf` 文件中的设置进行日志记录，使用 `logging` 模块输出日志信息。
"""



import logging
import logging.config

def get_logging_config():
    """
    配置日志记录系统。
    
    该函数从 'logging.conf' 文件中加载日志配置，该文件应该是一个标准的
    Python logging 配置文件。它会根据文件中的配置信息设置日志记录器、
    日志处理器、日志格式等。
    
    在这个函数执行完后，可以使用 logging 模块中的日志记录功能，
    按照 'logging.conf' 文件中的设置输出日志。
    """
    try:
        # 通过配置文件 'logging.conf' 设置日志记录系统
        with open('logging.conf', encoding='utf-8') as f:
            logging.config.fileConfig(f)
        
        # 提示配置加载成功
        logging.info("Log Set Successfully")
    except Exception as e:
        # 如果配置文件加载失败，输出错误日志
        logging.error("Log Set Error: %s", e)
        raise  # 如果配置加载失败，则抛出异常