import re
import requests
import time
from typing import List, Dict, Optional, Tuple
from pytubefix import YouTube
from tqdm import tqdm

class YouTubeSubtitleTranslator:
    SYSTEM_PROMPT = """Translate the subtitles given into Simplified Chinese. For example, when you receive:
258
But what kind of mother would execute their child in broad daylight
259
for running to China because they were starving?
You reply:
258
但是 什么样的母亲会因为孩子因饥饿而逃往中国
259
就在大白天处决自己的他们？

现在请翻译以下内容："""

    def __init__(self, api_key: str):
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def download_subtitles(self, video_url: str) -> Optional[str]:
        try:
            yt = YouTube(video_url)
            if 'a.en' not in yt.captions:
                print("视频没有英文字幕")
                return None
            return yt.captions['a.en'].generate_srt_captions()
        except Exception as e:
            print(f"下载字幕失败: {e}")
            return None

    def parse_srt(self, srt_content: str) -> Tuple[List[Dict], str]:
        blocks = []
        clean_text = []
        for block in srt_content.split('\n\n'):
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                blocks.append({
                    'num': lines[0],
                    'time': lines[1],
                    'text': '\n'.join(lines[2:])
                })
                clean_text.append('\n'.join(lines[2:]))
        return blocks, '\n'.join(clean_text)

    def create_chunks(self, blocks: List[Dict], chunk_size=12, overlap=3) -> List[str]:
        chunks = []
        for i in range(0, len(blocks), chunk_size - overlap):
            chunk_blocks = blocks[i:i + chunk_size]
            chunk = '\n\n'.join(
                f"{b['num']}\n{b['text']}" for b in chunk_blocks
            )
            chunks.append(chunk)
        return chunks

    def translate_chunk(self, chunk: str) -> Optional[str]:
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": "deepseek-ai/DeepSeek-R1",
                    "messages": [
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": chunk}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"翻译出错: {e}")
            return None

    def rebuild_srt(self, blocks: List[Dict], translated: str) -> str:
        translated_blocks = translated.split('\n\n')
        output = []
        for orig, trans in zip(blocks, translated_blocks):
            lines = trans.split('\n')
            if len(lines) >= 2:
                output.append(
                    f"{orig['num']}\n{orig['time']}\n{lines[1]}"
                )
        return '\n\n'.join(output)

    def translate(self, video_url: str) -> Optional[str]:
        srt_content = self.download_subtitles(video_url)
        if not srt_content:
            return None

        blocks, _ = self.parse_srt(srt_content)
        chunks = self.create_chunks(blocks)
        
        translated_chunks = []
        for chunk in tqdm(chunks, desc="翻译进度"):
            translated = self.translate_chunk(chunk)
            if translated:
                translated_chunks.append(translated)
            time.sleep(1)  # 避免API限流
        
        if not translated_chunks:
            return None

        return self.rebuild_srt(blocks, '\n\n'.join(translated_chunks))
