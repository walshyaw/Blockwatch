
# Blockwatch

This project is a simple Discord bot that enables the users to see the status of a Minecraft server at any given time straight from their own Discord server. It is compatible with Java and Bedrock and will work with any version of the game above 1.7.

## Authors

- [@walshyaw](https://github.com/walshyaw)



## Features

- Support for Java and Bedrock Editions of the game
- ANY version of Minecraft 1.7+
- Custom Widget with live updates of your server status
- Uses the mcsrvstat API

## Run Locally

Clone the project

```bash
  git clone https://github.com/walshyaw/Blockwatch.git
```

Go to the project directory

```bash
  cd .\Blockwatch\
```

Install dependencies

```bash
  pip install -r requirements.txt

```

Allocate proper Bot privileges in the Discord Developer Portal

```bash
  • Manage Channels
  • View Channels
  • Send Messages
  • Manage Messages
  • Embed Links
  • Read Message History
  • Use Slash Commands
  • Use Embedded Activities
```

Find your bot's API key and paste it into the .env file.

```bash
  DISCORD_TOKEN=YOUR_API_KEY
```

Start the bot

```bash
  python .\blockWatch.py
```

## Demo

![Demo](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2FvdjQwOGd3MDdlc2s1Mzk4N2Nma3JsNDNqc3Njd25jYTN0Z3V4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L5crTzS1g6aHqftryy/giphy.gif)



## Acknowledgements

 - [mcsrvstat API](https://api.mcsrvstat.us/)
