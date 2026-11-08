import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ============ TEKS MENU BARU - UDAH DIP OLES ============

START_TEXT = """
✨ ═══════════════════ ✨
   ZUAN PANEL - BOT KE-3
✨ ═══════════════════ ✨

👋 Halo, Selamat Datang Bosku!

Terima kasih sudah mampir ke toko kami.
Di sini semua serba OTOMATIS, tanpa antri, tanpa drama nunggu admin.

⚡ AKTIF 24 JAM
💰 MULAI Rp 2.000 AJA
🛡️ GARANSI FULL 15 HARI
📦 STOK SELALU UPDATE

👇 Silakan pilih menu di bawah ini:
"""

STOK_TEXT = """
📦 ═══ INFO STOK TERBARU ═══ 📦

🟢 PANEL 1GB : 15 Stok
🟢 PANEL 2GB : 11 Stok
🟢 PANEL 3GB : 9 Stok
🟢 PANEL 4GB : 7 Stok
🟢 PANEL 5GB : 5 Stok
🟢 UNLIMITED : 5 Stok

✅ Stok ready, langsung gas!
Jangan sampai kehabisan, stok menipis tiap hari.
"""

HARGA_TEXT = """
💰 ═══ LIST HARGA ZUAN PANEL ═══ 💰

🥉 1GB — Rp 2.000
🥈 2GB — Rp 4.000
🥇 3GB — Rp 6.000
💎 4GB — Rp 8.000
👑 5GB — Rp 9.000
🔥 UNLIMITED — Rp 10.000

✨ Semua paket sudah termasuk:
- Garansi 15 Hari
- Full Akses Admin
- Free Req Username

Mau yang mana bosku? 👇
"""

PAYMENT_TEXT = """
🧾 ═══ PAYMENT ZUAN PANEL ═══ 🧾

Silakan transfer ke salah satu di bawah ini:

💙 DANA
0858-7225-7850
a/n MUHAMAD IKHSANDI AKBAR

💚 GOPAY
0858-7225-7850
a/n MUHAMAD IKHSANDI AKBAR

📷 QRIS
(Kirim QRIS, scan langsung)

⚠️ WAJIB:
Setelah bayar, kirim bukti TF ke OWNER
dengan format: #ORDER - Nama - Paket

Orderan akan diproses 1-5 menit.
"""

ORDER_TEXT = """
📝 ═══ CARA ORDER ═══ 📝

Gampang banget, 3 langkah doang:

1️⃣ Pilih paket di LIST HARGA
2️⃣ Bayar ke PAYMENT
3️⃣ Kirim bukti ke OWNER / CS

Contoh format:
#ORDER - Budi - 1GB

Langsung klik tombol OWNER di bawah ya bosku!
"""

OWNER_TEXT = """
👑 ═══ OWNER / CS ═══ 👑

Butuh bantuan? Chat langsung owner kami:

👤 Owner: @ShanxPLD
⏰ Fast Respon 07.00 - 23.00 WIB

Jangan sungkan, tanya-tanya dulu juga boleh!
"""

TESTI_TEXT = """
📢 ═══ TESTIMONI ZUAN PANEL ═══ 📢

⭐⭐⭐⭐⭐
"Order jam 2 pagi masih dilayani bot, 1 menit langsung aktif! Mantap!" - Rizky

⭐⭐⭐⭐⭐
"Udah 3x order di sini, gak pernah gagal. Garansi beneran di claim!" - Andi

⭐⭐⭐⭐⭐
"Harga paling murah se-Telegram, adminnya ramah banget!" - Fajar

Mau jadi testimoni selanjutnya?
Langsung order sekarang! 👇
"""

# ============ TOMBOL MENU ============

MAIN_KEYBOARD = [
    [InlineKeyboardButton("📦  CEK STOK PANEL", callback_data="stok")],
    [InlineKeyboardButton("💰  LIST HARGA", callback_data="harga"),
     InlineKeyboardButton("🧾  PAYMENT", callback_data="payment")],
    [InlineKeyboardButton("📝  CARA ORDER", callback_data="order"),
     InlineKeyboardButton("👑  OWNER / CS", callback_data="owner")],
    [InlineKeyboardButton("📢  TESTIMONI & BUKTI", callback_data="testi")],
]

BACK_KEYBOARD = [
    [InlineKeyboardButton("⬅️  KEMBALI KE MENU", callback_data="start")],
    [InlineKeyboardButton("🛒  LANGSUNG ORDER", callback_data="owner")],
]

OWNER_KEYBOARD = [
    [InlineKeyboardButton("💬  CHAT OWNER SEKARANG", url="https://t.me/ShanxPLD")],
    [InlineKeyboardButton("⬅️  KEMBALI KE MENU", callback_data="start")],
]

# ============ HANDLER ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, reply_markup=InlineKeyboardMarkup(MAIN_KEYBOARD))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start":
        await query.edit_message_text(START_TEXT, reply_markup=InlineKeyboardMarkup(MAIN_KEYBOARD))
    elif data == "stok":
        await query.edit_message_text(STOK_TEXT, reply_markup=InlineKeyboardMarkup(BACK_KEYBOARD))
    elif data == "harga":
        await query.edit_message_text(HARGA_TEXT, reply_markup=InlineKeyboardMarkup(BACK_KEYBOARD))
    elif data == "payment":
        await query.edit_message_text(PAYMENT_TEXT, reply_markup=InlineKeyboardMarkup(BACK_KEYBOARD))
    elif data == "order":
        await query.edit_message_text(ORDER_TEXT, reply_markup=InlineKeyboardMarkup(BACK_KEYBOARD))
    elif data == "owner":
        await query.edit_message_text(OWNER_TEXT, reply_markup=InlineKeyboardMarkup(OWNER_KEYBOARD))
    elif data == "testi":
        await query.edit_message_text(TESTI_TEXT, reply_markup=InlineKeyboardMarkup(BACK_KEYBOARD))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot ZUAN PANEL jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
