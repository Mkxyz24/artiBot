from utils import make_call
import discord
import asyncio
from datetime import datetime



def time_check(cur_time):
    #function to check if calls been made last hour
    try:
        with open('last_call.txt','r') as f:
            r = f.read()     
            print('read')
    except FileNotFoundError:
        print("file not found, creating one")
        with open('last_call.txt','w+') as f:
            f.write(cur_time)
        return True
    except:
        print("error while reading file")
        return False
    else:
        with open('last_call.txt','w+') as f:

            d1 = datetime.strptime(r, "%d:%m:%Y:%H:%M:%S")
            d2 = datetime.strptime(cur_time, "%d:%m:%Y:%H:%M:%S")
            diff = d2-d1
            diff_s = diff.total_seconds()
            diff_hours = divmod(diff_s, 3600)[0]
            #print(diff_s, diff_hours)
            f.write(cur_time)
        if (diff_hours > 1):
            return True


async def send_msg(bot, courses, ctx):

    #get channel id

    author = None
    id = None
    if ctx == None:
        ch_gen = bot.get_all_channels()
        for channel in ch_gen:
            if channel.name == "course-updates":
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
            utc_dt = datetime.utcnow()
            c_t = utc_dt.strftime(r"%d:%m:%Y:%H:%M:%S")
            if(time_check(c_t)):
                make_call.make_call(phone_nums, courses) 
                #make a call to the specified numbers
        except:
            print("error in making call")
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
