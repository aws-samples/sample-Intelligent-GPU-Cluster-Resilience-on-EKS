#!/usr/bin/env python3
"""部署 SageMaker 端点用于 GPU 监控"""

import argparse
from sagemaker.jumpstart.model import JumpStartModel
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer


def deploy_endpoint(
    model_id: str = "huggingface-llm-mistral-small-24B-Instruct-2501",
    model_version: str = "2.0.1",
    instance_type: str = "ml.g5.12xlarge",
    instance_count: int = 1,
    endpoint_name: str = None
):
    """部署 SageMaker JumpStart 模型端点
    
    Args:
        model_id: JumpStart 模型 ID
        model_version: 模型版本
        instance_type: 实例类型
        instance_count: 实例数量
        endpoint_name: 端点名称（可选）
    """
    print(f"正在部署模型: {model_id} v{model_version}")
    print(f"实例类型: {instance_type}")
    print(f"实例数量: {instance_count}")
    
    model = JumpStartModel(
        model_id=model_id,
        model_version=model_version
    )
    
    predictor = model.deploy(
        accept_eula=True,
        initial_instance_count=instance_count,
        instance_type=instance_type,
        endpoint_name=endpoint_name,
        serializer=JSONSerializer(),
        deserializer=JSONDeserializer()
    )
    
    print(f"\n✓ 端点部署成功!")
    print(f"端点名称: {predictor.endpoint_name}")
    print(f"\n配置到 config/models.yaml:")
    print(f"""
sagemaker_custom:
  provider: sagemaker
  endpoint_name: {predictor.endpoint_name}
  region: {predictor.sagemaker_session.boto_region_name}
  temperature: 0.1
  max_tokens: 2048
""")
    
    return predictor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="部署 SageMaker 端点")
    parser.add_argument("--model-id", default="huggingface-llm-mistral-small-24B-Instruct-2501")
    parser.add_argument("--model-version", default="2.0.1")
    parser.add_argument("--instance-type", default="ml.g5.12xlarge")
    parser.add_argument("--instance-count", type=int, default=1)
    parser.add_argument("--endpoint-name", default=None)
    
    args = parser.parse_args()
    
    deploy_endpoint(
        model_id=args.model_id,
        model_version=args.model_version,
        instance_type=args.instance_type,
        instance_count=args.instance_count,
        endpoint_name=args.endpoint_name
    )
