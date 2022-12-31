import disnake
from disnake.ext import commands
import data.cords as cords

class CordModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="X",
                custom_id="x",
                style=disnake.TextInputStyle.short,
                placeholder="The coordinates X value",
                required=False
            ),
            disnake.ui.TextInput(
                label="Y",
                custom_id="y",
                style=disnake.TextInputStyle.short,
                placeholder="The coordinates Y value",
                required=False
            ),
            disnake.ui.TextInput(
                label="Z",
                custom_id="z",
                style=disnake.TextInputStyle.short,
                placeholder="The coordinates Z value",
                required=False
            ),
            disnake.ui.TextInput(
                label="Info",
                custom_id="info",
                style=disnake.TextInputStyle.short,
                max_length=30,
                required=True,
                placeholder="Don't use the same names!"
            )
        ]
        super().__init__(
            title="Save Coordinates",
            components=components
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        author = interaction.author
        inputs = interaction.text_values
        embed = disnake.Embed(
            title="Coordinates Saved!",
            color=disnake.Color.brand_green()
        )
        embed.add_field(name=f'{inputs["info"]}:', value="\u200B", inline=False)
        info = inputs["info"]
        del inputs["info"]
        for cord, value in inputs.items():
            embed.add_field(name=f"{cord.upper()}: {value}", value="\u200B", inline=False)
        cords.add_cord(interaction.guild_id, author.id, inputs["x"], inputs["y"], inputs["z"], info)
        await interaction.response.send_message(embed=embed)
        

@commands.slash_command(name="save", description="Saves given coordinates with given information")
async def add(interaction: disnake.AppCmdInter):
    await interaction.response.send_modal(modal=CordModal())

def setup(bot: commands.Bot):
    bot.add_slash_command(add)