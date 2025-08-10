# ScrapeWebTeleBot

A Telegram bot that can download and send videos from Twitter/X posts and YouTube shorts.

## Features

- ✅ Download Twitter/X post videos
- ✅ Download YouTube shorts and regular videos
- ✅ Send videos directly to Telegram chat
- ✅ Support for multiple URL formats
- ✅ Rich metadata display (title, uploader, duration, views)
- ✅ File size validation (50MB limit for Telegram)
- ✅ Duration validation (10 minutes max)
- ✅ User-friendly interface with commands
- ✅ Bot statistics tracking
- ✅ Error handling and user feedback

## Supported URLs

### Twitter/X
- `https://twitter.com/user/status/123456789`
- `https://x.com/user/status/123456789`
- `https://mobile.twitter.com/user/status/123456789`
- `https://t.co/abcd123` (shortened URLs)

### YouTube
- `https://youtube.com/shorts/abc123def`
- `https://youtu.be/abc123def`
- `https://youtube.com/watch?v=abc123def`
- `https://m.youtube.com/shorts/abc123def`

## Bot Commands

- `/start` - Show welcome message and bot introduction
- `/help` - Display detailed usage instructions
- `/about` - Information about the bot and its features
- `/stats` - View download statistics

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
# Option 1: Direct execution
cd twitter_downloader_bot
python main.py

# Option 2: Using the startup script (recommended)
./start_bot.sh
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
5. Use `/stats` to see download statistics
6. Use `/about` to learn more about the bot

## Example Usage

Send any of these URLs to the bot:
- `https://twitter.com/user/status/1234567890123456789`
- `https://youtube.com/shorts/dQw4w9WgXcQ`
- `https://youtu.be/dQw4w9WgXcQ`

The bot will respond with the downloaded video and metadata!

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