import os
import requests
import time
import telebot
import urllib.parse
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonDefault

try:
    from PIL import Image, ImageDraw, ImageFont
    ADA_PIL = True
except:
    ADA_PIL = False

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "849370608"))
KASERA_API_KEY = os.getenv("KASERA_API_KEY")
KASERA_BASE = "https://pay.kasera.id/v1"
bot = telebot.TeleBot(TOKEN)

try:
    bot.delete_my_commands()
    bot.set_my_commands([])
    bot.set_chat_menu_button(menu_button=MenuButtonDefault())
except:
    pass

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
    "unli": {"nama": "Panel UNLIMITED", "harga": 30000},
}
orders = {}

# ================= BANNER MODEL TOKOSHOPP - ZUAN VERSION =================
def bikin_gambar_qris(qr_string, d):
    try:
        # 1. QR ASLI Kasera
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&margin=5&data={urllib.parse.quote(qr_string)}"
        r = requests.get(qr_url, timeout=15)
        qr_img = Image.open(BytesIO(r.content)).convert("RGB")

        # 2. Gambar kanan - pake foto.jpg lu (robot ZUAN)
        kanan_img = None
        for f in ["foto.jpg", "banner.jpg", "zuan.jpg"]:
            try:
                kanan_img = Image.open(f).convert("RGB")
                break
            except:
                continue
        if kanan_img is None:
            kanan_img = Image.new("RGB", (500, 500), (10, 25, 60))

        # Kanvas: 1000 x 1150 - persis model TOKOSHOPP
        W, H = 1000, 1150
        canvas = Image.new("RGB", (W, H), (255, 248, 230))
        draw = ImageDraw.Draw(canvas)
        try:
            f_judul = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
            f_besar = ImageFont.truetype("DejaVuSans-Bold.ttf", 62)
            f_total = ImageFont.truetype("DejaVuSans-Bold.ttf", 68)
            f_logo = ImageFont.truetype("DejaVuSans-Bold.ttf", 66)
            f_kecil = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
            f_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
            f_biasa = ImageFont.truetype("DejaVuSans.ttf", 22)
        except:
            f_judul = f_besar = f_total = f_logo = f_kecil = f_med = f_biasa = ImageFont.load_default()

        def center(y, teks, font, warna):
            bb = draw.textbbox((0, 0), teks, font=font)
            draw.text(((W - (bb[2]-bb[0]))//2, y), teks, fill=warna, font=font)
        def center_x(x0, x1, y, teks, font, warna):
            bb = draw.textbbox((0, 0), teks, font=font)
            w = bb[2]-bb[0]
            draw.text((x0 + (x1-x0-w)//2, y), teks, fill=warna, font=font)

        # Border hitam tebal
        draw.rectangle([0, 0, W-1, H-1], outline=(0, 0, 0), width=10)

        # ===== ATAS KIRI: QRIS HANYA BERLAKU 1 JAM =====
        # Kotak kiri 0-500, kanan 500-1000
        draw.rectangle([10, 10, 500, 820], fill=(255, 248, 230), outline=(0, 0, 0), width=5)
        center_x(10, 500, 20, "QRIS HANYA", f_judul, (220, 0, 0))
        center_x(10, 500, 70, "BERLAKU 1 JAM", f_judul, (220, 0, 0))
        # QR
        qr_img = qr_img.resize((420, 420))
        canvas.paste(qr_img, (45, 150))
        center_x(10, 500, 590, "BAYAR DILUAR WAKTU", f_med, (220, 0, 0))
        center_x(10, 500, 625, "EXPIRED? SALDO HANGUS", f_med, (220, 0, 0))

        # ===== KANAN: GAMBAR ROBOT =====
        kanan_crop = kanan_img.resize((490, 810))
        canvas.paste(kanan_crop, (500, 10))
        draw.rectangle([500, 10, 990, 820], outline=(0, 0, 0), width=5)

        # ===== BAWAH: LOGO ZUANPANEL =====
        center(835, "ZUANPANEL.WEB.ID", f_logo, (20, 80, 200))
        center(910, "PAYMENT EDITION", f_med, (0, 0, 0))

        # ===== BAR BIRU TOTAL PEMBAYARAN =====
        draw.rectangle([10, 970, 990, 1080], fill=(20, 90, 180))
        draw.text((25, 990), "TOTAL PEMBAYARAN", fill=(255, 255, 255), font=f_med)
        draw.text((25, 1025), "Gunakan e-wallet atau m-banking", fill=(220, 220, 220), font=f_kecil)
        nominal = f"Rp {d['harga']:,}"
        bb = draw.textbbox((0, 0), nominal, font=f_total)
        draw.text((990 - (bb[2]-bb[0]) - 250, 990), nominal, fill=(255, 255, 255), font=f_total)
        # Kotak kuning peringatan
        draw.rectangle([740, 1080, 990, 1140], fill=(255, 200, 0))
        draw.text((750, 1090), "⚠️ WAJIB BAYAR", fill=(0, 0, 0), font=f_kecil)
        draw.text((750, 1112), "SESUAI NOMINAL", fill=(0, 0, 0), font=f_kecil)
        draw.text((15, 1095), d['nama'].upper(), fill=(0, 0, 0), font=f_med)
        draw.text((15, 1122), f"Username: {d['username']}", fill=(60, 60, 60), font=f_kecil)

        buf = BytesIO()
        canvas.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception as e:
        print("Gagal bikin banner:", e)
        return None

def menu_awal():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🟢  MENU LAYANAN", callback_data="menu_layanan"))
    m.add(InlineKeyboardButton("💎  INSTALL PANEL FREE", callback_data="install_free"))
    m.add(InlineKeyboardButton("👑  OWNER BOT", callback_data="owner"))
    m.add(InlineKeyboardButton("⭐  CHANNEL TESTI ↗️", url="https://t.me/ZuanTesti"))
    return m

def teks_welcome():
    return (
        "🌟✦ ━━━━ 『 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 』 ━━━━ ✦🌟\n\n"
        "<blockquote>┌── 「 👤 𝐏𝐑𝐎𝐅𝐈𝐋 𝐁𝐎𝐓 」 ──\n"
        "│ 👑 Owner · <b>ZUAN PANEL</b>\n"
        "│ 🤖 Name · <b>AUTO ORDER ZUAN PANEL</b>\n"
        "│ ⚡ Status · <b>BETA · VIP Only</b>\n"
        "│ 📖 Prefix · <b>/</b>\n"
        "└──────────────</blockquote>\n\n"
        "<blockquote>┌── 「 📊 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐊 」 ──\n"
        "│ 👥 Total User · <b>481</b>\n"
        "│ 💰 Pendapatan · <b>Rp 2.438.400</b>\n"
        "│ 🔥 Stok · <b>READY ALL</b>\n"
        "└──────────────</blockquote>\n\n"
        "<blockquote>👋 <b>Selamat Datang di Bot AUTO ORDER ZUAN PANEL!</b></blockquote>"
    )

def edit_pesan(c, teks, markup=None):
    try:
        if c.message.photo or c.message.caption:
            bot.edit_message_caption(caption=teks, chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=markup, parse_mode="HTML")
        else:
            bot.edit_message_text(teks, chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=markup, parse_mode="HTML")
    except:
        try:
            bot.send_message(c.message.chat.id, teks, reply_markup=markup, parse_mode="HTML")
        except:
            pass

@bot.message_handler(commands=['start'])
def start(m):
    for f in ["foto.jpg", "banner.jpg", "zuan.jpg", "photo.jpg"]:
        try:
            with open(f, "rb") as foto:
                bot.send_photo(m.chat.id, foto, caption=teks_welcome(), reply_markup=menu_awal(), parse_mode="HTML")
                return
        except:
            continue
    bot.send_message(m.chat.id, teks_welcome(), reply_markup=menu_awal(), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: True)
def semua_callback(c):
    chat_id = c.message.chat.id
    data = c.data
    bot.answer_callback_query(c.id)
    if data == "menu_layanan":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("📦  CEK STOK", callback_data="zuan_stok"))
        m.add(InlineKeyboardButton("💰  LIST HARGA", callback_data="zuan_harga"))
        m.add(InlineKeyboardButton("🛒  ORDER PANEL", callback_data="zuan_order"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="back_home"))
        edit_pesan(c, "✨ <b>MENU LAYANAN ZUAN PANEL</b> ✨\n\n<blockquote>Silahkan pilih layanan yang Anda butuhkan 👇</blockquote>", m)
    elif data == "back_home":
        try: bot.delete_message(chat_id, c.message.message_id)
        except: pass
        start(c.message)
    elif data == "install_free":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="back_home"))
        edit_pesan(c, "💎 <b>INSTALL PANEL FREE</b>\n\n<blockquote>┌── 「 📋 SYARAT 」 ──\n│ 1️⃣ Join Channel Testi\n│ 2️⃣ Screenshot Bot ini &amp; kirim ke Owner\n│ 3️⃣ Menunggu proses dari Admin\n└──────────────</blockquote>", m)
    elif data == "owner":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("📞  HUBUNGI OWNER", url="https://t.me/ZuanPanel"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="back_home"))
        edit_pesan(c, "👑 <b>OWNER BOT</b>\n\n<blockquote>┌── 「 OWNER 」 ──\n│ 👑 Owner : <b>ZUAN PANEL</b>\n│ ⚡ Respon : <b>FAST 24 JAM</b>\n│ 🛡️ Garansi : <b>15 HARI FULL</b>\n└──────────────</blockquote>", m)
    elif data == "zuan_stok":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🛒  ORDER SEKARANG", callback_data="zuan_order"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="menu_layanan"))
        edit_pesan(c, "📦 <b>STOK PANEL ZUAN</b>\n\n<blockquote>┌── 「 ✅ READY 」 ──\n│ 💚 1GB - 10GB · <b>TERSEDIA</b>\n│ 🔥 UNLI · <b>TERSEDIA</b>\n└──────────────</blockquote>", m)
    elif data == "zuan_harga":
        teks = ("💰 <b>DAFTAR HARGA ZUAN PANEL</b> 💰\n━━━━━━━━━━━━━━━━━━\n\n"
            "<blockquote>💚 <b>PAKET RAM</b>\n"
            "├ 1GB  ─ Rp <b>4.000</b>\n├ 2GB  ─ Rp <b>6.000</b>\n├ 3GB  ─ Rp <b>8.000</b>\n├ 4GB  ─ Rp <b>10.000</b>\n├ 5GB  ─ Rp <b>12.000</b>\n├ 6GB  ─ Rp <b>15.000</b>\n├ 7GB  ─ Rp <b>18.000</b>\n├ 8GB  ─ Rp <b>20.000</b>\n├ 9GB  ─ Rp <b>22.000</b>\n└ 10GB ─ Rp <b>25.000</b></blockquote>\n\n"
            "<blockquote>🔥 <b>UNLIMITED</b>\n└ UNLI ─ Rp <b>30.000</b> 👑</blockquote>\n\n"
            "💳 <b>QRIS</b> Semua Pembayaran  •  🛡️ <b>Garansi 15 Hari</b>")
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🛒  ORDER SEKARANG 🚀", callback_data="zuan_order"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="menu_layanan"))
        edit_pesan(c, teks, m)
    elif data == "zuan_order":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("💚 1GB · 4K", callback_data="buy_1gb"), InlineKeyboardButton("💚 2GB · 6K", callback_data="buy_2gb"))
        m.add(InlineKeyboardButton("💙 3GB · 8K", callback_data="buy_3gb"), InlineKeyboardButton("💙 4GB · 10K", callback_data="buy_4gb"))
        m.add(InlineKeyboardButton("💜 5GB · 12K", callback_data="buy_5gb"), InlineKeyboardButton("💜 6GB · 15K", callback_data="buy_6gb"))
        m.add(InlineKeyboardButton("🧡 7GB · 18K", callback_data="buy_7gb"), InlineKeyboardButton("🧡 8GB · 20K", callback_data="buy_8gb"))
        m.add(InlineKeyboardButton("❤️ 9GB · 22K", callback_data="buy_9gb"), InlineKeyboardButton("❤️ 10GB · 25K", callback_data="buy_10gb"))
        m.add(InlineKeyboardButton("🔥  UNLI · 30K  👑", callback_data="buy_unli"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="menu_layanan"))
        edit_pesan(c, "🛒 <b>PILIH PAKET ANDA</b>\n\n<blockquote>💎 Kualitas Premium\n⚡ Aktivasi Cepat\n🛡️ Garansi 15 Hari</blockquote>", m)
    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = HARGA[key]
        orders[chat_id] = {"paket": key, "nama": item['nama'], "harga": item['harga']}
        bot.send_message(chat_id, f"✨ <b>PEMESANAN {item['nama'].upper()}</b>\n━━━━━━━━━━━━━━━━━━\n\n<blockquote>📦 Paket : <b>{item['nama']}</b>\n💰 Harga : <b>Rp {item['harga']:,}</b>\n⚡ Status : <b>Tersedia</b></blockquote>\n\n<b>LANGKAH 1/2</b> ─ Silahkan kirim <b>Username Panel</b> Anda:\n<i>Contoh: <code>zuan123</code></i>", parse_mode="HTML")
        bot.register_next_step_handler(c.message, proses_username)
    elif data == "buat_qris":
        buat_qris(c)
    elif data == "cek_bayar":
        cek_bayar(c)
    elif data == "batalkan":
        orders.pop(chat_id, None)
        bot.send_message(chat_id, "❌ <b>Pesanan Dibatalkan.</b>\n\n<blockquote>Pesanan Anda telah dibatalkan. Silahkan order kembali kapan saja.</blockquote>", parse_mode="HTML")

