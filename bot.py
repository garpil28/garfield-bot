# bot.py
import telebot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID
from database import create_tables, add_order, get_orders, update_status

bot = telebot.TeleBot(BOT_TOKEN)
create_tables()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Selamat datang di *Auto Payment Bot*\nKetik /order untuk memulai.", parse_mode="Markdown")

@bot.message_handler(commands=['order'])
def order(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Produk A - Rp10.000", "Produk B - Rp20.000")
    msg = bot.send_message(message.chat.id, "Pilih produk yang ingin kamu beli:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_product)

def process_product(message):
    user_id = message.from_user.id
    username = message.from_user.username
    product = message.text
    if "Rp10.000" in product:
        price = 10000
    elif "Rp20.000" in product:
        price = 20000
    else:
        bot.reply_to(message, "❌ Produk tidak valid.")
        return

    text = f"🛍 Produk: {product}\n💰 Harga: Rp{price}\n\nSilakan bayar ke:\n📱 DANA: 08123456789 (GARFIELD STORE)\n📸 Kirim bukti pembayaran ke admin setelah bayar."
    add_order(user_id, username, product, price, "DANA")

    bot.send_message(message.chat.id, text)
    bot.send_message(ADMIN_ID, f"🆕 Order baru dari @{username}\nProduk: {product}\nHarga: Rp{price}")

@bot.message_handler(commands=['orders'])
def orders(message):
    if message.from_user.id != ADMIN_ID:
        return
    data = get_orders()
    text = "📦 *Daftar Order:*\n\n"
    for d in data:
        text += f"#{d['id']} - @{d['username']} | {d['product']} | {d['status']}\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['update'])
def update_order(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.send_message(message.chat.id, "Masukkan ID order dan status baru (contoh: `5 Paid`):", parse_mode="Markdown")
    bot.register_next_step_handler(msg, do_update)

def do_update(message):
    try:
        order_id, status = message.text.split()
        update_status(order_id, status)
        bot.reply_to(message, f"✅ Order #{order_id} diupdate ke '{status}'")
    except:
        bot.reply_to(message, "❌ Format salah. Gunakan: ID STATUS")

print("🤖 Bot sedang berjalan...")
bot.infinity_polling()
