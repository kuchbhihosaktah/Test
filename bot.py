import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS
import os

BOT_TOKEN = "8386912250:AAHWppIHrXHpG8lQuZ7l3xkO4AjMUkIkhZg"
bot = telebot.TeleBot(BOT_TOKEN)

Store user data temporarily

user_data = {}

Step 0: Receive text

@bot.message_handler(func=lambda msg: True)
def receive_text(message):
user_data[message.chat.id] = {"text": message.text}
language_buttons(message.chat.id)

Step 1: Language selection

def language_buttons(chat_id):
markup = InlineKeyboardMarkup()
markup.row_width = 2
markup.add(
InlineKeyboardButton("Hindi 🇮🇳", callback_data="lang_hi"),
InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
)
bot.send_message(chat_id, "Step 1️⃣: Select Language", reply_markup=markup)

Step 2: Voice selection

def voice_buttons(chat_id):
markup = InlineKeyboardMarkup()
markup.row_width = 2
markup.add(
InlineKeyboardButton("Male 👨", callback_data="voice_male"),
InlineKeyboardButton("Female 👩", callback_data="voice_female"),
InlineKeyboardButton("Robot 🤖", callback_data="voice_robot"),
InlineKeyboardButton("Soft 🧸", callback_data="voice_soft")
)
bot.send_message(chat_id, "Step 2️⃣: Select Voice", reply_markup=markup)

Step 3: Emotion selection

def emotion_buttons(chat_id):
markup = InlineKeyboardMarkup()
markup.row_width = 2
markup.add(
InlineKeyboardButton("Happy 😄", callback_data="emo_happy"),
InlineKeyboardButton("Sad 😢", callback_data="emo_sad"),
InlineKeyboardButton("Angry 😡", callback_data="emo_angry"),
InlineKeyboardButton("Neutral 😐", callback_data="emo_neutral")
)
bot.send_message(chat_id, "Step 3️⃣: Select Emotion", reply_markup=markup)

Step 4: Optional speed/pitch buttons

def speed_buttons(chat_id):
markup = InlineKeyboardMarkup()
markup.row_width = 3
markup.add(
InlineKeyboardButton("Slow 🐢", callback_data="speed_slow"),
InlineKeyboardButton("Normal 🐎", callback_data="speed_normal"),
InlineKeyboardButton("Fast ⚡", callback_data="speed_fast")
)
bot.send_message(chat_id, "Step 4️⃣: Select Speed", reply_markup=markup)

Handle button presses

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
chat_id = call.message.chat.id
data = call.data

if chat_id not in user_data:  
    bot.send_message(chat_id, "Please send text first.")  
    return  

# Language  
if data.startswith("lang_"):  
    user_data[chat_id]["lang"] = data.split("_")[1]  
    bot.edit_message_text("✅ Language selected", chat_id, call.message.message_id)  
    voice_buttons(chat_id)  

# Voice  
elif data.startswith("voice_"):  
    user_data[chat_id]["voice"] = data.split("_")[1]  
    bot.edit_message_text("✅ Voice selected", chat_id, call.message.message_id)  
    emotion_buttons(chat_id)  

# Emotion  
elif data.startswith("emo_"):  
    user_data[chat_id]["emotion"] = data.split("_")[1]  
    bot.edit_message_text("✅ Emotion selected", chat_id, call.message.message_id)  
    speed_buttons(chat_id)  

# Speed  
elif data.startswith("speed_"):  
    speed_map = {"slow": 0.8, "normal": 1.0, "fast": 1.2}  
    user_data[chat_id]["speed"] = speed_map[data.split("_")[1]]  
    bot.edit_message_text("✅ Speed selected", chat_id, call.message.message_id)  
    generate_voice(chat_id)

Generate final voice

def generate_voice(chat_id):
info = user_data.get(chat_id)
if not info:
bot.send_message(chat_id, "Error: No data found.")
return

text = info["text"]  
lang = info.get("lang", "en")  
voice = info.get("voice", "male")  
emotion = info.get("emotion", "neutral")  
speed = info.get("speed", 1.0)  

# Simple emotion to pitch mapping  
pitch_map = {"happy": 70, "sad": 50, "angry": 55, "neutral": 60}  
pitch = pitch_map.get(emotion, 60)  

# Generate gTTS  
tts = gTTS(text=text, lang=lang)  
tts.save("output.mp3")  

# Adjust speed using ffmpeg  
os.system(f"ffmpeg -y -i output.mp3 -filter:a 'atempo={speed}' output_final.mp3 > /dev/null 2>&1")  

# Send voice  
with open("output_final.mp3", "rb") as audio:  
    bot.send_voice(chat_id, audio)  

# Cleanup  
os.remove("output.mp3")  
os.remove("output_final.mp3")  
user_data.pop(chat_id, None)

print("🤖 Fully Interactive Telegram TTS Bot running with buttons...")
bot.polling()

