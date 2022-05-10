import discord
from discord.ext import commands
import os
import sys
import random
from dotenv import load_dotenv
from utils import scrape

def main():
    load_dotenv()

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if BOT_TOKEN == None:
        with open('./tokens/BOT_TOKEN.token','r') as token:
            BOT_TOKEN = token.read()

    intents = discord.Intents().all()
    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"),intents=intents)


    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')


        '''
        running the scraper on_ready
        '''
        text_channel_list=[]
        id = None
        ch_gen = bot.get_all_channels()
        for channel in ch_gen:
            if channel.name == "general":
                id = channel.id
                break
        courses = scrape.get_courses()
        #await ctx.send(f'{ctx.message.author.mention} Courses available:')
        embed=discord.Embed(
        title="Available Classes",
            description="Here are the classes available from your desired list",
            color=discord.Color.blue())
        embed.set_author(name="Arti")
        for course in courses:
            embed.add_field(name="Title", value=course['title'], inline=True)
            embed.add_field(name="Available seats", value=course['available'], inline=True)
            embed.add_field(name="total", value=course['total'], inline=True)
        embed.set_footer(text="class search: https://webapp4.asu.edu/catalog/")
        channel = bot.get_channel(id)
        await channel.send(embed=embed)
        
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            bot.load_extension(f'cogs.{filename[:-3]}')
    
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    main()
