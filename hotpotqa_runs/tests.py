
import joblib
from react_cls import ReactReflectAgent
from mocks import DocStoreExplorerMock, LLMMock

test_q = "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?"
test_a = "1,800 to 7,000 ft"

agent = ReactReflectAgent(test_q, test_a)

agent.run()

print(agent._build_agent_prompt())
print(agent._build_reflection_prompt())