import discord
import asyncio
import os  # Para leer variables de entorno
from datetime import datetime, timedelta
from discord.ext import commands

# Configurar permisos
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal donde quieres mostrar la hora
CHANNEL_ID = 1354268659828260985  # Cambia esto por el ID real de tu canal

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("⚠️ No se encontró el canal. Verifica el ID.")
        return

    while True:
        now = datetime.utcnow() - timedelta(hours=6)  # 📌 Restar 6 horas a UTC
        formatted_time = now.strftime("%H:%M")  # Solo horas y minutos
        try:
            await channel.edit(name=f"🕒│Hora Server: {formatted_time}")
            print(f"Canal actualizado: {formatted_time}")
        except discord.errors.Forbidden:
            print("⚠️ No tengo permisos para cambiar el nombre del canal.")
        except discord.errors.HTTPException as e:
            print(f"⚠️ Error de Discord: {e}")

        await asyncio.sleep(360)  # Se actualiza cada segundo

# Leer el token desde las variables de entorno
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
