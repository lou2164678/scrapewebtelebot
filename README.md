# ScrapeWebTeleBot

A Telegram bot that can download and send videos from Twitter/X posts and YouTube shorts.

## Features

- ✅ Download Twitter/X post videos
- ✅ Download YouTube shorts
- ✅ Send videos directly to Telegram chat
- ✅ Support for multiple URL formats
- ✅ File size validation (50MB limit for Telegram)
- ✅ User-friendly interface with commands

## Supported URLs

### Twitter/X
- `https://twitter.com/user/status/123456789`
- `https://x.com/user/status/123456789`
- `https://t.co/abcd123` (shortened URLs)

### YouTube
- `https://youtube.com/shorts/abc123def`
- `https://youtu.be/abc123def`

## Setup

### Prerequisites
- Python 3.11 or higher
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))

### Installation

1. Clone this repository:
```bash
git clone https://github.com/lou2164678/scrapewebtelebot.git
cd scrapewebtelebot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Telegram Bot Token:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

4. Run the bot:
```bash
cd twitter_downloader_bot
python main.py
```

### Using with uv (Recommended)

```bash
uv sync
cd twitter_downloader_bot
uv run python main.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send `/help` to see usage instructions
4. Send any supported URL and the bot will download and send the video

## Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (required)

## Limitations

- Maximum file size: 50MB (Telegram limit)
- Only supports video content
- Private/protected content may not be accessible
- Rate limiting may apply depending on the platform

## Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `yt-dlp` - Universal video downloader
- `aiohttp` - Async HTTP client
- `requests` - HTTP library

## License

This project is open source and available under the [MIT License](LICENSE).