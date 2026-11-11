import os
import requests
import time
import telebot
import urllib.parse
import io
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonDefault

# PIL buat bikin banner QRIS
try:
    from PIL import Image, ImageDraw, ImageFont
    ADA_PIL = True
except:
    ADA_PIL = False

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "849370608"))
KASERA_API_KEY = os.getenv("KASERA_API_KEY")
KASERA_BASE = "https://pay.kasera.id/v1"

bot = telebot.TeleBot(TOKEN)

# ===== HAPUS MENU BAWAH LAMA =====
try:
    bot.delete_my_commands()
    bot.set_my_commands([])
    bot.set_chat_menu_button(menu_button=MenuButtonDefault())
except Exception as e:
    print("Gagal hapus menu:", e)

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

# ================= BIKIN GAMBAR QRIS + BANNER =================
def bikin_gambar_qris(qr_string, d):
    """
    QR polosan dari Kasera -> dibikin jadi gambar banner keren!
    Atas: ZUAN PANEL - PEMBAYARAN RESMI
    Tengah: QR ASLI
    Bawah: QRIS RESMI + Nama Merchant + Nominal
    """
    try:
        # 1. Download QR asli dari Kasera (via qrserver render)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=600x600&margin=10&data={urllib.parse.quote(qr_string)}"
        r = requests.get(qr_url, timeout=15)
        qr_img = Image.open(BytesIO(r.content)).convert("RGB")
        qr_img = qr_img.resize((640, 640))

        # 2. Bikin kanvas baru: 800 x 1180
        W, H = 800, 1180
        canvas = Image.new("RGB", (W, H), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Coba load font tebal, kalo gagal pake default
        try:
            font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
            font_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
            font_small = ImageFont.truetype("DejaVuSans.ttf", 24)
            font_mini = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        except:
            font_big = ImageFont.load_default()
            font_med = font_big
            font_small = font_big
            font_mini = font_big

        def teks_tengah(y, teks, font, warna):
            bbox = draw.textbbox((0, 0), teks, font=font)
            w = bbox[2] - bbox[0]
            draw.text(((W - w) // 2, y), teks, fill=warna, font=font)

        # ===== BANNER ATAS - BIRU GELAP =====
        draw.rectangle([0, 0, W, 160], fill=(10, 25, 60))
        draw.rectangle([0, 160, W, 168], fill=(0, 212, 255))
        teks_tengah(18, "💎  ZUAN PANEL  💎", font_big, (255, 255, 255))
        teks_tengah(72, "PEMBAYARAN RESMI - QRIS", font_med, (0, 212, 255))
        teks_tengah(110, "AUTO ORDER • AMAN • TERPERCAYA", font_mini, (180, 180, 180))

        # ===== INFO PAKET =====
        teks_tengah(190, d['nama'].upper(), font_big, (10, 25, 60))
        teks_tengah(240, f"Rp {d['harga']:,}", font_big, (0, 160, 0))
        teks_tengah(292, f"Username : {d['username']}", font_small, (80, 80, 80))

        # ===== QR DI TENGAH =====
        canvas.paste(qr_img, ((W - 640) // 2, 330))

        # ===== BANNER BAWAH - BUKTI ASLI =====
        y0 = 990
        draw.rectangle([0, y0, W, H], fill=(10, 25, 60))
        draw.rectangle([0, y0, W, y0+8], fill=(0, 212, 255))
        teks_tengah(y0+18, "✅  QRIS RESMI  ✅", font_med, (0, 255, 130))
        teks_tengah(y0+58, "Terverifikasi Bank Indonesia", font_small, (255, 255, 255))
        teks_tengah(y0+92, "Merchant : MUHAMAD IKHSANDI AKBAR", font_mini, (200, 200, 200))
        teks_tengah(y0+122, "100% AMAN • Pembayaran Terverifikasi Otomatis", font_mini, (0, 212, 255))

        # Simpen ke memory
        buf = BytesIO()
        canvas.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception as e:
        print("Gagal bikin banner QRIS:", e)
        return None

# ================= MENU =================
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

# ================= START =================
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

# ================= CALLBACK =================
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
        try:
            bot.delete_message(chat_id, c.message.message_id)
        except:
            pass
        start(c.message)

    elif data == "install_free":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="back_home"))
        edit_pesan(c, "💎 <b>INSTALL PANEL FREE</b>\n\n<blockquote>┌── 「 📋 SYARAT 」 ──\n│ 1️⃣ Join Channel Testi\n│ 2️⃣ Screenshot Bot ini &amp; kirim ke Owner\n│ 3️⃣ Menunggu proses dari Admin\n└──────────────</blockquote>\n\n<i>Slot terbatas setiap hari!</i>", m)

    elif data == "owner":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("📞  HUBUNGI OWNER", url="https://t.me/ZuanPanel"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="back_home"))
        edit_pesan(c, "👑 <b>OWNER BOT</b>\n\n<blockquote>┌── 「 OWNER 」 ──\n│ 👑 Owner : <b>ZUAN PANEL</b>\n│ ⚡ Respon : <b>FAST 24 JAM</b>\n│ 🛡️ Garansi : <b>15 HARI FULL</b>\n└──────────────</blockquote>", m)

    elif data == "zuan_stok":
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🛒  ORDER SEKARANG", callback_data="zuan_order"))
        m.add(InlineKeyboardButton("🔙  KEMBALI", callback_data="menu_layanan"))
        edit_pesan(c, "📦 <b>STOK PANEL ZUAN</b>\n\n<blockquote>┌── 「 ✅ READY 」 ──\n│ 💚 1GB - 10GB · <b>TERSEDIA</b>\n│ 🔥 UNLI · <b>TERSEDIA</b>\n│ ⚡ Stok Update Setiap Hari\n└──────────────</blockquote>", m)

    elif data == "zuan_harga":
        teks = (
            "💰 <b>DAFTAR HARGA ZUAN PANEL</b> 💰\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<blockquote>💚 <b>PAKET RAM</b>\n"
            "├ 1GB  ─ Rp <b>4.000</b>\n"
            "├ 2GB  ─ Rp <b>6.000</b>\n"
            "├ 3GB  ─ Rp <b>8.000</b>\n"
            "├ 4GB  ─ Rp <b>10.000</b>\n"
            "├ 5GB  ─ Rp <b>12.000</b>\n"
            "├ 6GB  ─ Rp <b>15.000</b>\n"
            "├ 7GB  ─ Rp <b>18.000</b>\n"
            "├ 8GB  ─ Rp <b>20.000</b>\n"
            "├ 9GB  ─ Rp <b>22.000</b>\n"
            "└ 10GB ─ Rp <b>25.000</b></blockquote>\n\n"
            "<blockquote>🔥 <b>UNLIMITED</b>\n"
            "└ UNLI ─ Rp <b>30.000</b> 👑</blockquote>\n\n"
            "💳 <b>QRIS</b> Semua Pembayaran  •  🛡️ <b>Garansi 15 Hari</b>  •  ⚡ <b>Aktif 24 Jam</b>"
        )
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
        edit_pesan(c, "🛒 <b>PILIH PAKET ANDA</b>\n\n<blockquote>💎 Kualitas Premium\n⚡ Aktivasi Cepat\n🛡️ Garansi 15 Hari</blockquote>\n<i>Silahkan pilih paket yang Anda inginkan 👇</i>", m)

    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = HARGA[key]
        orders[chat_id] = {"paket": key, "nama": item['nama'], "harga": item['harga']}
        bot.send_message(chat_id, f"✨ <b>PEMESANAN {item['nama'].upper()}</b>\n━━━━━━━━━━━━━━━━━━\n\n<blockquote>📦 Paket : <b>{item['nama']}</b>\n💰 Harga : <b>Rp {item['harga']:,}</b>\n⚡ Status : <b>Tersedia</b></blockquote>\n\n<b>LANGKAH 1/2</b> ─ Silahkan kirim <b>Username Panel</b> Anda:\n<i>Contoh: <code>zuan123</code></i>\n\n<i>Minimal 4 karakter, tanpa spasi.</i>", parse_mode="HTML")
        bot.register_next_step_handler(c.message, proses_username)

    elif data == "buat_qris":
        buat_qris(c)
    elif data == "cek_bayar":
        cek_bayar(c)

# ================= ORDER STEP =================
def proses_username(m):
    chat_id = m.chat.id
    username = m.text.strip().lower().replace(" ", "")
    if len(username) < 4:
        bot.send_message(chat_id, "❌ <b>Username tidak valid.</b>\nMohon gunakan minimal 4 karakter.", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_username)
        return
    orders[chat_id]["username"] = username
    bot.send_message(chat_id, f"✅ <b>Username Berhasil Disimpan</b>\n\n<blockquote>👤 Username : <code>{username}</code></blockquote>\n\n<b>LANGKAH 2/2</b> ─ Silahkan kirim <b>Email</b> Anda untuk login panel:\n<i>Contoh: <code>zuan@gmail.com</code></i>", parse_mode="HTML")
    bot.register_next_step_handler(m, proses_email)

def proses_email(m):
    chat_id = m.chat.id
    email = m.text.strip()
    if "@" not in email:
        bot.send_message(chat_id, "❌ <b>Email tidak valid.</b>\nMohon kirim alamat email yang benar.", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_email)
        return
    orders[chat_id]["email"] = email
    d = orders[chat_id]
    teks = (
        "📋 <b>KONFIRMASI PESANAN</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "<blockquote>"
        f"📦 Paket : <b>{d['nama']}</b>\n"
        f"👤 Username : <code>{d['username']}</code>\n"
        f"📧 Email : <code>{d['email']}</code>\n"
        f"💰 Total Pembayaran : <b>Rp {d['harga']:,}</b>\n"
        f"💳 Metode : <b>QRIS RESMI</b>\n"
        "</blockquote>\n\n"
        "Apakah data di atas sudah benar? Silahkan lanjutkan untuk membuat kode pembayaran."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅  LANJUTKAN PEMBAYARAN 💳", callback_data="buat_qris"))
    bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)

# ================= QRIS ASLI + BANNER =================
def buat_qris(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    bot.send_message(chat_id, f"⏳ <b>Mohon Tunggu...</b>\n<i>Sedang menyiapkan kode pembayaran resmi sebesar Rp {d['harga']:,} untuk Anda.</i>", parse_mode="HTML")
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        ext_id = f"ZUAN-{chat_id}-{int(time.time())}"
        payload = {
            "amount": d['harga'],
            "description": f"ZUAN PANEL - {d['nama']} - {d['username']}",
            "external_id": ext_id,
            "payment_methods": ["qris"],
            "expires_in_minutes": 60
        }
        headers["Idempotency-Key"] = ext_id
        r = requests.post(f"{KASERA_BASE}/transactions", json=payload, headers=headers, timeout=20)
        print("KASERA STATUS:", r.status_code, r.text[:500])
        res = r.json()
        if r.status_code not in [200, 201]:
            raise Exception(f"Kasera {r.status_code}: {res}")
        data = res.get("data") or res
        tx_id = data.get("id") or data.get("transaction_id") or ext_id
        payment = data.get("payment") or {}
        qr_string = payment.get("qr_string") or payment.get("qr_code") or data.get("qr_string")
        checkout_url = data.get("checkout_url") or data.get("payment_url")
        if not qr_string and not checkout_url:
            raise Exception(f"Kasera tidak kirim QR: {res}")
        d["tx_id"] = tx_id
        d["external_id"] = ext_id
        d["checkout_url"] = checkout_url
        d["qr_string"] = qr_string
    except Exception as e:
        print("Kasera Error:", e)
        bot.send_message(chat_id, "❌ <b>Maaf, Gagal Membuat Pembayaran.</b>\n\n<blockquote>Sistem pembayaran sedang mengalami kendala. Mohon coba beberapa saat lagi atau hubungi Admin.</blockquote>", parse_mode="HTML")
        try:
            bot.send_message(ADMIN_ID, f"⚠️ KASERA ERROR!\nUser: @{c.from_user.username}\nError: {e}")
        except:
            pass
        return

    # ===== BIKIN GAMBAR QR + BANNER! =====
    gambar_qris = None
    if d.get("qr_string"):
        gambar_qris = bikin_gambar_qris(d["qr_string"], d)

    teks = (
        "💎 <b>ZUAN PANEL — PEMBAYARAN RESMI</b> 💎\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "<blockquote>"
        f"📦 Paket : <b>{d['nama']}</b>\n"
        f"👤 Username : <code>{d['username']}</code>\n"
        f"💰 Total : <b>Rp {d['harga']:,}</b>\n"
        f"🧾 Invoice : <code>{d.get('external_id')}</code>\n"
        "</blockquote>\n\n"
        "✅ <b>INI QRIS ASLI &amp; RESMI!</b>\n"
        "<blockquote>QR ini diterbitkan langsung oleh <b>Kasera Pay</b> &amp; terverifikasi <b>Bank Indonesia</b>. Bukan gambar editan! Silahkan scan, pastikan nama merchant &amp; nominal muncul sesuai di aplikasi Anda.</blockquote>\n\n"
        "📱 <b>Cara Bayar:</b>\n"
        "1️⃣ Buka DANA / OVO / GoPay / M-Banking\n"
        "2️⃣ Scan QRIS di atas &amp; pastikan nama <b>MUHAMAD IKHSANDI AKBAR</b>\n"
        "3️⃣ Pastikan nominal <b>sesuai</b>, lalu konfirmasi\n\n"
        "⏰ <i>QR ini berlaku 60 menit.</i>\n"
        "🛡️ <i>100% Aman • Terverifikasi Otomatis • Garansi Uang Kembali Jika Tidak Masuk</i>"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍  SAYA SUDAH BAYAR ✅", callback_data="cek_bayar"))
    try:
        if gambar_qris:
            bot.send_photo(chat_id, gambar_qris, caption=teks, parse_mode="HTML", reply_markup=markup)
        else:
            # Fallback kalo PIL gagal: QR polosan tapi tetep asli
            qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=600x600&data={urllib.parse.quote(d['qr_string'])}"
            bot.send_photo(chat_id, qr_img_url, caption=teks, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print("Kirim QR Error:", e)
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
        print("CEK STATUS:", r.status_code, r.text[:500])
        j = r.json()
        data = j.get("data") or j
        status = str(data.get("status", "")).lower()
        if status == "succeeded":
            lunas = True
    except Exception as e:
        print("Cek Error:", e)
    if not lunas:
        bot.send_message(chat_id, "❌ <b>Pembayaran Belum Diterima.</b>\n\n<blockquote>Mohon selesaikan pembayaran terlebih dahulu, tunggu 1 menit, lalu tekan tombol <b>Saya Sudah Bayar</b> kembali.</blockquote>", parse_mode="HTML")
        return
    bot.send_message(chat_id, "✅ <b>PEMBAYARAN BERHASIL!</b> 🎉\n\n<blockquote>Terima kasih atas kepercayaan Anda.\nPesanan Anda sedang kami siapkan oleh Admin.\nDetail login akan kami kirimkan sesaat lagi.</blockquote>\n\n<i>— ZUAN PANEL —</i>", parse_mode="HTML")
    try:
        bot.send_message(ADMIN_ID, f"💰 *PESANAN LUNAS - MOHON DIPROSES*\n\nUser: @{c.from_user.username} (ID: {chat_id})\nPaket: {d['nama']}\nUsername: `{d['username']}`\nEmail: `{d['email']}`\nTotal: Rp {d['harga']:,}")
    except:
        pass

print("Bot jalan! ZUAN PANEL FINAL - QRIS + BANNER RESMI READY!")
bot.infinity_polling()
