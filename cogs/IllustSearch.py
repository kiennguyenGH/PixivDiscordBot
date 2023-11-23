import os
import discord
import logging
import sys
from pixivpy3 import *
from dotenv import load_dotenv
from discord.ext import commands

class IllustSearch(commands.Cog):
	def __init__(self, client):
		self.client = client

	logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

	load_dotenv()
	api = AppPixivAPI()
	REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
	api.auth(refresh_token = REFRESH_TOKEN)
	COLOR = 0x009cff

	@commands.command()
	async def search(self, ctx, arg):
		COLOR = IllustSearch.COLOR
		api = IllustSearch.api
		json_result = api.illust_detail(arg)
		#print(json_result)
		illust = json_result.illust
		img_url = illust.image_urls['large']
		api.download(img_url, fname = "image.jpg")
		embed = discord.Embed(title = illust.title, url = "https://pixiv.net/en/artworks/" + str(illust.id), description = illust.caption, color = COLOR)
		embed.set_author(name = illust.user['name'], url = "https://pixiv.net/en/users/" +  str(illust.user['id']))
		embed.add_field(name = "Views", value = illust['total_view'], inline = True)
		embed.add_field(name = "Bookmarks", value = illust['total_bookmarks'], inline = True)
		with open('image.jpg', 'rb') as file:
			image = discord.File(file)
			embed.set_image(url = "attachment://image.jpg")
			await ctx.send(embed = embed, file = image)
		os.remove('image.jpg')

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			if isinstance(error.original, AttributeError):
				await ctx.send("Error: Image does not exist.")

async def setup(client):
	await client.add_cog(IllustSearch(client))
