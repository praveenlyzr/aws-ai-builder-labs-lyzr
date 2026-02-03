# AI Experimentation with Lyzr (Needs work)

[Lyzr](https://lyzr.ai) is the simplest agent framework to build ‘Secure, Safe and Responsible’ GenAI apps faster. 

lyzr is the framework, lyzr studio is a platfrom that lets you build and deploy lyzr agents.

It delivers value by acting as a focused AI agent platform that shortens the path from AI idea to production‐ready workflows for enterprises. 

It is built to help teams move from prototypes and isolated POCs into robust, orchestrated AI agents that plug into existing tools, data, and processes, especially in domains where reliability and governance really matter. This combination of speed, control, and enterprise‐grade design is where most of its practical value shows up. 🚀


# Scenario

Your mission: Build an AI-powered customer support system for AWS Pet Store using a multi-agent architecture (manager - subagents). The central Support Coordinator routes inquiries to specialized sub-agents for order tracking, returns/refunds, and product recommendations. Maintain a casual, friendly tone with strict customer verification protocols, escalate complex cases to humans with complete conversation context, and ensure data privacy through agent isolation and guardrails.


# User Stories

- As a pet parent, I want to quickly check my order status so I know exactly when my pet supplies will arrive.
- As a customer requesting a return, I want the agent to verify my order details and eligibility upfront so I can process refunds seamlessly without human delays.
- As a shopper, I want personalized product recommendations based on my pet's type, size, and preferences so I can discover the best items fast.
- As a customer facing a complex issue, I want smooth escalation to a human agent who receives my full conversation history and context. 

# Success Criteria and Score Validation?
 <!-- needs a better title -->

By the end, you'll have:

- ✅ Lyzr account hooked up and API received
- ✅ Configure Bedrock in AWS account to use Anthropic models in Lyzr workflow
- ✅ Multi-Agent Architecture Set up (Manager + Specialists)
- ✅ Tools Integration with Agents
- ✅ Knowledge Base integration
- ✅ End-to-End Workflow Quality (Retail Readiness)

Pro tip: Most of the Lambda tooling is already written for you. You just
need to consume it via lyzr studio! Don't forget to create KB in Lyzr with
the pdf files provided. Hint: Use Qdrant



# High Level Steps
## 1) Set up your Account on the Lyzr Studio

Open The  [Lyzr Studio](https://studio.lyzr.ai/) and sign in or sign up to create an account. 
1. Verify your email and complete any workspace or organization setup
prompts.
2. Open the Sidebar, on the top find my organization and click on it. this should open a menu. Click on 'Account and API Keys' and it should open a page with your API Key. 

This is how we identify you. (insert instructions for AWS usage to insert tools and kb to user's account). 

Before we proceed to the next step, from the side bar, open the Knowledge bases tab and ensure there are 2 knowledge bases present. open the tools tab and you should see 3 tools present. these tools and knowledge bases are preconfigured to simplify the the agent building experience for the intents of the workshop.

---


## 2. Configure bedrock
<!-- This was taken from shashi, attach media when possible -->

1. In Lyzr Studio, open the Models or LLM Providers section and choose the Amazon Bedrock setup option.
2. Deploy the provided CloudFormation or IAM setup template in your AWS account to create the Bedrock access role.
3. After the stack completes, copy the IAM role ARN from the stack outputs.
4. Paste the role ARN into the Bedrock configuration screen in Lyzr Studio and save the connection.
5. Select which Bedrock models (for example Anthropic Claude, Mistral, or others) should be available for your agents.

---
<!-- Next Page ?  -->
[Next Page](./1-agent-config.md)
