import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
bot = telebot.TeleBot(TOKEN)

OWNER_USERNAME = "@ShanXPLD"

WELCOME_CAPTION = """✨ ━━━━━━━━━━━━━━━━━━━ ✨
      ZUAN PANEL
   Auto Order Panel
✨ ━━━━━━━━━━━━━━━━━━━ ✨

👋 Halo, Selamat Datang Bosku!

Terima kasih sudah mampir ke toko kami.
Di sini semua serba OTOMATIS, tanpa antri,
tanpa drama nunggu admin.

⚡ AKTIF 24 JAM
🛡️ GARANSI FULL 15 HARI
📦 STOK SELALU UPDATE
⚡ FAST RESPON
✅ AMANAH & TERPERCAYA
👑 PREMIUM QUALITY

👇 Silakan pilih menu di bawah ini:"""

def main_menu():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🔵 📦 CEK STOK", callback_data="stok"),
        InlineKeyboardButton("🟢 💰 LIST HARGA", callback_data="harga"),
        InlineKeyboardButton("🟡 🧾 PAYMENT", callback_data="payment"),
        InlineKeyboardButton("🟠 📝 CARA ORDER", callback_data="cara"),
        InlineKeyboardButton("🔴 👑 OWNER / CS", callback_data="owner"),
        InlineKeyboardButton("🟣 📣 TESTIMONI", callback_data="testi"),
    )
    return m

def back_menu():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("⬜ 🔙 KEMBALI KE MENU", callback_data="back"))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    try:
        with open("banner.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=WELCOME_CAPTION, reply_markup=main_menu())
    except FileNotFoundError:
        bot.send_message(message.chat.id, WELCOME_CAPTION, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.data == "back":
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            with open("banner.jpg", "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=WELCOME_CAPTION, reply_markup=main_menu())
            return

        texts = {
            "stok": "📦 **CEK STOK PANEL**\n\n✅ 1GB - 10GB : READY\n✅ UNLIMITED : READY\n\nStok selalu update 24 jam! 🔥",
            "harga": "💰 **LIST HARGA PANEL**\n\n• 1GB - Rp 2.000\n• 2GB - Rp 3.000\n• 3GB - Rp 4.000\n• 4GB - Rp 5.000\n• 5GB - Rp 6.000\n• 6GB - Rp 7.000\n• 7GB - Rp 8.000\n• 8GB - Rp 9.000\n• 9GB - Rp 10.000\n• 10GB - Rp 11.000\n• UNLIMITED - Rp 13.000\n\n🛡️ Garansi Full 15 Hari",
            "payment": "🧾 **PAYMENT**\n\n• DANA\n• GOPAY\n• OVO\n• QRIS\n\nChat OWNER dulu untuk nomor payment ya bosku!",
            "cara": "📝 **CARA ORDER**\n\n1. Pilih panel di List Harga\n2. Chat OWNER / CS\n3. Transfer\n4. Kirim bukti TF\n5. Panel langsung dibuatin!",
            "owner": f"👑 **OWNER / CS**\n\nChat langsung: {OWNER_USERNAME}\nFast respon, amanah 100% ✅",
            "testi": "📣 **TESTIMONI & BUKTI**\n\nRibuan customer udah order di ZUAN PANEL.\nTesti lengkap cek ke OWNER ya bosku!\nDijamin aman, garansi full!",
        }

        text = texts.get(call.data, "Menu tidak ditemukan")
        try:
            if call.message.photo:
                bot.edit_message_caption(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_menu())
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_menu())
        except:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=back_menu())

        bot.answer_callback_query(call.id)

    except Exception as e:
        print(e)
        bot.answer_callback_query(call.id, "Coba lagi bosku!")

print("Bot jalan...")
bot.infinity_polling()
