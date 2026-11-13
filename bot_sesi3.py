import os
import requests
import time
import telebot
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
KASERA_API_KEY = os.getenv("KASERA_API_KEY")
KASERA_BASE = "https://pay.kasera.id/v1"
bot = telebot.TeleBot(TOKEN)

# ===== GANTI LINK BANNER LU DISINI! =====
# Pake link foto banner robot biru ZUAN PANEL lu!
BANNER_URL = "https://telegra.ph/file/PASTE-LINK-BANNER-LU-DISINI.jpg"
# Kalo mau pake file lokal, ganti jadi "banner.jpg" dan upload banner.jpg ke Github juga

HARGA = {
    "1gb": {"nama": "Panel 1GB", "harga": 5000},
    "5gb": {"nama": "Panel 5GB", "harga": 15000},
    "10gb": {"nama": "Panel 10GB", "harga": 25000},
    "unli": {"nama": "Panel UNLI", "harga": 50000},
}

orders = {}
orders_by_id = {}
# Buat statistik palsu biar keliatan rame, ganti sesuai asli lu
TOTAL_USER = 481
TOTAL_PENDAPATAN = 2438400

def buat_payment_kasera(total, order_id):
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        payload = {"amount": total, "order_id": order_id, "method": "QRIS", "expired": 60}
        r = requests.post(f"{KASERA_BASE}/payment/create", json=payload, headers=headers, timeout=20)
        return r.json()
    except Exception as e:
        print("Error Kasera:", e)
        return None

def cek_payment_kasera(order_id):
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}"}
        r = requests.get(f"{KASERA_BASE}/payment/{order_id}", headers=headers, timeout=20)
        return r.json()
    except:
        return None

