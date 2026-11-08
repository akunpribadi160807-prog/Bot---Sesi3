import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
bot = telebot.TeleBot(TOKEN)

OWNER_USERNAME = "@ShanXPLD"
OWNER_WA = "083169944241"
CHANNEL_TESTI = "https://t.me/ZUANPANEL"
CHANNEL_INFO = "https://t.me/ZUANPANEL"

user_order = {}

PRODUK = {
    "admin": {"nama": "Admin Panel", "harga": 3000, "desc": "Akun Root Admin (Full Akses)"},
    "pterodactyl": {"nama": "Panel Pterodactyl", "harga": 2000, "desc": "Panel 1GB - 10GB"},
    "pterodactyl_legal": {"nama": "Panel Pterodactyl Legal", "harga": 5000, "desc": "Panel Legal Garansi Full"},
    "reseller": {"nama": "Reseller Panel", "harga": 10000, "desc": "Akses Reseller Panel"},
    "reseller_legal": {"nama": "Reseller Panel Legal", "harga": 13000, "desc": "Akses Reseller Panel Legal"},
    "1gb": {"nama": "Panel 1GB", "harga": 2000},
    "2gb": {"nama": "Panel 2GB", "harga": 3000},
    "3gb": {"nama": "Panel 3GB", "harga": 4000},
    "4gb": {"nama": "Panel 4GB", "harga": 5000},
    "5gb": {"nama": "Panel 5GB", "harga": 6000},
    "6gb": {"nama": "Panel 6GB", "harga": 7000},
    "7gb": {"nama": "Panel 7GB", "harga": 8000},
    "8gb": {"nama": "Panel 8GB", "harga": 9000},
    "9gb": {"nama": "Panel 9GB", "harga": 10000},
    "10gb": {"nama": "Panel 10GB", "harga": 11000},
    "unli": {"nama": "Panel UNLIMITED", "harga": 13000},
}

def format_rp(n):
    return f"Rp {n:,}".replace(",", ".")

def menu_utama():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🟢 Menu Layanan", callback_data="menu_layanan"))
    m.add(InlineKeyboardButton("🔵 Install Panel Free", callback_data="install_free"))
    m.add(InlineKeyboardButton("🔴 Owner Bot", callback_data="owner"))
    m.add(InlineKeyboardButton("🟢 Channel Testi ↗", url=CHANNEL_TESTI))
    m.add(InlineKeyboardButton("🔵 Channel Info ↗", url=CHANNEL_INFO))
    return m

def menu_layanan():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔵 Admin Panel - Rp 3.000", callback_data="beli_admin"))
    m.add(InlineKeyboardButton("🔵 Panel Pterodactyl", callback_data="beli_pterodactyl"))
    m.add(InlineKeyboardButton("🔵 Panel Pterodactyl Legal", callback_data="beli_pterodactyl_legal"))
    m.add(InlineKeyboardButton("🔵 Reseller Panel", callback_data="beli_reseller"))
    m.add(InlineKeyboardButton("🔵 Reseller Panel Legal", callback_data="beli_reseller_legal"))
    m.add(InlineKeyboardButton("🟢 Panel 1GB - 10GB / UNLI", callback_data="list_panel"))
    m.add(InlineKeyboardButton("🔴 ⬅ Kembali", callback_data="back"))
    return m

def list_panel():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔵 1GB - Rp 2.000", callback_data="beli_1gb"))
    m.add(InlineKeyboardButton("🔵 2GB - Rp 3.000", callback_data="beli_2gb"))
    m.add(InlineKeyboardButton("🔵 3GB - Rp 4.000", callback_data="beli_3gb"))
    m.add(InlineKeyboardButton("🔵 4GB - Rp 5.000", callback_data="beli_4gb"))
    m.add(InlineKeyboardButton("🔵 5GB - Rp 6.000", callback_data="beli_5gb"))
    m.add(InlineKeyboardButton("🔵 6GB - Rp 7.000", callback_data="beli_6gb"))
    m.add(InlineKeyboardButton("🔵 7GB - Rp 8.000", callback_data="beli_7gb"))
    m.add(InlineKeyboardButton("🔵 8GB - Rp 9.000", callback_data="beli_8gb"))
    m.add(InlineKeyboardButton("🔵 9GB - Rp 10.000", callback_data="beli_9gb"))
    m.add(InlineKeyboardButton("🔵 10GB - Rp 11.000", callback_data="beli_10gb"))
    m.add(InlineKeyboardButton("🔵 UNLIMITED - Rp 13.000", callback_data="beli_unli"))
    m.add(InlineKeyboardButton("🔴 ⬅ Kembali", callback_data="menu_layanan"))
    return m

def menu_bayar():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🟢 Bayar QRIS", callback_data="bayar_qris"))
    m.add(InlineKeyboardButton("🔵 Bayar Saldo Bot", callback_data="bayar_saldo"))
    m.add(InlineKeyboardButton("🔴 Batal", callback_data="batal"))
    return m

def menu_batal():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔴 Batal Order", callback_data="batal"))
    return m

def menu_kembali():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🟢 ⬅ Kembali", callback_data="back"))
    return m

