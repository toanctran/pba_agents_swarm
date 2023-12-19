import sys

import gradio as gr

from organization_swarm import set_openai_key

sys.path.insert(0, '../agency-swarm')

from organization_swarm.organization.organization import Agency
from tests.ceo.ceo import Ceo
from tests.test_agent.test_agent import TestAgent
from tests.test_agent2.test_agent2 import TestAgent2

test_agent1 = TestAgent()
test_agent2 = TestAgent2()
ceo = Ceo()

agency = Agency([
    ceo,
    [ceo, test_agent1, test_agent2],
    [ceo, test_agent2],
], shared_instructions="./manifesto.md")


agency.demo_gradio(height=1500)

