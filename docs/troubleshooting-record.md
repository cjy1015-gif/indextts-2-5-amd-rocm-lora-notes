# Sanitized troubleshooting record / 脱敏排障记录

This document condenses the private engineering record into reusable failure patterns. It intentionally omits commercial-game material, speaker identities, transcripts, dataset manifests, model weights, generated audio, absolute paths, and private logs.

本文将私有工程记录压缩为可复用的故障模式，刻意省略商业游戏素材、说话人身份、台词、数据集清单、模型权重、生成音频、绝对路径和私人日志。

## Environment and dependency boundary / 环境与依赖边界

### Official inference code was mistaken for a training API

**Symptom:** inference worked, but there was no maintained training entry point, data contract, objective, or resume protocol.

**Lesson:** prove that the upstream project actually exposes training support. If not, do not invent an interface by modifying inference code. Use a separately reviewed experimental source and pin the exact commit privately.

**现象：**推理可用，但没有维护中的训练入口、数据契约、目标函数和恢复协议。

**经验：**先确认上游是否真的支持训练。没有就不要从推理代码臆造接口；应隔离审查实验性来源并私下固定源码提交。

### A small missing package attempted to replace the GPU stack

**Symptom:** installing an audio or utility package planned to pull a large NVIDIA CUDA Torch build into a ROCm environment.

**Fix:** stop dependency resolution, inspect the actual interpreter, ABI, package paths, cache, and wheel plan, then add only the compatible minimal dependency. Never exchange a verified ROCm Torch build for a convenient CUDA wheel.

**现象：**安装音频或工具包时，解析器准备把大型 NVIDIA CUDA 版 Torch 拉进 ROCm 环境。

**修复：**立即停止解析，检查真实解释器、ABI、包路径、缓存和 wheel 计划，只补兼容的最小依赖。不能为了方便安装而替换已验证的 ROCm Torch。

### TorchCodec linked against NVIDIA libraries

**Symptom:** audio decoding failed because a dynamic library expected NVIDIA CUDA components.

**Fix:** separate model computation from audio I/O and use an already compatible reader such as `soundfile`; do not install CUDA components merely to satisfy one decoder.

**现象：**音频解码因为动态库依赖 NVIDIA CUDA 组件而失败。

**修复：**把模型计算和音频 I/O 分开验收，优先使用当前环境兼容的读取器，例如 `soundfile`；不要为了一个解码器安装 CUDA 组件。

## Shell, path, and process issues / Shell、路径与进程问题

### PowerShell and Bash expanded each other's variables

**Symptom:** a command appeared to fail before Python started; variables, command substitutions, or boolean expressions were consumed by the outer shell.

**Fix:** put long logic in a script, use explicit paths, and make one shell responsible for each variable expansion. Confirm PID, log timestamp, and output creation instead of trusting the last terminal line.

**现象：**命令在 Python 启动前就失败，变量、命令替换或布尔表达式被外层 shell 提前解析。

**修复：**长逻辑写入脚本，使用明确路径，让每个变量只由一个 shell 展开。通过 PID、日志时间戳和输出文件确认运行状态，不能只看终端最后一行。

### A background WSL watcher did not remain alive

**Symptom:** a one-shot WSL invocation returned, but the intended watcher was gone.

**Fix:** launch a hidden host process that keeps the watcher in the foreground inside WSL, and verify it independently through PID, log, and checkpoint evidence.

**现象：**一次性 WSL 调用返回后，原本的守候进程已经消失。

**修复：**使用隐藏宿主进程让 WSL 内守候脚本保持前台运行，并通过 PID、日志和检查点三重确认。

### Warnings were mistaken for fatal errors

**Symptom:** messages about optional system libraries, MIOpen workspace, or text normalization triggered unnecessary reinstall attempts.

**Fix:** classify by process exit code, traceback, OOM, NaN/Inf, and actual artifacts. A warning is not a failure unless the acceptance criteria fail.

**现象：**可选系统库、MIOpen workspace 或文本 normalization 的提示导致重复重装。

**修复：**以退出码、Traceback、OOM、NaN/Inf 和实际产物分类判断。只有验收标准失败时，警告才应升级为故障。

## AMD/ROCm model adaptation / AMD/ROCm 模型适配

### NVIDIA-oriented defaults were enabled on AMD

**Symptom:** the experimental trainer assumed BF16, CUDA-only kernels, compilation, or DeepSpeed.

**Fix:** separate the ROCm device API from NVIDIA-only acceleration. Start with FP32, single GPU, no CUDA-only kernel, no compile, and no DeepSpeed. Add one optimization only after a passing baseline.

**现象：**实验训练器默认启用 BF16、CUDA 专用 kernel、编译或 DeepSpeed。

**修复：**把 ROCm 设备 API 与 NVIDIA 专用加速区分开。基线使用 FP32、单 GPU、关闭 CUDA 专用 kernel、compile 和 DeepSpeed；稳定后一次只加一个优化。

