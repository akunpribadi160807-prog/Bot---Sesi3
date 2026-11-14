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
    for target, nama in [(GROUP_PAYMENT, "PAYMENT"), (ADMIN_ID, "ADMIN")]:
        try:
            bot.send_message(target, teks, parse_mode="Markdown")
            print(f"[KIRIM OK] {nama} {target}")
        except Exception as e:
            print(f"[KIRIM GAGAL] {nama} {target} - {e}")

def kirim_testi(teks):
    try: bot.send_message(GROUP_TESTI, teks, parse_mode="Markdown")
    except Exception as e: print(f"[TESTI GAGAL] {e}")

def kirim_promo(teks, foto=None):
    for gid, nama in [(GROUP_UTAMA, "UTAMA"), (GROUP_PROMO, "PROMO")]:
        try:
            if foto:
                img = requests.get(foto, timeout=20).content
                bot.send_photo(gid, BytesIO(img), caption=teks, parse_mode="Markdown")
            else:
                bot.send_message(gid, teks, parse_mode="Markdown")
            print(f"[PROMO OK] {nama}")
        except Exception as e: print(f"[PROMO GAGAL] {nama} - {e}")

def kirim_welcome_testi(user):
    try:
        uname = f"@{user.username}" if user.username else "-"
        nama = user.first_name or "Pelanggan Baru"
        uid = user.id
        waktu = datetime.now().strftime("%H:%M, %d/%m/%y")
        caption_foto = f"✨ *SELAMAT DATANG PELANGGAN BARU!* ✨\n\n> WELCOME *{nama}*\n> Restock • Promo • Harga • Stock\n> Panel • Auto Order\n\n> *ZUAN PANEL - COMMUNITY ONLINE*"
        markup_foto = InlineKeyboardMarkup()
        markup_foto.add(InlineKeyboardButton("🛒  START JUGA", url="https://t.me/Auto_orderpanelbaru_bot?start=start"))
        try:
            img = requests.get(WELCOME_URL, timeout=20).content
            bot.send_photo(GROUP_TESTI, BytesIO(img), caption=caption_foto, parse_mode="Markdown", reply_markup=markup_foto)
        except:
            bot.send_message(GROUP_TESTI, caption_foto, parse_mode="Markdown", reply_markup=markup_foto)
        tabel = (
            f"✨ *PELANGGAN BARU DATANG* ✨\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"         *INFO PELANGGAN*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"> 👤 *USERNAME* : {uname}\n"
            f"> 🆔 *ID* : `{uid}`\n"
            f"> ⏰ *WAKTU START* : {waktu}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"> Selamat datang di *ZUAN PANEL* kak {nama}! 🤍\n"
            f"> Semoga betah, jangan lupa order ya!"
        )
        markup_tabel = InlineKeyboardMarkup()
        markup_tabel.add(InlineKeyboardButton("🚀  START JUGA", url="https://t.me/Auto_orderpanelbaru_bot?start=start"))
        bot.send_message(GROUP_TESTI, tabel, parse_mode="Markdown", reply_markup=markup_tabel)
        print(f"[WELCOME OK] {nama} {uid}")
    except Exception as e:
        print(f"[WELCOME GAGAL] {e}")

