import discord
import config
import readimg

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.user.id)

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content == '$rate':
        await message.channel.send('Hello!')

    if "artiBot" in (user.name for user in message.mentions):
        # print("stop disturbing me biatch")
        # await message.channel.send('stop disturbing me ' + message.author.mention)
        # print(message.attachments)
        # for url in (attachment.url for attachment in message.attachments):
        #     readimg.url_to_image(url)

        for attachment in message.attachments:
            #print(attachment.content_type)
            if "image" in attachment.content_type:
                #print("found image biatch")
                print(attachment.url)
                image = readimg.url_to_image(attachment.url)

    # for user in message.mentions:
    #     print(user.name)

client.run(config.token)