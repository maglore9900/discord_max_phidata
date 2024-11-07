import discord
import environ
from modules import agent
import asyncio

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
    # print(f"message: {message}")
    # print(f"message content: {message.content}")
    # print(f"client user: {client.user}")
    # print(f"client user id: {client.user.id}")
    # print(f"User mentions: {message.mentions}")
    # print(f"Role mentions: {message.role_mentions}")
    # print(f"attachments {message.attachments}")
    # Ignore messages from the bot itself
    # if message.author == client.user:
    #     return

    if client.user in message.mentions or any(role in message.role_mentions for role in message.guild.get_member(client.user.id).roles):
        print("heard")
        if len(message.attachments) > 0:
            print("found attachment")
            for attachment in message.attachments:
                await attachment.save(fp=f"./tmp/{attachment.filename}")
                attachments.append(f"{attachment.filename}")
        received_message = message.content.replace(f'<@{client.user.id}>', '').strip()
        try:
            output = await ag.invoke_agent(received_message, attachments)
            output = output.content
        except Exception as e:
            output = f"Error: {e}"

        await message.channel.send(f'{output}')

async def main():
    try:
        await client.start(TOKEN)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Shutting down...")
    finally:
        await client.close()
        print("Bot has been disconnected.")

# Run the asyncio event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Program terminated by user.")