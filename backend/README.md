# Chat Bot DSL 语法说明文档

欢迎来到 客服机器人 DSL（领域专用语言）语法说明文档！在这里，您将学习如何使用这一灵活而强大的语言，构建属于您自己的智能客服机器人。通过本 DSL，您可以定义机器人的各种 状态机规则，从而使机器人能够根据用户的输入做出精确的反应，并引导用户完成预定的交互流程。

本 DSL 让机器人不仅仅是一个简单的对话工具，它能根据不同的用户需求和情境动态地切换状态，从 `初始问候` 到 `问题解答`，甚至可以根据用户的行为和输入调整应答策略，提供更加个性化的服务。

例如，您可以设定简单的规则，让机器人在初次对话时用亲切的问候迎接用户，在遇到特定关键字时自动转到帮助模式，甚至可以根据用户输入的数据生成定制化的反馈。每一个交互都通过精确的语法控制，确保机器人始终能够准确地理解并回应用户的需求。

DSL 语法的核心概念
    本 DSL 基于 `状态机模型`，允许您为机器人定义不同的“状态”，并为每个状态设置相应的 `条件规则` 和 `回应动作`。通过规则之间的条件判断，机器人可以实现流畅的对话逻辑和多种情境处理。而如果遇到无法识别的输入，机器人会转到默认状态，确保交互永远不至于中断。

您将学会如何使用 DSL 来：

    1.设定机器人的初始状态，定义不同的交互阶段。
    2.创建灵活的条件语句，使机器人能够识别用户输入并作出相应的回答。
    3.使用 transition 跳转到其他状态，形成完整的对话流程。
    4.处理异常和错误输入，确保机器人能够应对各种突发情况。

通过这一 DSL，您将能够使机器人具备更加 `智能化` 和 `人性化` 的对话能力，提升用户体验，让机器人真正成为您业务的一部分，助力实现高效和精准的自动化客服服务。

接下来，我们将详细介绍 DSL 的语法结构、规则定义以及如何编写功能强大的对话逻辑。

---

## **1. 语法结构**

DSL 语法由多个 `状态定义（state_definition）`和 `条件语句（conditional_statement）`组成。每个状态都包含一组条件判断和相应的操作，能够根据用户输入处理不同的情境。顶层语法结构如下：

```yaml
start: statement+
```
- **`statement`**：状态定义及其对应的表达式块，包含条件语句或默认语句。
- **`state_definition`**：表示机器人的某个具体状态（例如 `INIT`、`ASSIST`）。
- **`conditional_statement`**：用于根据用户输入进行条件匹配并执行相应的操作，包含`条件（when）`和`操作块（respond）`，并可能跳转到`其他状态（transition）`。

## **2. 状态定义与语句**
### **状态定义（state_definition）**
状态是机器人在某个时刻的具体行为或位置，通常用于标记不同的交互阶段。每个状态由状态名（例如 `INIT`、`ASSIST`）定义，后跟一个表达式块。

### **保留字状态**

DSL 中有两个特殊的状态：`INIT` 和 `DEFAULT`，它们是必需的。

- **`INIT`**：
   定义机器人初始状态，用户输入会首先匹配 `INIT` 状态中的规则。如果未定义 `transition`，会默认跳转回 `INIT` 状态。
  
- **`DEFAULT`**：
   定义当所有状态都未能处理用户输入时的默认回复。`DEFAULT` 状态仅能使用 `respond` 指令，不能定义其他规则。



```yaml
state_definition: IDENTIFIER
```
- **`IDENTIFIER`**：状态的名称，例如 `INIT`、`ASSIST`。

### **条件语句（conditional_statement）**
条件语句用于根据用户输入的条件匹配并执行相应的操作。语法如下：

```yaml
conditional_statement: "when" condition (othercons)* "then" action_block ["transition" state_transition]
```
- **`condition`**：要匹配的字符串条件，可以是多个条件通过 `or` 连接。例如 `"hello" or "hi" or "Hikari"`。
- **`othercons`**：附加条件，可以使用 `or` 连接多个条件。
- **`action_block`**：条件匹配成功后的操作块，通常是回应消息。
- **`state_transition`**（可选）：当条件匹配后，机器人可以跳转到另一个状态。
示例：

