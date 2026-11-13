import os
import requests
import time
import telebot
import urllib.parse
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

try:
    from PIL import Image, ImageDraw, ImageFont
    ADA_PIL = True
except:
    ADA_PIL = False

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
KASERA_API_KEY = os.getenv("KASERA_API_KEY")
KASERA_BASE = "https://pay.kasera.id/v1"
bot = telebot.TeleBot(TOKEN)

try:
    bot.delete_my_commands()
    bot.set_my_commands([])
    bot.set_chat_menu_button(menu_button=None)
except:
    pass

# ===== HARGA PANEL =====
HARGA = {
    "1gb": {"nama": "Panel 1GB", "harga": 5000, "ram": 1024},
    "5gb": {"nama": "Panel 5GB", "harga": 15000, "ram": 5120},
    "10gb": {"nama": "Panel 10GB", "harga": 25000, "ram": 10240},
    "unli": {"nama": "Panel UNLI", "harga": 50000, "ram": 0},
}

# Simpan order sementara
orders = {}  # user_id -> {step, paket, username_panel, email, order_id, ...}
orders_by_id = {}

# ===== FUNGSI BUAT QRIS KASERA =====
def buat_payment_kasera(total, order_id):
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "amount": total,
            "order_id": order_id,
            "method": "QRIS",
            "expired": 60
        }
        r = requests.post(f"{KASERA_BASE}/payment/create", json=payload, headers=headers, timeout=20)
        data = r.json()
        return data
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

# ===== /START - TEKS BARU LEBIH KEREN =====
@bot.message_handler(commands=['start'])
def start(message):
    nama = message.from_user.first_name or "Bang"
    teks = (
        f"👋 *HALO {nama.upper()}! SELAMAT DATANG DI ZUANPANEL.WEB.ID* 🔥\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⚡ *FAST RESPON | AMANAH & TERPERCAYA*\n"
        f"⚡ *STOK SELALU READY | AUTO PROSES*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🛒 *MAU ORDER PANEL? GAS PILIH DI BAWAH!*\n"
        f"📦 Panel murah, spek gacor, anti lemot!\n\n"
        f"👇 *GAS ORDER SEKARANG, JANGAN CUMA DILIHAT!*"
    )
    markup = InlineKeyboardMarkup()
    for key, val in HARGA.items():
        markup.add(InlineKeyboardButton(f"📦 {val['nama']} - Rp {val['harga']:,}".replace(",", "."), callback_data=f"order_{key}"))
    markup.add(InlineKeyboardButton("💬 HUBUNGI ADMIN", url="https://t.me/zuanww"))
    markup.add(InlineKeyboardButton("🌐 WEBSITE KAMI", url="https://zuanpanel.web.id"))
    bot.send_message(message.chat.id, teks, parse_mode="Markdown", reply_markup=markup)

# ===== KLIK ORDER =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("order_"))
def handle_order(call):
    paket_key = call.data.replace("order_", "")
    paket = HARGA.get(paket_key)
    if not paket:
        return
    orders[call.from_user.id] = {"step": "username", "paket": paket_key, "paket_nama": paket["nama"], "harga": paket["harga"]}
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
        f"📦 *LU PILIH {paket['nama'].upper()}! PILIHAN YANG TEPAT!* 🔥\n\n"
        f"👤 *Sekarang kirim Username Panel yang lu mau!*\n"
        f"Contoh: `zuanww`\n\n"
        f"⚠️ Username tanpa spasi, huruf kecil semua ya!",
        parse_mode="Markdown")