def proses_username(m):
    chat_id = m.chat.id
    username = m.text.strip().lower().replace(" ", "")
    if len(username) < 4:
        bot.send_message(chat_id, "❌ <b>Username tidak valid.</b>\nMohon gunakan minimal 4 karakter.", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_username)
        return
    orders[chat_id]["username"] = username
    bot.send_message(chat_id, f"✅ <b>Username Berhasil Disimpan</b>\n\n<blockquote>👤 Username : <code>{username}</code></blockquote>\n\n<b>LANGKAH 2/2</b> ─ Silahkan kirim <b>Email</b> Anda:\n<i>Contoh: <code>zuan@gmail.com</code></i>", parse_mode="HTML")
    bot.register_next_step_handler(m, proses_email)

def proses_email(m):
    chat_id = m.chat.id
    email = m.text.strip()
    if "@" not in email:
        bot.send_message(chat_id, "❌ <b>Email tidak valid.</b>", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_email)
        return
    orders[chat_id]["email"] = email
    d = orders[chat_id]
    teks = ("📋 <b>KONFIRMASI PESANAN</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        "<blockquote>"
        f"📦 Paket : <b>{d['nama']}</b>\n"
        f"👤 Username : <code>{d['username']}</code>\n"
        f"📧 Email : <code>{d['email']}</code>\n"
        f"💰 Total : <b>Rp {d['harga']:,}</b>\n"
        f"💳 Metode : <b>QRIS RESMI</b>\n"
        "</blockquote>\n\nApakah data sudah benar?")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅  LANJUTKAN PEMBAYARAN 💳", callback_data="buat_qris"))
    bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)

