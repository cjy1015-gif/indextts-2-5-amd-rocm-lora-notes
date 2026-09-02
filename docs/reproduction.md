# Reproduction guide / 复现指南

This is a methods guide, not a turnkey model package. Bring your own authorized model installation, audio, text, and isolated runtime.

本指南只描述方法，不是开箱即用的模型包。请自行准备获得授权的模型安装、音频、文本和隔离运行环境。

## Before starting / 开始前

- Use Linux or WSL2 only if the selected ROCm/PyTorch combination supports the target GPU.
- Confirm the interpreter and package search path from the same shell that will launch training.
- Verify GPU visibility with a tiny tensor allocation before loading the TTS model.
- Check that the audio reader does not pull an incompatible NVIDIA CUDA dependency.
- Keep the dataset manifest, model output, and evaluation output outside the public repository.

- 只有在目标 ROCm/PyTorch 组合支持显卡时，才使用 Linux 或 WSL2。
- 在实际启动训练的同一个 shell 中确认解释器和包搜索路径。
- 加载 TTS 模型前，先用最小张量分配验证 GPU 可见性。
- 确认音频读取器不会拉入不兼容的 NVIDIA CUDA 依赖。
- 数据清单、模型输出和评估输出都应放在公开仓库之外。

## Staged workflow / 分阶段流程

### Stage A: environment probe / 阶段 A：环境探针

Run `scripts/environment_check.sh` and save its output privately. Review the interpreter path, Torch backend, HIP version, GPU name, and memory before any installation.

运行 `scripts/environment_check.sh`，但只私下保存输出。在安装任何依赖前，检查解释器路径、Torch 后端、HIP 版本、GPU 名称和内存。

### Stage B: one-step smoke test / 阶段 B：单步冒烟

Use batch size 1, FP32, a very small LoRA rank, and one optimizer update. Confirm forward, backward, clipping, optimizer update, adapter save, and fresh-process reload. Do not infer success from a zero exit code alone.

使用 batch size 1、FP32、很小的 LoRA rank 和一次优化器更新。确认前向、反向、裁剪、优化器更新、适配器保存和新进程加载。不能只根据退出码为 0 判断成功。

### Stage C: short stability run / 阶段 C：短时稳定性

Run a short authorized-data trial and monitor loss finiteness, gradient norms, GPU allocation, process RSS, and checkpoint completeness. If any value becomes non-finite, stop and preserve the failing batch and configuration privately.

使用获得授权的数据进行短时试跑，监控 loss 有限性、梯度范数、显存分配、进程 RSS 和检查点完整性。如果出现非有限值，停止并私下保留失败批次和配置。

### Stage D: interruption and resume / 阶段 D：中断与恢复

Test a graceful SIGINT/SIGTERM at a known checkpoint. Verify that the process exits at a safe optimizer boundary, the checkpoint files are complete, and the next process restores step, optimizer, scheduler, and data cursor. Never use a machine shutdown as this test.

在已知检查点进行一次安全 SIGINT/SIGTERM 测试。验证进程在安全优化器边界退出、检查点文件完整，并且下一进程能够恢复步数、优化器、调度器和数据游标。不要用关机代替这个测试。

### Stage E: final validation / 阶段 E：最终验收

Use `scripts/finite_check.py` on private checkpoint paths. Then load the adapter in a fresh process and run an authorized validation input. Keep generated audio and logs private.

对私有检查点路径运行 `scripts/finite_check.py`。然后在新进程加载适配器并使用获得授权的验证输入。生成音频和日志继续保持私有。

## Suggested experiment log / 建议实验日志

Record the following without source text, audio, usernames, or absolute paths:

记录以下信息，但不要写入源文本、音频、用户名或绝对路径：

| Field / 字段 | Example form / 示例形式 |
| --- | --- |
| Runtime | OS family, Python, Torch, ROCm |
| Hardware | GPU class, VRAM class, host-memory class |
| Objective | native acoustic objective or named auxiliary objective |
| LoRA | rank, alpha, dropout, target-module family |
| Stability | precision, batch, accumulation, clip threshold |
| Recovery | checkpoint interval, resume test status |
| Validation | finite scan, fresh load, authorized output decode |
