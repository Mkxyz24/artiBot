import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils import scrape, send_classes_msg
import threading, asyncio



async def not_courses(bot,clientLoop):

    '''
    running the scraper on_ready
    '''
    #send embed function
    while True:
 
        courses = scrape.get_courses()
        # print(courses)
        send_fut = asyncio.run_coroutine_threadsafe(send_classes_msg.send_msg(bot,courses,None), clientLoop)
        send_fut.result()
        await asyncio.sleep(1)


def run_continuously(*params):

    #clientLoop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    task = loop.create_task(not_courses(*params))
    loop.run_until_complete(task)



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

        #not_courses(bot)

        print("starting schedule thread")

        '''
        Note from official docs threading library (https://docs.python.org/3/library/threading.html): 
        Daemon threads are abruptly stopped at shutdown.
        Their resources (such as open files, database transactions, etc.) 
        may not be released properly. If you want your threads to stop gracefully, 
        make them non-daemonic and use a suitable signalling mechanism such as an Event.
        '''
        clientLoop = asyncio.get_event_loop()
        job_thread = threading.Thread(target=run_continuously, args=(bot,clientLoop,), daemon=True)
        job_thread.start()


    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            bot.load_extension(f'cogs.{filename[:-3]}')
    
    print("running bot")
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    main()
