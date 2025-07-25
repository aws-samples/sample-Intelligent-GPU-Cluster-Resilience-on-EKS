# sample-Intelligent-GPU-Cluster-Resilience-on-EKS


## Overview

A GPU cluster resilience solution built on EKS that continuously collects monitoring information through DCGM DaemonSet, utilizes Claude 3.7 for log analysis and classification, and implements automatic task recovery through Kubeflow. It can also integrate notification and alerting mechanisms as needed.

## System Architecture

### 1. AWS Infrastructure
- **EKS Cluster**: Managed Kubernetes cluster for running GPU workloads
- **CloudWatch**: Metrics collection and log management
- **Amazon Bedrock Claude 3.7**: LLM intelligent analysis service
- **FSx for Lustre**: High-speed shared file storage
- **(Optional) Lambda Functions**: Cloud-based error handling logic
- **(Optional) SNS**: Notification service


### 2. GPU Monitoring
- **DCGM Server Pods**: Node DaemonSet providing GPU metrics and error logs
- **DCGM Monitor**: Main monitoring script that periodically collects and analyzes GPU metrics
- **LLM Metrics Processor**: Uses Bedrock Claude to analyze and classify error types, avoiding complex regex matching
- **Exclusion Manager**: Prevents duplicate processing of the same failed node
- **GPU Utils**: Retrieves node information and DCGM Server Pod metrics

### 3. Error Detection and Classification Layer
The system can intelligently identify and classify the following GPU error types:
- **XID_CRITICAL_<xid_code>**: Critical GPU errors requiring immediate instance replacement
- **XID_WARNING_<xid_code>**: GPU warnings that need monitoring but may not require immediate action
- **ECC_ERROR**: GPU ECC memory errors
- **GPU_HEALTH_WARNING/ERROR**: Overall GPU health status anomalies
- **HEALTHY**: Normal GPU status

### 4. Fault Handling Layer
Executes corresponding recovery strategies based on error types:
- **Node Isolation (Cordon)**: Prevents new Pods from being scheduled to failed nodes
- **Pod Eviction (Drain)**: Safely migrates Pods to other nodes
- **Instance Reboot**: Reboots for recoverable errors
- **Instance Replacement**: Replaces instances for severe hardware failures
- **Recovery from Isolation (UnCordon)**: Restores scheduling to repaired nodes

### 5. Notification and Feedback
- **SNS Topic Notifications**: (Template) Can send structured notification messages
- **Webhook Notifications**: (Template) Can integrate with third-party notification systems
- **CloudWatch Metrics**: Records anomaly information by node and error type, configurable alerts


## Monitoring and Processing Flow

```mermaid
flowchart TD
    A[Start Monitoring] --> A1{Check Instance Exclusion List}
    subgraph Anomaly Monitoring
    A1 --> |Excluded (Processing)| B0[Continue Monitoring and Logging]
    A1 --> |Not in Exclusion List| B[Collect Monitoring Metrics from DCGM Server]
    B --> C{LLM Log Analysis (Custom Anomaly Classification)}
    end
    
    C -->|HEALTHY| F[Continue Monitoring and Logging]
    
    C -->|OTHERS| G{Is it a Critical Error?}
    G -->|No| H[Report to CloudWatch + Continue Monitoring]
        
    G -->|Yes| L[Report to CloudWatch + Execute Handling Strategy]
    subgraph Fault Handling
    L --> O[Node Isolation]
    O --> P[Pod Eviction]
    
    P --> Q{Need Replacement?}
    Q -->|Yes| R[Instance Replacement]
    Q -->|No| S[Instance Reboot]
    end

    R --> A
    S --> A

    style Anomaly Monitoring font-size:16px,font-weight:bold
    style Fault Handling fill:#ffcccc,stroke:#ff0000,stroke-width:2px,color:#333,font-size:16px,font-weight:bold
```


## Configuration and Deployment

### Deployment Steps
1. Configure DCGM DaemonSet on existing EKS cluster
2. Deploy the sample solution to EC2 or Fargate

### Monitoring Metrics (Customizable)
- GPU ECC error count
- GPU XID error count and types
- GPU health status

### Environment Variables
```bash
export MONITOR_INTERVAL=300         # Monitoring interval (seconds)
export LOG_LEVEL=DEBUG              # Log level
export WEBHOOK_URL=<webhook_url>    # Webhook notification URL
export LAMBDA_FUNCTION=<func_name>  # Lambda function name
export SNS_TOPIC_ARN=<topic_arn>    # SNS topic ARN
```

## File Structure

```
250701-eks-gpu-cluster-resilience/
├── dcgm-monitor-modular.py          # Main monitoring script
├── gpu_monitor_exclusions.json     # Exclusion list file
├── test-handlers.py                 # Test script
└── lib/
    ├── exclusion_manager.py         # Exclusion manager
    ├── metrics_processor_llm.py     # LLM metrics processor
    ├── gpu-utils.sh                 # GPU utilities library
    └── handlers/
        ├── error_dispatch.py        # Error dispatcher
        ├── lambda-gpu-error-handler.py  # Lambda handler
        ├── sns_handler.py           # SNS handler
        ├── webhook-receiver.py      # Webhook receiver
        ├── gpu-instance-reboot.sh   # Instance reboot script
        └── gpu-instance-replace.sh  # Instance replacement script
```

## Use Cases

1. **Production GPU Cluster Monitoring**: 24/7 monitoring of GPU health status
2. **Automatic Fault Recovery**: Unattended fault handling
3. **Cost Optimization**: No need to provision standby instances
4. **Flexibility**: Easy customization of fault classification without writing regex log parsing, enabling rapid corresponding processing


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
