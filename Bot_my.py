import discord
from discord.ext import commands
from datetime import datetime
import pytz
import os
import random
import aiohttp

TOKEN = 'MTI3MTQ5MDM3MDM1Nzk1NjY3MQ.Ghx3zP.9SIkuPNR-1wDwnuEhc7JIFOa2oJYHGW3xxIvXU'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

MEMES_DIR = 'memes'
THEMES = {
    'animals': {
        'folder': 'animals',
        'memes': [
            {'file': 'cat.jpg', 'weight': 5},
            {'file': 'dog.jpg', 'weight': 3},
            {'file': 'panda.jpg', 'weight': 2}
        ]
    },
    'general': {
        'folder': 'general',
        'memes': [
            {'file': 'funny1.jpg', 'weight': 4},
            {'file': 'funny2.jpg', 'weight': 6}
        ]
    }
}

def choose_meme(theme):
    # Получаем данные о мемах для выбранной темы
    theme_data = THEMES.get(theme)
    if not theme_data:
        return None
    
    # Собираем список мемов с учетом их веса
    memes = theme_data['memes']
    weighted_memes = []
    for meme in memes:
        weighted_memes.extend([meme['file']] * meme['weight'])
    
    # Выбираем случайный мем
    selected_meme = random.choice(weighted_memes)
    return os.path.join(MEMES_DIR, theme_data['folder'], selected_meme)

@bot.command(name='commands')
async def list_commands(ctx):
    # Создаем список всех команд
    commands_list = [f'**{command.name}**: {command.description or "No description"}' for command in bot.commands]
    
    # Форматируем и отправляем список команд
    commands_message = "\n".join(commands_list)
    await ctx.send(f"Вот список всех доступных команд:\n{commands_message}")

@bot.command(name='meme')
async def send_meme(ctx, theme='general'):
    meme_path = choose_meme(theme)
    if meme_path and os.path.isfile(meme_path):
        await ctx.send(file=discord.File(meme_path))
    else:
        await ctx.send("Не удалось найти мем для указанной темы.")


@bot.command(name='time')
async def time(ctx, timezone: str = 'UTC'):
    try:
        now = datetime.now(pytz.timezone(timezone))
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        await ctx.send(f'Текущее время в{timezone} - {current_time}')
    except Exception as e:
        await ctx.send(f'Ошибка: {str(e)}. Пожалуйста, укажите действительный часовой пояс')
@bot.command(name='coinflip')
async def coinflip(ctx):
    result = random.choice(['Орёл', 'Решка'])
    await ctx.send(f'Монетка показала: {result}')


@bot.command(name='emoji')
async def emoji(ctx):
    emojis = ['😀', '😂', '🥳', '😎', '👍', '💥', '🔥', '🎉', '🤖', '💻']
    random_emoji = random.choice(emojis)
    await ctx.send(f'Вот ваш случайный смайлик: {random_emoji}')

MEMES_FOLDER = 'BOT/images'

@bot.command(name='mem')
async def send_meme(ctx):

    memes = os.listdir(MEMES_FOLDER)
    if not memes:
        await ctx.send("Папка с мемами пуста!")
        return
    random_meme = random.choice(memes)
    meme_path = os.path.join(MEMES_FOLDER, random_meme)

    await ctx.send(file=discord.File(meme_path))
@bot.command(name='anime')
async def send_anime(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://nekos.life/api/v2/img/wallpaper') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['url']
                await ctx.send(image_url)
            else:
                await ctx.send("Не удалось получить картинку, попробуйте позже.")

@bot.event
async def on_ready():
    print(f'Вошел в систему как {bot.user}')
bot.run(TOKEN)
