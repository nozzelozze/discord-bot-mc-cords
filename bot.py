import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import data.cords

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=disnake.Intents.all()
)

@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.streaming, activity=disnake.Game(name="Saving some cords!"))
    print(f"{bot.user} is connected to:")
    for guild in bot.guilds:
        print(f"\t{guild.name}")
        if str(guild.id) in data.cords.get():
            pass
        else:
            data.cords.add_server(guild.id)

bot.load_extension("commands.add")
bot.load_extension("commands.show")

bot.run(TOKEN)