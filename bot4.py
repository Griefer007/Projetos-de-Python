import discord
from random import choice
from discord.ext import commands

import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def pokemon(ctx, pokename):
    url = 'https://pokeapi.co/api/v2/pokemon/' + pokename + '/'

    res = requests.get(url)

    data = res.json()

    pokemon_image = data["sprites"]['front_default']

    await ctx.send(f"{pokemon_image}")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá eu sou um bot {bot.user}!')

    
bot.run("TOKEN")
