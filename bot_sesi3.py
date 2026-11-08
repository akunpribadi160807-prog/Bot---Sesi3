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
    m.add(InlineKeyboardButton("
