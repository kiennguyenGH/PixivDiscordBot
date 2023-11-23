import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
intents = discord.Intents.all()
TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix='!', intents = intents)

@client.event
async def on_ready():
	print("Pixiv Discord Bot")
	print("-------------------")

async def load_extensions():
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
	async with client:
		await load_extensions()
		await client.start(TOKEN)

asyncio.run(main())