def buat_qris(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    bot.send_message(chat_id, f"⏳ <b>Mohon Tunggu...</b>\n<i>Sedang menyiapkan kode pembayaran resmi sebesar Rp {d['harga']:,} untuk Anda.</i>", parse_mode="HTML")
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        ext_id = f"ZUAN-{chat_id}-{int(time.time())}"
        payload = {"amount": d['harga'], "description": f"ZUAN PANEL - {d['nama']} - {d['username']}", "external_id": ext_id, "payment_methods": ["qris"], "expires_in_minutes": 60}
        headers["Idempotency-Key"] = ext_id
        r = requests.post(f"{KASERA_BASE}/transactions", json=payload, headers=headers, timeout=20)
        res = r.json()
        if r.status_code not in [200, 201]:
            raise Exception(f"Kasera {r.status_code}: {res}")
        data = res.get("data") or res
        tx_id = data.get("id") or data.get("transaction_id") or ext_id
        payment = data.get("payment") or {}
        qr_string = payment.get("qr_string") or payment.get("qr_code") or data.get("qr_string")
        if not qr_string:
            raise Exception(f"Kasera tidak kirim QR: {res}")
        d["tx_id"] = tx_id
        d["external_id"] = ext_id
        d["qr_string"] = qr_string
    except Exception as e:
        print("Kasera Error:", e)
        bot.send_message(chat_id, "❌ <b>Maaf, Gagal Membuat Pembayaran.</b>\n\n<blockquote>Sistem pembayaran sedang mengalami kendala. Mohon coba beberapa saat lagi.</blockquote>", parse_mode="HTML")
        return

    gambar_qris = bikin_gambar_qris(d["qr_string"], d) if d.get("qr_string") else None

    # Kata-kata bawahnya BIARIN persis kayak contoh TOKOSHOPP!
    teks = (
        "📋 <b>PEMBAYARAN ANDA!</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "<blockquote>"
        f"Item: <b>{d['nama']} (x1)</b> - {d['username']}\n"
        f"Total Bayar: <b>Rp {d['harga']:,}</b>\n"
        f"Order ID: <code>INV-QRIS-{d.get('external_id')}</code>\n"
        "</blockquote>\n\n"
        "⚠️ <i>Bayar pas sesuai nominal!</i>\n"
        "⏰ <i>Expired: 60 Menit</i>\n\n"
        "Setelah membayar tekan tombol ✅ <b>Cek Status Pembayaran</b>."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅  Cek Status Pembayaran", callback_data="cek_bayar"))
    markup.add(InlineKeyboardButton("❌  Batalkan", callback_data="batalkan"))
    try:
        if gambar_qris:
            bot.send_photo(chat_id, gambar_qris, caption=teks, parse_mode="HTML", reply_markup=markup)
        else:
            qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=600x600&data={urllib.parse.quote(d['qr_string'])}"
            bot.send_photo(chat_id, qr_img_url, caption=teks, parse_mode="HTML", reply_markup=markup)
    except:
        bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)
    try:
        bot.send_message(ADMIN_ID, f"🔔 PESANAN BARU\nUser: @{c.from_user.username}\nPaket: {d['nama']}\nUsername: `{d['username']}`\nEmail: `{d['email']}`\nTotal: Rp {d['harga']:,}\nStatus: Menunggu Pembayaran")
    except:
        pass

def cek_bayar(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    bot.answer_callback_query(c.id, "Memeriksa pembayaran...")
    lunas = False
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}"}
        tx_id = d.get("tx_id") or d.get("external_id")
        r = requests.get(f"{KASERA_BASE}/transactions/{tx_id}", headers=headers, timeout=15)
        j = r.json()
        data = j.get("data") or j
        if str(data.get("status", "")).lower() == "succeeded":
            lunas = True
    except Exception as e:
        print("Cek Error:", e)
    if not lunas:
        bot.send_message(chat_id, "❌ <b>Pembayaran Belum Diterima.</b>\n\n<blockquote>Mohon selesaikan pembayaran terlebih dahulu, tunggu 1 menit, lalu tekan tombol <b>Cek Status Pembayaran</b> kembali.</blockquote>", parse_mode="HTML")
        return
    bot.send_message(chat_id, "✅ <b>PEMBAYARAN BERHASIL!</b> 🎉\n\n<blockquote>Terima kasih atas kepercayaan Anda.\nPesanan Anda sedang kami siapkan oleh Admin.</blockquote>\n\n<i>— ZUAN PANEL —</i>", parse_mode="HTML")
    try:
        bot.send_message(ADMIN_ID, f"💰 *PESANAN LUNAS - MOHON DIPROSES*\n\nUser: @{c.from_user.username} (ID: {chat_id})\nPaket: {d['nama']}\nUsername: `{d['username']}`\nEmail: `{d['email']}`\nTotal: Rp {d['harga']:,}")
    except:
        pass

print("Bot jalan! ZUAN PANEL - BANNER TOKOSHOPP STYLE READY!")
bot.infinity_polling()
