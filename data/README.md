# Private data boundary / 私有数据边界

No audio, text, manifest, speaker metadata, or dataset archive belongs in this public repository.

本公开仓库不应包含音频、文本、数据清单、说话人元数据或数据集压缩包。

## Private manifest shape / 私有清单格式

Keep the actual file private. A local manifest may use a structure like this, with paths and text stored outside GitHub:

实际文件必须私下保存。私有清单可以采用类似结构，但路径和文本不能提交到 GitHub：

```json
{"audio":"PRIVATE_AUDIO_PATH","speaker":"AUTHORIZED_SPEAKER_ID","language":"ja","text":"PRIVATE_TRANSCRIPT"}
```

Before training, validate:

- authorization and provenance for every audio item;
- audio existence, duration, sample rate, and decodability;
- transcript/audio alignment;
- deterministic ordering and a SHA-256 manifest lock;
- no private path or transcript is copied into logs or public configs.

训练前检查：

- 每条音频的授权和来源；
- 音频存在性、时长、采样率和可解码性；
- 台词与音频是否对应；
- 固定排序和 SHA-256 清单锁定；
- 私人路径或台词不会写入日志和公开配置。