```yaml
when "hello" or "hi" or "Hikari" then respond "Hello! I am Hikari! How can I assist you?"
```
### **默认语句（default_statement）**
默认语句用于处理未匹配的情况。如果没有条件语句匹配，机器人将执行默认语句。语法如下：



```yaml
default_statement: "otherwise" action_block ["transition" state_transition]
```
- **`action_block`**：未匹配任何条件时的回应内容。
- **`state_transition`**（可选）：执行后跳转的状态。如果未定义 transition，则默认跳转到 INIT。

**注意**：  
如果一个状态未定义 `otherwise`，未匹配的输入会缺省回复 `DEFAULT` 状态中的 `response`。

示例：

```yaml
otherwise respond "链接失效，尝试重连..."
transition INIT
```

---
## **3. 完整语法定义**
```yaml
start: statement+

statement: state_definition ":" expression_block

state_definition: IDENTIFIER

expression_block: (conditional_statement | default_statement)+

conditional_statement: "when" condition (othercons)* "then" action_block ["transition" state_transition]

othercons: "or" condition

condition: STR

action_block: "respond" response

response: STR

state_transition: IDENTIFIER

default_statement: "otherwise" action_block ["transition" state_transition]
```

---

## **4. 示例说明**
以下为不同状态的 DSL 示例及其功能描述：

**4.1 初始状态 (INIT)**
   - 当用户输入包含某些特定关键词时，机器人将回复不同的内容，并根据输入跳转至相应状态。
   - 如果输入未匹配任何条件，则会执行默认回复。

```yaml
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
```

**4.2 协助状态 (ASSIST)**
   - 用户输入 `"search"` 或 `"查询"` 时，提示查询玩家潜力值。
   - 其他输入提供帮助或默认回复。

```yaml
ASSIST:
    when "search" or "查询" then
        respond "请问需要查询哪位玩家的potential呢？{ids}"
        transition SEARCH

    otherwise
        respond "你到底需要什么帮助？"
        transition ASSIST
```

**4.3 搜索状态 (SEARCH)**
   - 用户输入玩家 `ID` 时，返回玩家成绩。
   - 输入 `"quit"` 或 `"exit"` 时，返回到初始状态 `INIT`。
   - 其他情况，提供默认信息。

```yaml
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
```

**4.4 潜力值状态 (PTT)**
   - 用户查询潜力值时，提供相关信息。
   - 输入 `"quit"`、`"exit"` 或 `"退出"` 时，返回初始状态。
   - 其他情况，提供默认回复。

```yaml

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
```

**4.5 默认状态 (DEFAULT)**
   - 未能匹配任何输入时，回复默认内容。
   

```yaml
DEFAULT:
    otherwise
        respond "链接失效，尝试重连至Arcaea..."
        transition INIT
```

---
## **5. 扩展说明**
- **5.1 动态参数处理**：

    在 DSL 中，可以使用动态参数，如 `{id}`，在响应中根据实际输入填充。例如，`{id.ptt}` 会根据输入的玩家 `ID` 动态生成成绩回应。

- **5.2 状态跳转规则**：
    - 状态之间的跳转通过 `transition` 指令进行。如果某个状态未定义跳转规则，默认会跳转到 `INIT` 状态。
    - 状态之间的跳转确保了状态机的闭环，即每个输入都能引发某种响应或状态转换。
- **5.3 保留字状态机制**：
    - `INIT` 和 `DEFAULT` 是必须定义的状态。
    - `INIT` 作为起始状态，始终是用户交互的起点。
    - `DEFAULT` 用于处理未匹配的输入，确保机器人在任何情况下都能作出合理的回应。
- **5.4 错误处理和容错性**：

    通过 otherwise 和 transition 机制，机器人能够有效处理错误输入，并确保机器人状态的连续性。无论输入是否匹配任何条件，机器人始终能提供默认回应或继续引导用户进入下一状态。