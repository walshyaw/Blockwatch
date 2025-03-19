# @WALSHYAW | https://github.com/walshyaw/
# Created on 03/12/2025. Last modified on 03/12/2025.

import discord, os
from discord.ext import commands
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
        title="Blockwatch | Setup Panel",
        description="Please select the version of Minecraft that your server is running. Blockwatch supports Java and Bedrock servers on versions 1.7+.",
        colour=0x72FA7C,
    )

    embed.set_author(
        name="Blockwatch",
        url="https://github.com/walshyaw",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
    )

    embed.set_thumbnail(
        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
    )

    embed.set_footer(text="Built by @walshyaw | 2025")

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
        title="Blockwatch | Server Address",
        description="Please provide the IP Address for your server. The port may be needed as well, it just depends on the server.",
        colour=0x72FA7C,
    )

    embed.set_author(
        name="Blockwatch",
        url="https://github.com/walshyaw",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
    )

    embed.set_thumbnail(
        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
    )

    embed.set_footer(text="Built by @walshyaw | 2025")
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
        title="Blockwatch | Pinging Server...",
        description="Loading server information...",
        colour=0x72FA7C,
    )

    server_embed.set_author(
        name="Blockwatch",
        url="https://github.com/walshyaw",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
    )

    server_embed.set_thumbnail(
        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
    )

    server_embed.set_footer(text="Built by @walshyaw | 2025")
    status = await interaction.channel.send(embed=server_embed)
    await asyncio.sleep(4)

    # LOOP TO CONTINUOUSLY PING THE SERVER FOR IT'S STATUS
    while True:

        url = "https://api.mcsrvstat.us/3/" + SERVER_IP
        response = requests.get(url)
        data = response.text
        logs = json.loads(data)

        # ONLINE
        if logs["online"]:

            motd = str(logs["motd"]["clean"]).strip("['']")

            embed = discord.Embed(
                title="Blockwatch | Server Information",
                description="**Current Status:**  🟩"
                "\n**Title:** "
                f"{motd}"
                ""
                "\n\n**Version**: *"
                f"{logs["protocol"]["name"]}*"
                ""
                "\n**Players**: *"
                f"{logs["players"]["online"]} / {logs["players"]["max"]}*"
                "\n**IP Address**: "
                f"{SERVER_IP}",
                colour=0x72FA7C,
            )

            embed.set_author(
                name="Blockwatch",
                url="https://github.com/walshyaw",
                icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
            )

            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
            )

            embed.set_footer(text="Built by @walshyaw | 2025")

            await status.edit(embed=embed)

        # OFFLINE
        else:
            embed = discord.Embed(
                title="Blockwatch | Server Information",
                description="Current Status: " "🟥\n\nIP Address: " f"{logs["ip"]}",
                colour=0xFD0D00,
            )

            embed.set_author(
                name="Blockwatch",
                url="https://github.com/walshyaw",
                icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
            )

            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
            )

            embed.set_footer(text="Built by @walshyaw | 2025")

            await status.edit(embed=embed)

        await asyncio.sleep(30)


# BEDROCK EDITION SETUP
async def bedrock_setup(interaction):

    # FIRST SETUP EMBED
    embed = discord.Embed(
        title="Blockwatch | Server Address",
        description="Please provide the IP Address for your server. The port may be needed as well, it just depends on the server.",
        colour=0x72FA7C,
    )

    embed.set_author(
        name="Blockwatch",
        url="https://github.com/walshyaw",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
    )

    embed.set_thumbnail(
        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
    )

    embed.set_footer(text="Built by @walshyaw | 2025")
    await interaction.response.send_message(embed=embed)
    bedrock_embed = await interaction.original_response()

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
    await bedrock_embed.delete()

    # SERVER STATUS PANEL EMBED
    server_embed = discord.Embed(
        title="Blockwatch | Pinging Server...",
        description="Loading server information...",
        colour=0x72FA7C,
    )

    server_embed.set_author(
        name="Blockwatch",
        url="https://github.com/walshyaw",
        icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
    )

    server_embed.set_thumbnail(
        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
    )

    server_embed.set_footer(text="Built by @walshyaw | 2025")
    status = await interaction.channel.send(embed=server_embed)
    await asyncio.sleep(4)

    # LOOP TO CONTINUOUSLY PING THE SERVER FOR IT'S STATUS
    while True:

        url = "https://api.mcsrvstat.us/bedrock/3/" + SERVER_IP
        response = requests.get(url)
        data = response.text
        logs = json.loads(data)

        # ONLINE
        if logs["online"]:

            motd = str(logs["motd"]["clean"]).strip("['']")

            embed = discord.Embed(
                title="Blockwatch | Server Information",
                description="**Current Status:**  🟩"
                "\n**Title:** "
                f"{motd}"
                ""
                "\n\n**Version**: *"
                f"{logs["protocol"]["name"]}*"
                ""
                "\n**Players**: *"
                f"{logs["players"]["online"]} / {logs["players"]["max"]}*"
                "\n**IP Address**: "
                f"{SERVER_IP}",
                colour=0x72FA7C,
            )

            embed.set_author(
                name="Blockwatch",
                url="https://github.com/walshyaw",
                icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
            )

            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
            )

            embed.set_footer(text="Built by @walshyaw | 2025")

            await status.edit(embed=embed)

        # OFFLINE
        else:
            embed = discord.Embed(
                title="Blockwatch | Server Information",
                description="Current Status: " "🟥\n\nIP Address: " f"{logs["ip"]}",
                colour=0xFD0D00,
            )

            embed.set_author(
                name="Blockwatch",
                url="https://github.com/walshyaw",
                icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartcraft.com%2Fimages%2Fminecraft-logo-png-2.png&f=1&nofb=1&ipt=9a79845d4044a6c22ec383f4058dcd63000a0e6ee534112de86770ca42299ec4&ipo=images",
            )

            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F7f%2Fa4%2F85%2F7fa485a49e92979b2abc2518485b95fc.jpg&f=1&nofb=1&ipt=f9ae67232e006c4b55f5c4d0435a51ff4c59af4645c3ec27b71bd9738cce200c&ipo=images"
            )

            embed.set_footer(text="Built by @walshyaw | 2025")

            await status.edit(embed=embed)

        await asyncio.sleep(30)


# START THE BOT
@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Logged in as {client.user}")


client.run(TOKEN)
