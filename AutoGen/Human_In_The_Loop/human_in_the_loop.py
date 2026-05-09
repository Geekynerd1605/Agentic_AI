import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import os
from autogen_agentchat.ui import Console


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key)

assistant=AssistantAgent(name="Assistant", model_client=model_client, description="You are a great assistant", 
                          system_message="You are a really helpful assistant who helps on the given task.")

user_proxy_agent=UserProxyAgent(name="UserProxy", description="You are a user proxy agent", input_func=input)

termination_condition=TextMentionTermination(text="APPROVE")

team = RoundRobinGroupChat(
        participants=[assistant, user_proxy_agent], 
        termination_condition=termination_condition, 
        max_turns=10)

stream=team.run_stream(task="Write a great poem about India.")

async def main():
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())