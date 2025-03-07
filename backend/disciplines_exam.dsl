INIT:
    when "hello" or "hi" or "Hikari" then
        respond "Hello! I am Hikari! How can I HELP you?"

    when "help" then
        respond "Sure, biolink complished. What do you need?"
        transition HELP

    otherwise
        respond "请使用界内文字！无法理解"
        transition INIT

HELP:
    when "LOOKUP" or "查询" then
        respond "请问需要查询哪位玩家的段位呢？{ids}"
        transition LOOKUP

    otherwise
        respond "需要什么帮助？"
        transition HELP


LOOKUP:
    when "{id}" then
        respond "玩家{id}的段位为{id.ptt}"
        transition LOOKUP

    when "quit" or "exit" or "退出" then
        respond "正在返回初始界面"
        transition INIT

DEFAULT:
    otherwise
        respond "链接失效，尝试重连..."
        transition INIT