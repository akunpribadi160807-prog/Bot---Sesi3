import os
‎import telebot
‎from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
‎
‎TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
‎bot = telebot.TeleBot(TOKEN)
‎
‎OWNER_USERNAME = "@ShanXPLD"
‎OWNER_WA = "085872257850"
‎CHANNEL_TESTI = "https://t.me/ZUANPANEL"
‎CHANNEL_INFO = "https://t.me/ZUANPANEL"
‎
‎user_order = {}
‎
‎PRODUK = {
‎    "admin": {"nama": "Admin Panel", "harga": 3000, "desc": "Akun Root Admin (Full Akses)"},
‎    "pterodactyl": {"nama": "Panel Pterodactyl", "harga": 2000, "desc": "Panel 1GB - 10GB"},
‎    "pterodactyl_legal": {"nama": "Panel Pterodactyl Legal", "harga": 5000, "desc": "Panel Legal Garansi Full"},
‎    "reseller": {"nama": "Reseller Panel", "harga": 10000, "desc": "Akses Reseller Panel"},
‎    "reseller_legal": {"nama": "Reseller Panel Legal", "harga": 13000, "desc": "Akses Reseller Panel Legal"},
‎    "1gb": {"nama": "Panel 1GB", "harga": 6000},
‎    "2gb": {"nama": "Panel 2GB", "harga": 8000},
‎    "3gb": {"nama": "Panel 3GB", "harga": 10000},
‎    "4gb": {"nama": "Panel 4GB", "harga": 12000},
‎    "5gb": {"nama": "Panel 5GB", "harga": 14000},
‎    "6gb": {"nama": "Panel 6GB", "harga": 16000},
‎    "7gb": {"nama": "Panel 7GB", "harga": 18000},
‎    "8gb": {"nama": "Panel 8GB", "harga": 20000},
‎    "9gb": {"nama": "Panel 9GB", "harga": 22000},
‎    "10gb": {"nama": "Panel 10GB", "harga": 25000},
‎    "unli": {"nama": "Panel UNLIMITED", "harga": 30000},
‎}
‎
‎def format_rp(n):
‎    return f"Rp {n:,}".replace(",", ".")
‎
‎def menu_utama():
‎    m = InlineKeyboardMarkup()
‎    m.add(InlineKeyboardButton("🟢 Menu Layanan", callback_data="menu_layanan"))
‎    m.add(InlineKeyboardButton("🔵 Install Panel Free", callback_data="install_free"))
‎    m.add(InlineKeyboardButton("🔴 Owner Bot", callback_data="owner"))
‎    m.add(InlineKeyboardButton("🟢 Channel Testi ↗", url=CHANNEL_TESTI))
‎    m.add(InlineKeyboardButton("🔵 Channel Info ↗", url=CHANNEL_INFO))
‎    return m
‎
‎def menu_layanan():
‎    m = InlineKeyboardMarkup()
‎    m.add(InlineKeyboardButton("🔵 Admin Panel - Rp 10.000", callback_data="beli_admin"))
‎    m.add(InlineKeyboardButton("🔵 Panel Pterodactyl", callback_data="beli_pterodactyl"))
‎    m.add(InlineKeyboardButton("🔵 Panel Pterodactyl Legal", callback_data="beli_pterodactyl_legal"))
‎    m.add(InlineKeyboardButton("🔵 Reseller Panel", callback_data="beli_reseller"))
‎    m.add(InlineKeyboardButton("🔵 Reseller Panel Legal", callback_data="beli_reseller_legal"))
‎    m.add(InlineKeyboardButton("🟢 Panel 1GB - 10GB / UNLIMITED", callback_data="list_panel"))
‎    m.add(InlineKeyboardButton("🔴 ⬅ Kembali", callback_data="back"))
‎    return m
‎
‎def list_panel():
‎    m = InlineKeyboardMarkup()
‎    m.add(InlineKeyboardButton("🔵 1GB - Rp 6.000", callback_data="beli_1gb"))
‎    m.add(InlineKeyboardButton("🔵 2GB - Rp 8.000", callback_data="beli_2gb"))
‎    m.add(InlineKeyboardButton("🔵 3GB - Rp 10.000", callback_data="beli_3gb"))
‎    m.add(InlineKeyboardButton("🔵 4GB - Rp 12.000", callback_data="beli_4gb"))
‎    m.add(InlineKeyboardButton("🔵 5GB - Rp 14.000", callback_data="beli_5gb"))
‎    m.add(InlineKeyboardButton("🔵 6GB - Rp 16.000", callback_data="beli_6gb"))
‎    m.add(InlineKeyboardButton("🔵 7GB - Rp 18.000", callback_data="beli_7gb"))
‎    m.add(InlineKeyboardButton("🔵 8GB - Rp 20.000", callback_data="beli_8gb"))
‎    m.add(InlineKeyboardButton("🔵 9GB - Rp 22.000", callback_data="beli_9gb"))
‎    m.add(InlineKeyboardButton("🔵 10GB - Rp 25.000", callback_data="beli_10gb"))
‎    m.add(InlineKeyboardButton("🔵 UNLIMITED - Rp 30.000", callback_data="beli_unli"))
‎    m.add(InlineKeyboardButton("🔴 ⬅ Kembali", callback_data="menu_layanan"))
‎    return m
‎
‎def menu_bayar():
‎    m = InlineKeyboardMarkup()
‎    m.add(InlineKeyboardButton("🟢 Bayar QRIS", callback_data="bayar_qris"))
‎    m.add(InlineKeyboardButton("🔵 Bayar Saldo Bot", callback_data="bayar_saldo"))
‎    m.add(InlineKeyboardButton("🔴 Batal", callback_data="batal"))
‎    return m
‎
‎def menu_batal():
‎    m = InlineKeyboardMarkup()
‎    m.add(InlineKeyboardButton("🔴 Batal Order", callback_data="batal"))
‎    return m
‎
‎def menu_kembali():
‎    m = InlineKeyboardMarkup()
‎    m.add(InlineKeyboardButton("🟢 ⬅ Kembali", callback_data="back"))
‎    return m
‎
‎# UDAH GUE HAPUS PREFIX NYA BANG!
‎WELCOME_TEXT = """🌟 ━━━━ [ WELCOME ] ━━━━ 🌟
‎👑 PROFIL BOT
‎👤 Owner : ZUAN PANEL
‎📛 Name : AUTO ORDER ZUAN PANEL
‎⚡ Status : VIP
‎
‎📊 STATISTIK
‎👥 Total User : 481
‎💰 Pendapatan : Rp 2.438.400
‎
‎[ 👋 ] Deymm Bro, Welcome To Bot AUTO ORDER ZUAN PANEL!"""
‎
‎@bot.message_handler(commands=['start'])
‎def start(message):
‎    user_order.pop(message.chat.id, None)
‎    try:
‎        with open("banner.jpg", "rb") as photo:
‎            bot.send_photo(message.chat.id, photo, caption=WELCOME_TEXT, reply_markup=menu_utama())
‎    except:
‎        bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=menu_utama())
‎
‎@bot.callback_query_handler(func=lambda call: True)
‎def callback(call):
‎    cid = call.message.chat.id
‎    mid = call.message.message_id
‎    data = call.data
‎
‎    def edit(text, markup):
‎        try:
‎            if call.message.photo or call.message.caption:
‎                bot.edit_message_caption(text, cid, mid, reply_markup=markup)
‎            else:
‎                bot.edit_message_text(text, cid, mid, reply_markup=markup)
‎        except:
‎            bot.send_message(cid, text, reply_markup=markup)
‎    bot.answer_callback_query(call.id)
‎
‎    if data == "back":
‎        try: bot.delete_message(cid, mid)
‎        except: pass
‎        try:
‎            with open("banner.jpg", "rb") as photo:
‎                bot.send_photo(cid, photo, caption=WELCOME_TEXT, reply_markup=menu_utama())
‎        except:
‎            bot.send_message(cid, WELCOME_TEXT, reply_markup=menu_utama())
‎        return
‎
‎    if data == "menu_layanan":
‎        edit("🛍️ ━━━ DAFTAR MENU LAYANAN BOT ━━━ 🛍️\n\nSilahkan Pilih Produk Yang Ingin Anda Order.", menu_layanan())
‎        return
‎
‎    if data == "list_panel":
‎        edit("💰 LIST HARGA PANEL\n\nPilih panel yang mau dibeli bosku!", list_panel())
‎        return
‎
‎    if data == "install_free":
‎        edit("🎁 INSTALL PANEL FREE\n\nUntuk Install Panel Free, chat OWNER dulu ya bosku!\n\nSyarat: Follow Channel Testi & Info dulu!", menu_kembali())
‎        return
‎
‎    if data == "owner":
‎        edit(f"📞 ━━━ CONTACT OWNER BOT ━━━\n\n👤 Name : ZUAN PANEL\n📱 Whatsapp : {OWNER_WA}\n✈️ Telegram : {OWNER_USERNAME}\n\nKamu Limit? Silahkan Klik Command Dibawah", menu_kembali())
‎        return
‎
‎    if data == "batal":
‎        user_order.pop(cid, None)
‎        edit("❌ Order dibatalkan!\n\nBalik ke menu
