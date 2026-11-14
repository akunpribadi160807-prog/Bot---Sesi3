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

def kirim_welcome_testi(user):
    if user.id in udah_welcome:
        print(f"[WELCOME SKIP] {user.id} udah pernah, gak kirim lagi")
        return
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
        caption_testi = (
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
        caption_utama = (
            f"👑 *PELANGGAN BARU DATANG* 👑\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✨ Selamat datang, *{nama}*! ✨\n"
            f"Welcome to *ZUAN PANEL* — tempatnya panel premium.\n\n"
            f"╭ ─── *INFO PELANGGAN* ─── ╮\n"
            f"│ 👤 Username : {uname}\n"
            f"│ 🆔 ID : `{user.id}`\n"
            f"│ ⏰ Start : {waktu}\n"
            f"╰ ───────────────── ╯\n\n"
            f"╔ ═══ *TOTAL PELANGGAN BARU* ═══ ╗\n"
            f"║  👥  *{total_baru} PELANGGAN*  udah join!  ║\n"
            f"╚ ═══════════════════════ ╝\n\n"
            f"📊 *MENUJU {target} PELANGGAN*\n"
            f"[{bar}] {total_baru}/{target}\n"
            f"Kurang {sisa} lagi, gas ramein! 🔥\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎁 *BONUS MEMBER BARU*\n"
            f"│ • Garansi Full — Kalo ada apa-apa, diganti baru!\n"
            f"│ • Support 24 Jam — Admin fast respon!\n"
            f"│ • Proses Otomatis — Tidak perlu menunggu lama!\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔥 *PALING LARIS HARI INI*\n"
            f"│ ⭐ Panel 5GB — Rp 15.000 aja!\n"
            f"│ 💎 Panel UNLI — Rp 50.000, bebas puas-puasin!\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⭐⭐⭐⭐⭐  *5.0 / 5.0* — 100% Pelanggan Puas!\n"
            f"📦 Stok : *READY* — Langsung gas order!\n\n"
            f"👑 Yuk jadi pelanggan ke-*{total_baru + 1}* selanjutnya!\n"
            f"Semoga betah ya kak *{nama}*, jangan lupa order! 🤍"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚀  START JUGA — GAS ORDER!", url="https://t.me/Auto_orderpanelbaru_bot?start=start"))
        for gid, caption, nama_grup in [(GROUP_TESTI, caption_testi, "TESTI"), (GROUP_UTAMA, caption_utama, "UTAMA")]:
            try:
                img = requests.get(WELCOME_URL, timeout=20).content
                bot.send_photo(gid, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
                print(f"[WELCOME OK] {nama_grup} {nama} - Total: {total_baru}")
            except Exception as e:
                print(f"[WELCOME GAGAL {nama_grup}] {e}")
                try: bot.send_message(gid, caption, parse_mode="Markdown", reply_markup=markup)
                except: pass
        simpan_welcome(user.id)
        print(f"[WELCOME OK] {nama} {user.id} - Total sekarang {total_baru}")
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
    caption = (
        f"✨ *Halo, {nama}!* ✨\n"
        f"Selamat datang di *ZUAN PANEL* 🤍\n\n"
        f"Disini semua serba otomatis, jadi kakak tidak perlu menunggu lama.\n\n"
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
        f"Tidak usah bingung, tinggal klik aja yang kakak suka 👇"
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
            f"Tinggal scan QRIS diatas ya kak, abis itu klik tombol dibawah 🤍"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅  Saya Sudah Bayar", callback_data=f"bayar_{order_id}"))
        markup.add(InlineKeyboardButton("🔍  Cek Status Pembayaran", callback_data=f"cek_{order_id}"))
        markup.add(InlineKeyboardButton("✕  Batalkan Pesanan", callback_data=f"batal_{order_id}"))
        try:
            if "PASTE-LINK" not in QRIS_STATIS_URL:
                img = requests.get(QRIS_STATIS_URL, timeout=20).content
                bot.send_photo(message.chat.id, BytesIO(img), caption=caption, parse_mode="Markdown", reply_markup=markup)
            else: bot.send_message(message.chat.id, caption + "\n\n⚠️ QRIS belum di-set, hubungi admin @zuanww ya kak", parse_mode="Markdown", reply_markup=markup)
        except: bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)
        uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        kirim_payment(f"🔔 *PESANAN BARU MASUK!* 🔔\n━━━━━━━━━━━━━━━━━━\n👤 Customer : {uname}\n📦 Paket : {data['paket_nama']}\n👤 Username Panel : `{data['username_panel']}`\n📧 Email : `{data['email']}`\n💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n⏳ Status : Menunggu Pembayaran\n🆔 Order ID : `{order_id}`\n━━━━━━━━━━━━━━━━━━\n\nAda orderan baru @zuanww, siap-siap cek mutasi! 🔥", jangan_kirim_ke=message.from_user.id)

@bot.message_handler(content_types=['photo'])
def handle_bukti_tf(message):
    uid = message.from_user.id
    data = orders.get(uid)
    if not data or data.get("step") != "nunggu_bukti":
        return
    order_id = data.get("order_id")
    if not order_id:
        return
    data["bukti_terkirim"] = True
    data["step"] = "bukti_dikirim"
    orders_by_id[order_id] = data
    foto_id = message.photo[-1].file_id
    uname = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    nama_pelanggan = message.from_user.first_name or "-"
    data["foto_bukti_id"] = foto_id
    data["uname_tele"] = uname
    data["nama_pelanggan"] = nama_pelanggan
    orders_by_id[order_id] = data
    caption_bukti = (
        f"✅ *CUSTOMER UDAH BAYAR!* 🔥\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 Customer : {uname}\n"
        f"👤 Nama : {nama_pelanggan}\n"
        f"🆔 ID Telegram : `{uid}`\n"
        f"📦 Paket : {data['paket_nama']}\n"
        f"👤 Username Panel : `{data.get('username_panel','-')}`\n"
        f"📧 Email : `{data.get('email','-')}`\n"
        f"💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n"
        f"🆔 Order ID : `{order_id}`\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📸 *BUKTI TF DI ATAS!*\n"
        f"Cek mutasi @zuanww, gas buatin panelnya! 🔥"
    )
    for target in [GROUP_PAYMENT, ADMIN_ID]:
        try:
            if target == ADMIN_ID and uid == ADMIN_ID:
                continue
            bot.send_photo(target, foto_id, caption=caption_bukti, parse_mode="Markdown")
        except Exception as e: print(f"[BUKTI GAGAL KE {target}] {e}")
    markup_izin = InlineKeyboardMarkup()
    markup_izin.add(InlineKeyboardButton("✅  Boleh, Gas! Jadiin Testi", callback_data=f"izin_ya_{order_id}"))
    markup_izin.add(InlineKeyboardButton("❌  Jangan, Privasi Kak", callback_data=f"izin_tidak_{order_id}"))
    bot.send_message(message.chat.id, f"Yeayy makasih kak! 🤍\n\nFoto bukti TF nya sudah kami teruskan ke admin, sedang dicek ya kak.\n\nSebelum itu, kami mau izin dulu nih kak 🙏\n\n*📸 Boleh kah bukti TF kakak ini kami jadikan testimoni di grup?*\n\nBiar pelanggan lain makin yakin kalau *ZUAN PANEL* itu asli & amanah, bukan kaleng-kaleng! 🔥\n\nTenang saja kak, kalau kakak tidak berkenan, kami *TIDAK AKAN* menyebarkannya kok, privasi kakak nomor 1! 🤍\n\nGimana kak, boleh ya? 😊", parse_mode="Markdown", reply_markup=markup_izin)

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
        caption_testi_bukti = (
            f"✅ *TESTI BARU MASUK!* 💎\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 Paket : {data['paket_nama']}\n"
            f"👤 Customer : {uname}\n"
            f"💰 Total : Rp {data['harga']:,}".replace(",", ".") + f"\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"📸 *BUKTI TRANSFER ASLI!*\n"
            f"Sudah diizinkan sama customernya langsung! 🤍\n"
            f"Makasih sudah order di *ZUAN PANEL!*\n\n"
            f"Yuk yang belum order, gas nyusul! 🔥"
        )
        try:
            bot.send_photo(GROUP_TESTI, foto_id, caption=caption_testi_bukti, parse_mode="Markdown")
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
            bot.answer_callback_query(call.id, "Belum ada bukti TF nya kak! ❌", show_alert=True)
            bot.send_message(call.message.chat.id, "Eitss belum bisa kak! 😅\n\nKakak belum kirim *foto bukti TF* nya nih.\nKirim dulu foto SS nya, baru bisa klik Cek Status ya 📸", parse_mode="Markdown")
            return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        stiker(call.message.chat.id, "🎉")
        bot.send_message(call.message.chat.id, f"Yeayy makasih banyak kak! 🤍\n\nBukti TF kakak sudah kami teruskan ke admin.\nPesanan *{data['paket_nama']}* buat username *`{data['username_panel']}`* lagi dicek admin, bentar lagi jadi kok! ✨\nDitunggu yaa~", parse_mode="Markdown")
        return
    if call.data.startswith("bayar_"):
        order_id = call.data.replace("bayar_", "")
        data = orders_by_id.get(order_id)
        if not data:
            bot.answer_callback_query(call.id, "Pesanan tidak ditemukan."); return
        hapus_pesan_lama(call.message.chat.id, call.message.message_id)
        data["step"] = "nunggu_bukti"
        orders[call.from_user.id] = data
        bot.send_message(call.message.chat.id, f"Siapp kak! 🔥\n\nTinggal 1 langkah lagi nih.\n\n📸 *Kirim foto bukti TF / SS nya* kesini ya kak.\n\nBiar admin bisa langsung cek mutasi & buatin panelnya.\nJangan di crop ya kak, biar jelas! 🤍", parse_mode="Markdown")
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
print("✅ ZUAN PANEL - FINAL ELEGAN JALAN!")
bot.infinity_polling()
