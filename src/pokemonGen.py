import configparser
import json
import os
import logging
import random
import requests
import time

from Classes.Pokemon import Pokemon
from enum import Enum
from io import BytesIO
from math import floor

# logging.basicConfig(level=logging.DEBUG)

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

class PokemonSpawner:
    def __init__(self, config):
        self.message_count = 0
        self.spawn_queue = []
        self.config = config

    def get_rand_pokemon(self):
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

    def replace_chars(self, pokemon):
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
                replaced_pokemon += "-"
            else:
                replaced_pokemon += pokemon[char]

        return replaced_pokemon

    def fetch_pokemon_image(self, pokemon_name):
        pokemon_res = requests.get(self.config['DEFAULT']['imageURL']+pokemon_name.lower())
        if pokemon_res.status_code == 200:
            pokemon = Pokemon(pokemon_res.json())
            response = requests.get(pokemon.sprite)
            return BytesIO(response.content), True
        else:   
            logging.error(f"Pokemon causing issues: {pokemon_name}")
            return None, False

    def auto_spawn_pokemon(self):
        self.message_count += 1
        if  self.message_count >= int(self.config["DEFAULT"]["messageThreshold"]):
            self.message_count = 0
            if len(self.spawn_queue) < int(self.config["DEFAULT"]["queueSize"]):
                self.spawn_queue.append(self.get_rand_pokemon())
        else:
            print("+1")
