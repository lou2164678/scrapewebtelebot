#!/bin/bash
# Startup script for ScrapeWebTeleBot

echo "🤖 ScrapeWebTeleBot Startup Script"
echo "================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "twitter_downloader_bot/main.py" ]; then
    echo "❌ Please run this script from the project root directory"
    echo "   Expected to find: twitter_downloader_bot/main.py"
    exit 1
fi

# Check for virtual environment
if [ ! -d "venv" ] && [ ! -d ".venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No virtual environment detected."
    echo "   It's recommended to use a virtual environment."
    echo "   Create one with: python3 -m venv venv && source venv/bin/activate"
    echo ""
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "
try:
    import telegram
    import yt_dlp
    print('✅ Dependencies are installed')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('   Install with: pip install -r requirements.txt')
    exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Check for bot token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  TELEGRAM_BOT_TOKEN environment variable is not set"
    echo ""
    echo "Please set your Telegram Bot Token:"
    echo "1. Get a token from @BotFather on Telegram"
    echo "2. Export it: export TELEGRAM_BOT_TOKEN='your_token_here'"
    echo "3. Or create a .env file with: TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    echo "For now, please enter your token:"
    read -p "Bot Token: " token
    if [ -n "$token" ]; then
        export TELEGRAM_BOT_TOKEN="$token"
        echo "✅ Token set for this session"
    else
        echo "❌ No token provided, exiting"
        exit 1
    fi
fi

echo ""
echo "🚀 Starting bot..."
echo "   Press Ctrl+C to stop"
echo ""

cd twitter_downloader_bot
python3 main.py