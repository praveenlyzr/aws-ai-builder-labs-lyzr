# AWS AI Builder Labs - Lyzr Agent Workshop

Build an AI-powered customer support system for AWS Pet Store using Lyzr's multi-agent architecture.

## Problem Statement

Build an AI-powered customer support system using a multi-agent architecture (manager + sub-agents). The central Support Coordinator routes inquiries to specialized sub-agents for:
- Order tracking
- Returns/refunds
- Product recommendations

Requirements:
- Casual, friendly tone
- Strict customer verification protocols
- Escalate complex cases to humans with complete conversation context
- Data privacy through agent isolation and guardrails

---

## Repository Structure

```
aws-ai-builder-labs-lyzr/
├── lab-content/           # Workshop instructions and guides
├── scoring-functions/     # Lambda function for agent scoring API
├── scoring-agent/         # Scoring agent configuration
├── scoring metrics/       # Scoring criteria documentation
└── raw results/           # Sample scoring outputs
```

---

## Quick Links

### Workshop Content
| Document | Description |
|----------|-------------|
| [Lab Overview](./lab-content/README.md) | Main workshop instructions |
| [Agent Configuration](./lab-content/1-agent-config.md) | How to configure agents |
| [Architecture Plan](./lab-content/2-architecture-plan.md) | Multi-agent architecture design |
| [Agent Usage](./lab-content/3-agent-usage.md) | Using agents effectively |
| [Agent Launching](./lab-content/4-agent-launching.md) | Deploying your agents |
| [Agent Hardening](./lab-content/5-agent-hardening.md) | Security and guardrails |

### Scoring System
| Document | Description |
|----------|-------------|
| [Scoring API](./scoring-functions/README.md) | API endpoint documentation |
| [Scoring Metrics](./scoring%20metrics/README.md) | Scoring criteria (0-200 points) |
| [Ideal Agent Config](./scoring%20metrics/ideal-agent-config.md) | Reference implementation |
| [Scoring Agent](./scoring-agent/README.md) | Scoring agent prompts |

---

## Scoring Overview

Agents are evaluated on a **200-point scale** across 5 categories:

| Category | Max Points | Description |
|----------|------------|-------------|
| Architecture | 25 | Multi-agent structure (manager + specialists) |
| Tools | 25 | Tool integration and attachment |
| Knowledge | 25 | Knowledge base configuration |
| Quality | 25 | End-to-end workflow coverage |
| Prompts | 100 | Prompt quality across 5 subcategories |
| **Total** | **200** | |

### Scoring API

```bash
curl -X POST "https://jitzti21x0.execute-api.us-east-1.amazonaws.com/default/fetchAgentsRecursively" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "YOUR_AGENT_ID", "api_key": "YOUR_LYZR_API_KEY"}'
```

### Sample Response

```json
{
  "score": 195,
  "breakdown": {
    "architecture": 25,
    "tools": 25,
    "knowledge": 25,
    "quality": 25,
    "prompts": 95
  }
}
```

---

## Ideal Agent Architecture

```
[Manager] Support Coordinator
├── [Specialist] Order Tracking Specialist
│   └── Tool: GetOrderStatus
├── [Specialist] Returns Specialist
│   └── Tool: create_return_request
└── [Specialist] Product Info Specialist
    └── Knowledge Base: productcatalogkb
```

### Requirements for Maximum Score

| Category | Requirement |
|----------|-------------|
| Architecture | Manager + 3 specialists with clear domain separation |
| Tools | 3+ tools distributed across agents |
| Knowledge | KB on specialist(s) only, not on manager |
| Quality | 3+ specialists covering orders, returns, products |
| Prompts | Clear role, comprehensive instructions, friendly tone, guardrails, escalation |

---

## Getting Started

1. **Set up Lyzr Account**
   - Sign up at [Lyzr Studio](https://studio.lyzr.ai/)
   - Get your API key from Account Settings

2. **Configure AWS Bedrock** (optional)
   - Deploy the CloudFormation template for Bedrock access
   - Configure models in Lyzr Studio

3. **Build Your Agents**
   - Follow the [workshop instructions](./lab-content/README.md)
   - Use the [scoring metrics](./scoring%20metrics/README.md) as a guide

4. **Test Your Score**
   - Use the scoring API to evaluate your agents
   - Aim for 200/200!

---

## Resources

- [Lyzr Documentation](https://docs.lyzr.ai/)
- [Lyzr Studio](https://studio.lyzr.ai/)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)

---

## License

See [LICENSE](./LICENSE) for details.
