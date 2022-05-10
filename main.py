import discord
from discord.ext import commands
import os
import sys
import random
from dotenv import load_dotenv

def main():
    load_dotenv()

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if BOT_TOKEN == None:
        with open('./tokens/BOT_TOKEN.token','r') as token:
            BOT_TOKEN = token.read()

    intents = discord.Intents().all()
    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix = commands.when_mentioned_or(">"),intents=intents)


    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            bot.load_extension(f'cogs.{filename[:-3]}')
    
    # @discord_common.on_ready_event_once(bot)
    # async def init():
    #     clist_api.cache()
    #     asyncio.create_task(discord_common.presence(bot))

    # bot.add_listener(discord_common.bot_error_handler, name='on_command_error')
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    main()