# ===== TERIMA USERNAME & EMAIL =====
@bot.message_handler(func=lambda m: m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    user_id = message.from_user.id
    data = orders[user_id]
    text = message.text.strip()

    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id,
            f"✅ *USERNAME `{text}` DIAMANKAN!*\n\n"
            f"📧 *Terakhir, kirim Email lu!*\n"
            f"Contoh: `email@gmail.com`\n\n"
            f"Email buat login panel nanti!",
            parse_mode="Markdown")
        return

    if data["step"] == "email":
        data["email"] = text
        data["step"] = "bayar"
        order_id = f"INV-QRIS-ZUAN-{int(time.time())}-{user_id}"
        data["order_id"] = order_id
        orders_by_id[order_id] = data

        # Buat payment ke Kasera
        bot.send_message(message.chat.id, "⏳ *Lagi bikinin QRIS lu, sabar bentar...* 🔥", parse_mode="Markdown")
        pay = buat_payment_kasera(data["harga"], order_id)

        qr_url = None
        if pay and pay.get("data"):
            qr_url = pay["data"].get("qr_image") or pay["data"].get("qr_url") or pay["data"].get("checkout_url")

        # ===== TEKS INVOICE KEREN - YANG DI SS LU =====
        caption = (
            f"🧾 *INVOICE - ZUANPANEL.WEB.ID*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 *Produk:* {data['paket_nama']} (x1)\n"
            f"👤 *Username:* `{data['username_panel']}`\n"
            f"🆔 *Order ID:* `{order_id}`\n"
            f"💰 *Total Bayar:* Rp {data['harga']:,}".replace(",", ".") + "\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"⚠️ *BAYAR PAS SESUAI NOMINAL!*\n"
            f"⏰ *Expired:* 60 Menit\n"
            f"🚫 *Bayar Diluar Waktu? Saldo Hangus!*\n\n"
            f"✅ *Udah bayar? Gas tekan tombol di bawah!*"
        )

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ CEK STATUS PEMBAYARAN", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("❌ BATALKAN PESANAN", callback_data=f"batal_{order_id}"))

        # Kirim QRIS
        try:
            if qr_url and qr_url.startswith("http"):
                img_data = requests.get(qr_url, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img_data), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

        # ===== TEKS KE ADMIN - PESANAN BARU KEREN =====
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
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏰ *Gas pantau, jangan sampe lolos!*"
        )
        try:
            bot.send_message(ADMIN_ID, pesan_admin, parse_mode="Markdown")
        except:
            pass
        return

# ===== CEK STATUS & BATAL =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Order tidak ditemukan!")
            return
        # Cek ke Kasera
        res = cek_payment_kasera(order_id)
        status = ""
        if res and res.get("data"):
            status = res["data"].get("status", "").lower()
        
        if status in ["paid", "success", "lunas", "completed"]:
            bot.send_message(call.message.chat.id,
                f"✅ *PEMBAYARAN LU UDAH MASUK!* 🔥\n\n"
                f"📦 Panel {data['paket_nama']} lagi diproses!\n"
                f"👤 Username: `{data['username_panel']}`\n\n"
                f"Tunggu bentar, admin lagi gas buatin panel lu!",
                parse_mode="Markdown")
            # Notif ke admin kalo lunas
            try:
                bot.send_message(ADMIN_ID, f"✅ *ORDER LUNAS!*\n🆔 `{order_id}`\n📦 {data['paket_nama']} - {data['username_panel']}\nGas buatin panelnya!", parse_mode="Markdown")
            except: pass
        else:
            bot.answer_callback_query(call.id, "⏳ Belum masuk bang, coba lagi bentar!")
            bot.send_message(call.message.chat.id,
                f"⏳ *BELUM MASUK BANG!*\n\n"
                f"💰 Total: Rp {data['harga']:,}".replace(",", ".") + "\n"
                f"🆔 Order ID: `{order_id}`\n\n"
                f"Coba cek lagi mutasi lu, kalo udah bayar tapi masih gini, chat admin!",
                parse_mode="Markdown")
        return

    if call.data.startswith("batal_"):
        order_id = call.data.replace("batal_", "")
        if order_id in orders_by_id:
            del orders_by_id[order_id]
        # Hapus juga dari orders user
        for uid in list(orders.keys()):
            if orders[uid].get("order_id") == order_id:
                del orders[uid]
        bot.edit_message_text(
            f"❌ *PESANAN DIBATALKAN!*\n\n"
            f"Yahh padahal dikit lagi punya panel gacor! 😢\n\n"
            f"Mau order lagi? Ketik /start aja!",
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Pesanan dibatalkan!")
        return

print("✅ ZUANPANEL BOT ONLINE!")
bot.infinity_polling()
