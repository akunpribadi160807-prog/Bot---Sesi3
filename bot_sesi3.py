import json, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes


TOKEN = os.getenv("TOKEN", "GANTI_TOKEN_BOT_KE3_LU_DISINI")
OWNER_USERNAME = "ShanXPLD"

FILE = "data_sesi3.json"

if os.path.exists(FILE):
    with open(FILE) as f: DATA = json.load(f)
else:
    DATA = {
        "dana": "0838xxxx",
        "gopay": "0838xxxx",
        "qris_nama": "ZUAN PANEL",
        "stok": {"1GB": 15, "2GB": 8, "UNLIMITED": 5},
        "harga": {"1GB": 2000, "2GB": 4000, "3GB": 6000, "4GB": 8000, "5GB": 9000, "UNLIMITED": 10000}
    }

def save():
    with open(FILE, "w") as f: json.dump(DATA, f)

def is_owner(update):
    return update.effective_user.username and update.effective_user.username.lower() == OWNER_USERNAME.lower()

def menu_utama():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 CEK STOK", callback_data="stok")],
        [InlineKeyboardButton("💰 LIST HARGA", callback_data="harga")],
        [InlineKeyboardButton("💳 PAYMENT / BAYAR", callback_data="payment")],
        [InlineKeyboardButton("🛒 CARA ORDER", callback_data="order")],
        [InlineKeyboardButton("👤 OWNER / CS", callback_data="owner")],
    ])

def tombol_balik():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 KEMBALI KE MENU", callback_data="menu")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 HALO! SELAMAT DATANG DI\n⚡ ZUAN PANEL - BOT KE-3 ⚡\n\nPanel murah, aman, garansi full!\nPencet tombol di bawah ya bang 👇", reply_markup=menu_utama())

async def tombol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "menu":
        await query.edit_message_text("👋 BALIK KE MENU UTAMA\n\nPilih lagi bang 👇", reply_markup=menu_utama())
    elif query.data == "stok":
        teks = "☁️ INFO STOK PANEL ☁️\n\n"
        for k,v in DATA["stok"].items():
            teks += f"⚡ PANEL {k}\n- Sisa : {v} stok\n- Harga : Rp {DATA['harga'].get(k,0):,}\n\n"
        await query.edit_message_text(teks, reply_markup=tombol_balik())
    elif query.data == "harga":
        teks = "💰 LIST HARGA ZUAN PANEL 💰\n\n"
        for k,v in DATA["harga"].items():
            teks += f"{k} : Rp {v:,}\n"
        teks += "\nSemua garansi 15 hari!"
        await query.edit_message_text(teks, reply_markup=tombol_balik())
    elif query.data == "payment":
        teks = f"💳 PAYMENT ZUAN PANEL 💳\n\n📱 DANA : {DATA['dana']}\n📱 GOPAY : {DATA['gopay']}\n📷 QRIS : A.N {DATA['qris_nama']}\n\n⚠️ Transfer sesuai harga, screenshot bukti, terus pencet tombol bawah!"
        kb = [[InlineKeyboardButton("✅ UDAH TRANSFER, KIRIM BUKTI", url=f"https://t.me/{OWNER_USERNAME}")],[InlineKeyboardButton("🔙 KEMBALI KE MENU", callback_data="menu")]]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(kb))
    elif query.data == "order":
        await query.edit_message_text("🛒 CARA ORDER 🛒\n\n1. Pilih paket\n2. Pencet PAYMENT, transfer dulu\n3. Screenshot bukti\n4. Pencet UDAH TRANSFER\n5. Panel langsung dikirim!", reply_markup=tombol_balik())
    elif query.data == "owner":
        await query.edit_message_text(f"👤 OWNER / CS\n\nChat langsung:\n@{OWNER_USERNAME}\n\nFast respon 24 jam!", reply_markup=tombol_balik())

async def setdana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    if not context.args: await update.message.reply_text("Cara: /setdana 0838xxxx"); return
    DATA["dana"] = context.args[0]; save()
    await update.message.reply_text(f"✅ DANA diubah jadi: {DATA['dana']}")
async def setgopay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    if not context.args: await update.message.reply_text("Cara: /setgopay 0838xxxx"); return
    DATA["gopay"] = context.args[0]; save()
    await update.message.reply_text(f"✅ GOPAY diubah jadi: {DATA['gopay']}")
async def setstok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    if len(context.args) < 2: await update.message.reply_text("Cara: /setstok 1GB 20"); return
    DATA["stok"][context.args[0].upper()] = int(context.args[1]); save()
    await update.message.reply_text(f"✅ Stok {context.args[0].upper()} jadi {context.args[1]}")
async def setharga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    if len(context.args) < 2: await update.message.reply_text("Cara: /setharga 1GB 2000"); return
    DATA["harga"][context.args[0].upper()] = int(context.args[1]); save()
    await update.message.reply_text(f"✅ Harga {context.args[0].upper()} jadi Rp {int(context.args[1]):,}")
async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    await update.message.reply_text("🔧 PERINTAH OWNER:\n\n/setdana 0838xxxx\n/setgopay 0838xxxx\n/setstok 1GB 20\n/setharga 1GB 2500")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", help_admin))
app.add_handler(CommandHandler("setdana", setdana))
app.add_handler(CommandHandler("setgopay", setgopay))
app.add_handler(CommandHandler("setstok", setstok))
app.add_handler(CommandHandler("setharga", setharga))
app.add_handler(CallbackQueryHandler(tombol))
print("Bot Sesi 3 jalan di Hosting...")
app.run_polling()
