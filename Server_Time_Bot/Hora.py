

import discord
import asyncio
from datetime import datetime
from discord.ext import commands

# Configura el bot con permisos de intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal que quieres actualizar (reemplázalo con el tuyo)
CHANNEL_ID = 1354268659828260985  # Cambia esto por el ID de tu canal

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        try:
            await channel.edit(name=f"Hora: {now}")
        except discord.errors.Forbidden:
            print("No tengo permisos para cambiar el nombre del canal.")
        await asyncio.sleep(300)  # Espera 60 segundos antes de actualizar

# Inicia el bot con tu token
TOKEN = "MTM1NDE4ODc3NzQ3MTM0ODg2Nw.GayC1E.Km1SshepPb4iI3NahsViuzBU8b4KtKP9Jumk9o"
bot.run(TOKEN)
