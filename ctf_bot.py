import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('8705202155:AAHNPmrkNQ4_Npuwx5vcWzvPOVzOQAsaSNk')

scoreboard = {}

FLAG_ANS = {
    "chal_1": "NUT{wh4t_1s_e_valu3?}",
    "chal_2": "NUT{wh4t?}",
    "chal_3": "NUT{bond_university_robina}"
}

POINTS_PER_CHAL = 100

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "Welcome to the Mini CTF! 🚩\n\n"
        "Here are your challenges:\n"
        "1. **Crypto:** Optimized RSA\n"
        "2. **Misc:** javascript moment\n"
        "3. **OSINT:** doxxed\n\n"
        "Click a challenge below to view details and submit a flag. Type /scoreboard to see rankings!"
    )
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Challenge 1", callback_data="chal_1")
    btn2 = InlineKeyboardButton("Challenge 2", callback_data="chal_2")
    btn3 = InlineKeyboardButton("Challenge 3", callback_data="chal_3")
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['scoreboard'])
def show_scoreboard(message):
    if not scoreboard:
        bot.reply_to(message, "Scoreboard is currently empty.")
        return
    
    sorted_players = sorted(scoreboard.values(), key=lambda x: x['score'], reverse=True)
    
    board_text = "**Scoreboard: **\n\n"
    for i, player in enumerate(sorted_players, 1):
        board_text += f"{i}. @{player['username']} - {player['score']} pts\n"
        
    bot.send_message(message.chat.id, board_text, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    
    bot.answer_callback_query(call.id)
    if call.data == "chal_1":
        msg = bot.send_message(chat_id, "🚩 **Crypto: Optimized RSA**\n\nAlice is encrypting her flags. She learned from a blog post that RSA can be slow, so she tried to optimize it, while keeping security at first hand.\n\nShe sent you the resulting file. See if you can recover her secret.", parse_mode='Markdown')
        with open('output.txt', 'rb') as doc:
            bot.send_document(chat_id, doc)
        msg = bot.send_message(chat_id, "*Type your flag below:*", parse_mode='Markdown')
        bot.register_next_step_handler(msg, check_flag, "chal_1")
    
    elif call.data == "chal_2":
        msg = bot.send_message(chat_id, "🚩 **Misc: javascript moment**\n\nI recently learned about JavaScript, and I realized how stupid it is.", parse_mode='Markdown')
        with open('jsf.txt', 'rb') as doc:
                    bot.send_document(chat_id, doc)
        msg = bot.send_message(chat_id, "*Type your flag below:*", parse_mode='Markdown')
        bot.register_next_step_handler(msg, check_flag, "chal_2")
    
    elif call.data == "chal_3":
        msg = bot.send_message(chat_id, "🚩 **OSINT: doxxed**\n\nhaha whose university is this? find out the university and the city this is located in. for example, NUT{harvard\_university\_boston}", parse_mode='Markdown')
        with open('scary.jpg', 'rb') as doc:
                            bot.send_document(chat_id, doc)
        msg = bot.send_message(chat_id, "*Type your flag below:*", parse_mode='Markdown')
        bot.register_next_step_handler(msg, check_flag, "chal_3")


def check_flag(message, chal_id):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name 
    submitted_flag = message.text.strip()
    if user_id not in scoreboard:
        scoreboard[user_id] = {"username": username, "score": 0, "solved": []}

    if chal_id in scoreboard[user_id]["solved"]:
        bot.reply_to(message, "⚠️ You have already solved this challenge! Try another one.")
        return

    if submitted_flag == FLAG_ANS[chal_id]:
        scoreboard[user_id]["score"] += POINTS_PER_CHAL
        scoreboard[user_id]["solved"].append(chal_id)
        
        bot.reply_to(message, f"🎉 **Correct!** You've been awarded with {POINTS_PER_CHAL} points.\nCheck your rank with /scoreboard", parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ Incorrect flag. Try again!")

print("CTF Bot is running locally...")
bot.polling(none_stop=True)