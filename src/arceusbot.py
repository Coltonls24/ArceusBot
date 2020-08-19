import configparser
import discord
import os

from pokemonGen import PokemonSpawner

CUR_DIR = os.getcwd()
config = configparser.ConfigParser()
config.read(f'{CUR_DIR}/config.ini')

client = discord.Client()
spawner = PokemonSpawner(config)

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
        pokemon = spawner.get_rand_pokemon()
        pokemon_img, success = spawner.fetch_pokemon_image(pokemon)
        if success:
            await message.channel.send("Who's that pokemon?!", file=discord.File(pokemon_img, "Pokemon.png"))
    else:
        spawner.auto_spawn_pokemon()


client.run(config['AUTH']['token'])