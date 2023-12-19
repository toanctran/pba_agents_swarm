# Agency Swarm

![Framework](https://github.com/toanctran/pba_agents_swarm/blob/main/AI_AGENT_SWARM.png)



## Installation

```bash
pip install git+https://github.com/toanctran/pba_agents_swarm
```

## Getting Started


1. **Set Your OpenAI Key**:

```python
from orangization_swarm import set_openai_key
set_openai_key("YOUR_API_KEY")
```

2. **Create Tools**:
Define your custom tools with [Instructor](https://github.com/jxnl/instructor):
```python
from orangization_swarm.tools import BaseTool
from pydantic import Field

class MyCustomTool(BaseTool):
    """
    A brief description of what the custom tool does. 
    The docstring should clearly explain the tool's purpose and functionality.
    """

    # Define the fields with descriptions using Pydantic Field
    example_field: str = Field(
        ..., description="Description of the example field, explaining its purpose and usage."
    )

    # Additional fields as required
    # ...

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform its task.
        Doc string description is not required for this method.
        """

        # Your custom tool logic goes here
        do_something(self.example_field)

        # Return the result of the tool's operation
        return "Result of MyCustomTool operation"
```

**NEW**: Import in 1 line of code from [Langchain](https://python.langchain.com/docs/integrations/tools)
    
```python
from langchain.tools import YouTubeSearchTool
from organization_swarm.tools import ToolFactory

LangchainTool = ToolFactory.from_langchain_tool(YouTubeSearchTool)
```

or 

```python
from langchain.agents import load_tools

tools = load_tools(
    ["arxiv", "human"],
)

tools = ToolFactory.from_langchain_tools(tools)
```


3. **Define Agent Roles**: Start by defining the roles of your agents. For example, a CEO agent for managing tasks and a developer agent for executing tasks.

```python
from organization_swarm import Organization

ceo = Organization(name="CEO",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=[MyCustomTool, LangchainTool])
```

4. **Define Agency Communication Flows**: 
Establish how your agents will communicate with each other.

```python
from organization_swarm import Organization

organization = Organization([
    ceo,  # CEO will be the entry point for communication with the user
    [ceo, dev],  # CEO can initiate communication with Developer
    [ceo, va],   # CEO can initiate communication with Virtual Assistant
    [dev, va]    # Developer can initiate communication with Virtual Assistant
], shared_instructions='organization_manifesto.md') # shared instructions for all agents
```

 In Organization Swarm, communication flows are directional, meaning they are established from left to right in the organization_chart definition. For instance, in the example above, the CEO can initiate a chat with the developer (dev), and the developer can respond in this chat. However, the developer cannot initiate a chat with the CEO. The developer can initiate a chat with the virtual assistant (va) and assign new tasks.

5. **Run Demo**: 
Run the demo to see your agents in action!

```python
organization.demo_gradio(height=900)
```

or get completion from the agency:

```python
organization.get_completion("Please create a new website for our client.")
```

