import discord
import asyncio
import os  # Para leer variables de entorno
from datetime import datetime
from discord.ext import commands

# Configurar permisos
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal donde quieres mostrar la hora
CHANNEL_ID = 123456789012345678  # Cambia esto por el ID real de tu canal

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("⚠️ No se encontró el canal. Verifica el ID.")
        return

    while True:
        now = datetime.now().strftime("%H:%M:%S")  # Obtener la hora actual
        try:
            await channel.edit(name=f"🕒 {now}")
            print(f"Canal actualizado: {now}")
        except discord.errors.Forbidden:
            print("⚠️ No tengo permisos para cambiar el nombre del canal.")
        except discord.errors.HTTPException as e:
            print(f"⚠️ Error de Discord: {e}")

        await asyncio.sleep(360)  # Se actualiza cada segundo

# Leer el token desde las variables de entorno
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
