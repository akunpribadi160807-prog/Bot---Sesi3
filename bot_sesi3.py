import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
bot = telebot.TeleBot(TOKEN)

OWNER_USERNAME = "@ShanXPLD"
OWNER_WA = "083169944241"

user_order = {}

PRODUK = {
    "Admin Panel": 3000,
    "Panel Pterodactyl": 2000,
    "Panel Pterodactyl Legal": 5000,
    "Reseller Panel": 10000,
    "Reseller Panel Legal": 13000,
    "Panel 1GB": 2000, "Panel 2GB": 3000, "Panel 3GB": 4000,
    "Panel 4GB": 5000, "Panel 5GB": 6000, "Panel 6GB": 7000,
    "Panel 7GB": 8000, "Panel 8GB": 9000, "Panel 9GB": 10000,
    "Panel 10GB": 11000, "Panel UNLIMITED": 13000,
}

def format_rp(n):
    return f"Rp {n:,}".replace(",", ".")

# INI KUNCINYA BANG: ReplyKeyboard, 1 tombol = 1 baris = FULL 1 KOTAK
def kb_utama():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🟢 Menu Layanan"))
    kb.add(KeyboardButton("🔵 Install Panel Free"))
    kb.add(KeyboardButton("🔴 Owner Bot"))
    kb.add(KeyboardButton("🟢 Channel Testi"))
    kb.add(KeyboardButton("🔵 Channel Info"))
    return kb

def kb_layanan():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔵 Admin Panel"))
    kb.add(KeyboardButton("🔵 Panel Pterodactyl"))
    kb.add(KeyboardButton("🔵 Panel Pterodactyl Legal"))
    kb.add(KeyboardButton("🔵 Reseller Panel"))
    kb.add(KeyboardButton("🔵 Reseller Panel Legal"))
    kb.add(KeyboardButton("🟢 Panel 1GB - 10GB / UNLI"))
    kb.add(KeyboardButton("🔴 ⬅ Kembali"))
    return kb

def kb_panel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for nama in ["Panel 1GB","Panel 2GB","Panel 3GB","Panel 4GB","Panel 5GB","Panel 6GB","Panel 7GB","Panel 8GB","Panel 9GB","Panel 10GB","Panel UNLIMITED"]:
        kb.add(KeyboardButton(f"🔵 {nama}"))
    kb.add(KeyboardButton("🔴 ⬅ Kembali"))
    return kb

def kb_bayar():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🟢 Bayar QRIS"))
    kb.add(KeyboardButton("🔵 Bayar Saldo Bot"))
    kb.add(KeyboardButton("🔴 Batal"))
    return kb

def kb_batal():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔴 Batal Order"))
    return kb

WELCOME_TEXT = """🌟 ━━━━ [ WELCOME ] ━━━━ 🌟
👑 PROFIL BOT
👤 Owner : ZUAN PANEL
📛 Name : AUTO ORDER ZUAN PANEL
⚡ Status : BETA - VIP Only
📌 Prefix : /

📊 STATISTIK
👥 Total User : 481
💰 Pendapatan : Rp 2.438.400

[ 👋 ] Demm Bro, Welcome To Bot AUTO ORDER ZUAN PANEL!"""

@bot.message_handler(commands=['start'])
def start(message):
    user_order.pop(message.chat.id, None)
    try:
        with open("banner.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=WELCOME_TEXT, reply_markup=kb_utama())
    except:
        bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=kb_utama())

