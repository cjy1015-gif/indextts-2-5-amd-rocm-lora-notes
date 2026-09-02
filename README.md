# IndexTTS-2.5 AMD/ROCm LoRA Engineering Notes

# IndexTTS-2.5 AMD/ROCm LoRA 工程经验

This repository documents a reproducible engineering route for experimenting with IndexTTS-2.5 GPT-side LoRA training on constrained AMD/ROCm hardware. It focuses on environment isolation, numerical stability, low-memory operation, checkpoint recovery, and validation.

本仓库记录在受限 AMD/ROCm 硬件上开展 IndexTTS-2.5 GPT 部分 LoRA 实验的工程方法，重点包括环境隔离、数值稳定性、低内存运行、断点恢复和结果验收。

> **Learning and research use only / 仅限学习研究**
>
> This is a sanitized methods project. It does not publish commercial-game voices, scripts, transcripts, datasets, speaker identities, model weights, generated audio, private logs, or local absolute paths.
>
> 这是脱敏后的方法项目，不公开商业游戏语音、台词、转写文本、数据集、说话人身份、模型权重、生成音频、私人日志或本机绝对路径。

## Scope / 项目边界

- Community experimental workflow; not an official IndexTTS training recipe.
- GPT-side LoRA only; not full-model fine-tuning.
- Documentation and safe templates only; no data or model download is provided.
- Use only data, reference audio, and model components that you own or are explicitly authorized to use.

- 社区实验性流程，不代表 IndexTTS 官方训练方案。
- 仅讨论 GPT 部分 LoRA，不是全模型微调。
- 只提供文档和安全模板，不提供数据集或模型下载。
- 只能使用自有或获得明确授权的数据、参考音频和模型组件。

## Tested stack / 实测环境

| Item / 项目 | Tested configuration / 实测配置 |
| --- | --- |
| OS | Windows 11 + WSL2 Ubuntu 24.04 |
| GPU | AMD Radeon RX 9070 XT, 16GB VRAM |
| Host memory | 16GB |
| GPU stack | ROCm/HIP |
| Python | 3.12.x |
| PyTorch | ROCm build in the 2.12.x line |
| Precision | FP32 |
| Devices | Single GPU |

These values describe one verified combination, not a guarantee for every AMD card or software release.

这些版本只描述一组已验证组合，不保证所有 AMD 显卡或软件版本都能得到相同结果。

## What is included / 公开内容

- [Reproduction guide](docs/reproduction.md)
- [Sanitized troubleshooting record](docs/troubleshooting-record.md)
- [Method notes](docs/method.md)
- Safe configuration templates under `configs/`
- Empty data-layout guidance under `data/`
- Environment and finite-value checks under `scripts/`
- Third-party notices and a permissive license

## What is intentionally excluded / 明确不公开

- Commercial or third-party voices, scripts, transcripts, and data manifests
- Character-specific adapters, speaker embeddings, checkpoints, and optimizer states
- Generated audio, evaluation files, training logs, and private experiment outputs
- Usernames, account information, cookies, machine identifiers, and absolute paths

## Non-commercial notice / 非商业声明

This repository is intended for personal learning, research, and non-commercial experimentation. Do not use it for unauthorized voice replication, impersonation, fraud, harassment, or any activity that violates applicable law, platform rules, or third-party rights. The user is responsible for rights clearance and safe use.

本仓库用于个人学习、研究和非商业实验。不得将其用于未经授权的声音复制、身份冒用、欺诈、骚扰，或任何违反适用法律、平台规则及第三方权利的行为。使用者应自行负责权利确认和安全使用。

## Quick route / 推荐路线

1. Confirm the real interpreter, ROCm/PyTorch build, GPU visibility, working directory, and module path.
2. Reuse a compatible existing environment; do not let a small missing package replace a ROCm Torch build with CUDA packages.
3. Disable unverified CUDA-only kernels, DeepSpeed, compilation, and low-precision paths.
4. Freeze non-target modules and inject LoRA only into the GPT Transformer.
5. Build a filtered, hashed manifest from authorized data.
6. Run one optimizer step, scan finite values, reload in a fresh process, and generate a validation artifact.
7. Add structured logs, periodic checkpoints, safe signal handling, and resume-state validation before a longer run.
8. Select checkpoints using both objective signals and authorized human evaluation; the last step is not automatically the best.

## License / 许可证

Original documentation and helper scripts are released under the MIT License. Third-party software, models, and data remain subject to their own licenses and permissions; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

原创文档和辅助脚本采用 MIT 许可证。第三方软件、模型和数据仍受其自身许可证及授权约束，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
