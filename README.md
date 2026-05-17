# 这是一个“固定工作流的轻量级知乎心理学科普生成 Agent”。

它面向知乎心理学科普文章场景，能够自动完成：

用户输入题材
→ 自动搜索资料
→ 自动生成大纲
→ 自动写初稿
→ 自动润色
→ 流式返回文章结果

# 整个链路支持实时执行状态反馈和流式内容输出。

# 项目采用前后端分离架构。
并且支持实时展示 Agent 当前执行步骤。

# 采用技术栈：
前端：React+Vite

后端：FastAPI+langchain

流式响应：SSE

搜索工具：DuckDuckGOSearch

整体Agent架构：Agent固定流程编排

# 开发思路：迭代开发。
先跑通各个tool，然后组合实现后台流式输出，最后结合前端实现前端流式输出。

# 详细开发日志参考上面的知乎写作助手开发日志.md

# 效果展示：
<img width="1046" height="438" alt="微信图片_20260509184810_554_28" src="https://github.com/user-attachments/assets/9e8cbf49-825e-42d0-9268-7ef3bf332854" />
------------
<img width="954" height="498" alt="微信图片_20260509184824_555_28" src="https://github.com/user-attachments/assets/c08e3f57-ca16-4689-993f-e4c96907d2d5" />
----------------
<img width="1001" height="875" alt="微信图片_20260509184905_556_28" src="https://github.com/user-attachments/assets/0b4a188d-dec4-43c9-836c-2a5ccf121995" />



