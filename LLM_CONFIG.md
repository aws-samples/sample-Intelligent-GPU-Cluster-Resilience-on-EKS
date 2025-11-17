# LLM 配置说明

本项目支持两种 LLM 提供商：Amazon Bedrock 和 SageMaker Endpoint。

## 配置方式

通过环境变量配置，无需修改代码：

### 使用 Amazon Bedrock（默认）

```bash
export LLM_PROVIDER=bedrock
export BEDROCK_MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0
```

### 使用 SageMaker Endpoint

```bash
export LLM_PROVIDER=sagemaker
export SAGEMAKER_ENDPOINT_NAME=your-endpoint-name
```

## 环境变量说明

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `LLM_PROVIDER` | LLM 提供商：`bedrock` 或 `sagemaker` | `bedrock` | 否 |
| `BEDROCK_MODEL_ID` | Bedrock 模型 ID | `us.anthropic.claude-3-7-sonnet-20250219-v1:0` | 使用 Bedrock 时可选 |
| `SAGEMAKER_ENDPOINT_NAME` | SageMaker Endpoint 名称 | 无 | 使用 SageMaker 时必填 |

## 测试配置

```bash
# 测试 SageMaker
export LLM_PROVIDER=sagemaker
export SAGEMAKER_ENDPOINT_NAME=hf-llm-mistral-small-24b-instruct-2501-2025-11-04-03-00-57-671
python3 lib/metrics_processor_llm.py

# 测试 Bedrock
export LLM_PROVIDER=bedrock
python3 lib/metrics_processor_llm.py
```

## SageMaker Endpoint 要求

SageMaker endpoint 需要支持以下输入格式：

```json
{
  "inputs": "<prompt text>",
  "parameters": {
    "max_new_tokens": 512,
    "temperature": 0.1,
    "return_full_text": false
  }
}
```

输出格式应为：
```json
[{"generated_text": "<response>"}]
```
或
```json
{"generated_text": "<response>"}
```
