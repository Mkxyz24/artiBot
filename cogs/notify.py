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

class Info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def notify(self,ctx,char_name):
        courses = scrape.get_courses
        await ctx.send(f'{ctx.message.author.mention} Courses available:',courses)


def setup(bot):
    bot.add_cog(Info(bot))