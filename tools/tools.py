# import Required Libraries
import os
from dotenv import load_dotenv
from agents import (
    Agent,                      # core agent class
    Runner,                     # Run the agent
    AsyncOpenAI,                # OpenAI_Compatibla async client 
    OpenAIChatCompletionsModel, # Chat model interface
    function_tool,              # Decurator to run puthon function into tools
    set_tracing_disabled        # Disable internal tracing/logging
    )

# Load environment variable from .env file
load_dotenv()

# Disable internal for clean output (optional for beginners)
set_tracing_disabled(disabled=True)

#  1) Environment & clean setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Get the API key from the environment variable
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/" # Base URL for the Gemini API

# Initialize the AsyncOpenAI-compatible client with Gemini details
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

# 2) Model Intialization
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# 3) Define tools (function wrapped for tool calling)
@function_tool
def multiply(a: int, b: int) -> int:
    """Exact multiplication (use this instead of guessing math)"""
    return a * b

@function_tool
def sum(a: int, b: int) -> int:
    """Exact addition(use the instead of gussing match.)"""
    return a + b

# 4) Create agent and register tools
agent: Agent = Agent(
    name="Assistant",  #  Agent's identity
    instructions=(
        "You are a helpful assistant. "
        "Always use tools for math questions. Always follow DMAS rule (division, multiplication, addition, subtraction). "
        "Explain answers clearly and briefly for beginners."
    ),
    model=model,
    tools=[multiply, sum] # Register tools here
)

prompt = input("What's the question? ")

result = Runner.run_sync(agent, prompt)

# print("\n Calling Agent...")
print(result.final_output)