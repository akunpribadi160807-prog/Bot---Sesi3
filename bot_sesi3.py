import os
import time
import requests
import telebot
import threading
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
KASERA_API_KEY = os.getenv("KASERA_API_KEY")
KASERA_BASE = "https://pay.kasera.id/v1"
bot = telebot.TeleBot(TOKEN)

GROUP_UTAMA = int(os.getenv("GROUP_UTAMA", "0"))
GROUP_PROMO = int(os.getenv("GROUP_PROMO", "0"))
GROUP_TESTI = int(os.getenv("GROUP_TESTI", "0"))
GROUP_PAYMENT = int(os.getenv("GROUP_PAYMENT", "0"))

# ===== BANNER ZUAN PANEL - ROBOT BIRU UDAH KEPASANG =====
BANNER_URL = "https://i.ibb.co.com/v4XNy1Jv/IMG-20261109-WA0076.jpg"

HARGA = {
    "1gb": {"nama": "Panel 1GB", "harga": 5000, "desc": "Buat yang baru mulai, ringan & hemat."},
    "5gb": {"nama": "Panel 5GB", "harga": 15000, "desc": "Paling laris, buat harian udah enak banget."},
    "10gb": {"nama": "Panel 10GB", "harga": 25000, "desc": "Buat yang butuh power lebih, anti lemot."},
    "unli": {"nama": "Panel UNLI", "harga": 50000, "desc": "Bebas tanpa batas, puas-puasin."},
}

orders = {}
orders_by_id = {}

def hapus_pesan_lama(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass

def kirim_payment(teks):
    if GROUP_PAYMENT != 0:
        try: bot.send_message(GROUP_PAYMENT, teks, parse_mode="Markdown")
        except: pass
    if ADMIN_ID != 0:
        try: bot.send_message(ADMIN_ID, teks, parse_mode="Markdown")
        except: pass

def kirim_testi(teks):
    if GROUP_TESTI != 0:
        try: bot.send_message(GROUP_TESTI, teks, parse_mode="Markdown")
        except: pass

def kirim_promo(teks, foto=None):
    for gid in [GROUP_UTAMA, GROUP_PROMO]:
        if gid != 0:
            try:
                if foto:
                    img = requests.get(foto, timeout=20).content
                    bot.send_photo(gid, BytesIO(img), caption=teks, parse_mode="Markdown")
                else:
                    bot.send_message(gid, teks, parse_mode="Markdown")
            except: pass

def buat_payment(total, order_id):
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        r = requests.post(f"{KASERA_BASE}/payment/create", json={"amount": total, "order_id": order_id, "method": "QRIS", "expired": 60}, headers=headers, timeout=20)
        return r.json()
    except: return None

def cek_payment(order_id):
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}"}
        r = requests.get(f"{KASERA_BASE}/payment/{order_id}", headers=headers, timeout=20)
        return r.json()
    except: return None

@bot.message_handler(commands=['start'])
def start(message):
    nama = message.from_user.first_name or "Kak"
    caption = (
        f"✨ *Selamat Datang, {nama}* ✨\n"
        f"Di *ZUAN PANEL* — Tempatnya Panel Premium.\n\n"
        f"Terima kasih sudah mampir.\n"
        f"Semua serba otomatis, jadi Kakak tidak perlu menunggu lama.\n\n"
        f"╭ ──── *Profil Bot* ──── ╮\n"
        f"│ 👑 Owner : ZUAN PANEL\n"
        f"│ 🤖 Bot : Auto Order Panel\n"
        f"│ ⚡ Status : Online 24 Jam\n"
        f"╰ ───────────────── ╯\n\n"
        f"╭ ──── *Statistik* ──── ╮\n"
        f"│ 👥 Total User : 481\n"
        f"│ 🔥 Stok : Ready Semua\n"
        f"╰ ───────────────── ╯\n\n"
        f"Silahkan pilih menu di bawah, Kak. Kami siap melayani. 🤍"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🛒  Order Panel", callback_data="menu_order"),
        InlineKeyboardButton("💳  Top Up Saldo", callback_data="menu_topup")
    )
    markup.add(
        InlineKeyboardButton("📦  Cek Stok", callback_data="menu_stok"),
        InlineKeyboardButton("💬  Hubungi Admin", url="https://t.me/zuanww")
    )
    markup.add(InlineKeyboardButton("🌐  Kunjungi Website", url="https://zuanpanel.web.id"))
    try:
        img = requests.get(BANNER_URL, timeout=20).content
        bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "menu_order")
