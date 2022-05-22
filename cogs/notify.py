import discord
from discord.ext import commands
import random
import sys
import os
from random import randint
import json
from utils import scrape,make_call,send_classes_msg
import io
from PIL import Image

class Noti(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def notify(self,ctx):
        courses = scrape.get_courses()
        

        #new one using send_classes_msg
        await send_classes_msg.send_msg(self.bot, courses,ctx)


def setup(bot):
    bot.add_cog(Noti(bot))