@bot.message_handler(func=lambda m: True)
def semua_chat(message):
    cid = message.chat.id
    text = message.text.strip() if message.text else ""
    # Bersihin emoji biar gampang dibaca
    bersih = text.replace("🟢 ","").replace("🔵 ","").replace("🔴 ","").replace("⬅ ","").strip()

    # LAGI NGETIK USERNAME?
    order = user_order.get(cid)
    if order and order.get("step") == "username":
        if bersih in ["Batal Order", "Batal", "Kembali"]:
            user_order.pop(cid, None)
            bot.send_message(cid, "❌ Order dibatalkan!", reply_markup=kb_utama())
            return
        username = text.strip()
        if len(username) < 5:
            bot.send_message(cid, f"❌ Kependekan bosku! '{username}' cuma {len(username)} huruf.\nMinimal 5-9 huruf! Contoh: PanelZuan", reply_markup=kb_batal())
            return
        if len(username) > 9:
            bot.send_message(cid, f"❌ Kepanjangan bosku! '{username}' udah {len(username)} huruf.\nMaksimal 9 huruf! Contoh: PanelZuan", reply_markup=kb_batal())
            return
        if " " in username:
            bot.send_message(cid, "❌ Username gak boleh ada spasi! Contoh: PanelZuan", reply_markup=kb_batal())
            return
        order["username"] = username
        order["step"] = "bayar"
        bot.send_message(cid, f"💳 PILIH METODE PEMBAYARAN\n\n🛍️ Item : {order['produk']} ({username})\n💰 Total : {format_rp(order['harga'])}\n💰 Saldo Bot kamu : Rp 0", reply_markup=kb_bayar())
        return

    if bersih == "Menu Layanan":
        bot.send_message(cid, "🛍️ ━━━ DAFTAR MENU LAYANAN BOT ━━━ 🛍️\n\nSilahkan Pilih Produk Yang Ingin Anda Order.", reply_markup=kb_layanan())
    elif bersih == "Panel 1GB - 10GB / UNLI":
        bot.send_message(cid, "💰 LIST HARGA PANEL\nPilih panel yang mau dibeli bosku!", reply_markup=kb_panel())
    elif bersih == "Install Panel Free":
        bot.send_message(cid, "🎁 INSTALL PANEL FREE\n\nChat OWNER dulu ya bosku!\nSyarat: Follow Channel dulu!", reply_markup=kb_utama())
    elif bersih == "Owner Bot":
        bot.send_message(cid, f"📞 ━━━ CONTACT OWNER BOT ━━━\n\n👤 Name : ZUAN PANEL\n📱 Whatsapp : {OWNER_WA}\n✈️ Telegram : {OWNER_USERNAME}", reply_markup=kb_utama())
    elif bersih == "Channel Testi":
        bot.send_message(cid, "📣 Channel Testi: https://t.me/ZUANPANEL", reply_markup=kb_utama())
    elif bersih == "Channel Info":
        bot.send_message(cid, "📣 Channel Info: https://t.me/ZUANPANEL", reply_markup=kb_utama())
    elif bersih == "Kembali":
        bot.send_message(cid, "Balik ke menu utama!", reply_markup=kb_utama())
    elif bersih == "Batal" or bersih == "Batal Order":
        user_order.pop(cid, None)
        bot.send_message(cid, "❌ Order dibatalkan!", reply_markup=kb_utama())
    elif bersih == "Bayar QRIS":
        if not order:
            bot.send_message(cid, "Order tidak ditemukan, /start lagi ya!", reply_markup=kb_utama())
            return
        bot.send_message(cid, f"📱 BAYAR VIA QRIS\n\nItem : {order['produk']} ({order.get('username','')})\nTotal : {format_rp(order['harga'])}\n\nChat OWNER untuk dapetin QRIS: {OWNER_USERNAME}", reply_markup=kb_utama())
    elif bersih == "Bayar Saldo Bot":
        bot.send_message(cid, "💳 Saldo Bot kamu : Rp 0\nSaldo kurang! Topup dulu ke OWNER ya!", reply_markup=kb_utama())
    elif bersih in PRODUK or bersih.replace("Panel ","Panel ") in PRODUK:
        # Cari nama produk yang bener
        nama_produk = None
        for k in PRODUK:
            if k in text or k == bersih:
                nama_produk = k
                break
        if not nama_produk:
            # Coba cocokin tanpa emoji
            for k in PRODUK:
                if bersih == k:
                    nama_produk = k
        if nama_produk:
            user_order[cid] = {"produk": nama_produk, "harga": PRODUK[nama_produk], "step": "username"}
            bot.send_message(cid, f"🛒 BELI {nama_produk.upper()}\n\nHarga : {format_rp(PRODUK[nama_produk])}\n\n✏️ Silahkan Kirim Username Untuk Panel Yang Ingin Kamu Beli Dengan Minimal 5-9 Huruf.\n\nContoh : PanelZuan, ZuanStore", reply_markup=kb_batal())
    else:
        # Kalo ketik sembarangan, biarin aja, jangan spam
        pass

print("Bot ZUAN ReplyKeyboard ala WANZZ jalan...")
bot.infinity_polling()
