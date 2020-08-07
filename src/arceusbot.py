import configparser
import discord
import os
import json
import random

from enum import Enum
from math import floor

CUR_DIR = os.getcwd()
config = configparser.ConfigParser()
config.read(f'{CUR_DIR}/config.ini')

client = discord.Client()

class PokemonGen(Enum):
    """
    A class containing Enums for the various pokemon generations to
    provide a single source of truth for generations.

    Attributes
    ----------
    GEN1 : Enum
        enum for generation I
    GEN2 : Enum
        enum for generation II
    GEN3 : Enum
        enum for generation II
    GEN4 : Enum
        enum for generation IV
    GEN5 : Enum
        enum for generation V
    GEN6 : Enum
        enum for generation VI
    GEN7 : Enum
        enum for generation VII
    GEN8 : Enum
        enum for generation VIII
    """

    GEN1 = 1
    GEN2 = 2
    GEN3 = 3
    GEN4 = 4
    GEN5 = 5
    GEN6 = 6
    GEN7 = 7
    GEN8 = 8

def get_rand_pokemon():
    """
    Function used to grab random pokemon from random generation

    Parameters
    ----------

    Returns
    -------
    pokemon
    a string of the name of the randomly selected pokemon
    """

    gen = random.randint(1, 8)
    with open('pokemon.json', 'r') as pokemon:
        pokemonGenList = json.load(pokemon)[PokemonGen(gen).name]
        
    pokemonIndex = random.randint(0, len(pokemonGenList))

    return pokemonGenList[pokemonIndex]

def replace_chars(pokemon):
    """
    Function used to replace a random number of characters in the pokemon's
    name w/ '_'. Minimum number of chars replaced is 2 and the max is N,
    where N is equal to the floor of 2/3 the length of the pokemon's name

    Parameters
    ----------
    pokemon : str
        the pokemon's name

    Returns
    -------
    replaced_pokemon
        the pokemon's name with some characters replaced with '_'
    """

    num_replace = random.randint(2, floor(len(pokemon) * .67))
    possible_chars = []

    for char in range(len(pokemon)):
        possible_chars.append(char)

    chars_to_replace = random.sample(possible_chars, num_replace)

    replaced_pokemon = ""

    for char in range(len(pokemon)):
        if char in chars_to_replace:
            replaced_pokemon += "_"
        else:
            replaced_pokemon += pokemon[char]

    return replaced_pokemon

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
        await message.channel.send(f"Summoned a {pokemon}")
        puzzle_name = replace_chars(pokemon)
        print(puzzle_name)
        await message.channel.send("Summoned a "+puzzle_name)


client.run(config['AUTH']['token'])