# Todo List AI Server

基于 Python FastAPI 的 Web 服务。

## 环境准备

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 配置 OpenAI

```powershell
$env:OPENAI_API_KEY="你的 OpenAI API Key"
$env:OPENAI_MODEL="你的模型名称"
$env:OPENAI_BASE_URL="https://api.xxx.com/v1"
```

## 启动服务

```powershell
uvicorn app.main:app --reload
```

启动后访问：

- API: http://127.0.0.1:8000
- 健康检查: http://127.0.0.1:8000/health
- Swagger 文档: http://127.0.0.1:8000/docs
- ReDoc 文档: http://127.0.0.1:8000/redoc

## 初始化待办接口

```powershell
curl.exe -X POST http://127.0.0.1:8000/init_from_llm `
  -H "Content-Type: application/json" `
  -d "{\"content\":\"明天上午整理周报，下午和客户开会\"}"
```

响应示例：

```json
["整理周报", "和客户开会"]
```
