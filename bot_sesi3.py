import os
import requests
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "849370608"))
KASERA_API_KEY = os.getenv("KASERA_API_KEY")
KASERA_BASE = "https://api.kasera.id"

bot = telebot.TeleBot(TOKEN)

HARGA = {
    "1gb": {"nama": "Panel 1GB", "harga": 4000},
    "2gb": {"nama": "Panel 2GB", "harga": 6000},
    "3gb": {"nama": "Panel 3GB", "harga": 8000},
    "4gb": {"nama": "Panel 4GB", "harga": 10000},
    "5gb": {"nama": "Panel 5GB", "harga": 12000},
    "6gb": {"nama": "Panel 6GB", "harga": 15000},
    "7gb": {"nama": "Panel 7GB", "harga": 18000},
    "8gb": {"nama": "Panel 8GB", "harga": 20000},
    "9gb": {"nama": "Panel 9GB", "harga": 22000},
    "10gb": {"nama": "Panel 10GB", "harga": 25000},
    "unli": {"nama": "Panel UNLI", "harga": 30000},
}

orders = {}

# ================= TAMPILAN LAMA - TETEP! =================
def menu_awal():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🟢 Menu Layanan", callback_data="menu_layanan"))
    markup.add(InlineKeyboardButton("🔵 Install Panel Free", callback_data="install_free"))
    markup.add(InlineKeyboardButton("🔴 Owner Bot", callback_data="owner"))
    markup.add(InlineKeyboardButton("🟢 Channel Testi ↗️", url="https://t.me/ZuanTesti"))
    return markup

def teks_welcome():
    return (
        "🌟✦ ━━━━ 『 WELCOME 』 ━━━━ ✦🌟\n\n"
        "┌── 「 PROFIL BOT 」 ── ”\n"
        "│ Owner · ZUAN PANEL\n"
        "│ 🤖 Name · AUTO ORDER ZUAN PANEL\n"
        "│ ⚡ Status · BETA · VIP Only\n"
        "│ 📖 Prefix · /\n"
        "└──────────────\n\n"
        "┌── 「 📊 STATISTIK 」 ── ”\n"
        "│ 👥 Total User · 481\n"
        "│ 💰 Pendapatan · Rp 2.438.400\n"
        "└──────────────\n\n"
        "[ 👋 ] Demm Bro, Welcome To Bot AUTO ORDER ZUAN PANEL!"
    )

