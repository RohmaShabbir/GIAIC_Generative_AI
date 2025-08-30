import asyncio
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()

set_tracing_disabled(disabled=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client : AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Defune a simple context using a dataclass
@dataclass
class UserInfo:
    name: str
    u_id: int

# A tool function that access local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"User {wrapper.context.name} is 47 year old"

async def main():
    # Create your context object
    user_info = UserInfo(name="John", u_id=123)

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](
        name="Assistant",
        tools=[fetch_user_age],
        model=model,
    )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())