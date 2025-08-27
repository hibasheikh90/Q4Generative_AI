# import asyncio
# import os
# from dotenv import load_dotenv
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# # Disable agent tracing
# set_tracing_disabled(disabled=True)
# load_dotenv()
# API_KEY = os.getenv("API_KEY")

# # Setup model
# BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# MODEL = "gemini-2.0-flash"  

# client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

# async def main():
#     # Define 3 Analyst Agents
#     agents = [
#         Agent(
#             name="Lyric Poetry Analyst",
#             instructions="You only analyze lyric poetry. If the poem shows personal emotions or feelings, give  explanation.",
#             handoff_description="Lyric poetry expert.",
#             model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
#         ),
#         Agent(
#             name="Narrative Poetry Analyst",
#             instructions="You only analyze narrative poetry. If the poem tells a story with characters/events, give explanation.",
#             handoff_description="Narrative poetry expert.",
#             model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
#         ),
#         Agent(
#             name="Dramatic Poetry Analyst",
#             instructions="You specialize in dramatic poetry.If the poem is not dramatic, you can still provide feedback explaining why it doesn't fit the dramatic style and what would make it one. Then give a brief analysis anyway, in English. ",
#             handoff_description="Dramatic poetry expert.",
#             model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
#         )
#     ]

#     # Input poem
#     poem = """
# I walk alone beneath the moon,  
# Thinking of a forgotten tune.  
# The wind it howls, the stars all hide,  
# As memories drift like waves and tide.  

# The night is deep, my heart feels sore,  
# I knock and knock on memory’s door.  
# No one hears, no one replies,  
# Only silence beneath the skies.
# """

#     print("📜 Poem Input:\n", poem.strip())

#     # Run all agents one by one
#     for agent in agents:
#         print(f"\n🔍 {agent.name} says:")
#         try:
#             result = await Runner.run(agent, poem)
#             print(result.final_output.strip())
#         except Exception as e:
#             print(f"❌ Error from {agent.name}: {str(e)}")


# if __name__ == "__main__":
#     asyncio.run(main())












import os
import chainlit as cl
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner  

# Load .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = "gemini-2.0-flash"  # Or "gpt-4o", "venice/uncensored:free", etc.

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

# Create poetry analysis agents
def get_agents():
    return [
        Agent(
            name="Lyric Poetry Analyst",
            instructions="You only analyze lyric poetry. If the poem shows personal emotions or feelings, give explanation.",
            handoff_description="Lyric poetry expert.",
            model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
        ),
        Agent(
            name="Narrative Poetry Analyst",
            instructions="You only analyze narrative poetry. If the poem tells a story with characters/events, give explanation.",
            handoff_description="Narrative poetry expert.",
            model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
        ),
        Agent(
            name="Dramatic Poetry Analyst",
            instructions="""You specialize in dramatic poetry. If the poem is not dramatic, you can still provide feedback explaining why it doesn't fit the dramatic style and what would make it one. Then give a brief analysis anyway, in English.""",
            handoff_description="Dramatic poetry expert.",
            model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
        )
    ]

@cl.on_message
async def analyze_poem(message: cl.Message):
    poem = message.content.strip()
    await cl.Message(content=f"📜 Poem Received:\n\n{poem}").send()

    agents = get_agents()

    for agent in agents:
        await cl.Message(content=f"🔍 **{agent.name}** is analyzing...").send()
        try:
            result = await Runner.run(agent, poem)
            await cl.Message(content=f"📝 **{agent.name} says:**\n\n{result.final_output.strip()}").send()
        except Exception as e:
            await cl.Message(content=f"❌ Error from {agent.name}:\n{str(e)}").send()
