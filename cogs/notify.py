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
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Noti(bot))