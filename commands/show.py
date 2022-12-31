import disnake
from disnake.ext import commands
import data.cords
from bot import bot

@commands.slash_command(name="server", description="Shows saved coordinates on this server")
async def show_server(interaction: disnake.AppCmdInter):
    coordinates = data.cords.get()[str(interaction.guild_id)]
    embed = disnake.Embed(
        title="All Server Coordinates",
        color=disnake.Color.orange(),
    )
    if bool(coordinates):
        for id, cords in coordinates.items():
            member = await bot.guilds[0].fetch_member(id)
            name = f"{member.name}:\n\u200B\n"
            value = ""
            for cord in cords:
                value += f'{cord["x"]}, {cord["y"]}, {cord["z"]} - **{cord["info"].title()}**\n\u200B\n'
            embed.add_field(name=name, value=value, inline=True)
    else: 
        embed.description = "There's nothing here :cricket:\nSave some coordinates!"
    await interaction.response.send_message(embed=embed)

@commands.slash_command(name="cords", description="Shows your saved coordinates")
async def show_self(interaction: disnake.AppCmdInter):
    coordinates = dict(data.cords.get())[str(interaction.guild_id)]
    author = interaction.author

    async def remove(interaction: disnake.Interaction):
        undo_copy = data.cords.remove(interaction.guild_id, author.id, choose.values[0])
        embed = disnake.Embed(title=f"{choose.values[0].title()} was removed", color=disnake.Color.brand_green())

        async def undo(interaction: disnake.Interaction):
            data.cords.add_cord(interaction.guild_id, author.id, undo_copy["x"], undo_copy["y"], undo_copy["z"], undo_copy["info"])
            embed.title = f"{choose.values[0].title()} was added back!"
            await interaction.response.send_message(embed=embed)

        view = disnake.ui.View()
        undo_button = disnake.ui.Button(
            style=disnake.ButtonStyle.blurple,
            label="Undo"
        )
        undo_button.callback = undo
        view.add_item(undo_button)
        await interaction.response.send_message(embed=embed, view=view)

    view = disnake.ui.View()
    options = []
    embed = disnake.Embed(
        title="Your Saved Coordinates",
        color=disnake.Color.orange(),
    )
    if str(author.id) in coordinates:
        for cord in coordinates[str(author.id)]:
            name = f"{cord['info'].title()}:"
            value = f'{cord["x"]}, {cord["y"]}, {cord["z"]}'
            embed.add_field(name=name, value=value, inline=False)
            options.append(disnake.SelectOption(label=cord['info'].title(), value=cord["info"]))
    else: 
        embed.description = "There's nothing here :cricket:\nSave some coordinates!"

    choose = disnake.ui.Select(
        placeholder="Select an coordinate to remove",
        max_values=1,
        options=options
    )
    choose.callback = remove
    view.add_item(choose)
    if str(author.id) in coordinates:
        await interaction.response.send_message(embed=embed, view=view)
    else: await interaction.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_slash_command(show_server)
    bot.add_slash_command(show_self)