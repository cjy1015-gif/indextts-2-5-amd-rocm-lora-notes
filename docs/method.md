# Method notes / 方法说明

## 1. Establish the real baseline / 先确认真实基线

Inference success is not training success. Before changing code, record the actual Python executable, Python version, Torch version, HIP/ROCm information, visible GPU, working directory, `PYTHONPATH`, and available memory.

推理成功不等于训练成功。修改代码前，先记录真实 Python 可执行文件、Python 版本、Torch 版本、HIP/ROCm 信息、可见 GPU、工作目录、`PYTHONPATH` 和可用内存。

The official inference repository should not be treated as a training API unless a maintained training entry point, objective, data contract, and checkpoint protocol are actually present. If those are absent, use a separately reviewed experimental source and pin its commit.

如果官方推理仓库没有明确维护的训练入口、目标函数、数据契约和检查点协议，就不能把它当作训练 API。需要实验时，应隔离审查第三方来源并固定源码提交。

## 2. AMD/ROCm compatibility boundary / AMD/ROCm 兼容边界

ROCm PyTorch commonly exposes the device through the unified `torch.cuda` API. That API name alone does not mean that NVIDIA CUDA is being used. The important boundary is the installed wheel and the runtime libraries.

ROCm 版 PyTorch 通常仍通过统一的 `torch.cuda` API 暴露设备。API 名称本身不代表使用 NVIDIA CUDA，真正需要确认的是已安装的 wheel 和运行时库。

For a first stable pass:

- use FP32;
- disable CUDA-only kernels, DeepSpeed, compile, and unverified acceleration;
- keep single-GPU execution;
- set a conservative process memory fraction;
- keep CPU thread count bounded;
- use an audio reader already compatible with the environment.

第一次稳定实验建议：

- 使用 FP32；
- 关闭 CUDA 专用 kernel、DeepSpeed、compile 和未经验证的加速；
- 使用单 GPU；
- 设置保守的进程显存上限；
- 限制 CPU 线程数；
- 使用当前环境已经兼容的音频读取器。

## 3. Minimize the trainable surface / 缩小可训练范围

Freeze semantic encoders, codec, speaker encoders, vocoders, and other non-target modules. Inject LoRA only into the autoregressive GPT Transformer, for example the attention and feed-forward projection families used by the selected implementation.

冻结语义编码器、codec、说话人编码器、声码器和其他非目标模块。LoRA 只注入自回归 GPT Transformer，例如所选实现中的注意力和前馈投影模块。

Do not enable auxiliary heads merely because the training code supports them. If the base checkpoint does not contain those heads, enabling them may train randomly initialized parameters and add an unverified loss path. Start with the native acoustic objective, then add one auxiliary objective at a time only after independent validation.

不要因为训练代码支持辅助头就默认启用。如果基础检查点不包含这些头，启用后可能会训练随机初始化参数，并引入未经验证的损失路径。先使用原生声学目标，完成独立验证后再一次只增加一个辅助目标。

## 4. Dtype boundaries / dtype 边界

Avoid a global `.half()` or `.bfloat16()` conversion. Preserve each encoder's native dtype, and convert only at the boundary where a conditioning tensor enters a target layer. Compute cross-entropy from floating-point logits and fail fast on non-finite loss or gradients.

避免全局 `.half()` 或 `.bfloat16()`。保留各编码器的原生 dtype，只在条件张量进入目标层的边界处转换。交叉熵使用浮点 logits 计算，并在 loss 或梯度出现非有限值时立即失败。

## 5. Checkpoint protocol / 检查点协议

An interruption-safe checkpoint should include:

- adapter weights and configuration;
- optimizer state;
- scheduler state;
- completed optimizer step;
- a configuration snapshot;
- a data-manifest hash;
- a structured run result.

可安全中断的检查点应包含：

- 适配器权重和配置；
- 优化器状态；
- 调度器状态；
- 已完成的优化器步数；
- 配置快照；
- 数据清单哈希；
- 结构化运行结果。

Write to a temporary location and atomically rename only after all required files are complete. A signal handler should set a stop event; the training loop should save at a safe optimizer boundary. Do not treat a process kill, WSL shutdown, or power loss as a graceful pause.

先写入临时位置，所有必需文件完成后再原子改名。信号处理器只设置停止事件，训练循环在安全的优化器边界保存。强制杀进程、关闭 WSL 或断电都不能视为安全暂停。

## 6. Acceptance criteria / 验收标准

Declare an experiment technically valid only when all of these pass:

1. one or more optimizer updates completed;
2. LoRA tensors are finite and show non-zero updates;
3. a fresh process can load the adapter;
4. optimizer and scheduler state can be restored;
5. an authorized validation input produces a decodable, non-silent artifact;
6. the result is recorded without exposing source data or private paths.

只有以下条件全部通过，才可宣布工程链路有效：

1. 至少完成一次优化器更新；
2. LoRA 张量均为有限值并产生非零更新；
3. 新进程可以加载适配器；
4. 优化器和调度器状态可以恢复；
5. 使用获得授权的验证输入生成可解码、非静音的产物；
6. 记录结果时不暴露源数据和私人路径。
