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

        #send embed function
        courses = scrape.get_courses()
        #await ctx.send(f'{ctx.message.author.mention} Courses available:')

        no_of_courses = len(courses)
        pages = []
        for i in range(no_of_courses):
            if(i%5==0):
                page = discord.Embed(
                    title='Page ' + str(int(i/5) + 1) + '/' + str(int(no_of_courses/5) + 1),
                    description="Here are the available classes from your desired list",
                    colour = discord.Colour.orange()
                )
                pages.append(page)
            pages[int(i/5)].add_field(name="Title", value=courses[i]['title'], inline=True)
            pages[int(i/5)].add_field(name="Name", value=courses[i]['name'], inline=True)
            pages[int(i/5)].add_field(name="Available seats", value=courses[i]['available'], inline=True)
            pages[int(i/5)].add_field(name="total", value=courses[i]['total'], inline=True)
            pages[int(i/5)].add_field(name="\n\u200b", value="\n\u200b", inline=False)

        channel = bot.get_channel(id)
        message = await channel.send(embed = pages[0])
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        # def check(reaction, user):
        #     return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < int(no_of_courses/5):
                    i += 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = int(no_of_courses/5)
                await message.edit(embed = pages[i])
            
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout = 300.0)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()


        # courses = scrape.get_courses()
        # #await ctx.send(f'{ctx.message.author.mention} Courses available:')
        # embed=discord.Embed(
        # title="Available Classes",
        #     description="Here are the classes available from your desired list",
        #     color=discord.Color.blue())
        # embed.set_author(name="Arti")
        # for course in courses:
        #     embed.add_field(name="Title", value=course['title'], inline=True)
        #     embed.add_field(name="Name", value=course['name'], inline=True)
        #     embed.add_field(name="Available seats", value=course['available'], inline=True)
        #     embed.add_field(name="total", value=course['total'], inline=True)
        #     embed.add_field(name="\n\u200b", value="\n\u200b", inline=False)
        # embed.set_footer(text="class search: https://webapp4.asu.edu/catalog/")
        # channel = bot.get_channel(id)
        # await channel.send(embed=embed)
        
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            bot.load_extension(f'cogs.{filename[:-3]}')
    
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    main()
