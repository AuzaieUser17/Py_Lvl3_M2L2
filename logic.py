import aiohttp  # A library for asynchronous HTTP requests
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    stats = {}
    types = {}
    abilities = {}
    moves = {}

    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer, stat_pokemon=None, type_pokemon=None, ability_pokemon=None, pokemon_move=None):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1010)
        self.name = None
        self.hp = random.randint(200, 400)
        self.power = random.randint(30, 60)
        self.stats = {}
        self.types = {}
        self.abilities = {}
        self.moves = {}
        self.last_feed_time = datetime.now()

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        elif stat_pokemon not in Pokemon.stats:
            Pokemon.stats[stat_pokemon] = self
        elif type_pokemon not in Pokemon.types:
            Pokemon.types[type_pokemon] = self
        elif ability_pokemon not in Pokemon.abilities:
            Pokemon.abilities[ability_pokemon] = self
        elif pokemon_move not in Pokemon.moves:
            Pokemon.moves[pokemon_move] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]
            self = Pokemon.stats[stat_pokemon]
            self = Pokemon.types[type_pokemon]
            self = Pokemon.abilities[ability_pokemon]
            self = Pokemon.moves[pokemon_move]

    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
        return f"Nama Pokémonmu adalah: {self.name} Kekuatan Pokémon: {self.power} HP Pokémon: {self.hp}"  # Returning the string with the Pokémon's name

    async def show_img(self):
        # An asynchronous method to get the name of a Pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request to retrieve Pokémon data
                if response.status == 200:
                    data = await response.json()  # Receiving JSON response
                    img_url = data['sprites']['front_default']  # Retrieving the URL of a Pokémon
                    return img_url  # Returning the image's URL
                else:
                    return None  # Returning None if the request fails
    
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1,5)
            if chance == 1:
                return "Pokémon Penyihir menggunakan perisai dalam pertarungan"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} melawan @{enemy.pokemon_trainer}\nHP @{enemy.pokemon_trainer} sekarang {enemy.hp}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}"
    
    async def fetch_stats(self):
        # Mengambil statistik Pokémon dari PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                    self.types = {t['type']['name'] for t in data['types']}
                    self.abilities = {ability['ability']['name'] for ability in data['abilities']}
                else:
                    self.stats = {"HP": 50, "Attack": 50, "Defense": 50, "Special Attack": 100, "Special Defense": 100, "Speed": 50}  # Default values
                    self.types = {}
                    self.abilities = {}

    async def fetch_moves(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.moves = {move['move']['name'] for move in data['moves']}
                else:
                    return "Pokémon ini tidak memiliki gerakan."
    
    def show_stats(self):
        if not isinstance(self.stats, dict) or not self.stats:  # Jika stats kosong atau bukan dictionary
            return "**Statistik belum tersedia. Gunakan perintah /stats setelah beberapa saat.**"

        stats_info = "\n".join([f"**{key}:** {value}" for key, value in self.stats.items()])
        types_info = ", ".join(self.types) if self.types else "Tidak diketahui"
        abilities_info = ", ".join(self.abilities) if self.abilities else "Tidak diketahui"
        return f"**Statistik Pokémon:**\n{stats_info}\n\n**Tipe:** {types_info}\n\n**Kemampuan:** {abilities_info}"
    
    def show_moves(self):
        if not self.moves:
            return "**Pokemon ini tidak meliki Gerakan.**"

        moves_info = ", ".join(self.moves)
        return f"**Pokemon ini bisa mempelajari Gerakan:** {moves_info}"
    
    async def feed(self, feed_interval=60, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Kesehatan pokemon meningkat. Kesehatan pokemon sekarang: {self.hp}"
        else:
            return f"Waktu makan pokemon berikutnya: {current_time+delta_time}" 

class Wizard(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPokémon Petarung menggunakan serangan super. Kekuatan yang ditambahkan adalah:{super_power}"
    
    async def feed(self):
        return await super().feed(hp_increase=20)