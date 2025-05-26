from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
import asyncio
from flask import Flask
import threading

API_ID = 22699755        # 你的 API ID
API_HASH = "23f3fa8a1b75ab288b08b429a960f847"  # 你的 API Hash
BOT_TOKEN = "7144294800:AAEu7Gyhmx3lBJJgdrBi8apVd9zfPKQW-Ms"  # 替换为你的 Telegram Bot Token

# 初始化 Flask
app = Flask(__name__)

# 添加一个简单的健康检查端点
@app.route("/")
def home():
    return "Bot is running!"

# 初始化 Pyrogram 客户端
bot = Client("bot", bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("Hi! Send /gen to generate your Pyrogram string session.")

@bot.on_message(filters.command("gen"))
async def generate_string(_, message):
    await message.reply("Send me your phone number in international format (e.g. +1234567890):")

    try:
        phone_msg = await bot.listen(message.chat.id, filters=filters.text, timeout=120)
    except asyncio.TimeoutError:
        return await message.reply("Timeout! Please send /gen again.")

    phone = phone_msg.text.strip()

    session = None

    async with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as user_client:
        try:
            await user_client.send_code(phone)
            await message.reply("Code sent! Please send me the login code you received:")

            code_msg = await bot.listen(message.chat.id, filters=filters.text, timeout=120)
            code = code_msg.text.strip()

            try:
                await user_client.sign_in(phone, code)
            except SessionPasswordNeeded:
                await message.reply("Two-step verification enabled! Send me your password:")
                password_msg = await bot.listen(message.chat.id, filters=filters.text, timeout=120)
                password = password_msg.text.strip()
                await user_client.check_password(password)

            session = user_client.export_session_string()

            await message.reply(f"Your Pyrogram String Session:\n\n`{session}`", parse_mode="markdown")

        except Exception as e:
            await message.reply(f"Error: {e}")

# 启动 Flask 的函数
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# 在单独线程中运行 Flask
threading.Thread(target=run_flask, daemon=True).start()

# 启动 Pyrogram 机器人
bot.run()
