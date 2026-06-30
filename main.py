import os
import sys
import asyncio
from threading import Thread
from flask import Flask

try:
    import discord
except ImportError:
    os.system(f"{sys.executable} -m pip install discord.py")
    import discord

from discord.ext import commands

# سيرفر وهمي عشان خطة Render المجانية
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'=== {bot.user.name} جاهز للانطلاق وصاحي 24 ساعة! ===')
    try:
        synced = await bot.tree.sync()
        print(f"تمت مزامنة {len(synced)} أمر بنجاح!")
    except Exception as e:
        print(f"خطأ في المزامنة: {e}")

async def load_extensions():
    if os.path.exists('cogs'):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f' تم تحميل قسم: {filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print("خطأ: لم يتم العثور على التوكن!")
            return
        await bot.start(token)

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية الكود
    Thread(target=run_flask).start()
    asyncio.run(main())
