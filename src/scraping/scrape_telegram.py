import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")

# Folders
RAW_DATA_FOLDER = "data/raw/telegram_messages"
IMAGES_FOLDER = "data/raw/telegram_images"

# List of channels to scrape
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    # add more as needed
]


async def scrape_channel(client, channel_name):
    """
    Scrapes messages and media from a single Telegram channel.
    """
    messages_data = []
    images_downloaded = 0

    # Create partitioned folders
    date_str = datetime.now().strftime("%Y-%m-%d")
    json_dir = os.path.join(RAW_DATA_FOLDER, date_str)
    img_dir = os.path.join(IMAGES_FOLDER, date_str, channel_name)

    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    logging.info(f"Scraping channel: {channel_name}")

    try:
        async for message in client.iter_messages(channel_name, limit=500):
            msg_dict = {
                "id": message.id,
                "date": str(message.date),
                "message": message.message,
                "sender_id": str(message.sender_id),
                "has_media": bool(message.media),
                "media_file": None,
            }

            # Download image if available
            if isinstance(message.media, MessageMediaPhoto) or isinstance(
                message.media, MessageMediaDocument
            ):
                file_name = f"{message.id}.jpg"
                file_path = os.path.join(img_dir, file_name)
                try:
                    await message.download_media(file=file_path)
                    msg_dict["media_file"] = file_path
                    images_downloaded += 1
                except Exception as e:
                    logging.warning(
                        f"Failed to download media for message {message.id}: {e}"
                    )

            messages_data.append(msg_dict)

    except FloodWaitError as e:
        logging.error(f"Rate limited. Sleep for {e.seconds} seconds.")

    # Save JSON
    json_path = os.path.join(json_dir, f"{channel_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=2)

    logging.info(
        f"Finished scraping {channel_name}. Messages:"
        f" {len(messages_data)} | Images: {images_downloaded}"
    )


async def scrape_all_channels():
    client = TelegramClient("session_name", API_ID, API_HASH)
    await client.start()

    for channel in CHANNELS:
        await scrape_channel(client, channel)


if __name__ == "__main__":
    import asyncio

    asyncio.run(scrape_all_channels())
