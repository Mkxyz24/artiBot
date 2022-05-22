# artiBot
Discord bot for regular utilities. Currently using it to scrape details for course resgistration.

## Instructions
I would suggest using a virtual environment to install required packages using pip

```
python3 -m pip install virtualenv
```

creating virtual env:

```
python3 -m venv env
```

activate using:

```
#for mac:
source env/bin/activate
#for windows:
.\env\Scripts\activate
```

install the required packages

```
pip install -r requirements.txt 
```

If you have installed any new packages, update the `requirements.txt`:
```
pip freeze > requirements.txt
```


to deactivate virtual environment after you're done:

```
deactivate
```
## What it does
The bot is mainly based on two files - `main.py` and `main.yml`
main.py sets up the bot running and uses the rest of code as utilities. It runs `bot.load_extension` method which adds the cogs to the bot from the global `setup` function.
Cogs are a way to organize a collection of commands, listeners, and some state into one class.
main.yml sets up the continuous integration workflow on github and is scheduled to run every 6 hours* to keep the bot alive. Without the schedule the workflow will be cancelled because of the maximum execution time of 360 minutes for a job.


to add new commands/features use the existing cog or create a new one and add helper functions in utils folder.



