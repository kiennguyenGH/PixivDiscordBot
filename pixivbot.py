import os
import json
import discord
import locale
import requests
from pixivpy3 import *
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
api = AppPixivAPI()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents = intents)
TOKEN = os.getenv("DISCORD_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
api.auth(refresh_token = REFRESH_TOKEN)
COLOR = 0x009cff

json_result = api.illust_recommended()

@client.event
async def on_ready():
	print("Bot is starting...")
	print("-------------------")
	print(api.refresh_token)

@client.command()
async def search(ctx, arg):
	json_result = api.illust_detail(arg)
	print(json_result)
	illust = json_result.illust
	response = requests.get(illust.image_urls['large'])
	print(response)
	embed = discord.Embed(title = illust.title, url = "https://pixiv.net/en/artworks/" + str(illust.id), description = illust.caption, color = COLOR)
	embed.set_author(name = illust.user['name'], url = "https://pixiv.net/en/users/" +  str(illust.user['id']))
	embed.set_image(url = illust.meta_single_page['original_image_url'])
	await ctx.send(embed = embed)

client.run(TOKEN)