@bot.message_handler(commands=['cekgrup'])
def cek_grup(message):
    bot.send_message(message.chat.id, "⏳ *Lagi Ngetes 4 Grup...*\n> Tunggu 5 detik ya bang...", parse_mode="Markdown")
    hasil = []
    for gid, nama in [(GROUP_UTAMA, "GRUP UTAMA"), (GROUP_PROMO, "GRUP PROMO"), (GROUP_TESTI, "GRUP TESTI"), (GROUP_PAYMENT, "GRUP PAYMENT")]:
        try:
            bot.send_message(gid, f"✅ *TES BERHASIL!*\n> Grup {nama} udah kehubung!\n> ID : `{gid}`", parse_mode="Markdown")
            hasil.append(f"✅ {nama} — BERHASIL")
        except Exception as e:
            hasil.append(f"❌ {nama} — GAGAL: {e}")
    bot.send_message(message.chat.id, "📊 *HASIL TES 4 GRUP*\n━━━━━━━━━━━━━━━━━━\n" + "\n".join(hasil) + "\n━━━━━━━━━━━━━━━━━━\n> Semua grup udah aman bang!", parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def cek_id(message):
    bot.send_message(message.chat.id, f"🆔 *CEK ID*\n━━━━━━━━━━━━━━━━━━\n> ID Chat : `{message.chat.id}`\n> ID Lu : `{message.from_user.id}`\n━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    kirim_welcome_testi(message.from_user)
    nama = message.from_user.first_name or "Kak"
    caption = f"✨ *SELAMAT DATANG, {nama.upper()}* ✨\n\n> Di *ZUAN PANEL* — Tempatnya Panel Premium.\n> Semua serba otomatis, gak perlu nunggu lama.\n\n╭ ──── *PROFIL BOT* ──── ╮\n│ 👑 Owner : ZUAN PANEL\n│ 🤖 Bot : Auto Order Panel\n│ ⚡ Status : Online 24 Jam\n│ 💎 Garansi : Full Garansi\n╰ ───────────────── ╯\n\n> Silahkan pilih menu di bawah, Kak.\n> Kami siap melayani. 🤍"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🛒  Order Panel", callback_data="menu_order"), InlineKeyboardButton("💳  Top Up Saldo", callback_data="menu_topup"))
    markup.add(InlineKeyboardButton("📦  Cek Stok", callback_data="menu_stok"), InlineKeyboardButton("💬  Hubungi Admin", url="https://t.me/zuanww"))
    markup.add(InlineKeyboardButton("🌐  Kunjungi Website", url="https://zuanpanel.web.id"))
    try:
        img = requests.get(BANNER_URL, timeout=20).content
        bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "menu_order")
def menu_order(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    caption = f"🛒 *KATALOG PANEL KAMI*\n━━━━━━━━━━━━━━━━━━\n> Silahkan pilih paket yang Kakak inginkan.\n> Semua paket sudah termasuk garansi & support penuh.\n━━━━━━━━━━━━━━━━━━"
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
    bot.send_message(call.message.chat.id, f"✦ *{paket['nama'].upper()}* ✦\n━━━━━━━━━━━━━━━━━━\n> {paket['desc']}\n━━━━━━━━━━━━━━━━━━\n\n> Boleh kirimkan *Username Panel* yang Kakak inginkan?\n> Contoh : `zuanww`", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    uid = message.from_user.id
    data = orders[uid]
    text = message.text.strip()
    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id, f"✅ Username *`{text}`* sudah kami amankan. 🤍\n━━━━━━━━━━━━━━━━━━\n> Boleh kirimkan *Email* Kakak?\n> Contoh : `email@gmail.com`", parse_mode="Markdown")
        return
    if data["step"] == "email":
        data["email"] = text
        data["step"] = "bayar"
        order_id = f"INV-ZUAN-{int(time.time())}-{uid}"
        data["order_id"] = order_id
        orders_by_id[order_id] = data
        caption = f"🧾 *INVOICE PEMBAYARAN*\n*ZUAN PANEL*\n━━━━━━━━━━━━━━━━━━\n> 📦 Produk : {data['paket_nama']}\n> 👤 Username : `{data['username_panel']}`\n> 🆔 Order ID : `{order_id}`\n> 💰 Total : Rp {data['harga']:,}".replace(",", ".") + "\n━━━━━━━━━━━━━━━━━━\n\n> Silahkan scan QRIS di atas ya Kak.\n> Setelah membayar, tekan tombol di bawah. 🤍"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅  Saya Sudah Bayar", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("✕  Batalkan Pesanan", callback_data=f"batal_{order_id}"))
        try:
            if "PASTE-LINK" not in QRIS_STATIS_URL:
                img = requests.get(QRIS_STATIS_URL, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, caption + "\n\n> ⚠️ *QRIS belum di-set, hubungi admin @zuanww*", parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        kirim_payment(f"🔔 *PESANAN BARU MASUK!*\n━━━━━━━━━━━━━━━━━━\n> 👤 Customer : {uname}\n> 📦 Paket : {data['paket_nama']}\n> 👤 Username Panel : `{data['username_panel']}`\n> 📧 Email : `{data['email']}`\n> 💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n> ⏳ Status : Menunggu Pembayaran\n> 🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━")

@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"🤍 *TERIMA KASIH KAK!*\n━━━━━━━━━━━━━━━━━━\n> Laporan pembayaran diterima.\n> Pesanan *{data['paket_nama']}* untuk username *`{data['username_panel']}`* akan dicek admin dan segera diproses.\n━━━━━━━━━━━━━━━━━━\n> Ditunggu ya Kak, bentar lagi jadi! ✨", parse_mode="Markdown")
        kirim_testi(f"✅ *PEMBAYARAN DILAPORKAN!*\n*TESTI BARU MASUK!*\n━━━━━━━━━━━━━━━━━━\n> 📦 Paket : {data['paket_nama']}\n> 👤 Username : `{data['username_panel']}`\n> 💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n> 🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━\n\n> Terima kasih sudah order di *ZUAN PANEL!* 🤍\n> Dijamin puas, garansi full!")
        kirim_payment(f"✅ *CUSTOMER KLIK SUDAH BAYAR!*\n━━━━━━━━━━━━━━━━━━\n> 📦 Paket : {data['paket_nama']}\n> 👤 Username : `{data.get('username_panel','-')}`\n> 💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n> 🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━\n\n> Cek mutasi, gas buatin panelnya min! 🔥")
        return
    if call.data.startswith("batal_"):
        order_id = call.data.replace("batal_", "")
        data_batal = orders_by_id.get(order_id)
        if order_id in orders_by_id: del orders_by_id[order_id]
        for uid in list(orders.keys()):
            if orders[uid].get("order_id") == order_id: del orders[uid]
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"❌ *PESANAN DIBATALKAN*\n━━━━━━━━━━━━━━━━━━\n> Baik Kak, pesanan sudah kami batalkan.\n> Jika berubah pikiran, ketik /start kapan saja. 🤍\n━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Pesanan dibatalkan.")
        if data_batal:
            kirim_payment(f"❌ *PESANAN DIBATALKAN*\n━━━━━━━━━━━━━━━━━━\n> 🆔 Order ID : `{order_id}`\n> 📦 Paket : {data_batal['paket_nama']}\n> 👤 Username : `{data_batal.get('username_panel','-')}`\n━━━━━━━━━━━━━━━━━━")
        return

@bot.callback_query_handler(func=lambda c: c.data in ["menu_topup", "menu_stok"])
def menu_lain(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    if call.data == "menu_topup":
        bot.send_message(call.message.chat.id, "💳 *TOP UP SALDO*\n━━━━━━━━━━━━━━━━━━\n> Untuk Top Up Saldo, silahkan hubungi Admin ya Kak. 🤍\n> Admin : @zuanww\n━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, "📦 *CEK STOK*\n━━━━━━━━━━━━━━━━━━\n> Semua stok kami *READY* ya Kak.\n> Silahkan langsung order saja. ✨\n━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['promo'])
def cmd_promo(message):
    if message.from_user.id != ADMIN_ID: return
    teks_promo = f"🔥 *PROMO PANEL - ZUAN PANEL* 🔥\n━━━━━━━━━━━━━━━━━━\n> ✨ *Panel Premium, Harga Merakyat!*\n━━━━━━━━━━━━━━━━━━\n> 📦 Panel 1GB — Rp 5.000\n> 📦 Panel 5GB — Rp 15.000 ⭐ PALING LARIS\n> 📦 Panel 10GB — Rp 25.000\n> 📦 Panel UNLI — Rp 50.000\n━━━━━━━━━━━━━━━━━━\n\n> ✅ Garansi Full\n> ✅ Support 24 Jam\n> ✅ Proses Otomatis\n\n> 🛒 Order : @Auto_orderpanelbaru_bot\n> 💬 Admin : @zuanww"
    kirim_promo(teks_promo, foto=BANNER_URL)
    bot.send_message(message.chat.id, "✅ *Promo Terkirim!*\n> Udah gue kirim ke Grup Utama + Grup Bebas Promosi bang!", parse_mode="Markdown")

def auto_promo_loop():
    while True:
        time.sleep(7200)
        teks = f"🔥 *ZUAN PANEL READY!* 🔥\n━━━━━━━━━━━━━━━━━━\n> Panel 5GB cuma Rp 15.000 aja!\n> Garansi full, proses otomatis.\n━━━━━━━━━━━━━━━━━━\n\n> Order di : @Auto_orderpanelbaru_bot"
        kirim_promo(teks, foto=BANNER_URL)

threading.Thread(target=auto_promo_loop, daemon=True).start()
print("✅ ZUAN PANEL - 4 GRUP JALAN!")
bot.infinity_polling()
