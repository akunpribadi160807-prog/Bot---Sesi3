import os, time, requests, telebot, threading
from datetime import datetime
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8493708698"))
bot = telebot.TeleBot(TOKEN)

GROUP_UTAMA = -1004497488934
GROUP_PROMO = -1003900745031
GROUP_TESTI = -1004432426937
GROUP_PAYMENT = -1004257626762

BANNER_URL = "https://i.ibb.co.com/v4XNy1Jv/IMG-20261109-WA0076.jpg"
QRIS_STATIS_URL = "https://i.ibb.co.com/PASTE-LINK-QRIS-LU-DISINI.jpg"
WELCOME_URL = "https://i.ibb.co.com/b5Jx4qPb/IMG-20261114-WA3337.jpg"

HARGA = {
    "1gb": {"nama": "Panel 1GB", "harga": 5000, "desc": "Ringan, hemat, buat yang baru mulai cobain."},
    "5gb": {"nama": "Panel 5GB", "harga": 15000, "desc": "Ini sih yang paling laris, udah paling pas buat harian."},
    "10gb": {"nama": "Panel 10GB", "harga": 25000, "desc": "Buat yang butuh power lebih, dijamin anti lemot."},
    "unli": {"nama": "Panel UNLI", "harga": 50000, "desc": "Bebas tanpa batas, puas-puasin sampe bosen."},
}
orders = {}
orders_by_id = {}

