#!/usr/bin/env python3
"""
Telegram Bot for downloading Twitter/X posts and YouTube shorts
"""

import os
import re
import tempfile
import logging
import shutil
from typing import Optional
import asyncio

from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)
import yt_dlp
import aiohttp

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MediaDownloader:
    """Class to handle media downloading from various platforms"""
    
    def __init__(self):
        self.ydl_opts = {
            'format': 'best[height<=720]',  # Limit quality for Telegram
            'outtmpl': '%(uploader)s_%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
    
    def is_twitter_url(self, url: str) -> bool:
        """Check if URL is a Twitter/X post"""
        twitter_patterns = [
            r'https?://(www\.)?(twitter|x)\.com/\w+/status/\d+',
            r'https?://(www\.)?t\.co/\w+',
        ]
        return any(re.match(pattern, url) for pattern in twitter_patterns)
    
    def is_youtube_shorts_url(self, url: str) -> bool:
        """Check if URL is a YouTube Shorts"""
        shorts_patterns = [
            r'https?://(www\.)?youtube\.com/shorts/[\w-]+',
            r'https?://youtu\.be/[\w-]+',
        ]
        return any(re.match(pattern, url) for pattern in shorts_patterns)
    
    async def download_media(self, url: str) -> Optional[tuple[str, dict]]:
        """Download media from URL and return file path and metadata"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                opts = self.ydl_opts.copy()
                opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
                
                with yt_dlp.YoutubeDL(opts) as ydl:
                    # Extract info first to get metadata
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        return None
                    
                    # Check file size (Telegram limit is 50MB)
                    filesize = info.get('filesize') or info.get('filesize_approx')
                    if filesize and filesize > 50 * 1024 * 1024:
                        logger.warning(f"File too large: {filesize} bytes")
                        return None
                    
                    # Check duration (skip very long videos)
                    duration = info.get('duration', 0)
                    if duration and duration > 600:  # 10 minutes max
                        logger.warning(f"Video too long: {duration} seconds")
                        return None
                    
                    # Download the media
                    ydl.download([url])
                    
                    # Find the downloaded file
                    for file in os.listdir(temp_dir):
                        if file.endswith(('.mp4', '.mkv', '.webm', '.mov', '.avi')):
                            file_path = os.path.join(temp_dir, file)
                            # Copy to a permanent temp location for sending
                            import shutil
                            perm_path = f"/tmp/{file}"
                            shutil.copy2(file_path, perm_path)
                            
                            metadata = {
                                'title': info.get('title', 'Downloaded Video'),
                                'uploader': info.get('uploader', 'Unknown'),
                                'duration': duration,
                                'view_count': info.get('view_count'),
                                'upload_date': info.get('upload_date')
                            }
                            
                            return perm_path, metadata
                            
        except Exception as e:
            logger.error(f"Error downloading media: {e}")
            return None
    
    def get_platform_name(self, url: str) -> str:
        """Get platform name from URL"""
        if self.is_twitter_url(url):
            return "Twitter/X"
        elif self.is_youtube_shorts_url(url):
            return "YouTube"
        return "Unknown"

# Initialize downloader
downloader = MediaDownloader()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = (
        "🎬 Welcome to Media Downloader Bot!\n\n"
        "Send me a link to:\n"
        "• Twitter/X posts 🐦\n" 
        "• YouTube shorts 🎥\n\n"
        "I'll download and send you the media!"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📋 How to use this bot:\n\n"
        "1. Send me a Twitter/X post URL\n"
        "2. Send me a YouTube shorts URL\n"
        "3. I'll download and send you the video\n\n"
        "Supported formats:\n"
        "• https://twitter.com/user/status/...\n"
        "• https://x.com/user/status/...\n"
        "• https://youtube.com/shorts/...\n"
        "• https://youtu.be/...\n\n"
        "⚠️ File size limit: 50MB"
    )
    await update.message.reply_text(help_text)

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle URL messages and download media"""
    url = update.message.text.strip()
    
    # Check if it's a supported URL
    if not (downloader.is_twitter_url(url) or downloader.is_youtube_shorts_url(url)):
        await update.message.reply_text(
            "❌ Sorry, I only support Twitter/X posts and YouTube shorts.\n"
            "Use /help to see supported formats."
        )
        return
    
    platform = downloader.get_platform_name(url)
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        f"⏳ Downloading from {platform}... Please wait."
    )
    
    try:
        # Download the media
        result = await downloader.download_media(url)
        
        if result and len(result) == 2:
            file_path, metadata = result
            
            if os.path.exists(file_path):
                # Create a nice caption with metadata
                caption = f"✅ Downloaded from {platform}\n"
                if metadata.get('title'):
                    caption += f"📝 **{metadata['title']}**\n"
                if metadata.get('uploader'):
                    caption += f"👤 By: {metadata['uploader']}\n"
                if metadata.get('duration'):
                    duration = metadata['duration']
                    mins, secs = divmod(duration, 60)
                    caption += f"⏱️ Duration: {mins:02d}:{secs:02d}\n"
                if metadata.get('view_count'):
                    caption += f"👀 Views: {metadata['view_count']:,}\n"
                
                # Send the video file
                with open(file_path, 'rb') as video_file:
                    await update.message.reply_video(
                        video=video_file,
                        caption=caption,
                        parse_mode='Markdown'
                    )
                
                # Clean up
                try:
                    os.unlink(file_path)
                except:
                    pass
                    
            else:
                await update.message.reply_text(
                    f"❌ Failed to download media from {platform}.\n"
                    "The file could not be saved properly."
                )
        else:
            await update.message.reply_text(
                f"❌ Failed to download media from {platform}.\n"
                "Possible reasons:\n"
                "• The content is private or protected\n"
                "• The file is too large (>50MB)\n"
                "• The video is too long (>10 minutes)\n"
                "• The link is invalid or expired"
            )
    
    except Exception as e:
        logger.error(f"Error handling URL {url}: {e}")
        await update.message.reply_text(
            f"❌ Error downloading from {platform}. Please try again later.\n"
            f"Error details: {str(e)[:100]}..."
        )
    
    finally:
        # Delete processing message
        try:
            await processing_msg.delete()
        except:
            pass

def main() -> None:
    """Start the bot."""
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Handle URLs (any message that looks like a URL)
    url_filter = filters.TEXT & filters.Regex(r'https?://')
    application.add_handler(MessageHandler(url_filter, handle_url))
    
    # Handle other messages
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        lambda update, context: update.message.reply_text(
            "Please send me a valid URL. Use /help for more information."
        )
    ))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()