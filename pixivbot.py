import os
import discord
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

@client.event
async def on_ready():
	print("Pixiv Discord Bot")
	print("-------------------")

@client.command()
async def search(ctx, arg):
	json_result = api.illust_detail(arg)
	#print(json_result)
	illust = json_result.illust
	img_url = illust.image_urls['large']
	api.download(img_url, fname = "image.jpg")
	embed = discord.Embed(title = illust.title, url = "https://pixiv.net/en/artworks/" + str(illust.id), description = illust.caption, color = COLOR)
	embed.set_author(name = illust.user['name'], url = "https://pixiv.net/en/users/" +  str(illust.user['id']))
	embed.add_field(name = "Total Views", value = illust['total_view'], inline = True)
	embed.add_field(name = "Total Bookmarks", value = illust['total_bookmarks'], inline = True)
	with open('image.jpg', 'rb') as file:
		image = discord.File(file)
		embed.set_image(url = "attachment://image.jpg")
		await ctx.send(embed = embed, file = image)
	os.remove('image.jpg')
client.run(TOKEN)
