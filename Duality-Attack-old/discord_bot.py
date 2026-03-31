import discord
from discord.ext import commands
import subprocess
import requests
import os

# Konfigurasi
TOKEN = "INPUT_YOUR_DISCORD_BOT_TOKEN_HERE"
PREFIX = "!"
ALLOWED_CHANNELS = [] # Kosongkan dulu agar bisa di semua channel

# Gunakan hanya 1 instance Bot untuk semuanya
intents = discord.Intents.default()
intents.message_content = True  # WAJIB!
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# --- Event: Saat bot siap ---
@bot.event
async def on_ready():
    print(f'✅ Bot Online sebagai {bot.user}')

# --- Command: ping ---
@bot.command(name='ping')
async def ping(ctx):
    """Cek status bot"""
    await ctx.send(f'🏓 Pong! Latency: {round(bot.latency * 1000)}ms')

# --- Command: shell ---
@bot.command(name='shell')
async def shell(ctx, *, command):
    """Jalankan command di Termux"""
    # Cek channel jika diperlukan (opsional)
    # if ALLOWED_CHANNELS and ctx.channel.id not in ALLOWED_CHANNELS: return

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        if len(output) > 1900:
            output = output[:1900] + "..."
        await ctx.send(f"```bash\n{output}\n```")
    except subprocess.TimeoutExpired:
        await ctx.send("❌ Command timeout!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# --- Command: ip ---
@bot.command(name='ip')
async def ip_lookup(ctx, ip: str):
    """Cek IP address"""
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        if data.get('status') == 'success':
            embed = discord.Embed(title=f"🌍 IP Lookup: {ip}", color=discord.Color.green())
            embed.add_field(name="Country", value=data.get('country', 'N/A'), inline=True)
            embed.add_field(name="City", value=data.get('city', 'N/A'), inline=True)
            embed.add_field(name="ISP", value=data.get('isp', 'N/A'), inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ IP tidak ditemukan")
    except:
        await ctx.send("❌ Gagal lookup IP")

# Jalankan bot
if __name__ == "__main__":
    if TOKEN == "TOKEN_ASLI_KAMU":
        print("❌ GANTI DULU TOKENNYA!")
    else:
        bot.run(TOKEN)
