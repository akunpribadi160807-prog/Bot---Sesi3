import os, time, requests, telebot, threading, random
from datetime import datetime
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
DATA_FILE = "vps_orders.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8493708698"))
bot = telebot.TeleBot(TOKEN)

GROUP_UTAMA = -1004497488934
GROUP_PROMO = -1003900745031
GROUP_TESTI = -1004432426937
GROUP_PAYMENT = -1004257626762
# === LINK GRUP ZUAN PANEL - UDAH ASLI ===
LINK_GRUP_UTAMA = "https://t.me/+W3MpouTl421mYWI9"
LINK_GRUP_PROMO = "https://t.me/+jbxIKw7ic7gyMmQ1"
LINK_GRUP_PAYMENT = "https://t.me/+QOEOL7iMLWE1YTk1"
LINK_GRUP_TESTI = "https://t.me/+67DpU4ac2HxiY2U1"
# === PEMBAYARAN FINAL ===
NAMA_BISNIS = "DEVELOPER PANEL IN"
NAMA_REKENING = "MUHAMAD IKHSANDI AKBAR"
SEABANK_NO = "901242145662"
BSI_NO = "7342034459"
GOPAY_NO = "085872257850"

BANNER_URL = "https://i.ibb.co.com/v4XNy1Jv/IMG-20261109-WA0076.jpg"
QRIS_STATIS_URL = "https://i.ibb.co.com/HLnGJPGK/qr-ID1026639236524-14-11-26-1794643632-1794643632979.jpg"
WELCOME_URL = "https://i.ibb.co.com/b5Jx4qPb/IMG-20261114-WA3337.jpg"

HARGA = {
    "1gb": {"nama": "Panel 1GB", "harga": 5000, "desc": "Ringan, hemat, buat yang baru mulai cobain."},
    "5gb": {"nama": "Panel 5GB", "harga": 15000, "desc": "Ini sih yang paling laris, udah paling pas buat harian."},
    "10gb": {"nama": "Panel 10GB", "harga": 25000, "desc": "Buat yang butuh power lebih, dijamin anti lemot."},
    "unli": {"nama": "Panel UNLI", "harga": 50000, "desc": "Bebas tanpa batas, puas-puasin sampe bosen."},
}
VPS_KATEGORI = {
    "LOW": {
        "nama": "Paket VPS Hemat. Garansi 1 Hari",
        "list": [
            {"ram": "2GB", "cpu": "2 CPU", "ssd": "60GB SSD", "bw": "3TB BW", "harga": 3000},
            {"ram": "4GB", "cpu": "2 CPU", "ssd": "80GB SSD", "bw": "4TB BW", "harga": 3000},
            {"ram": "8GB", "cpu": "4 CPU", "ssd": "160GB SSD", "bw": "5TB BW", "harga": 3000},
            {"ram": "16GB", "cpu": "2 CPU", "ssd": "50GB SSD", "bw": "4TB BW", "harga": 3000},
        ]
    },
    "BASIC": {
        "nama": "Paket VPS Standar. Garansi 3 Hari",
        "list": [
            {"ram": "2GB", "cpu": "2 CPU", "ssd": "60GB SSD", "bw": "3TB BW", "harga": 4000},
            {"ram": "4GB", "cpu": "2 CPU", "ssd": "80GB SSD", "bw": "4TB BW", "harga": 4000},
            {"ram": "8GB", "cpu": "4 CPU", "ssd": "160GB SSD", "bw": "5TB BW", "harga": 4000},
            {"ram": "16GB", "cpu": "2 CPU", "ssd": "50GB SSD", "bw": "4TB BW", "harga": 4000},
        ]
    },
    "MEDIUM": {
        "nama": "Paket VPS Peforma Tinggi. Garansi 5 Hari",
        "list": [
            {"ram": "2GB", "cpu": "2 CPU", "ssd": "60GB SSD", "bw": "3TB BW", "harga": 5000},
            {"ram": "4GB", "cpu": "2 CPU", "ssd": "80GB SSD", "bw": "4TB BW", "harga": 5000},
            {"ram": "8GB", "cpu": "4 CPU", "ssd": "160GB SSD", "bw": "5TB BW", "harga": 5000},
            {"ram": "16GB", "cpu": "2 CPU", "ssd": "50GB SSD", "bw": "4TB BW", "harga": 5000},
        ]
    },
    "PREMIUM": {
        "nama": "Paket VPS Peforma Ultra. Garansi 6 Hari",
        "list": [
            {"ram": "2GB", "cpu": "2 CPU", "ssd": "60GB SSD", "bw": "3TB BW", "harga": 6000},
            {"ram": "4GB", "cpu": "2 CPU", "ssd": "80GB SSD", "bw": "4TB BW", "harga": 6000},
            {"ram": "8GB", "cpu": "4 CPU", "ssd": "160GB SSD", "bw": "5TB BW", "harga": 6000},
            {"ram": "16GB", "cpu": "2 CPU", "ssd": "50GB SSD", "bw": "4TB BW", "harga": 7000},
        ]
    },
}
orders = {}
orders_by_id = {}

