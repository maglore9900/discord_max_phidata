from modules import agent, adapter
import environ
import asyncio
env = environ.Env()
environ.Env.read_env()

ag = agent.Agents(env)

loop = asyncio.get_event_loop()

# ag.websearch_agent.print_response("what is happening paris?")
async def test():
    # result = await ag.invoke_agent("save this file to the datastore.", "blah.txt")
    result = await ag.invoke_agent("what is the first line in blah.txt?")
    print(result.content)
    
loop.run_until_complete(test())

# ad = adapter.Adapter(env)

# ad.add_to_datastore("test.txt")
# print(ad.query_datastore("what is the first line in test.txt?"))
