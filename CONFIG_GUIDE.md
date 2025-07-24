# ChatDev 环境配置指南

## 概述

ChatDev 现在支持通过 `.env` 配置文件来管理 API 密钥和模型配置，这使得配置管理更加方便和安全。

## 配置步骤

### 1. 安装依赖

确保安装了新的依赖：

```bash
pip install -r requirements.txt
```

### 2. 创建配置文件

复制示例配置文件并进行配置：

```bash
cp .env.example .env
```

### 3. 编辑配置文件

编辑 `.env` 文件，设置您的配置：

```bash
# 必填：OpenAI API密钥
OPENAI_API_KEY=your_actual_api_key_here

# 可选：自定义API端点（用于OpenAI兼容的API服务）
# BASE_URL=https://api.openai.com/v1

# 可选：默认模型名称
DEFAULT_MODEL=GPT_4

# 可选：模型参数配置
TEMPERATURE=0.2
TOP_P=1.0
MAX_RETRIES=5
```

## 配置选项说明

### 必填配置

- **OPENAI_API_KEY**: 您的 OpenAI API 密钥

### 可选配置

- **BASE_URL**: 自定义 API 端点，支持 OpenAI 兼容的 API 服务
- **DEFAULT_MODEL**: 默认使用的模型，支持的值：
  - `GPT_3_5_TURBO`
  - `GPT_4`
  - `GPT_4_TURBO`
  - `GPT_4O`
  - `GPT_4O_MINI`
- **TEMPERATURE**: 控制输出随机性的温度参数 (0.0-2.0)
- **TOP_P**: 控制输出多样性的 top-p 参数 (0.0-1.0)
- **MAX_RETRIES**: API 调用失败时的最大重试次数

## 使用方法

### 基本使用

配置完成后，直接运行 ChatDev：

```bash
python run.py --task "开发一个计算器应用" --name "Calculator"
```

### 覆盖配置文件设置

您仍然可以通过命令行参数覆盖配置文件中的设置：

```bash
python run.py --model GPT_4O --task "开发一个游戏" --name "Game"
```

## 兼容性

### OpenAI 兼容 API

如果您使用其他 OpenAI 兼容的 API 服务（如 Azure OpenAI、本地部署的模型等），只需在 `.env` 文件中设置 `BASE_URL`：

```bash
# 示例：Azure OpenAI
BASE_URL=https://your-resource.openai.azure.com/

# 示例：本地部署的兼容服务
BASE_URL=http://localhost:8000/v1
```

### 环境变量优先级

配置的优先级顺序：
1. 命令行参数（最高优先级）
2. `.env` 文件配置
3. 系统环境变量
4. 默认值（最低优先级）

## 安全注意事项

1. **不要提交 `.env` 文件到版本控制系统**
2. 确保 `.env` 文件的权限设置正确（仅当前用户可读）
3. 定期轮换 API 密钥
4. 在生产环境中使用环境变量而不是 `.env` 文件

## 故障排除

### 常见问题

1. **API 密钥未找到错误**
   - 确保 `.env` 文件存在且包含 `OPENAI_API_KEY`
   - 检查 API 密钥格式是否正确

2. **模型不支持错误**
   - 检查 `DEFAULT_MODEL` 的值是否在支持的模型列表中
   - 确保您的 API 密钥有权限访问指定的模型

3. **API 连接错误**
   - 检查网络连接
   - 如果使用自定义 `BASE_URL`，确保地址正确且可访问

### 调试模式

启动时会显示配置信息，帮助您确认配置是否正确：

```
Configuration loaded successfully!
Using model: GPT_4
Using custom API endpoint: https://api.openai.com/v1
```

## 迁移指南

### 从环境变量迁移

如果您之前使用系统环境变量，现在可以将它们移动到 `.env` 文件中：

```bash
# 之前的方式
export OPENAI_API_KEY="your_key"
export BASE_URL="your_url"

# 现在的方式（在 .env 文件中）
OPENAI_API_KEY=your_key
BASE_URL=your_url
```

### 批量部署

对于批量部署，您可以：
1. 创建模板 `.env` 文件
2. 使用脚本自动替换配置值
3. 或者继续使用系统环境变量（仍然支持）

## 更多信息

- 查看 `.env.example` 文件了解完整的配置选项
- 参考 `chatdev/config.py` 了解配置管理的实现细节
- 如有问题，请查看项目的 GitHub Issues 或提交新的 Issue