# ===== INI KUNCI BIAR GAK NUMPUK! NGEDIT, BUKAN KIRIM BARU! =====
def edit_pesan(c, teks, markup=None):
    try:
        # Kalo pesan nya foto (yang /start), edit caption nya
        if c.message.photo:
            bot.edit_message_caption(caption=teks, chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.edit_message_text(teks, chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except:
        # Kalo gagal edit (teks sama), kirim baru
        try:
            bot.send_message(c.message.chat.id, teks, reply_markup=markup, parse_mode="Markdown")
        except:
            pass

@bot.message_handler(commands=['start'])
def start(m):
    try:
        with open("foto.jpg", "rb") as foto:
            bot.send_photo(m.chat.id, foto, caption=teks_welcome(), reply_markup=menu_awal())
    except:
        bot.send_message(m.chat.id, teks_welcome(), reply_markup=menu_awal())

@bot.callback_query_handler(func=lambda c: True)
def semua_callback(c):
    chat_id = c.message.chat.id
    data = c.data
    bot.answer_callback_query(c.id)

    if data == "menu_layanan":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔵 CEK STOK", callback_data="zuan_stok"))
        markup.add(InlineKeyboardButton("🟢 LIST HARGA", callback_data="zuan_harga"))
        markup.add(InlineKeyboardButton("🛒 ORDER PANEL", callback_data="zuan_order"))
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="back_home"))
        edit_pesan(c, "🟢 *MENU LAYANAN ZUAN PANEL*\n\nPilih yang mau lu cek:", markup)

    elif data == "back_home":
        edit_pesan(c, teks_welcome(), menu_awal())

    elif data == "install_free":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="back_home"))
        edit_pesan(c, "🔵 *INSTALL PANEL FREE*\n\n┌── 「 SYARAT 」 ── ”\n│ 1. Join Channel Testi\n│ 2. SS Bot ini kirim ke Owner\n│ 3. Tunggu di proses!\n└──────────────", markup)

    elif data == "owner":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 Chat Owner", url="https://t.me/ZuanPanel"))
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="back_home"))
        edit_pesan(c, "🔴 *OWNER BOT*\n\nOwner: ZUAN PANEL\nFast Respon 24 Jam!", markup)

    elif data == "zuan_stok":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 Gas Order", callback_data="zuan_order"))
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="menu_layanan"))
        edit_pesan(c, "📦 *STOK PANEL*\n\n┌── 「 STOK READY 」 ── ”\n│ ✅ 1GB - 10GB READY\n│ ✅ UNLI READY\n└──────────────\n\nGas order bang!", markup)

    elif data == "zuan_harga":
        # ===== LIST HARGA BARU, CAKEP! =====
        teks = (
            "💰 *LIST HARGA ZUAN PANEL*\n\n"
            "┌── 「 PANEL RAM 」 ── ”\n"
            "│ 🟢 1GB  · Rp 4.000\n"
            "│ 🟢 2GB  · Rp 6.000\n"
            "│ 🟢 3GB  · Rp 8.000\n"
            "│ 🟢 4GB  · Rp 10.000\n"
            "│ 🟢 5GB  · Rp 12.000\n"
            "│ 🟢 6GB  · Rp 15.000\n"
            "│ 🟢 7GB  · Rp 18.000\n"
            "│ 🟢 8GB  · Rp 20.000\n"
            "│ 🟢 9GB  · Rp 22.000\n"
            "│ 🟢 10GB · Rp 25.000\n"
            "└──────────────\n\n"
            "┌── 「 PANEL UNLI 」 ── ”\n"
            "│ 🔥 UNLIMITED · Rp 30.000\n"
            "└──────────────\n\n"
            "💳 QRIS All Payment\n"
            "⚡ Garansi 15 Hari!"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 ORDER SEKARANG", callback_data="zuan_order"))
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="menu_layanan"))
        edit_pesan(c, teks, markup)

    elif data == "zuan_order":
        # ===== ORDER 2 KOLOM, BIAR GAK PANJANG! =====
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("1GB · 4k", callback_data="buy_1gb"),
            InlineKeyboardButton("2GB · 6k", callback_data="buy_2gb")
        )
        markup.add(
            InlineKeyboardButton("3GB · 8k", callback_data="buy_3gb"),
            InlineKeyboardButton("4GB · 10k", callback_data="buy_4gb")
        )
        markup.add(
            InlineKeyboardButton("5GB · 12k", callback_data="buy_5gb"),
            InlineKeyboardButton("6GB · 15k", callback_data="buy_6gb")
        )
        markup.add(
            InlineKeyboardButton("7GB · 18k", callback_data="buy_7gb"),
            InlineKeyboardButton("8GB · 20k", callback_data="buy_8gb")
        )
        markup.add(
            InlineKeyboardButton("9GB · 22k", callback_data="buy_9gb"),
            InlineKeyboardButton("10GB · 25k", callback_data="buy_10gb")
        )
        markup.add(InlineKeyboardButton("🔥 UNLI · 30k", callback_data="buy_unli"))
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="menu_layanan"))
        edit_pesan(c, "🛒 *PILIH PANEL LU:*\n\nPencet yang mau lu beli!", markup)

    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = HARGA[key]
        orders[chat_id] = {"paket": key, "nama": item['nama'], "harga": item['harga']}
        bot.send_message(chat_id, f"Lu mau beli *{item['nama']}* Rp {item['harga']:,}\n\nKirim *Username Panel*:\nContoh: `zuan123`", parse_mode="Markdown")
        bot.register_next_step_handler(c.message, proses_username)

    elif data == "buat_qris":
        buat_qris(c)

    elif data == "cek_bayar":
        cek_bayar(c)

