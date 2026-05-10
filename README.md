#这是一个“固定工作流的轻量级知乎心理学科普生成 Agent”。

它面向知乎心理学科普文章场景，能够自动完成：

用户输入题材
→ 自动搜索资料
→ 自动生成大纲
→ 自动写初稿
→ 自动润色
→ 流式返回文章结果

#整个链路支持实时执行状态反馈和流式内容输出。

#项目采用前后端分离架构。
并且支持实时展示 Agent 当前执行步骤。

#采用技术栈：
前端：React+Vite
后端：FastAPI+langchain
流式响应：SSE
搜索工具：DuckDuckGOSearch
整体Agent架构：Agent固定流程编排

#开发思路：迭代开发。
先跑通各个too，然后组合实现后台流式输出，最后结合前端实现前端流式输出。

#效果展示：
<img width="1001" height="875" alt="微信图片_20260509184905_556_28" src="https://github.com/user-attachments/assets/451b100e-25ac-4cd6-a5ae-4d5df8ddebf1" />
<img width="954" height="498" alt="微信图片_20260509184824_555_28" src="https://github.com/user-attachments/assets/d30b6a08-fc05-49f3-9ffe-d00148c9f93c" />
<img width="1046" height="438" alt="微信图片_20260509184810_554_28" src="https://github.com/user-attachments/assets/02355402-90ea-43e7-a40f-4633fc10719d" />
