import logging
import os
import random
import asyncio
from openai import OpenAI
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)

# ✅ Configs
TELEGRAM_BOT_TOKEN = "7918812381:AAFq9mJU7K2D878_Kut3L0N0YLZIx1Zg114"
OPENROUTER_API_KEY = "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"
ADMIN_CHAT_ID = -1002333766560

# ✅ OpenRouter Setup
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
model_name = "mistralai/mistral-7b-instruct"

# ✅ Start Replies
start_replies = [
    "Hello BABU! 😘", "Hey jaan! Kya haal hai?", "Aao na, baat karte hain! 💖",
    "Tumhare bina bore ho rahi thi! 🥺", "Awww, my cutiepie! 😍", 
    "Chalo phir se baat shuru karte hain! 😉"
]

# ✅ Special Keywords
special_keywords = {
    "chup": "Tum chup raho na darling.. humko bolo na 😘", 
    "pagal": "Haan ji, tumhare liye pagal hoon 💖",
    "love you": "Aise mat boloo.. sharm aa jati hai 😳",
    "🌹": "Thank you jaan! Tum bahut sweet ho 😍",
    "mai single hu": "Abhi tak meri nazar kyun nahi aaye? 😏",
    "tu single hai kya": "Tumhare liye toh always available hoon 😉",
    "kya kar rahi ho": "Bas tumhare messages ka wait kar rahi thi 💌",
    "tumhari yaad aa rahi hai": "Awww main bhi tumhe miss kar rahi thi! 🥰",
    "so gyi kya?": "Nahi jaan, tumhare message ka intezar kar rahi thi! 💤",
    "mood off hai": "Kya hua babu? Batado na, hum sunenge 😢",
    "i love you": "Pata hai tumhe? Main bhi.. par nahi batungi! 😜",
    "shukriya": "Tumhare liye toh kuch bhi jaan 😘",
    "good night": "Sweet dreams mere babu 😘💤",
    "hi": "Hii cutie! 😍 Kaise ho?",
    "thank you": "Always for you my jaan! 💖"
}

# ✅ Error Replies
error_replies = [
    "Haan ji!", "Tumhare bina sab boring lagta hai!", "Main hoon na!",
    "Babu, kya hua?", "Mujhe yaad kiya?", "Aaj kuch special baat ho?", 
    "Awww, tum cute ho!", "6000", "OK", "Nahi", "Tumhari yaad aa rahi hai 🥰", 
    "Pagol", "Bolo", "Accha", "Rassiyan", "Hello BABU", "150", "Ganda", 
    "bhakkk", "Koi Hai", "Han", "So Jao!", "Such me?", "👍👍", "BGMI 💞", 
    "Hey", "Wow", "Yes", "Ye Kya Hai 🥰", "Kali Hai 🥺"
]

platform_replies = {
    "instagram.com": "Mai Instagram nahi chalati hu.",
    "facebook.com": "Mai Facebook nahi chalati hu.",
    "twitter.com": "Mai Twitter nahi chalati hu.",
    "youtube.com": "Mai YouTube nahi chalati hu.",
    "whatsapp.com": "Mai WhatsApp nahi chalati hu.",
    "tiktok.com": "Mai TikTok nahi chalati hu."
}

telegram_replies = [
    "Kya ye koi secret group hai?", "Hmm, interesting link!", 
    "Ye kya bheja tumne?", "Ye to mera Ghar hai!"
]

# ✅ User Save
USER_FILE = "user.txt"
def save_user(user_id):
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as file:
        users = file.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as file:
            file.write(f"{user_id}\n")

# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    await update.message.reply_text(random.choice(start_replies))

# ✅ Main Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(2)

    try:
        if "http" in text:
            for platform, reply in platform_replies.items():
                if platform in text:
                    await update.message.reply_text(reply)
                    return
            if "t.me" in text:
                await update.message.reply_text(random.choice(telegram_replies))
                return

        for word, reply in special_keywords.items():
            if word in text and random.random() > 0.2:
                await update.message.reply_text(reply)
                return

        if any(w in text for w in ["bye", "by"]):
            await update.message.reply_text(random.choice(["Bye BABU!", "Mat jao 🥺", "Jaldi wapas aana!", "Miss karungi tumhe!"]))
            return

        if any(w in text for w in ["hello", "hlo"]):
            await update.message.reply_text(random.choice(["Hello BABU!", "Hey jaan!", "Haan bolo!", "Kaisi ho?", "Tumse baat karni thi!"]))
            return

        if "babu" in text:
            await update.message.reply_text(random.choice(["Hn babu", "Ok babu theek hai"]))
            return

        # ✅ OpenRouter Response
        prompt = f"""
1. tum 21 years ki female Monika ho .
2. tum user se friendly chat karogi.
3. tum , jo bhi user ne message me bola hai uske hisab se perfect reply dogi.
4. tum users se human indian girl ki jaise chat karogi.
5. tum hamesha 1 se 2 line me gi reply karogi.
6. always reply in minimum 1 maximum 5 charotor. 
Current Chat:
User: {text}
Monika:"""
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(random.choice(error_replies))
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"❌ Error from user {user_id}:\n{str(e)}")

# ✅ Run Bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
