import discord
import os
from discord.ext import commands
from discord.ui import View, Button

TOKEN = os.getenv("WWTOKEN")
GUILD_ID = 1349956314998116352  # ID del servidor de Discord
WELCOME_CHANNEL_ID = 1349962816928350363  # ID del canal de bienvenida

# Diccionario de clases y emojis
CLASSES = {
    "Chaman": "⚡",
    "Druida": "🌳",
    "Cazador": "🏹",
    "Picaro": "🗡️",
    "Guerrero": "⚔️",
    "Mago": "🔥",
    "Brujo": "💀",
    "Sacerdote": "🕊️",
}

# Intents necesarios
intents = discord.Intents.default()
intents.members = True  # Necesario para detectar miembros que entran
bot = commands.Bot(command_prefix="!", intents=intents)

class ClassSelectionView(View):
    """Vista con botones para seleccionar clases de WoW"""
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member
        self.selected_classes = set()

        # Crear botones para cada clase
        for class_name, emoji in CLASSES.items():
            self.add_item(ClassButton(class_name, emoji, self))

    async def update_roles(self):
        """Asigna los roles seleccionados al usuario"""
        guild = self.member.guild
        roles_to_assign = [discord.utils.get(guild.roles, name=cls) for cls in self.selected_classes]
        
        # Filtra los roles válidos
        roles_to_assign = [role for role in roles_to_assign if role]
        
        # Verifica si seleccionó más de 2 clases
        if len(self.selected_classes) > 2:
            await self.member.send("Solo puedes seleccionar hasta 2 clases.")
            return
        
        # Remueve roles anteriores de clases y asigna los nuevos
        class_roles = [discord.utils.get(guild.roles, name=cls) for cls in CLASSES.keys()]
        await self.member.remove_roles(*class_roles)
        await self.member.add_roles(*roles_to_assign)
        await self.member.send(f"Has seleccionado: {', '.join(self.selected_classes)}")

class ClassButton(Button):
    """Botón para seleccionar una clase"""
    def __init__(self, class_name, emoji, view):
        super().__init__(style=discord.ButtonStyle.primary, label=class_name, emoji=emoji)
        self.class_name = class_name
        self.view = view

    async def callback(self, interaction: discord.Interaction):
        if self.class_name in self.view.selected_classes:
            self.view.selected_classes.remove(self.class_name)
        else:
            self.view.selected_classes.add(self.class_name)
        
        await self.view.update_roles()
        await interaction.response.defer()  # Evita el mensaje de "pensando..."

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_member_join(member):
    """Cuando un usuario se une al servidor, se le envía un mensaje privado con las reglas y selección de clases"""
    try:
        embed = discord.Embed(title="¡Bienvenido a la Hermandad!", color=discord.Color.gold())
        embed.add_field(name="Reglas", value="1. Respeta a los demás.\n2. No spam.\n3. Usa los canales correctamente.", inline=False)
        embed.set_footer(text="Selecciona tu clase a continuación:")

        view = ClassSelectionView(member)
        await member.send(embed=embed, view=view)

    except Exception as e:
        print(f"Error al enviar mensaje de bienvenida: {e}")

bot.run(TOKEN)
