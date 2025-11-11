# Dify 医疗AI客户端

一个Python客户端，用于调用Dify医疗AI工作流API，支持对话、文件上传、流式响应等功能。

## 功能特性

- 🏥 医疗AI对话功能
- 📁 医学文件上传（PDF、DOCX、PNG、JPG等）
- ⚡ 流式响应支持（实时打字机效果）
- 🔗 会话连续性管理
- 📊 详细的错误处理和日志
- 🛡️ 完整的API密钥认证

## 使用方法

### 1. 基本配置

在 `dify_medical_client.py` 文件中配置你的Dify医疗AI API信息：

```python
BASE_URL = "http://192.168.1.102/v1"  # 你的Dify医疗AI服务器地址
API_KEY = "your-api-key-here"  # 请替换为你的实际API密钥
```

### 2. 运行客户端

```bash
python dify_medical_client.py
```

### 3. 使用方式

#### 方式1: 简单对话
```python
from dify_medical_client import DifyMedicalClient

client = DifyMedicalClient("http://192.168.1.127/v1", "your-api-key-here")
response = client.send_message("高血压患者需要注意什么？")
print(response["answer"])
```

#### 方式2: 上传文件并分析
```python
from dify_medical_client import DifyMedicalClient

client = DifyMedicalClient("http://192.168.1.127/v1", "your-api-key-here")

# 上传文件并分析
response = client.chat_with_files(
    file_paths=["病历.pdf", "检查报告.docx"],
    query="请分析这些医疗文件中的患者症状"
)
```

#### 方式3: 交互式聊天
直接运行脚本即可进入交互式聊天模式：
```bash
python dify_medical_client.py
```

交互式聊天支持以下命令：
- 直接输入问题进行对话
- 输入 `upload 文件路径1,文件路径2` 上传文件并分析

### 4. API接口

客户端支持以下核心API接口：

#### 发送对话消息
- **端点**: `POST /chat-messages`
- **参数**:
  - `query`: 用户提问（如 "高血压用药注意事项"）
  - `user`: 唯一用户ID（如 "patient_001"）
  - `conversation_id`: 会话ID（保持对话连续性）
  - `files`: 医学文件列表
  - `response_mode`: 响应模式（"blocking" 或 "streaming"）

#### 上传文件
- **端点**: `POST /files/upload`
- **参数**:
  - `file`: 本地文件（支持PDF/PNG/DOCX等）
  - `user`: 用户ID（需与发送消息的user一致）

#### 文件预览
- **端点**: `GET /files/:file_id/preview`
- **参数**: `file_id`: 上传文件返回的唯一ID

## 响应模式

### 阻塞模式 (blocking)
- 等待全量结果返回
- 100秒超时限制
- 适合后台处理场景

### 流式模式 (streaming)
- 实时返回文本块（类似打字机效果）
- 更好的用户体验
- 推荐用于实时对话

## 支持的文件类型

- 📄 文档：PDF、DOCX、TXT
- 🏥 影像：PNG、JPG（医学影像如CT、MRI）
- 🎵 音频：MP3、WAV（患者录音）
- 📊 表格：XLSX、CSV

## 错误处理

客户端包含完善的错误处理：
- HTTP错误（400、401、404、500等）
- 网络请求错误
- JSON解析错误
- 文件上传错误
- 流式响应错误

## 安全最佳实践

1. **API密钥保护**：
   - 仅在后端服务中存储密钥
   - 定期轮换API密钥（建议每3个月一次）
   - 严禁将密钥存储在前端代码中

2. **网络安全**：
   - 生产环境使用HTTPS传输
   - 配置IP白名单限制访问来源

3. **权限管控**：
   - 为不同角色分配不同权限的API密钥
   - 监控异常请求并及时处理

## 依赖说明

此客户端使用Python内置库，无需安装额外依赖：
- `urllib` - HTTP请求处理
- `json` - JSON数据处理
- `os` - 文件操作
- `typing` - 类型提示

## 常见问题

### Q: 如何获取API密钥？
A: 登录Dify控制台，进入"医疗AI"应用的「工具」-「访问API」页面生成。

### Q: 文件上传失败怎么办？
A: 检查文件格式是否支持，文件大小是否超出限制，网络连接是否正常。

### Q: 如何保持对话连续性？
A: 客户端会自动保存和传递conversation_id，确保在同一会话中进行连续对话。

### Q: 流式响应卡顿怎么办？
A: 检查网络连接，或改用blocking模式进行测试。

## 示例用法

```python
# 创建客户端
client = DifyMedicalClient("http://192.168.1.127/v1", "your-api-key")

# 简单对话
response = client.send_message("什么是高血压？")
print(response["answer"])

# 上传病历并分析
response = client.chat_with_files(
    file_paths=["patient_record.pdf"],
    query="请分析这份病历中的主要症状和建议"
)

# 连续对话
response1 = client.send_message("患者有高血压病史")
response2 = client.send_message("需要做什么检查？")  # 自动使用同一会话
