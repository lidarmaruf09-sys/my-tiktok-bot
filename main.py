import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_BOT_TOKEN = "9058935741:AAGtucsGkoYrid-lWgmbxR81Lg8eKWsUtXY"
TIKTOK_CLIENT_KEY = "mgzwwl2i0navmix8"
TIKTOK_CLIENT_SECRET = "nWuSacdBWsAuuo3vi51NP1H4mNkOBlTl"

async def upload_to_tiktok_api(image_url, loop_count=20):
    tiktok_url = "https://tiktokapis.com"
    
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    
    data = {
        "client_key": TIKTOK_CLIENT_KEY,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "post_info": {
            "title": "Uploaded automatically via Telegram Bot",
            "privacy_level": "PUBLIC_TO_EVERYONE"
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": 5242880
        }
    }

    for i in range(loop_count):
        try:
            response = requests.post(tiktok_url, headers=headers, json=data)
            if response.status_code == 200 or response.status_code == 201:
                print(f"পোস্ট {i+1} সফলভাবে টিকটকে পাঠানো হয়েছে।")
            else:
                print(f"পোস্ট {i+1} ব্যর্থ হয়েছে: {response.text}")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"ত্রুটি ঘটেছে: {e}")
            break

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    image_url = photo_file.file_path 
    await update.message.reply_text("🤖 ছবি পেয়েছি! ব্যাকগ্রাউন্ডে আপনার টিকটক আইডিতে ৬০ বার আপলোড হওয়া শুরু হয়েছে...")
    await upload_to_tiktok_api(image_url, loop_count=60)
    await update.message.reply_text("✅ ৬০টি পোস্ট করার প্রক্রিয়া সফলভাবে সম্পন্ন হয়েছে!")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("টেলিগ্রাম বট সফলভাবে চালু হয়েছে...")
    application.run_polling()

if __name__ == "__main__":
    main()
