from modules import adapter, agent
import environ
import asyncio




env = environ.Env()
environ.Env.read_env()
TOKEN = env('DISCORD_TOKEN')
ag = agent.Agents(env)

loop = asyncio.get_event_loop()
received_message = "Tell me a joke"
attachments = []

output =  loop.run_until_complete(ag.invoke_agent(received_message, attachments))
print(output.content)