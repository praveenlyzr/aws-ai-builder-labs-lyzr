## How do we Create and Configure a Lyzr Agent on The Lyzr Studio

From the sidebar, go to the ['Agents'](https://studio.lyzr.ai/agent-builder) page and create a new agent using the Create Agent button. This will prompt you with the various types of agents and workflows you can build on Lyzr. We will kick things off with a single agent.

There are essentially 3 main parts to how an agent functions. 
1. The Role -> Who it aims to be? 
2. The Goal -> What problem does it solve?
3. The Instructions -> How does it solve it?

To boost the functionality of the agent we have many features surrounding the build area that you can explore. Some features that we will be exploring today are:

1. Memory -> Helps the agent keep track of context between interactions.
2. Knowledge Bases -> Enables the agent to access an external knowledge base to ground answers with relevent information.
3. Tools -> Helps perform real world actions throuh API calls.

Since Lyzr Agents are autonomous in nature, use natural language instructions to use the attached features in the Agent Instructions.

### Memory

To configure an agent with memory, click on the memory toggle from the mid section of the build page. Once enabled, an option to configure it will be enabled. Clicking this opens a diaglogue box letting you choose the Memory Provider and the amount of messages it keeps in context before summarizing it.

More documentation on Memory can be found [here](https://docs.lyzr.ai/agent-lab/agent%20features/memory). Here's a [Quick Video Guide](https://www.youtube.com/watch?v=uIeLSSKP94s) explaining how it works!

### Tools

To configure an agent with a tool, click on the '+Add button' and it will prompt with a dialogue box with an option to select a tool. click the drop down button to select your desired tool. and click connect. 

If you do not see your tool here, click on the refresh button next to the drop down and try again. If you still do not see it. Open the [tools](https://studio.lyzr.ai/configure/tools) page and see if it was properly configured.

More documentation on Tools can be found [here](https://docs.lyzr.ai/agent-lab/tools/tools%20overview). Docs to Live Endpoints can found [here](https://docs.lyzr.ai/agent-lab/tools/api/Get%20User%20Tools)

### Knowledge Bases

To configure an agent with a knowledge base, click on the Knowledge Base toggle from the mid section of the build page and it will prompt you with a diaglogue box with an option to select a Knowledge Base. Select your desired Knowledge Base and configure it with the 'Number of Chunks', the 'Retrieval Type' and the minimum similariy Score Threshold you need.

If you do not see your knowledge base here, click on the refresh button next to the drop down and try again. If you still do not see it. Open the [Knowledge Bases](https://studio.lyzr.ai/knowledge-base) page and see if it was properly configured.

More documentation on Knowledge Bases can be found [here](https://docs.lyzr.ai/agent-lab/knowledgebase/introduction). Docs to Live Endpoints can found [here](https://docs.lyzr.ai/agent-lab/knowledgebase/api/Create%20RAG). Here's a [Detailed Walkthrough Video](https://www.youtube.com/watch?v=uYr0tyluWQ4) explaining how it works!

---
[Next Page: Architecture plan](./2-architecture-plan.md)