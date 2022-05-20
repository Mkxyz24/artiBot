from utils import make_call
import discord


async def send_msg(bot, courses):

    #get channel id
    text_channel_list=[]
    id = None
    ch_gen = bot.get_all_channels()
    for channel in ch_gen:
        if channel.name == "private":
            id = channel.id
            break

    #send embed
    no_of_courses = len(courses)
    pages = []
    phone_nums = ['NUM_1']
    if(no_of_courses!=0):
        make_call.make_call(phone_nums)
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
                reaction, user = await bot.wait_for('reaction_add', timeout = 60.0)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()