def menu_order(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    caption = f"🛒 *Katalog Panel Kami*\n\nSilahkan pilih paket yang Kakak inginkan.\nSemua paket sudah termasuk garansi & support penuh.\n\nSemua stok ready, langsung diproses setelah pembayaran. ✨"
    markup = InlineKeyboardMarkup()
    for key, val in HARGA.items():
        markup.add(InlineKeyboardButton(f"✦ {val['nama']}  —  Rp {val['harga']:,}".replace(",", "."), callback_data=f"order_{key}"))
    markup.add(InlineKeyboardButton("‹  Kembali", callback_data="back_start"))
    bot.send_message(call.message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back_start")
def back_start(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    call.message.text = "/start"
    start(call.message)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("order_"))
def handle_order(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    key = call.data.replace("order_", "")
    paket = HARGA.get(key)
    if not paket: return
    orders[call.from_user.id] = {"step": "username", "paket": key, "paket_nama": paket["nama"], "harga": paket["harga"]}
    bot.send_message(call.message.chat.id, f"✦ *{paket['nama']}* ✦\n\n{paket['desc']}\n\nBaik Kak, untuk melanjutkan...\nBoleh kirimkan *Username Panel* yang Kakak inginkan?\n\nContoh : `zuanww`\n_( tanpa spasi, huruf kecil )_", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    uid = message.from_user.id
    data = orders[uid]
    text = message.text.strip()
    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id, f"Baik, username *`{text}`* sudah kami amankan. 🤍\n\nLangkah terakhir, boleh kirimkan *Email* Kakak?\nEmail ini akan digunakan untuk login panel nanti.\n\nContoh : `email@gmail.com`", parse_mode="Markdown")
        return
    if data["step"] == "email":
        data["email"] = text
        data["step"] = "bayar"
        order_id = f"INV-ZUAN-{int(time.time())}-{uid}"
        data["order_id"] = order_id
        orders_by_id[order_id] = data
        bot.send_message(message.chat.id, "Mohon ditunggu sebentar ya Kak, kami sedang menyiapkan QRIS untuk Kakak... ✨", parse_mode="Markdown")
        pay = buat_payment(data["harga"], order_id)
        qr_url = None
        if pay and pay.get("data"): qr_url = pay["data"].get("qr_image") or pay["data"].get("qr_url")
        caption = (
            f"🧾 *Invoice Pembayaran*\n*ZUAN PANEL*\n──────────────────\n"
            f"📦 Produk : {data['paket_nama']}\n"
            f"👤 Username : `{data['username_panel']}`\n"
            f"🆔 Order ID : `{order_id}`\n"
            f"💰 Total : Rp {data['harga']:,}".replace(",", ".") + "\n"
            f"──────────────────\n\n"
            f"Mohon lakukan pembayaran sesuai nominal ya Kak.\nPesanan akan otomatis terhapus jika tidak dibayar dalam *60 Menit*.\n\nSetelah membayar, silahkan tekan tombol di bawah untuk konfirmasi. 🤍"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅  Saya Sudah Bayar", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("✕  Batalkan Pesanan", callback_data=f"batal_{order_id}"))
        try:
            if qr_url and qr_url.startswith("http"):
                img = requests.get(qr_url, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        kirim_payment(f"🔔 *PESANAN BARU MASUK!*\n──────────────────\n👤 Customer : {uname}\n📦 Paket : {data['paket_nama']}\n👤 Username Panel : `{data['username_panel']}`\n📧 Email : `{data['email']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n⏳ Status : Menunggu Pembayaran\n🆔 Order ID : `{order_id}`")
        return

@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        res = cek_payment(order_id)
        status = ""
        if res and res.get("data"): status = res["data"].get("status", "").lower()
        if status in ["paid", "success", "lunas", "completed"]:
            hapus_pesan_lama(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f"Terima kasih Kak, pembayaran sudah kami terima. 🤍\n\nPesanan Kakak sedang kami proses.\nPanel *{data['paket_nama']}* untuk username *`{data['username_panel']}`* akan segera kami kirimkan.\n\nMohon ditunggu sebentar ya.", parse_mode="Markdown")
            kirim_testi(f"✅ *PEMBAYARAN BERHASIL! TESTI BARU!*\n──────────────────\n📦 Paket : {data['paket_nama']}\n👤 Username : `{data['username_panel']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 Order ID : `{order_id}`\n\nTerima kasih sudah order di ZUAN PANEL! 🤍\nReal testi, bukan settingan! 🔥")
            kirim_payment(f"✅ *LUNAS - {data['paket_nama']}*\n👤 `{data.get('username_panel','-')}`\n💰 Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 `{order_id}`\n\nGas buatin panelnya min! 🔥")
        else:
            bot.answer_callback_query(call.id, "Pembayaran belum kami terima.")
            bot.send_message(call.message.chat.id, f"Mohon maaf Kak, pembayaran belum kami terima.\n\nJika Kakak sudah membayar, mohon tunggu 1-2 menit lalu coba cek kembali ya. 🤍", parse_mode="Markdown")
            kirim_payment(f"⚠️ *PEMBAYARAN BELUM MASUK*\n🆔 `{order_id}`\n📦 {data['paket_nama']} - `{data.get('username_panel','-')}`\nCustomer klik cek tapi belum bayar.")
        return
    if call.data.startswith("batal_"):
        order_id = call.data.replace("batal_", "")
        data_batal = orders_by_id.get(order_id)
        if order_id in orders_by_id: del orders_by_id[order_id]
        for uid in list(orders.keys()):
            if orders[uid].get("order_id") == order_id: del orders[uid]
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Baik Kak, pesanan sudah kami batalkan.\n\nJika Kakak berubah pikiran, silahkan ketik /start kapan saja.\nKami selalu siap melayani. 🤍", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Pesanan dibatalkan.")
        if data_batal:
            kirim_payment(f"❌ *PESANAN DIBATALKAN*\n🆔 `{order_id}`\n📦 {data_batal['paket_nama']} - `{data_batal.get('username_panel','-')}`")
        return

@bot.callback_query_handler(func=lambda c: c.data in ["menu_topup", "menu_stok"])
def menu_lain(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    if call.data == "menu_topup":
        bot.send_message(call.message.chat.id, "Untuk Top Up Saldo, silahkan hubungi Admin ya Kak. Kami akan bantu prosesnya dengan cepat. 🤍", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, "Semua stok kami *READY* ya Kak. Silahkan langsung order saja. ✨", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['promo'])
def cmd_promo(message):
    if message.from_user.id != ADMIN_ID: return
    teks_promo = (
        f"🔥 *PROMO PANEL - ZUAN PANEL* 🔥\n\n"
        f"✨ *Panel Premium, Harga Merakyat!*\n"
        f"──────────────────\n"
        f"📦 Panel 1GB — Rp 5.000\n"
        f"📦 Panel 5GB — Rp 15.000 ⭐ PALING LARIS\n"
        f"📦 Panel 10GB — Rp 25.000\n"
        f"📦 Panel UNLI — Rp 50.000\n"
        f"──────────────────\n\n"
        f"✅ Garansi Full\n"
        f"✅ Support 24 Jam\n"
        f"✅ Proses Otomatis, Gak Pake Nunggu\n"
        f"✅ Stok Ready Semua!\n\n"
        f"🛒 Order : @Auto_orderpanelbaru_bot\n"
        f"💬 Admin : @zuanww\n\n"
        f"Buruan, jangan sampe kehabisan! 🤍"
    )
    kirim_promo(teks_promo, foto=BANNER_URL)
    bot.send_message(message.chat.id, "✅ Promo udah gue kirim ke Grup Utama + Grup Bebas Promosi bang!")

@bot.message_handler(commands=['id'])
def cek_id(message):
    bot.send_message(message.chat.id, f"ID chat ini: `{message.chat.id}`\nID lu: `{message.from_user.id}`", parse_mode="Markdown")

def auto_promo_loop():
    while True:
        time.sleep(7200)
        teks = f"🔥 *ZUAN PANEL READY!* 🔥\n\nPanel 5GB cuma Rp 15.000 aja!\nGaransi full, proses otomatis.\n\nOrder di : @Auto_orderpanelbaru_bot\nJangan sampe kehabisan! ✨"
        kirim_promo(teks, foto=BANNER_URL)

threading.Thread(target=auto_promo_loop, daemon=True).start()
print("✅ ZUAN PANEL - 4 GRUP JALAN!")
bot.infinity_polling()