def proses_username(m):
    chat_id = m.chat.id
    username = m.text.strip().lower().replace(" ", "")
    if len(username) < 4:
        bot.send_message(chat_id, "❌ Username minimal 4 huruf! Kirim lagi:")
        bot.register_next_step_handler(m, proses_username)
        return
    orders[chat_id]["username"] = username
    bot.send_message(chat_id, f"✅ Username: `{username}`\n\nKirim *Email* buat login panel:", parse_mode="Markdown")
    bot.register_next_step_handler(m, proses_email)

def proses_email(m):
    chat_id = m.chat.id
    email = m.text.strip()
    if "@" not in email:
        bot.send_message(chat_id, "❌ Email gak valid! Kirim lagi:")
        bot.register_next_step_handler(m, proses_email)
        return
    orders[chat_id]["email"] = email
    d = orders[chat_id]
    teks = f"📋 *KONFIRMASI ORDER*\n\nPanel: {d['nama']}\nUsername: `{d['username']}`\nEmail: `{d['email']}`\nTotal: Rp {d['harga']:,}\n\nLanjut bikin QRIS?"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ YA, BUAT QRIS", callback_data="buat_qris"))
    bot.send_message(chat_id, teks, parse_mode="Markdown", reply_markup=markup)

def buat_qris(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    bot.send_message(chat_id, f"⏳ Lagi bikin QRIS Rp {d['harga']:,}...")
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        payload = {"amount": d['harga'], "reference": f"ZUAN-{chat_id}-{int(time.time())}", "description": f"Order {d['nama']} - {d['username']}"}
        r = requests.post(f"{KASERA_BASE}/v1/payment", json=payload, headers=headers, timeout=15)
        res = r.json()
        qris_url = res.get("data", {}).get("qr_url") or "https://api.qrserver.com/v1/create-qr-code/?data=ZUAN"
        d["reference"] = payload["reference"]
    except Exception as e:
        print("Kasera Error:", e)
        qris_url = "https://api.qrserver.com/v1/create-qr-code/?data=ZUAN"
        d["reference"] = f"ZUAN-{chat_id}-{int(time.time())}"
    teks = f"💳 *SCAN QRIS INI!*\n\nPanel: {d['nama']}\nUsername: `{d['username']}`\nTotal: Rp {d['harga']:,}\nRef: `{d['reference']}`\n\nAbis bayar klik CEK PEMBAYARAN!"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍 CEK PEMBAYARAN", callback_data="cek_bayar"))
    try:
        bot.send_photo(chat_id, qris_url, caption=teks, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(chat_id, teks, parse_mode="Markdown", reply_markup=markup)
    try:
        bot.send_message(ADMIN_ID, f"🔔 ORDER BARU!\nUser: @{c.from_user.username}\nPanel: {d['nama']}\nUsername: `{d['username']}`\nEmail: `{d['email']}`\nTotal: Rp {d['harga']:,}\nStatus: Nunggu Bayar")
    except:
        pass

def cek_bayar(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    bot.answer_callback_query(c.id, "Ngecek...")
    lunas = False
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}"}
        r = requests.get(f"{KASERA_BASE}/v1/payment/{d.get('reference')}", headers=headers, timeout=10)
        if "paid" in str(r.json()).lower() or "success" in str(r.json()).lower():
            lunas = True
    except:
        pass
    if not lunas:
        bot.send_message(chat_id, "❌ Belum terbayar! Bayar dulu, tunggu 1 menit, klik lagi!")
        return
    bot.send_message(chat_id, "✅ *PEMBAYARAN BERHASIL!*\n\nPanel lu lagi disiapin sama Admin!\nTunggu ya, nanti Admin kirim detail login nya ke sini!", parse_mode="Markdown")
    try:
        bot.send_message(ADMIN_ID, f"💰 *UDAH LUNAS! TOLONG BIKININ MANUAL!*\n\nUser: @{c.from_user.username} (ID: {chat_id})\nPanel: {d['nama']}\nUsername: `{d['username']}`\nEmail: `{d['email']}`\nTotal: Rp {d['harga']:,}")
    except:
        pass

print("Bot jalan! ZUAN PANEL FIX READY!")
bot.infinity_polling()
