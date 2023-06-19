import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
user_filename = 'subscribed_users.env'
subscribed_users = set()

try: 
    with open(user_filename, 'r') as f:
        for line in f:
            subscribed_users.add(int(line.strip()))
except FileNotFoundError:
    with open(user_filename, 'w') as f:
        pass

@bot.command()
async def subscribe(ctx):
    user_id = ctx.message.author.id
    subscribed_users.add(user_id)
    await ctx.send(f'You have been subscribed to weather updates.')
    with open(user_filename, 'a') as f:
        f.write(f'{user_id}\n')

@bot.command()
async def unsubscribe(ctx):
    user_id = ctx.message.author.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        await ctx.send(f'You have been unsubscribed from weather updates.')
    else:
        await ctx.send(f'You are not currently subscribed to weather updates.')

def get_weather():
    return "Weather data"

@tasks.loop(seconds=60)
async def send_weather_updates():
    weather_data = get_weather()
    for user_id in subscribed_users:
        user = await bot.fetch_user(user_id)
        await user.send(weather_data)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.event
async def on_ready():
    send_weather_updates.start()
    print(f'{bot.user.name} has connected to Discord!')

bot.run(os.getenv('DISCORD_TOKEN'))
