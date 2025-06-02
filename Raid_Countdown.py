#Countdown

import discord
import asyncio
import os
from datetime import datetime, timedelta
from discord.ext import commands

# Configurar permisos
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal donde quieres mostrar la cuenta regresiva
CHANNEL_ID = 1363964420648079427  # Cambia esto por el ID real de tu canal

# Fecha de la raid (15 de abril a las 20:00 UTC-6)
raid_date = datetime(2025, 6, 04, 19, 0)  # 📌 Cambia el año si es en 2026 o más

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("⚠️ No se encontró el canal. Verifica el ID.")
        return

    while True:
        now = datetime.utcnow() - timedelta(hours=6)  # UTC-6
        remaining_time = raid_date - now

        if remaining_time.total_seconds() > 0:
            days = remaining_time.days
            hours = remaining_time.seconds // 3600
            minutes = (remaining_time.seconds % 3600) // 60

            countdown_text = f"⏳│ Onyxia: {days} días, {hours} horas"
        else:
            countdown_text = "🎉 **¡La raid ha comenzado!** 🏹🔥⚔️"
            # countdown_text = "⏳│ Raid: Por Definir🔥"

        try:
            await channel.edit(name=f"{countdown_text}")
            print(f"Canal actualizado: {countdown_text}")
        except discord.errors.Forbidden:
            print("⚠️ No tengo permisos para cambiar el nombre del canal.")
        except discord.errors.HTTPException as e:
            print(f"⚠️ Error de Discord: {e}")

        print(now)
        await asyncio.sleep(600)  # Se actualiza cada 10 minutos

# Leer el token desde las variables de entorno
TOKEN = os.getenv("RCTOKEN")

bot.run(TOKEN)
