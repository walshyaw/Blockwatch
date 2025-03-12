#
#
#
#
#

import discord, os
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv
import json
import requests
import asyncio
from datetime import datetime

# GRABS BOT TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# INITIALIZE THE BOT
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


# COMMAND TREE
@client.tree.command(
    name="mcsetup",
    description="Starts the setup process.",
)

# INITIALIZES WIDGET SETUP
async def mcsetup(interaction):

    # SETUP EMBED
    embed = discord.Embed(
        title="MCTrack Server Status Setup",
        colour=0x1ADB28,
        description="Please select the version of Minecraft"
        " that your server is currently running.",
    )

    embed.set_author(name="@walshyaw", url="https://github.com/walshyaw")

    embed.set_footer(
        text="Built by @walshyaw | 2025",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com"
        "%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=a6fbb15173bb83d5a7dfa761477af3a442c"
        "3ce1adcabe38371df9c6ad9eb1f22&ipo=images",
    )

    # SETUP BUTTONS
    bedrock = Button(
        label="BEDROCK EDITION", style=discord.ButtonStyle.green, emoji="🔥"
    )
    java = Button(label="JAVA EDITION", style=discord.ButtonStyle.green, emoji="🌊")

    # ALLOWS BUTTONS TO RESPOND TO CLICKS
    async def bedrock_callback(interaction):
        await interaction.message.delete()
        await bedrock_setup(interaction)

    async def java_callback(interaction):
        await interaction.message.delete()
        await java_setup(interaction)

    bedrock.callback = bedrock_callback
    java.callback = java_callback

    # DISPLAYS BUTTONS
    view = View()
    view.add_item(bedrock)
    view.add_item(java)

    await interaction.response.send_message(embed=embed, view=view)


# JAVA EDITION SETUP
async def java_setup(interaction):

    # FIRST SETUP EMBED
    embed = discord.Embed(
        title="MCTrack Server Status Setup",
        description="Please enter your server's IP Address below.",
        colour=0x1ADB28,
    )

    embed.set_author(name="@walshyaw", url="https://github.com/walshyaw")

    embed.set_footer(
        text="Built by @walshyaw | 2025",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F"
        "clipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=a6fbb15173bb83"
        "d5a7dfa761477af3a442c3ce1adcabe38371df9c6ad9eb1f22&ipo=images",
    )
    await interaction.response.send_message(embed=embed)
    java_embed = await interaction.original_response()

    # ENSURES THAT THE BOT ONLY TAKES IP'S FROM THE USER WHO CALLED IT
    def check(message):
        return (
            message.author == interaction.user
            and message.channel == interaction.channel
        )

    # GRABS SERVER IP AND LOGS IT, DELETES THE EMBED.
    SERVER_IP = (await client.wait_for("message", check=check)).content
    print()
    print(f"Successfully logged IP: {SERVER_IP}")
    await java_embed.delete()

    # SERVER STATUS PANEL EMBED
    server_embed = discord.Embed(
        title="PINGING SERVER...", colour=0x1ADB28, timestamp=datetime.now()
    )
    server_embed.set_author(name="@walshyaw", url="https://github.com/walshyaw")
    server_embed.set_footer(
        text="Built by @walshyaw | 2025",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F"
        "clipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=a6fbb15173bb83d5a7dfa76147"
        "7af3a442c3ce1adcabe38371df9c6ad9eb1f22&ipo=images",
    )
    status = await interaction.followup.send(embed=server_embed)
    await asyncio.sleep(4)

    # LOOP TO CONTINUOUSLY PING THE SERVER FOR IT'S STATUS
    while True:

        url = "https://api.mcsrvstat.us/3/" + SERVER_IP
        response = requests.get(url)
        data = response.text
        logs = json.loads(data)

        if logs["online"]:

            motd = str(logs["motd"]["clean"]).strip("['']")

            embed = discord.Embed(
                title=f"{motd}",
                description=f"""
                      **Online: 🟩**\n\n
                      **Version**: *{logs["protocol"]["name"]}*\n\n
                      **Players:** *{logs["players"]["online"]} / {logs["players"]["max"]}*""",
                colour=0x1ADB28,
                timestamp=datetime.now(),
            )

            embed.set_author(name="@walshyaw", url="https://github.com/walshyaw")

            embed.set_footer(
                text="Built by @walshyaw | 2025",
                icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com"
                "%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=a6fbb15173bb83d5a7dfa761477af3a442"
                "c3ce1adcabe38371df9c6ad9eb1f22&ipo=images",
            )

            await status.edit(embed=embed)

        else:
            embed = discord.Embed(
                title=f"{logs[motd]}",
                description="**Offline:** 🟥",
                colour=0xD61F23,
                timestamp=datetime.now(),
            )

            embed.set_author(name="@walshyaw", url="https://github.com/walshyaw")

            embed.set_footer(
                text="Built by @walshyaw | 2025",
                icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com"
                "%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=a6fbb15173bb83d5a7dfa761477af3a442"
                "c3ce1adcabe38371df9c6ad9eb1f22&ipo=images",
            )

            await status.edit(embed=embed)

        await asyncio.sleep(30)


# BEDROCK EDITION SETUP
async def bedrock_setup(interaction):
    print()


# START THE BOT
@client.event
async def on_ready():

    # FOR LOOP USED TO LOOP THROUGH ALL THE SERVERS THE BOT IS IN AND SYNC THE COMMANDS TO EACH ONE.
    print()
    for guild in client.guilds:
        await client.tree.sync(guild=discord.Object(id=guild.id))
        print(f"Commands synced for guild: {guild.name} (ID: {guild.id})")

    print(f"Logged in as {client.user}")


client.run(TOKEN)
