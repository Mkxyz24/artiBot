import discord
from discord.ext import commands
import random
import sys
import os
from random import randint
import json
from utils import scrape
import io
from PIL import Image

class Noti(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def notify(self,ctx):
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

        message = await ctx.send(embed = pages[0])
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')
        def check(reaction, user):
            return user == ctx.author

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
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 3600.0, check = check)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()
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
        # await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Noti(bot))