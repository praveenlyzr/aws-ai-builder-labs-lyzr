# Planning the Agent Architecture

Break down the given use case into sub problems and assign specialized sub agents with unique abilities to offload effort and cognition of the manager (primary) agent. 

(Here the sub problems could be: order tracking, returns processing, and product information support.)

1. Design three specialized sub-agents: Order Tracking, Returns, and Product Info, each with a single, clear responsibility.
2. Add the Relevant tools and Knowledge Bases to the Sub Agents. Map the Tool/Knowledge Base usage in the instructions.
3. Add a Manager Agent that receives all user queries and routes to the appropriate sub-agent based on intent. 
4. Attach the Sub Agents with a simple instruction to instruct the Manager agent on How/When to use the Sub Agent.
5. Decide when the Manager should chain agents (for example: verify customer, then track order, then initiate return) in the Agent Instructions.

Hints:
- Tools: Order Tracking → Order Lambda tool, Returns → Returns Lambda tool, Product Info → product catalog.
- Knowledge Base: Product Info and Returns agents should reference the KB for policies and product details.
---


## 4. Adding Tools to the Agent (potentially removed)
<!-- Talk to shashi, will tools be made and pushed automatically using the api key or users have to copy paste? -->

1. Identify the Lambda functions that will act as tools, for example: Order Service (order status) and Returns Service (create return).
2. In Lyzr Studio, open the Tools or Integrations area and add a new tool for each Lambda-based endpoint.
3. Configure each tool with its invocation method (API Gateway URL or direct Lambda integration) and authentication details at a high level.
4. Write a brief natural-language description for each tool so agents know when to call it (for example: “Use this to fetch live order status by order ID”).
5. Decide which agents will be allowed to call which tools and note this for the agent configuration step.

## 5. Adding Knowledge Bases to the Agent (potentially removed)

1. Open the Knowledge Base section in Lyzr Studio and create a new KB for your ecommerce product and policy content.
2. Choose your data sources at a high level (for example: uploaded PDFs, product catalog exports, help center pages, or FAQs).


---
[Next Page: Architecture plan](./3-agent-usage.md)