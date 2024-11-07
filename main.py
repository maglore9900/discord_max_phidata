import discord
import environ
from modules import agent

env = environ.Env()
environ.Env.read_env()
TOKEN = env('DISCORD_TOKEN')
ag = agent.Agents(env)


# Initialize the client (your bot)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Define a command prefix, for example, '!'
command_prefix = '!'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@client.event
async def on_message(message):
    attachments = []
    print(f"message: {message}")
    print(f"message content: {message.content}")
    print(f"client user: {client.user}")
    print(f"client user id: {client.user.id}")
    # Ignore messages from the bot itself
    # if message.author == client.user:
    #     return

    # Check if the bot is mentioned in the message
    # if str(client.user) in message.content or str(client.user.id) in message.content or client.user in message.mentions or client.user.id in message.mentions:
    if client.user.mentioned_in(message):
        print("heard")
        if message.attachments:
            print("found attachment")
            for attachment in message.attachments:
                await attachment.save(fp=f"./tmp/{attachment.filename}")
                attachments.append(f"{attachment.filename}")
        # Extract the message (assuming it follows the mention)
        received_message = message.content.replace(f'<@{client.user.id}>', '').strip()
        # Execute command on the server
        try:
            # output = f"Here is your command {received_message}"
            output = await ag.invoke_agent(received_message, attachments)
            output = output.content
        except Exception as e:
            output = f"Error: {e}"

        await message.channel.send(f'{output}')

client.run(TOKEN)