FILE_WELCOME = "udah_welcome.txt"
udah_welcome = set()
try:
    if os.path.exists(FILE_WELCOME):
        with open(FILE_WELCOME, "r") as f:
            for line in f:
                line = line.strip()
                if line: udah_welcome.add(int(line))
        print(f"[WELCOME LOAD] {len(udah_welcome)} user udah pernah welcome")
except Exception as e: print(f"[WELCOME LOAD GAGAL] {e}")

def simpan_welcome(uid):
    try:
        udah_welcome.add(uid)
        with open(FILE_WELCOME, "a") as f:
            f.write(f"{uid}\n")
    except Exception as e: print(f"[SIMPAN WELCOME GAGAL] {e}")

def hapus_pesan_lama(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass

def stiker(chat_id, emoji):
    try: bot.send_message(chat_id, emoji)
    except: pass

def kirim_payment(teks, jangan_kirim_ke=None):
    targets = [GROUP_PAYMENT]
    if ADMIN_ID != jangan_kirim_ke:
        targets.append(ADMIN_ID)
    for target in targets:
        try: bot.send_message(target, teks, parse_mode="Markdown")
        except Exception as e: print(f"[PAYMENT GAGAL] {e}")

def kirim_promo(teks, foto=None):
    for gid in [GROUP_UTAMA, GROUP_PROMO]:
        try:
            if foto:
                img = requests.get(foto, timeout=20).content
                bot.send_photo(gid, BytesIO(img), caption=teks, parse_mode="Markdown")
            else: bot.send_message(gid, teks, parse_mode="Markdown")
        except Exception as e: print(f"[PROMO GAGAL] {e}")

def kirim_link_grup(chat_id):
    teks = (
        f"🎉 *MAKASIH UDAH ORDER DI ZUAN PANEL!* 🎉\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Biar kakak gak ketinggalan info, yuk gabung semua grup kita! 👇\n\n"
        f"👑 *GRUP UTAMA - ZUAN PANEL*\n"
        f"Tempat ngobrol, tanya-tanya, & info restock!\n"
        f"👉 {LINK_GRUP_UTAMA}\n\n"
        f"⭐ *GRUP TESTIMONI*\n"
        f"Bukti orderan pelanggan lain, asli no settingan!\n"
        f"👉 {LINK_GRUP_TESTI}\n\n"
        f"🔥 *GRUP BEBAS PROMOSI*\n"
        f"Promo tiap hari, harga miring, gas cepet-cepetan!\n"
        f"👉 {LINK_GRUP_PROMO}\n\n"
        f"💳 *GRUP PAYMENT / INFO PEMBAYARAN*\n"
        f"Info pembayaran & bukti TF yang udah ACC!\n"
        f"👉 {LINK_GRUP_PAYMENT}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Jangan lupa join semua ya kak, biar gak ketinggalan promo 5GB cuma 15K! 🤍"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👑  Gabung Grup Utama", url=LINK_GRUP_UTAMA))
    markup.add(InlineKeyboardButton("⭐  Liat Testimoni", url=LINK_GRUP_TESTI))
    markup.add(InlineKeyboardButton("🔥  Grup Bebas Promosi", url=LINK_GRUP_PROMO))
    markup.add(InlineKeyboardButton("💳  Grup Payment", url=LINK_GRUP_PAYMENT))
    try:
        bot.send_message(chat_id, teks, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"[LINK GRUP GAGAL] {e}")
        
def kirim_welcome_testi(user):
    if user.id in udah_welcome: return
    try:
        uname = f"@{user.username}" if user.username else "-"
        nama = user.first_name or "Pelanggan Baru"
        waktu = datetime.now().strftime("%H:%M, %d/%m/%y")
        total_baru = len(udah_welcome) + 1
        if total_baru < 20: target = 20
        elif total_baru < 50: target = 50
        elif total_baru < 100: target = 100
        else: target = total_baru + 50
        sisa = target - total_baru
        persen = int(total_baru / target * 10)
        bar = "█" * persen + "░" * (10 - persen)
        caption_testi = f"👑 *PELANGGAN BARU DATANG* 👑\n━━━━━━━━━━━━━━━━━━\n✨ Selamat datang, *{nama}*! ✨\nWelcome to *ZUAN PANEL* — tempatnya panel premium.\n\n╭ ─── *INFO PELANGGAN* ─── ╮\n│ 👤 Username : {uname}\n│ 🆔 ID : `{user.id}`\n│ ⏰ Start : {waktu}\n╰ ───────────────── ╯\n\nRestock • Promo • Harga • Stock • Panel • Auto Order\n\nSemoga betah ya kak, jangan lupa order, gas! 🔥"
        caption_utama = f"👑 *PELANGGAN BARU DATANG* 👑\n━━━━━━━━━━━━━━━━━━\n✨ Selamat datang, *{nama}*! ✨\nWelcome to *ZUAN PANEL* — tempatnya panel premium.\n\n╭ ─── *INFO PELANGGAN* ─── ╮\n│ 👤 Username : {uname}\n│ 🆔 ID : `{user.id}`\n│ ⏰ Start : {waktu}\n╰ ───────────────── ╯\n\n╔ ═══ *TOTAL PELANGGAN BARU* ═══ ╗\n║  👥  *{total_baru} PELANGGAN*  udah join!  ║\n╚ ═══════════════════════ ╝\n\n📊 *MENUJU {target} PELANGGAN*\n[{bar}] {total_baru}/{target}\nKurang {sisa} lagi, gas ramein! 🔥\n\n━━━━━━━━━━━━━━━━━━\n🎁 *BONUS MEMBER BARU*\n│ • Garansi Full — Kalo ada apa-apa, diganti baru!\n│ • Support 24 Jam — Admin fast respon!\n│ • Proses Otomatis — Tidak perlu menunggu lama!\n━━━━━━━━━━━━━━━━━━\n🔥 *PALING LARIS HARI INI*\n│ ⭐ Panel 5GB — Rp 15.000 aja!\n│ 💎 Panel UNLI — Rp 50.000, bebas puas-puasin!\n━━━━━━━━━━━━━━━━━━\n⭐⭐⭐⭐⭐  *5.0 / 5.0* — 100% Pelanggan Puas!\n📦 Stok : *READY* — Langsung gas order!\n\n👑 Yuk jadi pelanggan ke-*{total_baru + 1}* selanjutnya!\nSemoga betah ya kak *{nama}*, jangan lupa order! 🤍"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚀  START JUGA — GAS ORDER!", url="https://t.me/Auto_orderpanelbaru_bot?start=start"))
        for gid, caption, nama_grup in [(GROUP_TESTI, caption_testi, "TESTI"), (GROUP_UTAMA, caption_utama, "UTAMA")]:
            try:
                img = requests.get(WELCOME_URL, timeout=20).content
                bot.send_photo(gid, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
            except:
                try: bot.send_message(gid, caption, parse_mode="Markdown", reply_markup=markup)
                except: pass
        simpan_welcome(user.id)
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

@bot.message_handler(commands=['total'])
def cek_total(message):
    if message.from_user.id != ADMIN_ID: return
    bot.send_message(message.chat.id, f"👥 *TOTAL PELANGGAN BARU*\n━━━━━━━━━━━━━━━━━━\nTotal yang udah pernah /start : *{len(udah_welcome)} orang*\n━━━━━━━━━━━━━━━━━━\nMakin rame bang! 🔥", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    kirim_welcome_testi(message.from_user)
    nama = message.from_user.first_name or "Kak"
    stiker(message.chat.id, "👑")
    caption = f"✨ *Halo, {nama}!* ✨\nSelamat datang di *ZUAN PANEL* 🤍\n\nDisini semua serba otomatis, jadi kakak tidak perlu menunggu lama.\n\n╭ ──── *ZUAN PANEL* ──── ╮\n│ 👑 Owner : {NAMA_BISNIS}\n│ 🤖 Bot : Auto Order 24 Jam\n│ 💎 Garansi : Full Garansi\n╰ ───────────────── ╯\n\nYuk pilih menu dibawah, kakak mau order yang mana? 😊"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🛒  Order Panel", callback_data="menu_order"), InlineKeyboardButton("💳  Top Up Saldo", callback_data="menu_topup"))
    markup.add(InlineKeyboardButton("📦  Cek Stok", callback_data="menu_stok"), InlineKeyboardButton("💬  Hubungi Admin", url="https://t.me/zuanww"))
    markup.add(InlineKeyboardButton("🌐  Kunjungi Website", url="https://zuanpanel.web.id"))
    markup.add(InlineKeyboardButton("🖥 Order VPS Peforma Ultra", callback_data="menu_vps"))
    try:
        img = requests.get(BANNER_URL, timeout=20).content
        bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
    except: bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "menu_order")
def menu_order(call):
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    caption = f"🛒 *Katalog Panel Kami* 💎\n━━━━━━━━━━━━━━━━━━\nPilih aja kak, semua udah termasuk garansi & support penuh kok.\nTidak usah bingung, tinggal klik aja yang kakak suka 👇"
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

@bot.message_handler(func=lambda m: m.content_type == 'text' and m.from_user.id in orders and orders[m.from_user.id].get("step") in ["username", "email"])
def handle_input(message):
    uid = message.from_user.id
    data = orders[uid]
    text = message.text.strip()
    if data["step"] == "username":
        data["username_panel"] = text
        data["step"] = "email"
        bot.send_message(message.chat.id, f"Oke, username *`{text}`* sudah kami amankan nih 🤍\n\nTerakhir, boleh minta *Email* kakak?\nContoh : `email@gmail.com`", parse_mode="Markdown")
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
            f"💳 *PILIH METODE PEMBAYARAN:*\n\n"
            f"1️⃣ *QRIS DANA BISNIS - Scan diatas*\n"
            f"Atas Nama : {NAMA_BISNIS}\n"
            f"(a.n {NAMA_REKENING})\n\n"
            f"2️⃣ *SEABANK*\n"
            f"🏦 No Rek : `{SEABANK_NO}`\n"
            f"Atas Nama : {NAMA_REKENING}\n\n"
            f"3️⃣ *BSI (Bank Syariah Indonesia)*\n"
            f"🏦 No Rek : `{BSI_NO}`\n"
            f"Atas Nama : {NAMA_REKENING}\n\n"
            f"4️⃣ *GOPAY*\n"
            f"📱 No : `{GOPAY_NO}`\n"
            f"Atas Nama : {NAMA_REKENING}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ *PENTING!*\n"
            f"Pastikan atas nama *{NAMA_BISNIS}* / *{NAMA_REKENING}* ya kak, jangan TF ke nama lain!\n"
            f"Abis TF, klik tombol *Saya Sudah Bayar* dibawah, terus kirim foto buktinya 🤍"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅  Saya Sudah Bayar", callback_data=f"bayar_{order_id}"))
        markup.add(InlineKeyboardButton("🔍  Cek Status Pembayaran", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("✕  Batalkan Pesanan", callback_data=f"batal_{order_id}"))
        try:
            img = requests.get(QRIS_STATIS_URL, timeout=20).content
            bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
        except: bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        kirim_payment(f"🔔 *PESANAN BARU MASUK!* 🔔\n━━━━━━━━━━━━━━━━━━\n👤 Customer : {uname}\n📦 Paket : {data['paket_nama']}\n👤 Username Panel : `{data['username_panel']}`\n📧 Email : `{data['email']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n⏳ Status : Menunggu Pembayaran\n🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━\n\nAda orderan baru @zuanww, siap-siap cek mutasi! 🔥", jangan_kirim_ke=message.from_user.id)

# === CEK FOTO BUKTI - WAJIB DICEK DULU, GAK ADA CAPTION PUN TETEP DICEK ===
@bot.message_handler(content_types=['photo'])
def handle_bukti_tf(message):
    uid = message.from_user.id
    data = orders.get(uid)
    if not data or data.get("step") != "nunggu_bukti":
        return
    order_id = data.get("order_id")
    if not order_id: return
    foto_id = message.photo[-1].file_id
    data["foto_bukti_id"] = foto_id
    data["uname_tele"] = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    data["nama_pelanggan"] = message.from_user.first_name or "-"
    data["user_chat_id"] = uid
    # Tahan dulu, belum dianggap bayar!
    data["step"] = "menunggu_verifikasi"
    data["bukti_terkirim"] = False
    orders_by_id[order_id] = data
    # Kasih tau pelanggan: bukti lagi dicek, jangan nanya-nanya lagi
    bot.send_message(message.chat.id, f"Makasih kak fotonya udah masuk! 🙏\n\nBukti TF kakak lagi kami cek dulu ya, kami liat foto nya, kami cocokin nama + nominalnya.\n\nKalo udah bener transfer ke *{NAMA_BISNIS}* / *{NAMA_REKENING}*, langsung kami proses!\nTunggu sebentar ya kak, paling 1-2 menit! ✨", parse_mode="Markdown")
    # Kirim ke admin + grup payment dengan tombol verifikasi
    caption_bukti = (
        f"🔍 *CEK BUKTI TF - BELUM ACC!* 🔍\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 Customer : {data['uname_tele']}\n"
        f"👤 Nama : {data['nama_pelanggan']}\n"
        f"🆔 ID Telegram : `{uid}`\n"
        f"📦 Paket : {data['paket_nama']}\n"
        f"👤 Username Panel : `{data.get('username_panel','-')}`\n"
        f"📧 Email : `{data.get('email','-')}`\n"
        f"💰 Total Harus : Rp {data['harga']:,}".replace(",", ".") + f"\n"
        f"🆔 Order ID : `{order_id}`\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"⚠️ *CEK DULU BANG SEBELUM ACC:*\n"
        f"1. Nama di foto = *{NAMA_BISNIS}* / *{NAMA_REKENING}* ?\n"
        f"2. Nominalnya pas Rp {data['harga']:,} ?\n"
        f"3. Fotonya jelas, gak editan / gak blur ?\n\n"
        f"Kalo udah bener semua, klik ✅ VALID\n"
        f"Kalo namanya beda / nominal salah / editan, klik ❌ TOLAK"
    )
    markup_verif = InlineKeyboardMarkup()
    markup_verif.add(InlineKeyboardButton("✅  VALID - Nama Cocok, Gas!", callback_data=f"acc_{order_id}"))
    markup_verif.add(InlineKeyboardButton("❌  TOLAK - Nama Salah", callback_data=f"tolak_{order_id}"))
    for target in [GROUP_PAYMENT, ADMIN_ID]:
        try:
            if target == ADMIN_ID and uid == ADMIN_ID: continue
            bot.send_photo(target, foto_id, caption=caption_bukti, parse_mode="Markdown", reply_markup=markup_verif)
        except Exception as e: print(f"[BUKTI GAGAL KE {target}] {e}")

# === ADMIN KLIK VALID / TOLAK ===
@bot.callback_query_handler(func=lambda c: c.data.startswith("acc_") or c.data.startswith("tolak_"))
def handle_verif_admin(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Cuma admin yang bisa ACC ya bang!", show_alert=True)
        return
    is_acc = call.data.startswith("acc_")
    order_id = call.data.replace("acc_", "").replace("tolak_", "")
    data = orders_by_id.get(order_id)
    if not data:
        bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
    user_chat_id = data.get("user_chat_id")
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    if is_acc:
        # === VALID - LANJUTIN ===
        data["bukti_terkirim"] = True
        data["step"] = "bukti_dikirim"
        orders_by_id[order_id] = data
        if user_chat_id in orders:
            orders[user_chat_id] = data
        bot.answer_callback_query(call.id, "ACC! Pelanggan dilanjutin!")
        bot.send_message(call.message.chat.id, f"✅ Order {order_id} udah di-ACC! Pelanggan udah dikasih tau buat lanjut!")
        if user_chat_id:
            bot.send_message(user_chat_id, f"Alhamdulillah, makasih ya kak! ✅\n\nBukti transfer kakak udah kami cek, udah bener transfer ke *{NAMA_BISNIS}* / *{NAMA_REKENING}*! 🎉\n\nPanelnya langsung kami buatin ya, tunggu sebentar! 🙏✨", parse_mode="Markdown")
            kirim_link_grup(user_chat_id)
            markup_izin = InlineKeyboardMarkup()
            markup_izin.add(InlineKeyboardButton("✅  Boleh, Gas! Jadiin Testi", callback_data=f"izin_ya_{order_id}"))
            markup_izin.add(InlineKeyboardButton("❌  Jangan, Privasi Kak", callback_data=f"izin_tidak_{order_id}"))
            bot.send_message(user_chat_id, f"Sebelum itu, kami mau izin dulu nih kak 🙏\n\n*📸 Boleh kah bukti TF kakak ini kami jadikan testimoni di grup?*\n\nBiar pelanggan lain makin yakin kalau *ZUAN PANEL* itu asli & amanah! 🔥\n\nTenang saja kak, kalau kakak tidak berkenan, kami *TIDAK AKAN* menyebarkannya kok, privasi kakak nomor 1! 🤍", parse_mode="Markdown", reply_markup=markup_izin)
    else:
        # === TOLAK - NOLAK HALUS KE PELANGGAN ===
        data["step"] = "nunggu_bukti"
        data["bukti_terkirim"] = False
        orders_by_id[order_id] = data
        if user_chat_id in orders:
            orders[user_chat_id] = data
        bot.answer_callback_query(call.id, "Ditolak! Pelanggan dikasih tau halus!")
        bot.send_message(call.message.chat.id, f"❌ Order {order_id} ditolak, pelanggan udah dikasih tau halus!")
        if user_chat_id:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔄  Kirim Ulang Bukti Yang Benar", callback_data=f"bayar_{order_id}"))
            markup.add(InlineKeyboardButton("💬  Chat Admin, Aku Bingung", url="https://t.me/zuanww"))
            bot.send_message(user_chat_id,
                f"Maaf banget ya kak, aku jadi gak enak nih 🙏🥺\n\n"
                f"Barusan bukti TF kakak udah kami cek foto nya satu-satu, tapi kayaknya ada yang kurang pas kak.\n\n"
                f"Di sistem kami yang ke-daftar cuma 2 nama ini kak:\n\n"
                f"🏪 *{NAMA_BISNIS}*\n"
                f"👑 *{NAMA_REKENING}*\n\n"
                f"Takutnya kakak salah transfer ke toko lain, atau salah kirim bukti punya orang lain, atau nominalnya kurang pas.\n"
                f"Sayang banget kan kalo uang kakak nyangkut di tempat lain? 😢\n\n"
                f"Boleh tolong cek lagi gak kak? Coba liat lagi di bukti transfer kakak:\n"
                f"• Atas namanya udah bener *{NAMA_BISNIS}* / *{NAMA_REKENING}* belum?\n"
                f"• Nominalnya udah pas belum?\n"
                f"• Fotonya jelas gak ke-crop?\n\n"
                f"Kalo kakak yakin udah bener transfer ke *{NAMA_BISNIS}*, klik aja *CHAT ADMIN* di bawah, biar admin bantu cek manual ya kak, jangan khawatir, uang kakak aman kok! 🤗\n\n"
                f"Atau kalo kakak salah kirim, klik *KIRIM ULANG* aja ya kak!",
                parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("izin_"))
def handle_izin_testi(call):
    parts = call.data.split("_", 2)
    jawaban = parts[1]
    order_id = parts[2]
    data = orders_by_id.get(order_id)
    if not data:
        bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
    hapus_pesan_lama(call.message.chat.id, call.message.message_id)
    foto_id = data.get("foto_bukti_id")
    uname = data.get("uname_tele", "-")
    if jawaban == "ya":
        caption_testi_bukti = f"✅ *TESTI BARU MASUK!* 💎\n━━━━━━━━━━━━━━━━━━\n📦 Paket : {data['paket_nama']}\n👤 Customer : {uname}\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n━━━━━━━━━━━━━━━━━━\n\n📸 *BUKTI TRANSFER ASLI!*\nSudah diizinkan sama customernya langsung! 🤍\nMakasih sudah order di *ZUAN PANEL!*\n\nYuk yang belum order, gas nyusul! 🔥"
        try: bot.send_photo(GROUP_TESTI, foto_id, caption=caption_testi_bukti, parse_mode="Markdown")
        except Exception as e: print(f"[BUKTI TESTI GAGAL] {e}")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔍  Cek Status Pembayaran", callback_data=f"cek_{order_id}"))
        bot.send_message(call.message.chat.id, f"Wihh makasih banyak kak! 🥹🤍\n\nBerkat izin kakak, pelanggan lain jadi makin yakin order di sini!\n\nKakak emang the best, semoga sehat selalu dan rezekinya lancar terus ya kak! 🔥\n\nTinggal tunggu admin cek mutasi ya, sebentar lagi jadi kok! ✨", parse_mode="Markdown", reply_markup=markup)
        bot.answer_callback_query(call.id, "Makasih sudah izinin! 🤍")
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔍  Cek Status Pembayaran", callback_data=f"cek_{order_id}"))
        bot.send_message(call.message.chat.id, f"Siapp, aman kak! 🤍\n\nTenang saja, bukti TF kakak *TIDAK AKAN* kami sebarkan kemana-mana kok.\nHanya admin saja yang melihat untuk cek mutasi.\n\nPrivasi kakak nomor 1 di sini! 🫶\n\nTinggal tunggu admin cek ya, sebentar lagi jadi kok! ✨", parse_mode="Markdown", reply_markup=markup)
        bot.answer_callback_query(call.id, "Siap, privasi aman! 🤍")

@bot.callback_query_handler(func=lambda c: c.data.startswith("cek_") or c.data.startswith("bayar_") or c.data.startswith("batal_"))
def handle_cek_batal(call):
    if call.data.startswith("cek_"):
        order_id = call.data.replace("cek_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        if not data.get("bukti_terkirim"):
            bot.answer_callback_query(call.id, "Bukti TF nya lagi dicek admin dulu ya kak! ⏳", show_alert=True)
            bot.send_message(call.message.chat.id, "Sabar ya kak! 😊\n\nBukti TF kakak lagi kami cek foto nya dulu, kami cocokin nama + nominalnya.\nKalo udah bener, langsung kami proses kok! Tunggu sebentar ya 🙏", parse_mode="Markdown")
            return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        stiker(call.message.chat.id, "🎉")
        bot.send_message(call.message.chat.id, f"Yeayy makasih banyak kak! 🤍\n\nBukti TF kakak sudah kami cek dan udah VALID!\nPesanan *{data['paket_nama']}* buat username *`{data['username_panel']}`* lagi dibikin, bentar lagi jadi kok! ✨\nDitunggu yaa~", parse_mode="Markdown")
        return
    if call.data.startswith("bayar_"):
        order_id = call.data.replace("bayar_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        data["step"] = "nunggu_bukti"
        orders[call.from_user.id] = data
        bot.send_message(call.message.chat.id, f"Siapp kak! 🔥\n\nTinggal 1 langkah lagi nih.\n\n📸 *Kirim foto bukti TF / SS nya* kesini ya kak.\n\nBiar admin bisa langsung cek foto nya & cocokin nama + nominalnya.\nJangan di crop ya kak, biar jelas! 🤍", parse_mode="Markdown")
        bot.answer_callback_query(call.id)
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
        bot.send_message(call.message.chat.id, f"Yahh dibatalin 🥺\n\nGapapa kok kak, santai aja.\nKalo nanti berubah pikiran, tinggal klik dibawah aja ya, kami standby kok 🤍", parse_mode="Markdown", reply_markup=markup)
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
    bot.send_message(message.chat.id, "✅ Promo sudah kami kirim ke Grup Utama + Grup Bebas Promosi bang!", parse_mode="Markdown")

def auto_promo_loop():
    while True:
        time.sleep(7200)
        teks = f"🔥 *ZUAN PANEL READY!* 🔥\n━━━━━━━━━━━━━━━━━━\nPanel 5GB cuma Rp 15.000 aja!\nGaransi full, proses otomatis.\n\nOrder di : @Auto_orderpanelbaru_bot"
        kirim_promo(teks, foto=BANNER_URL)

threading.Thread(target=auto_promo_loop, daemon=True).start()

def kirim_vps_kategori(chat_id):
    teks = (
        f"🚀 *VPS DIGITALOCEAN*\n"
        f"✅ Stok sudah dicek saat membuka layanan.\n"
        f"🔒 Stok akan dicek lagi sebelum pembayaran.\n\n"
        f"📦 *PILIH PAKET*\n\n"
        f"🟢 *LOW*\n"
        f"🛡️ Garansi: 1 Hari\n"
        f"🔄 Replace: 1x Replace selama masa garansi\n\n"
        f"💎 *BASIC*\n"
        f"🛡️ Garansi: 3 Hari\n"
        f"🔄 Replace: 1x Replace selama masa garansi\n\n"
        f"🟢 *MEDIUM*\n"
        f"🛡️ Garansi: 5 Hari\n"
        f"🔄 Replace: 2x Replace selama masa garansi\n\n"
        f"💎 *PREMIUM*\n"
        f"🛡️ Garansi: 6 Hari\n"
        f"🔄 Replace: 1x Replace selama masa garansi\n\n"
        f"👇 Pilih paket untuk melihat spesifikasi dan harga.\n\n"
        f"📦 Total Stok Tersedia: 8 VPS\n"
        f"✅ STOK VPS TERUPDATE HARI INI!"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🟢 LOW", callback_data="vpskat_low"), InlineKeyboardButton("💎 BASIC", callback_data="vpskat_basic"))
    markup.add(InlineKeyboardButton("🟢 MEDIUM", callback_data="vpskat_medium"), InlineKeyboardButton("💎 PREMIUM", callback_data="vpskat_premium"))
    markup.add(InlineKeyboardButton("⬅️ Kembali", callback_data="menu_lain"))
    bot.send_message(chat_id, teks, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "menu_vps")
def menu_vps(call):
    kirim_vps_kategori(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("vpskat_"))
def detail_vps_kategori(call):
    kat = call.data.replace("vpskat_", "", 1).upper()
    data = VPS_KATEGORI[kat]
    teks = f"{data['nama']}\n\n🖥 PILIH SPESIFIKASI VPS\n\n"
    markup = InlineKeyboardMarkup(row_width=4)
    for i, s in enumerate(data["list"], 1):
        teks += f"━━━━━━━━━━━━━━\n[ {i} ] {s['ram']} RAM\n{s['cpu']}\n{s['ssd']}\n{s['bw']}\n└➡️ Rp {s['harga']:,}\n\n"
        markup.add(InlineKeyboardButton(str(i+1), callback_data=f"vps_spec|{kat}|{i}"))
    teks += "Silahkan pilih nomor spesifikasi."
    markup.add(InlineKeyboardButton("⬅️ Kembali", callback_data="menu_vps"))
    bot.send_message(call.message.chat.id, teks, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("vps_spec|") or (call.data.startswith("vps_") and len(call.data.split("_"))==3 and call.data.split("_")[2].isdigit()))
def pilih_vps(call):
    if "|" in call.data:
        _, kat, idx = call.data.split("|")
    else:
        # buat kode lama kaya vps_LOW_0
        parts = call.data.split("_")
        kat = parts[1]
        idx = parts[2]
    kat = kat.upper()
    spec = VPS_KATEGORI[kat]["list"][int(idx)]
    order_id = f"VPS{random.randint(1000, 9999)}"
    data = load_data()
    data[order_id] = {
        "user_id": call.from_user.id,
        "username": call.from_user.username,
        "paket": f"VPS {kat} - {spec['ram']} RAM",
        "harga": spec['harga'],
        "panel_user": "-",
        "email": "-",
        "status": "menunggu_bukti"
    }
    save_data(data)
    teks = (
        f"🧾 *INVOICE - ZUAN PANEL* 🧾\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🆔 Order ID: `{order_id}`\n"
        f"📦 Produk: VPS {kat} - {spec['ram']} RAM\n"
        f"{spec['cpu']}\n"
        f"{spec['ssd']}\n"
        f"{spec['bw']}\n"
        f"💰 Total: *Rp {spec['harga']:,}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💳 *METODE PEMBAYARAN ZUAN PANEL* 💳\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🏦 *SEABANK:* 901242145662\n"
        f"a.n MUHAMAD IKHSANDI AKBAR\n\n"
        f"🏦 *BSI:* 7342034459\n"
        f"a.n MUHAMAD IKHSANDI AKBAR\n\n"
        f"📱 *GOPAY:* 085872257850\n"
        f"a.n MUHAMAD IKHSANDI AKBAR\n\n"
        f"📷 *QRIS:* DEVELOPER PANEL IN\n"
        f"a.n MUHAMAD IKHSANDI AKBAR\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Setelah transfer, kirim *FOTO BUKTI TF* kesini ya kak! 🤍"
    )
    bot.send_message(call.message.chat.id, teks, parse_mode="Markdown")
    try:
        bot.send_photo(call.message.chat.id, "https://i.ibb.co.com/HLnGJPGK/qr-ID1026639236524-14-11-26-1794643632-1794643632979.jpg", caption="📷 *QRIS ZUAN PANEL*\nScan ini ya kak!", parse_mode="Markdown")
    except:
        pass
    hapus_pesan(call.message.chat.id, call.message.message_id)
print("✅ ZUAN PANEL - FINAL ELEGAN JALAN!")
bot.infinity_polling()