WELCOME_TEXT = """🌟 ━━━━ [ WELCOME ] ━━━━ 🌟
👑 PROFIL BOT
👤 Owner : ZUAN PANEL
📛 Name : AUTO ORDER ZUAN PANEL
⚡ Status : BETA - VIP Only
📌 Prefix : /

📊 STATISTIK
👥 Total User : 481
💰 Pendapatan : Rp 2.438.400

[ 👋 ] Demm Bro, Welcome To Bot AUTO ORDER ZUAN PANEL!"""

@bot.message_handler(commands=['start'])
def start(message):
    user_order.pop(message.chat.id, None)
    try:
        with open("banner.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=WELCOME_TEXT, reply_markup=menu_utama())
    except:
        bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=menu_utama())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data

    def edit(text, markup):
        try:
            if call.message.photo or call.message.caption:
                bot.edit_message_caption(text, cid, mid, reply_markup=markup)
            else:
                bot.edit_message_text(text, cid, mid, reply_markup=markup)
        except:
            bot.send_message(cid, text, reply_markup=markup)
    bot.answer_callback_query(call.id)

    if data == "back":
        try: bot.delete_message(cid, mid)
        except: pass
        try:
            with open("banner.jpg", "rb") as photo:
                bot.send_photo(cid, photo, caption=WELCOME_TEXT, reply_markup=menu_utama())
        except:
            bot.send_message(cid, WELCOME_TEXT, reply_markup=menu_utama())
        return

    if data == "menu_layanan":
        edit("🛍️ ━━━ DAFTAR MENU LAYANAN BOT ━━━ 🛍️\n\nSilahkan Pilih Produk Yang Ingin Anda Order.", menu_layanan())
        return

    if data == "list_panel":
        edit("💰 LIST HARGA PANEL\n\nPilih panel yang mau dibeli bosku!", list_panel())
        return

    if data == "install_free":
        edit("🎁 INSTALL PANEL FREE\n\nUntuk Install Panel Free, chat OWNER dulu ya bosku!\n\nSyarat: Follow Channel Testi & Info dulu!", menu_kembali())
        return

    if data == "owner":
        edit(f"📞 ━━━ CONTACT OWNER BOT ━━━\n\n👤 Name : ZUAN PANEL\n📱 Whatsapp : {OWNER_WA}\n✈️ Telegram : {OWNER_USERNAME}\n\nKamu Limit? Silahkan Klik Command Dibawah", menu_kembali())
        return

    if data == "batal":
        user_order.pop(cid, None)
        edit("❌ Order dibatalkan!\n\nBalik ke menu awal ya bosku!", menu_kembali())
        return

    if data.startswith("beli_"):
        key = data.replace("beli_", "")
        if key in PRODUK:
            p = PRODUK[key]
            user_order[cid] = {"produk": p["nama"], "harga": p["harga"], "step": "username"}
            # INI YANG GUE UBAH BANG: 5-9 HURUF
            edit(f"🛒 BELI {p['nama'].upper()}\n\nHarga : {format_rp(p['harga'])}\nBenefit : {p.get('desc','Panel Premium')}\n\n✏️ Silahkan Kirim Username Untuk Panel Yang Ingin Kamu Beli Dengan Minimal 5-9 Huruf.\n\nContoh : PanelZuan, ZuanStore, ZuanPanel", menu_batal())
            return

    if data == "bayar_qris":
        order = user_order.get(cid, {})
        if not order:
            edit("Order tidak ditemukan, mulai dari /start lagi ya!", menu_kembali())
            return
        edit(f"📱 BAYAR VIA QRIS\n\nItem : {order['produk']} ({order.get('username','')})\nTotal : {format_rp(order['harga'])}\n\nSilahkan scan QRIS ini, lalu kirim bukti TF ke {OWNER_USERNAME} ya bosku!\n\nQRIS : Chat OWNER untuk dapetin QRIS!", menu_kembali())
        return

    if data == "bayar_saldo":
        order = user_order.get(cid, {})
        edit(f"💳 BAYAR SALDO BOT\n\nItem : {order.get('produk','-')}\nTotal : {format_rp(order.get('harga',0))}\nSaldo Bot kamu : Rp 0\n\nSaldo kamu kurang bosku! Topup dulu ke OWNER ya!", menu_kembali())
        return

@bot.message_handler(func=lambda m: True)
def tangkap_username(message):
    cid = message.chat.id
    order = user_order.get(cid)
    if not order or order.get("step") != "username":
        return
    username = message.text.strip()

    # VALIDASI BARU: 5-9 HURUF
    if len(username) < 5:
        bot.send_message(cid, f"❌ Kependekan bosku! Username '{username}' cuma {len(username)} huruf.\n\nMinimal 5 huruf ya! Contoh: PanelZuan\nKirim lagi...")
        return
    if len(username) > 9:
        bot.send_message(cid, f"❌ Kepanjangan bosku! Username '{username}' udah {len(username)} huruf.\n\nMaksimal 9 huruf ya! Contoh: PanelZuan\nKirim lagi...")
        return
    if " " in username:
        bot.send_message(cid, "❌ Username gak boleh ada spasi! Contoh: PanelZuan\nKirim lagi...")
        return

    order["username"] = username
    order["step"] = "bayar"
    bot.send_message(cid,
        f"💳 PILIH METODE PEMBAYARAN\n\n🛍️ Item : {order['produk']} ({username})\n💰 Total : {format_rp(order['harga'])}\n💰 Saldo Bot kamu : Rp 0",
        reply_markup=menu_bayar())

print("Bot ZUAN ala WANZZ jalan...")
bot.infinity_polling()
