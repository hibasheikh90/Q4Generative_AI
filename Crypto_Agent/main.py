import os
import requests
import chainlit as cl
from dotenv import load_dotenv
from agents import (
    function_tool,
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel
)


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


@function_tool
def get_crypto_price(symbol: str = "BTC", currency: str = "USDT") -> str:
    """
    Fetch live crypto price from Binance API.
    """
    try:
        pair = f"{symbol.upper()}{currency.upper()}"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data.get("price")

        if price:
            return f"🪙 The price of {symbol.upper()} in {currency.upper()} is ${price}"
        else:
            return f" Symbol '{symbol}' or pair '{pair}' not found."
    except Exception as e:
        return f" Error fetching price from Binance: {str(e)}"


crypto_agent = Agent(
    name="CryptoAgent",
    instructions="You are a crypto expert. When the user asks about a cryptocurrency, return its latest market price.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[get_crypto_price],
)


run_config = RunConfig(
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    model_provider=client,
    tracing_disabled=True,
)


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="👋 Welcome to the Cryptocurrency Agent!\nAsk me about any coin (e.g., `What is the price of BTC?`)."
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    try:
        result = await Runner.run(crypto_agent, message.content)
        final_output = result.final_output or " No response from agent."
    except Exception as e:
        final_output = f" Error: {str(e)}"

    await cl.Message(content=final_output).send()
    history.append({"role": "assistant", "content": final_output})
    cl.user_session.set("history", history)











