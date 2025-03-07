INIT:
    when "hello" or "hi" or "Hikari" then
        respond "Hello! I am Hikari! How can I assist you?"

    when "你好" or "在吗" or "您好" or "光" then
        respond "好！我是光！需要什么助力呢？"
        transition ASSIST

    when "help" then
        respond "Sure, biolink complished. What do you need?"
        transition ASSIST

    when "帮助" then
        respond "生物链接！启动！需要什么帮助？"
        transition ASSIST

    when "damn" or "草" then
        respond "You Are Banned!给我爬！"
        transition INIT

    when "ptt" or "potential" or "潜力值" then
        respond "接下来我会根据master的提示给出回应哦~"
        transition PTT

    when "bye" or "拜拜" then
        respond "生物链接断开，回归休眠！"
        transition INIT
    
    otherwise
        respond "请使用界内文字！光是理解不了的(TAT)"
        transition INIT

ASSIST:
    when "search" or "查询" then
        respond "请问需要查询哪位玩家的potential呢？{ids}"
        transition SEARCH

    otherwise
        respond "你到底需要什么帮助？"
        transition ASSIST


SEARCH:
    when "{id}" then
        respond "玩家{id}的成绩为{id.ptt}"
        transition SEARCH

    when "quit" or "exit" or "退出" then
        respond "正在返回初始界面"
        transition INIT

    otherwise
        respond "读取信息不足，看看能帮你什么忙"
        transition ASSIST

PTT:
    when "search" or "查询" then
        respond "请问需要查询哪位玩家的potential呢？{ids}"
        transition SEARCH

    when "high" or "高" then
        respond "目前ptt最高值为13.12哟~你差得远呢"
        transition PTT

    when "low" or "低" then
        respond "目前ptt最低值为0.00哟~你差得不远呢！加油"
        transition PTT

    when "quit" or "exit" or "退出" then
        respond "正在返回初始界面"
        transition INIT

DEFAULT:
    otherwise
        respond "链接失效，尝试重连至Arcaea..."
        transition INIT