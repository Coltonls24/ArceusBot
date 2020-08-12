import configparser
import discord
import os

from pokemonGen import get_rand_pokemon, replace_chars, fetch_pokemon_image

CUR_DIR = os.getcwd()
config = configparser.ConfigParser()
config.read(f'{CUR_DIR}/config.ini')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$summon'):
        pokemon = get_rand_pokemon()
        pokemon_img, success = fetch_pokemon_image(pokemon)
        if success:
            await message.channel.send("Who's that pokemon?!", file=discord.File(pokemon_img, "Pokemon.png"))


client.run(config['AUTH']['token'])