from phi.agent import Agent
from phi.model.groq import Groq

from dotenv import load_dotenv
load_dotenv()

chef_agent = Agent(
    model=Groq(id='llama-3.3-70b-versatile'),
    tools=[],
    show_tool_calls=True,
    description="You are a recipe expart. You will be given a recipe and you have to answer the questions related to it.",
    instructions=[""],
)

def process_instruction(instruction: str) -> str:
    response = chef_agent.run(instruction, stream=False)
    return response.content

