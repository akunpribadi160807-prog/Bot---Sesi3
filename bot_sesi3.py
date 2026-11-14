import os, time, requests, telebot, threading
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8493708698"))
bot = telebot.TeleBot(TOKEN)

# ===== 4 GRUP LU - UDAH DITANEM, GAK USAH UBAH LAGI =====
GROUP_UTAMA = -1004497488934
GROUP_PROMO = -1003900745031
GROUP_TESTI = -1004432426937
GROUP_PAYMENT = -1004257626762

BANNER_URL = "https://i.ibb.co.com/v4XNy1Jv/IMG-20261109-WA0076.jpg"
QRIS_STATIS_URL = "https://i.ibb.co.com/PASTE-LINK-QRIS-LU-DISINI.jpg"

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

@bot.message_handler(commands=['cekgrup'])
def cek_grup(message):
    bot.send_message(message.chat.id, "⏳ Lagi ngetes 4 grup... tunggu 5 detik...")
    hasil = []
    for gid, nama in [(GROUP_UTAMA, "GRUP UTAMA"), (GROUP_PROMO, "GRUP PROMO"), (GROUP_TESTI, "GRUP TESTI"), (GROUP_PAYMENT, "GRUP PAYMENT")]:
        try:
            bot.send_message(gid, f"✅ *TES BERHASIL!*\nGrup {nama} ({gid}) udah kehubung!", parse_mode="Markdown")
            hasil.append(f"✅ {nama} - BERHASIL")
        except Exception as e:
            hasil.append(f"❌ {nama} - GAGAL: {e}")
    bot.send_message(message.chat.id, "📊 *HASIL TES 4 GRUP:*\n\n" + "\n".join(hasil), parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def cek_id(message):
    bot.send_message(message.chat.id, f"ID chat ini: `{message.chat.id}`\nID lu: `{message.from_user.id}`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    nama = message.from_user.first_name or "Kak"
    caption = f"✨ *Selamat Datang, {nama}* ✨\nDi *ZUAN PANEL* — Tempatnya Panel Premium.\n\nTerima kasih sudah mampir.\nSemua serba otomatis, jadi Kakak tidak perlu menunggu lama.\n\n╭ ──── *Profil Bot* ──── ╮\n│ 👑 Owner : ZUAN PANEL\n│ 🤖 Bot : Auto Order Panel\n│ ⚡ Status : Online 24 Jam\n╰ ───────────────── ╯\n\nSilahkan pilih menu di bawah, Kak. Kami siap melayani. 🤍"
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
    caption = f"🛒 *Katalog Panel Kami*\n\nSilahkan pilih paket yang Kakak inginkan.\nSemua paket sudah termasuk garansi & support penuh."
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
    bot.send_message(call.message.chat.id, f"✦ *{paket['nama']}* ✦\n\n{paket['desc']}\n\nBoleh kirimkan *Username Panel* yang Kakak inginkan?\n\nContoh : `zuanww`", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    uid = message.from_user.id
    data = orders[uid]
    text = message.text.strip()
    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id, f"Baik, username *`{text}`* sudah kami amankan. 🤍\n\nBoleh kirimkan *Email* Kakak?\n\nContoh : `email@gmail.com`", parse_mode="Markdown")
        return
    if data["step"] == "email":
        data["email"] = text
        data["step"] = "bayar"
        order_id = f"INV-ZUAN-{int(time.time())}-{uid}"
        data["order_id"] = order_id
        orders_by_id[order_id] = data
        caption = f"🧾 *Invoice Pembayaran*\n*ZUAN PANEL*\n──────────────────\n📦 Produk : {data['paket_nama']}\n👤 Username : `{data['username_panel']}`\n🆔 Order ID : `{order_id}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + "\n──────────────────\n\nSilahkan scan QRIS di atas ya Kak.\nSetelah membayar, tekan tombol di bawah. 🤍"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅  Saya Sudah Bayar", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("✕  Batalkan Pesanan", callback_data=f"batal_{order_id}"))
        try:
            if "PASTE-LINK" not in QRIS_STATIS_URL:
                img = requests.get(QRIS_STATIS_URL, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, caption + "\n\n⚠️ *QRIS belum di-set, hubungi admin @zuanww*", parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        kirim_payment(f"🔔 *PESANAN BARU MASUK!*\n──────────────────\n👤 Customer : {uname}\n📦 Paket : {data['paket_nama']}\n👤 Username Panel : `{data['username_panel']}`\n📧 Email : `{data['email']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n⏳ Status : Menunggu Pembayaran\n🆔 Order ID : `{order_id}`")

@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Terima kasih Kak, laporan pembayaran diterima. 🤍\n\nPesanan *{data['paket_nama']}* untuk username *`{data['username_panel']}`* akan dicek admin dan segera diproses.", parse_mode="Markdown")
        kirim_testi(f"✅ *PEMBAYARAN DILAPORKAN! TESTI BARU!*\n📦 Paket : {data['paket_nama']}\n👤 Username : `{data['username_panel']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 Order ID : `{order_id}`\n\nTerima kasih sudah order di ZUAN PANEL! 🤍")
        kirim_payment(f"✅ *CUSTOMER KLIK SUDAH BAYAR - {data['paket_nama']}*\n👤 `{data.get('username_panel','-')}`\n💰 Rp {data['harga']:,}".replace(",", ".") + f"\n🆔 `{order_id}`\n\nCek mutasi, gas buatin panelnya min! 🔥")
        return
    if call.data.startswith("batal_"):
        order_id = call.data.replace("batal_", "")
        data_batal = orders_by_id.get(order_id)
        if order_id in orders_by_id: del orders_by_id[order_id]
        for uid in list(orders.keys()):
            if orders[uid].get("order_id") == order_id: del orders[uid]
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Baik Kak, pesanan sudah kami batalkan.\n\nJika berubah pikiran, ketik /start kapan saja. 🤍", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Pesanan dibatalkan.")
        if data_batal:
            kirim_payment(f"❌ *PESANAN DIBATALKAN*\n🆔 `{order_id}`\n📦 {data_batal['paket_nama']} - `{data_batal.get('username_panel','-')}`")
        return

@bot.callback_query_handler(func=lambda c: c.data in ["menu_topup", "menu_stok"])
def menu_lain(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    if call.data == "menu_topup":
        bot.send_message(call.message.chat.id, "Untuk Top Up Saldo, silahkan hubungi Admin ya Kak. 🤍", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, "Semua stok kami *READY* ya Kak. Silahkan langsung order saja. ✨", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['promo'])
def cmd_promo(message):
    if message.from_user.id != ADMIN_ID: return
    teks_promo = f"🔥 *PROMO PANEL - ZUAN PANEL* 🔥\n\n✨ *Panel Premium, Harga Merakyat!*\n──────────────────\n📦 Panel 1GB — Rp 5.000\n📦 Panel 5GB — Rp 15.000 ⭐ PALING LARIS\n📦 Panel 10GB — Rp 25.000\n📦 Panel UNLI — Rp 50.000\n──────────────────\n\n✅ Garansi Full\n✅ Support 24 Jam\n✅ Proses Otomatis\n\n🛒 Order : @Auto_orderpanelbaru_bot\n💬 Admin : @zuanww"
    kirim_promo(teks_promo, foto=BANNER_URL)
    bot.send_message(message.chat.id, "✅ Promo udah gue kirim ke Grup Utama + Grup Bebas Promosi bang!")

def auto_promo_loop():
    while True:
        time.sleep(7200)
        teks = f"🔥 *ZUAN PANEL READY!* 🔥\n\nPanel 5GB cuma Rp 15.000 aja!\nGaransi full, proses otomatis.\n\nOrder di : @Auto_orderpanelbaru_bot"
        kirim_promo(teks, foto=BANNER_URL)

threading.Thread(target=auto_promo_loop, daemon=True).start()
print("✅ ZUAN PANEL - 4 GRUP JALAN!")
bot.infinity_polling()
