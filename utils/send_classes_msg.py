from utils import make_call
import discord
import asyncio


async def send_msg(bot, courses, ctx):

    #get channel id

    author = None
    id = None
    if ctx == None:
        ch_gen = bot.get_all_channels()
        for channel in ch_gen:
            if channel.name == "":
                id = channel.id
                break
        ctx = bot.get_channel(id)
    else:
        author = ctx.author
    

    #send embed
    no_of_courses = len(courses)
    pages = []
    phone_nums = ['NUM_1','NUM_4']
    if(no_of_courses!=0):
        try:
            make_call.make_call(phone_nums, courses) 
            #make a call to the specified numbers
        except:
            pass
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
        first_page_emoji = "\U000023EE"
        await message.add_reaction(first_page_emoji)
        previous_page_emoji = '\U000025C0'
        await message.add_reaction(previous_page_emoji)
        next_page_emoji = '\U000025B6'
        await message.add_reaction(next_page_emoji)
        last_page_emoji = '\U000023ED'
        await message.add_reaction(last_page_emoji)

        def check(reaction, user):
            if(author!=None):
                return user == ctx.author
            return True

        i = 0
        #reaction = None

        while True:
            
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout = 60.0, check = check)
                if str(reaction) == r'\U000023EE':
                    i = 0
                    await message.edit(embed = pages[i])

                elif str(reaction) == r'\U000025C0':
                    if i > 0:
                        i -= 1
                        await message.edit(embed = pages[i])
                    
                elif str(reaction) == r'\U000025B6':
                    if i < int(no_of_courses/5):
                        i += 1
                        await message.edit(embed = pages[i])
                  
                elif str(reaction) == r'\U000023ED':
                    i = int(no_of_courses/5)
                    await message.edit(embed = pages[i])

                if(bot.user.id != user.id):
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.clear_reactions()
                break