def hapus_pesan_lama(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass

def stiker(chat_id, emoji):
    try: bot.send_message(chat_id, emoji)
    except: pass

def kirim_payment(teks):
    for target in [GROUP_PAYMENT, ADMIN_ID]:
        try: bot.send_message(target, teks, parse_mode="Markdown")
        except Exception as e: print(f"[PAYMENT GAGAL] {e}")

def kirim_testi(teks):
    try: bot.send_message(GROUP_TESTI, teks, parse_mode="Markdown")
    except Exception as e: print(f"[TESTI GAGAL] {e}")

def kirim_promo(teks, foto=None):
    for gid in [GROUP_UTAMA, GROUP_PROMO]:
        try:
            if foto:
                img = requests.get(foto, timeout=20).content
                bot.send_photo(gid, BytesIO(img), caption=teks, parse_mode="Markdown")
            else: bot.send_message(gid, teks, parse_mode="Markdown")
        except Exception as e: print(f"[PROMO GAGAL] {e}")

# ===== WELCOME BARU - JADI 1 PESAN AJA, 1 TOMBOL AJA, TEKS LEBIH KEREN =====
def kirim_welcome_testi(user):
    try:
        uname = f"@{user.username}" if user.username else "-"
        nama = user.first_name or "Pelanggan Baru"
        waktu = datetime.now().strftime("%H:%M, %d/%m/%y")
        # 1 PESAN AJA - FOTO + SEMUA TEKS JADI SATU CAPTION
        caption = (
            f"👑 *PELANGGAN BARU DATANG* 👑\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✨ Selamat datang, *{nama}*! ✨\n"
            f"Welcome to *ZUAN PANEL* — tempatnya panel premium.\n\n"
            f"╭ ─── *INFO PELANGGAN* ─── ╮\n"
            f"│ 👤 Username : {uname}\n"
            f"│ 🆔 ID : `{user.id}`\n"
            f"│ ⏰ Start : {waktu}\n"
            f"╰ ───────────────── ╯\n\n"
            f"Restock • Promo • Harga • Stock • Panel • Auto Order\n\n"
            f"Semoga betah ya kak, jangan lupa order, gas! 🔥"
        )
        # CUMA 1 TOMBOL, GAK ADA 2 LAGI!
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚀  START JUGA — GAS ORDER!", url="https://t.me/Auto_orderpanelbaru_bot?start=start"))
        try:
            img = requests.get(WELCOME_URL, timeout=20).content
            bot.send_photo(GROUP_TESTI, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(GROUP_TESTI, caption, parse_mode="Markdown", reply_markup=markup)
    except Exception as e: print(f"[WELCOME GAGAL] {e}")

@bot.message_handler(commands=['cekgrup'])
def cek_grup(message):
    bot.send_message(message.chat.id, "⏳ Lagi ngetes 4 grup dulu ya bang, tunggu 5 detik...", parse_mode="Markdown")
    hasil = []
    for gid, nama in [(GROUP_UTAMA, "GRUP UTAMA"), (GROUP_PROMO, "GRUP PROMO"), (GROUP_TESTI, "GRUP TESTI"), (GROUP_PAYMENT, "GRUP PAYMENT")]:
        try:
            bot.send_message(gid, f"✅ TES BERHASIL!\nGrup {nama} udah kehubung!", parse_mode="Markdown")
            hasil.append(f"✅ {nama} — BERHASIL")
        except Exception as e: hasil.append(f"❌ {nama} — GAGAL")
    bot.send_message(message.chat.id, "📊 *HASIL TES 4 GRUP*\n━━━━━━━━━━━━━━━━━━\n" + "\n".join(hasil), parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def cek_id(message):
    bot.send_message(message.chat.id, f"ID chat ini : `{message.chat.id}`\nID lu : `{message.from_user.id}`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    kirim_welcome_testi(message.from_user)
    nama = message.from_user.first_name or "Kak"
    stiker(message.chat.id, "👑")
    caption = (
        f"✨ *Halo, {nama}!* ✨\n"
        f"Selamat datang di *ZUAN PANEL* 🤍\n\n"
        f"Disini semua serba otomatis, jadi kakak gak perlu nunggu lama.\n\n"
        f"╭ ──── *ZUAN PANEL* ──── ╮\n"
        f"│ 👑 Owner : ZUAN PANEL\n"
        f"│ 🤖 Bot : Auto Order 24 Jam\n"
        f"│ 💎 Garansi : Full Garansi\n"
        f"╰ ───────────────── ╯\n\n"
        f"Yuk pilih menu dibawah, kakak mau order yang mana? 😊"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🛒  Order Panel", callback_data="menu_order"), InlineKeyboardButton("💳  Top Up Saldo", callback_data="menu_topup"))
    markup.add(InlineKeyboardButton("📦  Cek Stok", callback_data="menu_stok"), InlineKeyboardButton("💬  Hubungi Admin", url="https://t.me/zuanww"))
    markup.add(InlineKeyboardButton("🌐  Kunjungi Website", url="https://zuanpanel.web.id"))
    try:
        img = requests.get(BANNER_URL, timeout=20).content
        bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
    except: bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "menu_order")
def menu_order(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    caption = (
        f"🛒 *Katalog Panel Kami* 💎\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Pilih aja kak, semua udah termasuk garansi & support penuh kok.\n"
        f"Gak usah bingung, tinggal klik aja yang kakak suka 👇"
    )
    markup = InlineKeyboardMarkup()
    for key, val in HARGA.items():
        markup.add(InlineKeyboardButton(f"✦ {val['nama']}  —  Rp {val['harga']:,}".replace(",", "."), callback_data=f"order_{key}"))
    markup.add(InlineKeyboardButton("‹  Kembali", callback_data="back_start"))
    bot.send_message(call.message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back_start")
def back_start(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    start(call.message)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("order_"))
def handle_order(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    key = call.data.replace("order_", "")
    paket = HARGA.get(key)
    if not paket: return
    orders[call.from_user.id] = {"step": "username", "paket": key, "paket_nama": paket["nama"], "harga": paket["harga"]}
    bot.send_message(call.message.chat.id, f"✦ *{paket['nama']}* ✦\n\nWihh pilihan bagus kak! 😍\n{paket['desc']}\n\nBoleh spill *Username Panel* yang kakak mau?\nContohnya kayak gini : `zuanww`", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    uid = message.from_user.id
    data = orders[uid]
    text = message.text.strip()
    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id, f"Oke, username *`{text}`* udah gue amankan nih 🤍\n\nTerakhir, boleh minta *Email* kakak?\nContoh : `email@gmail.com`", parse_mode="Markdown")
        return
    if data["step"] == "email":
        data["email"] = text
        data["step"] = "bayar"
        order_id = f"INV-ZUAN-{int(time.time())}-{uid}"
        data["order_id"] = order_id
        orders_by_id[order_id] = data
        caption = (
            f"🧾 *Invoice Pembayaran*\n*ZUAN PANEL* 💎\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 Produk : {data['paket_nama']}\n"
            f"👤 Username : `{data['username_panel']}`\n"
            f"🆔 Order ID : `{order_id}`\n"
            f"💰 Total : Rp {data['harga']:,}".replace(",", ".") + "\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"Tinggal scan QRIS diatas ya kak, abis itu klik tombol dibawah 🤍"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅  Saya Sudah Bayar", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("✕  Batalkan Pesanan", callback_data=f"batal_{order_id}"))
        try:
            if "PASTE-LINK" not in QRIS_STATIS_URL:
                img = requests.get(QRIS_STATIS_URL, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else: bot.send_message(message.chat.id, caption + "\n\n⚠️ QRIS belum di-set, hubungi admin @zuanww ya kak", parse_mode="Markdown", reply_markup=markup)
        except: bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        kirim_payment(f"🔔 *PESANAN BARU MASUK!* 🔔\n━━━━━━━━━━━━━━━━━━\n👤 Customer : {uname}\n📦 Paket : {data['paket_nama']}\n👤 Username Panel : `{data['username_panel']}`\n📧 Email : `{data['email']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n⏳ Status : Menunggu Pembayaran\n🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━")

@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        stiker(call.message.chat.id, "🎉")
        bot.send_message(call.message.chat.id, f"Yeayy makasih banyak kak! 🤍\n\nLaporan pembayaran kakak udah gue terima.\nPesanan *{data['paket_nama']}* buat username *`{data['username_panel']}`* lagi dicek admin, bentar lagi jadi kok! ✨\nDitunggu yaa~", parse_mode="Markdown")
        kirim_testi(f"✅ *PEMBAYARAN DILAPORKAN!*\n*TESTI BARU MASUK!* 💎\n━━━━━━━━━━━━━━━━━━\n📦 Paket : {data['paket_nama']}\n👤 Username : `{data['username_panel']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━\n\nMakasih udah order di *ZUAN PANEL!* 🤍")
        kirim_payment(f"✅ *CUSTOMER UDAH BAYAR!* 🔥\n━━━━━━━━━━━━━━━━━━\n📦 Paket : {data['paket_nama']}\n👤 Username : `{data.get('username_panel','-')}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━\n\nCek mutasi min, gas buatin panelnya! 🔥")
        return
    if call.data.startswith("batal_"):
        order_id = call.data.replace("batal_", "")
        data_batal = orders_by_id.get(order_id)
        if order_id in orders_by_id: del orders_by_id[order_id]
        for uid in list(orders.keys()):
            if orders[uid].get("order_id") == order_id: del orders[uid]
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        stiker(call.message.chat.id, "🥺")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒  Order Lagi Yuk", callback_data="menu_order"))
        bot.send_message(call.message.chat.id, f"Yahh dibatalin 🥺\n\nGapapa kok kak, santai aja.\nKalo nanti berubah pikiran, tinggal klik dibawah aja ya, gue standby kok 🤍", parse_mode="Markdown", reply_markup=markup)
        bot.answer_callback_query(call.id, "Pesanan dibatalkan.")
        if data_batal:
            kirim_payment(f"🥺 *PESANAN DIBATALKAN*\n━━━━━━━━━━━━━━━━━━\n🆔 Order ID : `{order_id}`\n📦 Paket : {data_batal['paket_nama']}\n👤 Username : `{data_batal.get('username_panel','-')}`\n━━━━━━━━━━━━━━━━━━\nCustomernya batal kak, gapapa, lanjut cari yang lain 🔥")
        return

@bot.callback_query_handler(func=lambda c: c.data in ["menu_topup", "menu_stok"])
def menu_lain(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    if call.data == "menu_topup":
        bot.send_message(call.message.chat.id, "Buat Top Up, langsung chat admin aja ya kak 🤍\nAdmin : @zuanww\nFast respon kok!", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, "Tenang kak, semua stok kita *READY* kok ✨\nLangsung order aja, gas!", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['promo'])
def cmd_promo(message):
    if message.from_user.id != ADMIN_ID: return
    teks_promo = f"🔥 *PROMO PANEL - ZUAN PANEL* 🔥\n━━━━━━━━━━━━━━━━━━\n✨ *Panel Premium, Harga Merakyat!*\n━━━━━━━━━━━━━━━━━━\n📦 Panel 1GB — Rp 5.000\n📦 Panel 5GB — Rp 15.000 ⭐ PALING LARIS\n📦 Panel 10GB — Rp 25.000\n📦 Panel UNLI — Rp 50.000\n━━━━━━━━━━━━━━━━━━\n\n✅ Garansi Full\n✅ Support 24 Jam\n✅ Proses Otomatis\n\n🛒 Order : @Auto_orderpanelbaru_bot\n💬 Admin : @zuanww"
    kirim_promo(teks_promo, foto=BANNER_URL)
    bot.send_message(message.chat.id, "✅ Promo udah gue kirim ke Grup Utama + Grup Bebas Promosi bang!", parse_mode="Markdown")

def auto_promo_loop():
    while True:
        time.sleep(7200)
        teks = f"🔥 *ZUAN PANEL READY!* 🔥\n━━━━━━━━━━━━━━━━━━\nPanel 5GB cuma Rp 15.000 aja!\nGaransi full, proses otomatis.\n\nOrder di : @Auto_orderpanelbaru_bot"
        kirim_promo(teks, foto=BANNER_URL)

threading.Thread(target=auto_promo_loop, daemon=True).start()
print("✅ ZUAN PANEL - 1 PESAN JALAN!")
bot.infinity_polling()