# ===== /START - VERSI BANNER KEREN (KAYAK SS KE-2) =====
@bot.message_handler(commands=['start'])
def start(message):
    nama = message.from_user.first_name or "Bang"
    user_id = message.from_user.id
    
    # Teksnya persis kayak yang lu mau, yang ada WELCOME + PROFIL + SALDO + STATISTIK
    caption = (
        f"🌟✦ ━━━━━ 『 WELCOME 』 ━━━━━ ✦🌟\n\n"
        f"┌ 「 👤 PROFIL BOT 」 ── ❞\n"
        f"│ 👑 Owner · ZUAN PANEL\n"
        f"│ 🤖 Name · AUTO ORDER ZUAN PANEL\n"
        f"│ ⚡ Status · BETA · VIP Only\n"
        f"│ 📖 Prefix · /\n"
        f"└──────────────────\n\n"
        f"┌ 「 👛 SALDO ANDA 」 ── ❞\n"
        f"│ 💰 Saldo · Rp 0\n"
        f"│ 💳 Top Up · QRIS Otomatis\n"
        f"└──────────────────\n\n"
        f"┌ 「 📊 STATISTIK 」 ── ❞\n"
        f"│ 👥 Total User · {TOTAL_USER}\n"
        f"│ 💰 Pendapatan · Rp {TOTAL_PENDAPATAN:,}".replace(",", ".") + "\n"
        f"│ 🔥 Stok · READY ALL\n"
        f"└──────────────────\n\n"
        f"┌ 「 👋 Selamat Datang di Bot AUTO ORDER 」 ── ❞\n"
        f"│ ZUAN PANEL!\n"
        f"└──────────────────"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛒 ORDER PANEL", callback_data="menu_order"))
    markup.add(InlineKeyboardButton("💰 TOP UP SALDO", callback_data="menu_topup"))
    markup.add(InlineKeyboardButton("📦 CEK STOK", callback_data="menu_stok"))
    markup.add(InlineKeyboardButton("💬 HUBUNGI ADMIN", url="https://t.me/zuanww"))
    markup.add(InlineKeyboardButton("🌐 WEBSITE KAMI", url="https://zuanpanel.web.id"))

    # Kirim BANNER + Caption, bukan teks polos lagi!
    try:
        if BANNER_URL.startswith("http"):
            img = requests.get(BANNER_URL, timeout=20).content
            bot.send_photo(message.chat.id, BytesIO(img), caption=caption, reply_markup=markup)
        else:
            # Kalo pake file lokal banner.jpg
            with open(BANNER_URL, 'rb') as f:
                bot.send_photo(message.chat.id, f, caption=caption, reply_markup=markup)
    except Exception as e:
        print("Gagal kirim banner:", e)
        # Fallback kalo banner gagal, kirim teks aja
        bot.send_message(message.chat.id, caption, reply_markup=markup)

# ===== MENU ORDER - KELUARIN LIST HARGA =====
@bot.callback_query_handler(func=lambda c: c.data == "menu_order")
def menu_order(call):
    markup = InlineKeyboardMarkup()
    for key, val in HARGA.items():
        markup.add(InlineKeyboardButton(f"📦 {val['nama']} - Rp {val['harga']:,}".replace(",", "."), callback_data=f"order_{key}"))
    markup.add(InlineKeyboardButton("🔙 KEMBALI", callback_data="back_start"))
    bot.send_message(call.message.chat.id, "🛒 *PILIH PANEL LU BANG! GAS!* 🔥\n\nPanel murah, spek gacor, anti lemot!", parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back_start")
def back_start(call):
    # Balik ke /start lagi biar banner muncul lagi
    call.message.text = "/start"
    start(call.message)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("order_"))
def handle_order(call):
    paket_key = call.data.replace("order_", "")
    paket = HARGA.get(paket_key)
    if not paket: return
    orders[call.from_user.id] = {"step": "username", "paket": paket_key, "paket_nama": paket["nama"], "harga": paket["harga"]}
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
        f"📦 *LU PILIH {paket['nama'].upper()}! PILIHAN YANG TEPAT!* 🔥\n\n"
        f"👤 *Kirim Username Panel yang lu mau!*\nContoh: `zuanww`",
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    user_id = message.from_user.id
    data = orders[user_id]
    text = message.text.strip()
    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id, f"✅ *USERNAME `{text}` DIAMANKAN!*\n\n📧 *Kirim Email lu!*\nContoh: `email@gmail.com`", parse_mode="Markdown")
        return
    if data["step"] == "email":
        data["email"] = text
        data["step"] = "bayar"
        order_id = f"INV-QRIS-ZUAN-{int(time.time())}-{user_id}"
        data["order_id"] = order_id
        orders_by_id[order_id] = data
        bot.send_message(message.chat.id, "⏳ *Lagi bikinin QRIS lu, sabar bentar...* 🔥", parse_mode="Markdown")
        pay = buat_payment_kasera(data["harga"], order_id)
        qr_url = None
        if pay and pay.get("data"):
            qr_url = pay["data"].get("qr_image") or pay["data"].get("qr_url")

        caption = (
            f"🧾 *INVOICE - ZUANPANEL.WEB.ID*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 *Produk:* {data['paket_nama']} (x1)\n"
            f"👤 *Username:* `{data['username_panel']}`\n"
            f"🆔 *Order ID:* `{order_id}`\n"
            f"💰 *Total Bayar:* Rp {data['harga']:,}".replace(",", ".") + "\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"⚠️ *BAYAR PAS SESUAI NOMINAL!*\n"
            f"⏰ *Expired:* 60 Menit\n\n"
            f"✅ *Udah bayar? Gas tekan tombol di bawah!*"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ CEK STATUS PEMBAYARAN", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("❌ BATALKAN PESANAN", callback_data=f"batal_{order_id}"))
        try:
            if qr_url and qr_url.startswith("http"):
                img_data = requests.get(qr_url, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img_data), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

        username_tele = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        pesan_admin = (
            f"🔔 *ADA ORDERAN BARU MASUK!* 🔥\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 *User:* {username_tele}\n"
            f"📦 *Paket:* {data['paket_nama']}\n"
            f"👤 *Username Panel:* `{data['username_panel']}`\n"
            f"📧 *Email:* `{data['email']}`\n"
            f"💰 *Total:* Rp {data['harga']:,}".replace(",", ".") + "\n"
            f"📊 *Status:* ⏳ Menunggu Pembayaran\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        try: bot.send_message(ADMIN_ID, pesan_admin, parse_mode="Markdown")
        except: pass
        return

@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Order tidak ditemukan!"); return
        res = cek_payment_kasera(order_id)
        status = ""
        if res and res.get("data"): status = res["data"].get("status", "").lower()
        if status in ["paid", "success", "lunas", "completed"]:
            bot.send_message(call.message.chat.id, f"✅ *PEMBAYARAN LU UDAH MASUK!* 🔥\n\n📦 Panel {data['paket_nama']} lagi diproses!", parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "⏳ Belum masuk bang!")
            bot.send_message(call.message.chat.id, f"⏳ *BELUM MASUK BANG!*\n\n💰 Total: Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 Order ID: `{order_id}`", parse_mode="Markdown")
        return
    if call.data.startswith("batal_"):
        order_id = call.data.replace("batal_", "")
        if order_id in orders_by_id: del orders_by_id[order_id]
        for uid in list(orders.keys()):
            if orders[uid].get("order_id") == order_id: del orders[uid]
        bot.edit_message_text(f"❌ *PESANAN DIBATALKAN!*\n\nMau order lagi? Ketik /start aja!", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Pesanan dibatalkan!")
        return

print("✅ ZUANPANEL BOT ONLINE - VERSI BANNER!")
bot.infinity_polling()
