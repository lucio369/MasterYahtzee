import os, discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('{} has connected to Discord!'.format(client.user))
    
client.run(TOKEN)