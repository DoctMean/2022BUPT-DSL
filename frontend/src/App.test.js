import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "./App";
import axios from "axios";

// 模拟 axios 的 post 方法
jest.mock("axios", () => ({
  post: jest.fn(),
}));

describe("App 组件", () => {
  beforeEach(() => {
    // 在每个测试之前重置 axios mock，确保每个测试是独立的
    axios.post.mockReset();
  });
  
  // 测试：渲染 Chat 组件并检查是否包含正确的标题
  it("渲染 Chat 组件并显示导航栏标题", () => {
    render(<App />);
    // 检查页面中是否包含 "Arcaea Ambassador" 文本
    expect(screen.getByText("Arcaea Ambassador")).toBeInTheDocument();
  });

  // 测试：用户发送消息并显示该消息
  it("发送用户消息并显示该消息", async () => {
    render(<App />);

    // 获取输入框和发送按钮
    const input = screen.getByRole("textbox");

    // 在输入框中输入消息并点击发送按钮
    fireEvent.change(input, { target: { value: "Hello" } });
    fireEvent.click(await screen.findByRole("button"));

    // 检查是否显示用户发送的消息
    expect(screen.getByText("Hello")).toBeInTheDocument();
  });

  // 测试：发送消息后，显示打字指示和机器人回复
  it("显示机器人回复", async () => {
    const mockReply = "你好，我是Hikari~";
    // 模拟接口返回数据
    axios.post.mockResolvedValueOnce({ data: { reply: mockReply } });

    render(<App />);

    // 等待机器人回复并检查其是否显示
    await waitFor(() => expect(screen.getByText(mockReply)).toBeInTheDocument());
  });

  // 测试：处理机器人无法回复的错误情况
  it("处理机器人无法回复的错误", async () => {
    // 模拟接口返回错误
    axios.post.mockRejectedValueOnce(new Error("Network error"));
    
    render(<App />);

    // 获取输入框和发送按钮
    const input = screen.getByRole("textbox");

    // 在输入框中输入消息并点击发送按钮
    fireEvent.change(input, { target: { value: "?" } });
    fireEvent.click(await screen.getByRole("button"));

    // 等待错误信息并检查是否显示
    jest.setTimeout(async () => {
      const errorMessage = await screen.queryByText(/光在睡觉/i);
      expect(errorMessage).toBeInTheDocument();
    }, 10000);
  });
});
