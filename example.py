from agents import Agent,Runner
from SQLImplementation import CockroachDBSession

agent = Agent(name="Assistant")

session = CockroachDBSession(session_id="First session")

runner = Runner.run(agent,"hi",session=session)