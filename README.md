# 🎬 视频脚本生成器

基于阿里云百炼 API 的 AI 视频脚本生成工具，输入主题即可一键生成高质量短视频脚本！

---

## ✨ 功能特性

- 🤖 **智能生成**：基于通义千问大模型，生成专业视频脚本
- 🎯 **一键生成**：输入主题，即刻获得完整脚本（标题+正文）
- 📱 **友好界面**：使用 Streamlit 打造的精美 Web 界面
- ⚙️ **参数可调**：支持调节视频时长和创造力指数
- 🌐 **多平台支持**：Windows、macOS、Linux 均可运行

---

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 编程语言 |
| Streamlit | 1.31+ | Web 框架 |
| LangChain | 0.1+ | LLM 应用开发框架 |
| 阿里云百炼 | - | 大模型服务 |
| 通义千问 | qwen-plus | AI 模型 |

---

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/your-username/video-script-generator.git
cd video-script-generator
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 获取 API 密钥

1. 访问 [阿里云百炼控制台](https://dashscope.console.aliyuncs.com/)
2. 注册/登录阿里云账号
3. 创建 API 密钥（AccessKey）

---

## 🚀 启动方式

### 方式一：使用启动脚本（推荐）

```bash
# Windows
start.bat

# macOS/Linux
bash start.sh
```

### 方式二：手动启动

```bash
streamlit run main.py --server.headless true
```

### 方式三：开发模式

```bash
streamlit run main.py
```

---

## 📖 使用说明

1. 在侧边栏输入你的 **阿里云百炼 API 密钥**
2. 输入视频主题（例如：AI绘画、Python教程、科技热点）
3. 设置视频时长（0.1-10分钟）
4. 调节创造力指数（0=严谨专业，1=放飞自我）
5. 点击「生成脚本」按钮
6. 等待 AI 生成脚本，查看结果

---

## 📁 项目结构

```
video-script-generator/
├── main.py              # Streamlit 主应用
├── utills.py            # 脚本生成核心逻辑
├── requirements.txt     # 项目依赖
├── start.bat            # Windows 启动脚本
├── start.sh             # macOS/Linux 启动脚本
├── .gitignore           # Git 忽略文件
└── README.md            # 项目说明文档
```

---

## 📝 核心代码

### 脚本生成逻辑

```python
def generate_script(subject, video_length, creativity, api_key):
    # 使用通义千问模型
    model = ChatOpenAI(
        openai_api_key=api_key,
        temperature=creativity,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus"
    )
    
    # 生成标题和脚本...
    return search_result, title, script
```

### 提示词设计

- **标题生成**：为主题生成吸引人的视频标题
- **脚本生成**：按照「开头、中间、结尾」结构生成完整脚本
- **风格要求**：轻松有趣，适合年轻人，开头抓眼球，结尾留钩子

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交代码：`git commit -m "feat: add your feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

---

## 📄 许可证

MIT License
---

*Made with ❤️ by your-name*