### Dtype mismatches appeared at conditioning boundaries

**Symptom:** speaker, emotion, semantic, or GPT conditioning tensors used different device/dtype combinations.

**Fix:** preserve native dtype inside each encoder and convert only at the target-layer boundary. Do not globally cast the entire model.

**现象：**说话人、情绪、语义或 GPT 条件张量的 device/dtype 不一致。

**修复：**保留各编码器内部的原生 dtype，只在目标层边界转换；不要对整个模型做粗暴全局转换。

### The inference-built model remained in eval mode

**Symptom:** LoRA dropout was silently inactive after injection.

**Fix:** explicitly switch the trainable GPT module to train mode after injection and after resume; keep frozen modules in eval mode as appropriate.

**现象：**注入 LoRA 后仍继承推理的 eval 状态，导致 dropout 静默关闭。

**修复：**注入和恢复 LoRA 后显式切换可训练 GPT 模块到 train 模式，冻结模块按需保持 eval。

## Data and objective / 数据与目标函数

### Optional auxiliary heads were enabled without base weights

**Symptom:** the base checkpoint lacked optional projection or phonetic-head parameters.

**Fix:** do not silently train random auxiliary heads. Start with the native acoustic objective and document every optional loss separately.

**现象：**基础检查点缺少可选投影层或音素头参数。

**修复：**不要静默训练随机初始化的辅助头。先使用原生声学目标，每个可选 loss 单独记录和验证。

### Manifest counts did not match the reader

**Symptom:** line counts, parsed records, valid files, and trainable samples differed.

**Fix:** count non-empty records, parse success, file existence, duration-filtered samples, and final training samples as separate fields. Lock the final manifest with a hash and verify it before launch.

**现象：**文件行数、解析记录、有效文件和训练样本数不一致。

**修复：**分别统计非空记录、解析成功数、文件存在性、时长过滤数和最终训练样本数；对最终清单做哈希锁定，启动前重新校验。

## Numerical stability / 数值稳定性

### Low-precision or optimizer combinations produced non-finite values

**Symptom:** AMP, gradient accumulation, a fused optimizer, or an aggressive attention path produced NaN/Inf.

**Fix:** reduce variables step by step; use FP32, batch size 1, AdamW, mathematical attention, real gradient clipping, and finite-value checks. Fail fast and preserve the failing configuration.

**现象：**AMP、梯度累计、融合优化器或激进注意力路径产生 NaN/Inf。

**修复：**逐项缩小变量，使用 FP32、batch size 1、AdamW、数学注意力、真实梯度裁剪和有限值检查。出现异常时立即失败并保留现场。

## Memory and resume / 内存与恢复

### Host memory approached the limit

**Symptom:** the GPU still had headroom, but system memory approached exhaustion.

**Fix:** use one process, `num_workers=0`, disable prefetch and persistent workers, disable unnecessary TensorBoard/image logging, and monitor both GPU allocation and process RSS.

**现象：**显存尚有余量，但系统内存接近耗尽。

**修复：**使用单进程、`num_workers=0`，关闭预取和常驻 worker，关闭不必要的 TensorBoard/图片日志，同时监控显存分配和进程 RSS。

### A graceful stop was confused with a kill

**Symptom:** a malformed shell command failed, while the trainer continued running.

**Fix:** never claim that training stopped until the verified PID disappears and the run result records a stop request. Send the signal to a PID obtained through a read-only check, then verify checkpoint completeness.

**现象：**停止命令因 shell 解析失败，但训练仍在继续。

**修复：**在核验 PID 消失且运行结果记录 stop request 前，不能声称训练已暂停。向只读检查得到的 PID 发送信号，再检查检查点完整性。

### Generator output was interpreted incorrectly

**Symptom:** model generation finished, but the validation script treated a generator or sampling-rate value as the audio array.

**Fix:** consume the documented return protocol, normalize it to `(sample_rate, PCM)`, then save audio. Validate model loading, generation, and file writing as separate stages.

**现象：**模型生成已完成，但验证脚本把生成器或采样率值误当成音频数组。

**修复：**完整消费返回协议，规范化为 `(sample_rate, PCM)` 后再写音频；将模型加载、生成和文件写入分开验证。

### Checkpoint choice was reduced to the last step

**Symptom:** the final checkpoint was assumed to sound best.

**Fix:** compare multiple checkpoints using objective indicators and authorized blind listening. Loss is useful for detecting divergence, but it does not replace perceptual evaluation.

**现象：**默认最后一个检查点听感最好。

**修复：**结合客观指标和获得授权的盲听比较多个检查点。loss 可用于发现发散，但不能替代听感评估。

## Reusable rule / 可复用准则

Inference, training, saving, loading, resuming, and audio writing are six separate claims. Test and record each claim independently.

推理、训练、保存、加载、恢复和音频写入是六个不同的结论，必须分别测试和记录。
