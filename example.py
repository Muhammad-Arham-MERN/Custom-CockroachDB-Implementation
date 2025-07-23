from agents import Agent,Runner
from SQLImplementation import CockroachDBSession
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os

load_dotenv()

# Not Needed if you have openai's api key, i dont have it so i am using gemini
model = LitellmModel(
    model="gemini/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")
)

agent = Agent(name="Assistant",model=model)

session = CockroachDBSession(session_id="First session")

runner = Runner.run_sync(agent,"What is quran",session=session)

print(runner.final_output)