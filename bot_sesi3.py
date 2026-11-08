import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
bot = telebot.TeleBot(TOKEN)

OWNER_USERNAME = "@ShanXPLD"
OWNER_ID = 0

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

def main_menu_2col():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔵 📦 CEK STOK PANEL", callback_data="stok"),
        InlineKeyboardButton("🟢 💰 LIST HARGA", callback_data="harga"),
        InlineKeyboardButton("🟡 🧾 PAYMENT", callback_data="payment"),
        InlineKeyboardButton("🟠 📝 CARA ORDER", callback_data="cara"),
        InlineKeyboardButton("🔴 👑 OWNER / CS", callback_data="owner"),
        InlineKeyboardButton("🟣 📣 TESTIMONI & BUKTI", callback_data="testi"),
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    try:
        with open("banner.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id, photo,
                caption=WELCOME_CAPTION,
                reply_markup=main_menu_2col()
            )
    except FileNotFoundError:
        bot.send_message(message.chat.id, WELCOME_CAPTION, reply_markup=main_menu_2col())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "stok":
        bot.answer_callback_query(call.id, "Cek stok...")
        bot.send_message(call.message.chat.id,
            "📦 **CEK STOK PANEL**\n\n"
            "✅ Panel 1GB : READY\n"
            "✅ Panel 2GB : READY\n"
            "✅ Panel 3GB : READY\n"
            "✅ Panel 4GB : READY\n"
            "✅ Panel 5GB : READY\n"
            "✅ Panel 6GB : READY\n"
            "✅ Panel 7GB : READY\n"
            "✅ Panel 8GB : READY\n"
            "✅ Panel 9GB : READY\n"
            "✅ Panel 10GB : READY\n"
            "✅ Panel UNLIMITED : READY\n\n"
            "Stok selalu update 24 jam, bosku! 🔥",
            parse_mode="Markdown",
            reply_markup=main_menu_2col())

    elif call.data == "harga":
        bot.send_message(call.message.chat.id,
            "💰 **LIST HARGA PANEL**\n\n"
            "• 1GB - Rp 2.000\n"
            "• 2GB - Rp 3.000\n"
            "• 3GB - Rp 4.000\n"
            "• 4GB - Rp 5.000\n"
            "• 5GB - Rp 6.000\n"
            "• 6GB - Rp 7.000\n"
            "• 7GB - Rp 8.000\n"
            "• 8GB - Rp 9.000\n"
            "• 9GB - Rp 10.000\n"
            "• 10GB - Rp 11.000\n"
            "• UNLIMITED - Rp 13.000\n\n"
            "🛡️ Garansi Full 15 Hari\n"
            "⚡ Aktif 24 Jam Otomatis\n"
            "✅ Amanah & Terpercaya",
            parse_mode="Markdown",
            reply_markup=main_menu_2col())

    elif call.data == "payment":
        bot.send_message(call.message.chat.id,
            "🧾 **PAYMENT**\n\n"
            "• DANA\n"
            "• GOPAY\n"
            "• OVO\n"
            "• QRIS\n\n"
            "Chat OWNER dulu untuk dapetin nomor payment ya bosku!",
            reply_markup=main_menu_2col())

    elif call.data == "cara":
        bot.send_message(call.message.chat.id,
            "📝 **CARA ORDER**\n\n"
            "1. Pilih panel yang mau dibeli di List Harga\n"
            "2. Chat OWNER / CS\n"
            "3. Transfer ke payment yang dikasih\n"
            "4. Kirim bukti TF\n"
            "5. Panel langsung dibuatin, gak pake lama!\n\n"
            "Gampang kan? 🔥",
            reply_markup=main_menu_2col())

    elif call.data == "owner":
        bot.send_message(call.message.chat.id,
            f"👑 **OWNER / CS**\n\n"
            f"Chat langsung: {OWNER_USERNAME}\n"
            f"Fast respon, amanah 100% ✅\n"
            f"Jangan sungkan tanya-tanya dulu ya bosku!",
            reply_markup=main_menu_2col())

    elif call.data == "testi":
        bot.send_message(call.message.chat.id,
            "📣 **TESTIMONI & BUKTI**\n\n"
            "Ribuan customer udah order di ZUAN PANEL.\n"
            "Testi lengkap bisa cek ke OWNER ya bosku!\n\n"
            "Dijamin aman, garansi full!",
            reply_markup=main_menu_2col())

print("Bot jalan...")
bot.infinity_polling()
