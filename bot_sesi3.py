import os
import requests
import time
import telebot
import urllib.parse
import json
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

def load_saldo():
    try:
        with open("saldo.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_saldo():
    try:
        with open("saldo.json", "w") as f:
            json.dump(saldo_db, f)
    except:
        pass

saldo_db = load_saldo()

def get_saldo(uid):
    return int(saldo_db.get(str(uid), 0))

def tambah_saldo(uid, nominal):
    saldo_db[str(uid)] = get_saldo(uid) + int(nominal)
    save_saldo()

def kurang_saldo(uid, nominal):
    saldo_db[str(uid)] = get_saldo(uid) - int(nominal)
    save_saldo()

topup_orders = {}
# ================= BANNER TOKOSHOPP =================
def bikin_gambar_qris(qr_string, d, judul_total="TOTAL PEMBAYARAN"):
    try:
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&margin=5&data={urllib.parse.quote(qr_string)}"
        r = requests.get(qr_url, timeout=15)
        qr_img = Image.open(BytesIO(r.content)).convert("RGB")
        kanan_img = None
        for f in ["foto.jpg", "banner.jpg", "zuan.jpg"]:
            try:
                kanan_img = Image.open(f).convert("RGB")
                break
            except:
                continue
        if kanan_img is None:
            kanan_img = Image.new("RGB", (500, 500), (10, 25, 60))
        W, H = 1000, 1150
        canvas = Image.new("RGB", (W, H), (255, 248, 230))
        draw = ImageDraw.Draw(canvas)
        try:
            f_judul = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
            f_total = ImageFont.truetype("DejaVuSans-Bold.ttf", 68)
            f_logo = ImageFont.truetype("DejaVuSans-Bold.ttf", 66)
            f_kecil = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
            f_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        except:
            f_judul = f_total = f_logo = f_kecil = f_med = ImageFont.load_default()
        def center_x(x0, x1, y, teks, font, warna):
            bb = draw.textbbox((0, 0), teks, font=font)
            w = bb[2]-bb[0]
            draw.text((x0 + (x1-x0-w)//2, y), teks, fill=warna, font=font)
        def center(y, teks, font, warna):
            bb = draw.textbbox((0, 0), teks, font=font)
            draw.text(((W - (bb[2]-bb[0]))//2, y), teks, fill=warna, font=font)
        draw.rectangle([0, 0, W-1, H-1], outline=(0, 0, 0), width=10)
        draw.rectangle([10, 10, 500, 820], fill=(255, 248, 230), outline=(0, 0, 0), width=5)
        center_x(10, 500, 20, "QRIS HANYA", f_judul, (220, 0, 0))
        center_x(10, 500, 70, "BERLAKU 1 JAM", f_judul, (220, 0, 0))
        qr_img = qr_img.resize((420, 420))
        canvas.paste(qr_img, (45, 150))
        center_x(10, 500, 590, "BAYAR DILUAR WAKTU", f_med, (220, 0, 0))
        center_x(10, 500, 625, "EXPIRED? SALDO HANGUS", f_med, (220, 0, 0))
        kanan_crop = kanan_img.resize((490, 810))
        canvas.paste(kanan_crop, (500, 10))
        draw.rectangle([500, 10, 990, 820], outline=(0, 0, 0), width=5)
        center(835, "ZUANPANEL.WEB.ID", f_logo, (20, 80, 200))
        center(910, "PAYMENT EDITION", f_med, (0, 0, 0))
        draw.rectangle([10, 970, 990, 1080], fill=(20, 90, 180))
        draw.text((25, 990), judul_total, fill=(255, 255, 255), font=f_med)
        draw.text((25, 1025), "Gunakan e-wallet atau m-banking", fill=(220, 220, 220), font=f_kecil)
        nominal = f"Rp {d['harga']:,}"
        bb = draw.textbbox((0, 0), nominal, font=f_total)
        draw.text((990 - (bb[2]-bb[0]) - 250, 990), nominal, fill=(255, 255, 255), font=f_total)
        draw.rectangle([740, 1080, 990, 1140], fill=(255, 200, 0))
        draw.text((750, 1090), "WAJIB BAYAR", fill=(0, 0, 0), font=f_kecil)
        draw.text((750, 1112), "SESUAI NOMINAL", fill=(0, 0, 0), font=f_kecil)
        draw.text((15, 1095), d['nama'].upper(), fill=(0, 0, 0), font=f_med)
        draw.text((15, 1122), f"Username: {d.get('username','-')}", fill=(60, 60, 60), font=f_kecil)
        buf = BytesIO()
        canvas.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception as e:
        print("Gagal bikin banner:", e)
        return None

def menu_awal(uid=None):
    saldo = get_saldo(uid) if uid else 0
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton(f"👛  SALDO SAYA : Rp {saldo:,}", callback_data="cek_saldo"))
    m.add(InlineKeyboardButton("💰  ISI SALDO", callback_data="isi_saldo"))
    m.add(InlineKeyboardButton("🟢  MENU LAYANAN", callback_data="menu_layanan"))
    m.add(InlineKeyboardButton("💎  INSTALL PANEL FREE", callback_data="install_free"))
    m.add(InlineKeyboardButton("👑  OWNER BOT", callback_data="owner"))
    m.add(InlineKeyboardButton("⭐  CHANNEL TESTI ↗️", url="https://t.me/ZuanTesti"))
    return m

def teks_welcome(uid=None):
    saldo = get_saldo(uid) if uid else 0
    return (
        "🌟✦ ━━━━ WELCOME ━━━━ ✦🌟\n\n"
        f"👛 Saldo Anda : Rp {saldo:,}\n"
        "👑 Owner : ZUAN PANEL\n"
        "🤖 Name : AUTO ORDER ZUAN PANEL\n"
        "⚡ Status : BETA - VIP Only\n\n"
        "👋 Selamat Datang di Bot AUTO ORDER ZUAN PANEL!"
    )

def edit_pesan(c, teks, markup=None):
    chat_id = c.message.chat.id
    try:
        bot.delete_message(chat_id, c.message.message_id)
    except:
        pass
    try:
        bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print("Edit Pesan Error:", e)

@bot.message_handler(commands=['start'])
def start(m):
    for f in ["foto.jpg", "banner.jpg", "zuan.jpg", "photo.jpg"]:
        try:
            with open(f, "rb") as foto:
                bot.send_photo(m.chat.id, foto, caption=teks_welcome(m.chat.id), reply_markup=menu_awal(m.chat.id), parse_mode="HTML")
                return
        except:
            continue
    bot.send_message(m.chat.id, teks_welcome(m.chat.id), reply_markup=menu_awal(m.chat.id), parse_mode="HTML")
    
def proses_topup_custom(m):
    chat_id = m.chat.id
    try:
        nominal = int(m.text.strip().replace(".", "").replace(",", "").replace("Rp", "").replace(" ", ""))
    except:
        bot.send_message(chat_id, "❌ <b>Nominal tidak valid.</b>\nKirim angka aja, contoh: <code>25000</code>", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_topup_custom)
        return
    if nominal < 5000 or nominal > 1000000:
        bot.send_message(chat_id, "❌ <b>Minimal Rp 5.000, Maksimal Rp 1.000.000</b>", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_topup_custom)
        return
    topup_orders[chat_id] = {"nama": f"Top Up Saldo Rp {nominal:,}", "harga": nominal, "username": m.from_user.username or "user", "tipe": "topup"}
    class FakeMsg:
        pass
    fake_c = FakeMsg()
    fake_c.message = m
    fake_c.from_user = m.from_user
    buat_qris_topup(fake_c, nominal)

def proses_username(m):
    chat_id = m.chat.id
    username = m.text.strip().lower().replace(" ", "")
    if len(username) < 4:
        bot.send_message(chat_id, "❌ <b>Username tidak valid.</b>\nMinimal 4 karakter.", parse_mode="HTML")
        bot.register_next_step_handler(m, proses_username)
        return
    orders[chat_id]["username"] = username
    bot.send_message(chat_id, f"✅ <b>Username Disimpan</b>\n\nUsername : <code>{username}</code>\n\n<b>LANGKAH 2/2</b> - Kirim <b>Email</b>:\nContoh: <code>zuan@gmail.com</code>", parse_mode="HTML")
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
    saldo = get_saldo(chat_id)
    teks = ("📋 <b>KONFIRMASI PESANAN</b>\n\n"
        f"📦 Paket : <b>{d['nama']}</b>\n"
        f"👤 Username : <code>{d['username']}</code>\n"
        f"📧 Email : <code>{d['email']}</code>\n"
        f"💰 Total : <b>Rp {d['harga']:,}</b>\n"
        f"👛 Saldo Anda : <b>Rp {saldo:,}</b>\n\nPilih metode pembayaran 👇")
    markup = InlineKeyboardMarkup()
    if saldo >= d['harga']:
        markup.add(InlineKeyboardButton(f"👛  BAYAR PAKAI SALDO (Rp {saldo:,})", callback_data="bayar_pake_saldo"))
    else:
        markup.add(InlineKeyboardButton(f"👛  SALDO KURANG (Rp {saldo:,}) - ISI SALDO", callback_data="isi_saldo"))
    markup.add(InlineKeyboardButton("💳  BAYAR PAKAI QRIS", callback_data="buat_qris"))
    bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)

def bayar_pake_saldo(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    saldo = get_saldo(chat_id)
    if saldo < d['harga']:
        bot.send_message(chat_id, f"❌ <b>Saldo Tidak Cukup!</b>\n\nSaldo : <b>Rp {saldo:,}</b>\nHarga : <b>Rp {d['harga']:,}</b>", parse_mode="HTML")
        return
    kurang_saldo(chat_id, d['harga'])
    sisa = get_saldo(chat_id)
    bot.send_message(chat_id, f"✅ <b>PEMBAYARAN BERHASIL PAKAI SALDO!</b>\n\nPaket : <b>{d['nama']}</b>\nUsername : <code>{d['username']}</code>\nDibayar : <b>Rp {d['harga']:,}</b>\nSisa Saldo : <b>Rp {sisa:,}</b>\n\nPesanan sedang disiapkan Admin.", parse_mode="HTML")
    try:
        bot.send_message(ADMIN_ID, f"💰 PESANAN LUNAS VIA SALDO\nUser: @{c.from_user.username} (ID: {chat_id})\nPaket: {d['nama']}\nUsername: {d['username']}\nEmail: {d['email']}\nTotal: Rp {d['harga']:,}\nSisa Saldo: Rp {sisa:,}")
    except:
        pass
        # ================= TOP UP QRIS =================
def buat_qris_topup(c, nominal):
    chat_id = c.message.chat.id
    d = topup_orders.get(chat_id)
    if not d:
        return
    bot.send_message(chat_id, f"⏳ <b>Mohon Tunggu...</b>\nMenyiapkan top up Rp {nominal:,}", parse_mode="HTML")
    try:
        headers = {"Authorization": f"Bearer {KASERA_API_KEY}", "Content-Type": "application/json"}
        ext_id = f"TOPUP-{chat_id}-{int(time.time())}"
        payload = {"amount": nominal, "description": f"TOPUP SALDO ZUAN - {nominal} - {d.get('username')}", "external_id": ext_id, "payment_methods": ["qris"], "expires_in_minutes": 60}
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
            raise Exception("Kasera tidak kirim QR")
        d["tx_id"] = tx_id
        d["external_id"] = ext_id
        d["qr_string"] = qr_string
    except Exception as e:
        print("Kasera Topup Error:", e)
        bot.send_message(chat_id, "❌ <b>Gagal Membuat Top Up.</b>\nCoba lagi nanti.", parse_mode="HTML")
        return
    gambar = bikin_gambar_qris(d["qr_string"], d, judul_total="TOP UP SALDO")
    teks = (f"💰 <b>ISI SALDO ZUAN PANEL</b>\n\nTop Up : <b>Rp {d['harga']:,}</b>\nUser : <code>{d.get('username')}</code>\nInvoice : <code>{d.get('external_id')}</code>\n\nScan QR di atas pake DANA / OVO / GoPay / M-Banking\nPastikan nama MUHAMAD IKHSANDI AKBAR\n\nQR berlaku 60 menit.")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍  SAYA SUDAH BAYAR ✅", callback_data="cek_bayar_topup"))
    try:
        if gambar:
            bot.send_photo(chat_id, gambar, caption=teks, parse_mode="HTML", reply_markup=markup)
        else:
            qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=600x600&data={urllib.parse.quote(d['qr_string'])}"
            bot.send_photo(chat_id, qr_img_url, caption=teks, parse_mode="HTML", reply_markup=markup)
    except:
        bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)

def cek_bayar_topup(c):
    chat_id = c.message.chat.id
    d = topup_orders.get(chat_id)
    if not d:
        return
    try:
        bot.answer_callback_query(c.id, "Memeriksa pembayaran...")
    except:
        pass
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
        print("Cek Topup Error:", e)
    if not lunas:
        bot.send_message(chat_id, "❌ <b>Pembayaran Belum Diterima.</b>\nSelesaikan bayar dulu, tunggu 1 menit, lalu pencet lagi.", parse_mode="HTML")
        return
    tambah_saldo(chat_id, d['harga'])
    saldo_baru = get_saldo(chat_id)
    bot.send_message(chat_id, f"✅ <b>ISI SALDO BERHASIL!</b>\n\nTop Up : <b>Rp {d['harga']:,}</b>\nSaldo Sekarang : <b>Rp {saldo_baru:,}</b>", parse_mode="HTML")
    try:
        bot.send_message(ADMIN_ID, f"💰 TOP UP LUNAS\nUser: @{c.from_user.username} (ID: {chat_id})\nNominal: Rp {d['harga']:,}\nSaldo Baru: Rp {saldo_baru:,}")
    except:
        pass

# ================= QRIS ORDER PANEL =================
def buat_qris(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    bot.send_message(chat_id, f"⏳ <b>Mohon Tunggu...</b>\nMenyiapkan pembayaran Rp {d['harga']:,}", parse_mode="HTML")
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
        bot.send_message(chat_id, "❌ <b>Gagal Membuat Pembayaran.</b>\nCoba lagi nanti.", parse_mode="HTML")
        return
    gambar_qris = bikin_gambar_qris(d["qr_string"], d) if d.get("qr_string") else None
    teks = (f"💎 <b>ZUAN PANEL - PEMBAYARAN</b>\n\nPaket : <b>{d['nama']}</b>\nUsername : <code>{d['username']}</code>\nTotal : <b>Rp {d['harga']:,}</b>\nInvoice : <code>{d.get('external_id')}</code>\n\nScan QR di atas pake DANA / OVO / GoPay / M-Banking\nPastikan nama MUHAMAD IKHSANDI AKBAR\n\nQR berlaku 60 menit.")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍  SAYA SUDAH BAYAR ✅", callback_data="cek_bayar"))
    try:
        if gambar_qris:
            bot.send_photo(chat_id, gambar_qris, caption=teks, parse_mode="HTML", reply_markup=markup)
        else:
            qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=600x600&data={urllib.parse.quote(d['qr_string'])}"
            bot.send_photo(chat_id, qr_img_url, caption=teks, parse_mode="HTML", reply_markup=markup)
    except:
        bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)
    try:
        bot.send_message(ADMIN_ID, f"🔔 PESANAN BARU\nUser: @{c.from_user.username}\nPaket: {d['nama']}\nUsername: {d['username']}\nEmail: {d['email']}\nTotal: Rp {d['harga']:,}\nStatus: Menunggu Pembayaran")
    except:
        pass

def cek_bayar(c):
    chat_id = c.message.chat.id
    d = orders.get(chat_id)
    if not d:
        return
    try:
        bot.answer_callback_query(c.id, "Memeriksa pembayaran...")
    except:
        pass
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
        bot.send_message(chat_id, "❌ <b>Pembayaran Belum Diterima.</b>\nSelesaikan bayar dulu, tunggu 1 menit, lalu pencet lagi.", parse_mode="HTML")
        return
    bot.send_message(chat_id, "✅ <b>PEMBAYARAN BERHASIL!</b>\n\nPesanan sedang disiapkan Admin.\nDetail login akan dikirim sesaat lagi.", parse_mode="HTML")
    try:
        bot.send_message(ADMIN_ID, f"💰 PESANAN LUNAS - MOHON DIPROSES\nUser: @{c.from_user.username} (ID: {chat_id})\nPaket: {d['nama']}\nUsername: {d['username']}\nEmail: {d['email']}\nTotal: Rp {d['harga']:,}")
    except:
        pass

print("Bot jalan! ZUAN PANEL - ISI SALDO + QRIS + BANNER READY!")
bot.infinity_polling()
