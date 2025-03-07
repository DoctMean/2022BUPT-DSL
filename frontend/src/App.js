import React, { useEffect } from "react";
import Chat, { Bubble, useMessages } from "@chatui/core";

import '@chatui/core/dist/index.css';
import './chatui-theme.css'; // 引入自定义主题样式

import imgUrl from './Hikari.png'; // 用户头像图片
import axios from "axios";

// 配置常量
const API_URL = "http://localhost:8000/chat"; // 后端API地址

export default function App() {
  // 使用 ChatUI 的 hook 来管理消息状态
  const { messages, appendMsg, setTyping } = useMessages([{
    type: 'text',
    content: { text: '你好，我是Hikari~' }, // 初始机器人问候消息
    user: {
      name: '光',
      avatar: imgUrl,
    },
  }]);

  // 发送消息
  async function handleSend(type, value) {
    if (type === "text" && value.trim()) {
      // 只有当消息类型是文本且用户输入不为空时，才会发送消息
      appendMsg({
        type: "text",
        content: { text: value },
        position: "right", // 用户消息显示在右边
      });

      try {
        // 向后端发送请求，获取机器人的回复
        const response = await axios.post(API_URL, { text: value });
        const reply = response.data.reply;

        // 机器人回复
        appendMsg({
          type: "text",
          content: { text: reply },
          user: {
            name: '光',
            avatar: imgUrl,
          },
        });
      } catch (error) {
        // 如果发生错误（如网络问题等），机器人发送错误提示消息
        console.error("Error Report:", error);
        appendMsg({
          type: "text",
          content: { text: "\"光在睡觉，不要打扰她比较好...\"" },
          user: {
            name: '光',
            avatar: imgUrl,
          },
        });
      }
    }
  }

  // 渲染消息内容
  function renderMessageContent(msg) {
    // 使用 ChatUI 的 Bubble 组件来渲染消息文本
    return <Bubble content={msg.content.text} />;
  }

  // 清理副作用，避免在组件卸载时发送消息
  useEffect(() => {
    return () => {
      setTyping(false);
    };
  }, [setTyping]);

  return (
    <Chat
      navbar={{ title: "Arcaea Ambassador" }} // 设置聊天顶部的标题
      messages={messages} // 当前的聊天消息列表
      renderMessageContent={renderMessageContent} // 渲染消息内容的函数
      onSend={handleSend} // 发送消息时的处理函数
    />
  );
}
