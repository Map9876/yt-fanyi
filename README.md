# yt-fanyi
YouTube 视频 srt 字幕 翻译 脚本 python ai。gpt

# YouTube 字幕翻译工具 (yt-fanyi)

一键将YouTube视频字幕翻译为中文SRT格式。

## 安装

```bash
pip install git+https://github.com/your-repo/yt-fanyi.git
```

## 使用方法

基本命令：
```bash
yt-fanyi "YouTube视频链接" --api-key YOUR_API_KEY
```

选项：
- `-o/--output`: 指定输出文件路径 (默认: translated.srt)
- `--api-key`: 硅基流动API密钥 (也可通过环境变量`SILICONFLOW_API_KEY`设置)

示例：
```bash
export SILICONFLOW_API_KEY="your_api_key_here"
yt-fanyi "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o output.srt
```

## 注意事项

1. 需要有效的硅基流动API密钥
2. 视频必须包含英文字幕
3. 翻译质量取决于API模型
