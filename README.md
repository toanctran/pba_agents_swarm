# Agency Swarm

[![Framework](https://github.com/toanctran/pba_agents_swarm/blob/main/AI_AGENT_SWARM.png)]



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
agency.demo_gradio(height=900)
```

or get completion from the agency:

```python
agency.get_completion("Please create a new website for our client.")
```

## Creating Agent Templates Locally (CLI)

This CLI command simplifies the process of creating a structured environment for each agent.

#### **Command Syntax:**

```bash
agency-swarm create-agent-template --name "AgentName" --description "Agent Description" [--path "/path/to/directory"] [--use_txt]
```

### Folder Structure

When you run the `create-agent-template` command, it creates the following folder structure for your agent:

```
/your-specified-path/
│
├── agency_manifesto.md or .txt # Agency's guiding principles (created if not exists)
└── agent_name/                 # Directory for the specific agent
    ├── agent_name.py           # The main agent class file
    ├── __init__.py             # Initializes the agent folder as a Python package
    ├── instructions.md or .txt # Instruction document for the agent
    ├── tools.py                # Tools specific to the agent
    ├── files/                  # Directory for additional resources
```

This structure ensures that each agent has its dedicated space with all necessary files to start working on its specific tasks. The `tools.py` can be customized to include tools and functionalities specific to the agent's role.

## Future Enhancements

- Asynchronous communication and task handling.
- Creation of agencies that can autonomously create other agencies.
- Inter-agency communication for a self-expanding system.

## Contributing

We welcome contributions to Agency Swarm! Please feel free to submit issues, pull requests, and suggestions to our GitHub repository.

## License

Agency Swarm is open-source and licensed under [MIT](https://opensource.org/licenses/MIT).



## Need Help?

If you require assistance in creating custom agent swarms or have any specific queries related to Agency Swarm, feel free to reach out through my website: [vrsen.ai](https://vrsen.ai)
