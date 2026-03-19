# AI Capability Service

一个最小可运行的后端服务，用统一接口封装不同的 AI capability。  
当前以 mock 方式实现 `text_summary` 和 `text_stats`，重点体现统一接口、能力分发、统一错误结构、输入校验，以及 `request_id` / `elapsed_ms` 这些工程化细节。

## 功能概览

- 统一入口：`POST /v1/capabilities/run`
- 已支持 capability：
  - `text_summary`
  - `text_stats`
- 健康检查：`GET /health`
- 统一成功/失败响应结构
- 统一错误处理
- 自动生成或透传 `request_id`
- 返回请求耗时 `elapsed_ms`

## 运行环境

- Python 3.11+

## 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 启动服务

```bash
python -m uvicorn app.main:app --reload
```

启动后默认访问地址：

- `http://127.0.0.1:8000`

## 示例请求

### health

```bash
curl http://127.0.0.1:8000/health
```

### text_summary

```bash
curl -X POST "http://127.0.0.1:8000/v1/capabilities/run" ^
  -H "Content-Type: application/json" ^
  -d "{\"capability\":\"text_summary\",\"input\":{\"text\":\"Long text content for summary demo.\",\"max_length\":20},\"request_id\":\"demo-req-1\"}"
```

成功响应示例：

```json
{
  "ok": true,
  "data": {
    "result": "Long text content fo..."
  },
  "meta": {
    "request_id": "demo-req-1",
    "capability": "text_summary",
    "elapsed_ms": 1
  }
}
```

### text_stats

```bash
curl -X POST "http://127.0.0.1:8000/v1/capabilities/run" ^
  -H "Content-Type: application/json" ^
  -d "{\"capability\":\"text_stats\",\"input\":{\"text\":\"hello world\nsecond line\"}}"
```

## 接口说明

### POST /v1/capabilities/run

请求体：

```json
{
  "capability": "text_summary",
  "input": {
    "text": "Long text content...",
    "max_length": 120
  },
  "request_id": "optional-id"
}
```

说明：

- `capability`: 要执行的能力名称
- `input`: 对应 capability 的输入参数
- `request_id`: 可选，客户端可自定义；未传时服务端自动生成 UUID

### 已实现 capability

#### text_summary

输入：

- `text`: 待摘要文本，必须为非空字符串
- `max_length`: 最大摘要长度，正整数，默认 `120`

行为：

- 压缩多余空白和换行
- 文本长度未超过 `max_length` 时直接返回
- 超过时截断并追加 `...`

#### text_stats

输入：

- `text`: 待统计文本，必须为非空字符串

输出：

- `char_count`
- `word_count`
- `line_count`

## 测试

```bash
python -m pytest .\tests
```

## 后续可扩展方向

- 增加更多 capability 模块并注册到 dispatcher
- 接入真实模型 provider
- 增加环境变量配置和更细粒度日志
