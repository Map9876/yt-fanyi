import argparse
import os
from .translator import YouTubeSubtitleTranslator

def main():
    parser = argparse.ArgumentParser(description='YouTube视频字幕翻译工具')
    parser.add_argument('url', help='YouTube视频URL')
    parser.add_argument('-o', '--output', default='translated.srt', help='输出文件路径')
    parser.add_argument('--api-key', default=os.getenv('SILICONFLOW_API_KEY'), 
                      help='硅基流动API密钥，也可通过环境变量SILICONFLOW_API_KEY设置')
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("错误: 必须提供API密钥")
        print("使用方法: yt-fanyi URL --api-key YOUR_KEY")
        print("或设置环境变量: export SILICONFLOW_API_KEY='your_key'")
        return

    translator = YouTubeSubtitleTranslator(args.api_key)
    result = translator.translate(args.url)
    
    if result:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"翻译完成! 结果已保存到 {args.output}")
    else:
        print("翻译失败，请检查URL和API密钥")

if __name__ == "__main__":
    main()
