import discord, random
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter

# Setting up intents for the bot
intents = discord.Intents.default()  # Getting the default settings
intents.messages = True              # Allowing the bot to process messages
intents.message_content = True       # Allowing the bot to read message content
intents.guilds = True                # Allowing the bot to work with servers (guilds)

# Creating a bot with a defined command prefix and activated intents
bot = commands.Bot(command_prefix='/', intents=intents)

# An event that is triggered when the bot is ready to run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Outputs the bot's name to the console

# The '/go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Dapatkan nama pengguna yang menggunakan perintah
    if author not in Pokemon.pokemons:  # Periksa apakah pengguna ini memiliki Pokémon 
        chance = random.randint(1, 3)  # Menghasilkan angka acak dari 1 hingga 3
        # Buat objek Pokémon tergantung pada nomor acak
        if chance == 1:
            pokemon = Pokemon(author)  # Membuat Pokémon standar
        elif chance == 2:
            pokemon = Wizard(author)  # Membuat Pokémon Wizard 
        elif chance == 3:
            pokemon = Fighter(author)  # Membuat Pokémon Fighter 
        await ctx.send(await pokemon.info())  # Mengirim informasi tentang Pokémon 
        image_url = await pokemon.show_img()  # Mendapatkan URL gambar Pokémon
        if image_url:
            embed = discord.Embed()  # Membuat pesan yang disematkan (embed)
            embed.set_image(url=image_url)  # Menyematkan gambar ke dalam pesan
            await ctx.send(embed=embed)  # Mengirim sematan dengan gambar
        else:
            await ctx.send("Gagal menampilkan gambar Pokémon.")  # Melaporkan kesalahan jika kami tidak dapat memuat gambar Pokémon 
    else:
        await ctx.send("Kamu berhasil mendapatkan Pokémon!")  # Menginformasikan kepada pengguna bahwa Pokémon telah dibuat

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mendapatkan pengguna yang disebutkan dalam pesan
    if target:  # Memeriksa apakah ada pengguna yang disebutkan
        # Memeriksa apakah yang diserang dan yang bertahan memiliki Pokémon 
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Mendapatkan Pokémon pemain bertahan
            attacker = Pokemon.pokemons[ctx.author.name]  # Mendapatkan Pokémon penyerang 
            result = await attacker.attack(enemy)  # Melakukan serangan dan mendapatkan hasilnya
            await ctx.send(result)  # Mengirimkan hasil serangan
        else:
            await ctx.send("Kedua player harus memiliki Pokémon untuk memulai pertempuran!")  # Mengumumkan bahwa setidaknya salah satu petarung tidak memiliki Pokémon 
    else:
        await ctx.send("Tentukan pengguna yang ingin Kalian serang dengan menyebut mereka.")  # Meminta untuk menyebutkan pengguna untuk menyerang

@bot.command()
async def stats(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        stat = Pokemon.pokemons[author]  # Ambil objek Pokémon pengguna
        await stat.fetch_stats()
        await ctx.send(stat.show_stats())  # Kirim status Pokémon ke Discord
    else:
        await ctx.send("Anda belum memiliki Pokémon! Gunakan /go untuk membuatnya.")

@bot.command()
async def moves(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        move = Pokemon.pokemons[author]
        await move.fetch_moves()
        await ctx.send(move.show_moves())
    else:
        await ctx.send("Anda belum memiliki Pokémon! Gunakan /go untuk membuatnya.")

@bot.command()
async def info(ctx):
    if ctx.author.name in Pokemon.pokemons:
        pok = Pokemon.pokemons[ctx.author.name]
        await ctx.send(await pok.info())
    else:
        await ctx.send("Anda belum memiliki Pokémon! Gunakan /go untuk membuatnya.")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("Anda tidak memiliki pokemon!")

# Running the bot
bot.run(token)