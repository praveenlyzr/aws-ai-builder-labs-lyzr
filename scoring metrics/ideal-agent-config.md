# Ideal Agent Configuration Reference

This document details the exact configuration of a 100/100 scoring Lyzr agent setup.

## Agent Tree Overview

```
[Agent] Support Coordinator (Manager)
  Model: gpt-4.1
  ID: 69735635a75ef8a94cc48694
  Role: Customer Support Coordinator
  Tools (1):
    - EscalationTool (custom_api)
  Sub-Agents (3):
    [Agent] Order Tracking Specialist
      Model: gpt-4.1
      ID: 697355d01b6268d7b9512ae2
      Role: Order Status Expert
      Tools (1):
        - GetOrderStatus (custom_api)
    [Agent] Returns Specialist
      Model: gpt-4.1
      ID: 697355efa75ef8a94cc4861d
      Role: Returns and Refunds Specialist
      Tools (1):
        - create_return_request (custom_api)
    [Agent] Product Info Specialist
      Model: gpt-4.1
      ID: 6973560d1b6268d7b9512b29
      Role: Product Recommendation Expert
      Knowledge Base: productcatalogkbjn3q
```

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Agents | 4 |
| Total Tools | 3 |
| Max Depth | 1 |
| Models Used | gpt-4.1 |
| Provider | OpenAI |
| Agents with Tools | 3 |
| Total Instruction Chars | 10,480 |

---

## Agent 1: Support Coordinator (Manager)

### Configuration
| Field | Value |
|-------|-------|
| Name | Support Coordinator |
| Role | Customer Support Coordinator |
| Model | gpt-4.1 |
| Provider | OpenAI |
| Temperature | 0.4 |
| Instruction Length | 1,717 chars |

### Description
```
Routes customer inquiries to appropriate specialist agents, maintains casual
friendly conversation tone, aggregates responses, handles escalation to human
agents with full context when edge cases detected
```

### Goal
```
Provide seamless customer support by routing inquiries to specialist agents
and delivering friendly, helpful responses
```

### Features
```json
[
  {
    "type": "MEMORY",
    "config": {
      "max_messages_context_count": 10
    }
  },
  {
    "type": "TOOL_CALLING",
    "config": {
      "max_tries": 3
    }
  }
]
```

### Tools Attached
| Tool Name | Source | Actions |
|-----------|--------|---------|
| EscalationTool | custom_api | escalate_to_human |

---

## Agent 2: Order Tracking Specialist

### Configuration
| Field | Value |
|-------|-------|
| Name | Order Tracking Specialist |
| Role | Order Status Expert |
| Model | gpt-4.1 |
| Provider | OpenAI |
| Temperature | 0.3 |
| Instruction Length | 1,332 chars |

### Description
```
Handles all order status inquiries, provides tracking information, shipping
details, and estimated delivery dates. Never promises specific dates without
real-time carrier data
```

### Goal
```
Provide accurate order tracking information and shipping details to customers
```

### Usage Description (How Manager Routes to This Agent)
```
Delegate all order status, tracking, and shipping inquiries to this agent.
Use when customers ask 'Where is my order?', 'When will it arrive?', or
request tracking information.
```

### Features
```json
[
  {
    "type": "TOOL_CALLING",
    "config": {
      "max_tries": 3
    }
  }
]
```

### Tools Attached
| Tool Name | Source | Actions |
|-----------|--------|---------|
| GetOrderStatus | custom_api | get_order_status |

---

## Agent 3: Returns Specialist

### Configuration
| Field | Value |
|-------|-------|
| Name | Returns Specialist |
| Role | Returns and Refunds Specialist |
| Model | gpt-4.1 |
| Provider | OpenAI |
| Temperature | 0.3 |
| Instruction Length | 6,012 chars |

### Description
```
Processes return requests, checks eligibility based on returns and shipping
policy, initiates return workflows. Always verifies order details before
processing any return or refund
```

### Goal
```
Process customer return requests, verify eligibility against return policies,
collect necessary information, and initiate return workflows when approved
```

### Usage Description (How Manager Routes to This Agent)
```
Delegate all return and refund requests to this agent. Use when customers
want to return products, request refunds, or ask about return eligibility
and policies.
```

### Features
```json
[]
```
*Note: No additional features needed as this agent focuses on tool execution*

### Tools Attached
| Tool Name | Source | Actions |
|-----------|--------|---------|
| create_return_request | custom_api | CREATE_RETURN |

---

## Agent 4: Product Info Specialist

### Configuration
| Field | Value |
|-------|-------|
| Name | Product Info Specialist |
| Role | Product Recommendation Expert |
| Model | gpt-4.1 |
| Provider | OpenAI |
| Temperature | 0.5 |
| Instruction Length | 1,419 chars |

### Description
```
Provides product information and recommendations from catalog. Always asks
about pet type and size before making recommendations to ensure suitability
```

### Goal
```
Help customers find the perfect products for their pets through personalized
recommendations
```

### Usage Description (How Manager Routes to This Agent)
```
Delegate product questions and recommendation requests to this agent. Use
when customers ask about product details, need recommendations for their
pets, or inquire about product availability.
```

### Features (Knowledge Base Configuration)
```json
[
  {
    "type": "KNOWLEDGE_BASE",
    "config": {
      "lyzr_rag": {
        "base_url": "https://rag-prod.studio.lyzr.ai",
        "rag_id": "697355ff115a3970d17427b5",
        "rag_name": "productcatalogkbjn3q",
        "params": {
          "top_k": 5,
          "retrieval_type": "basic",
          "score_threshold": 0
        }
      },
      "agentic_rag": []
    }
  }
]
```

### Knowledge Base Details
| Field | Value |
|-------|-------|
| RAG Name | productcatalogkbjn3q |
| RAG ID | 697355ff115a3970d17427b5 |
| Top K | 5 |
| Retrieval Type | basic |

---

## Score Breakdown

| Category | Score | Reason |
|----------|-------|--------|
| Architecture | 25/25 | Manager + 3 specialists with clear domain separation |
| Tools | 25/25 | 3 tools (EscalationTool, GetOrderStatus, create_return_request) |
| Knowledge | 25/25 | KB on specialist only (Product Info), not on manager |
| Quality | 25/25 | 3 specialists covering orders, returns, and products |
| **Total** | **100/100** | |

---

## Key Success Factors

1. **Clear Separation of Concerns**
   - Manager handles routing and escalation only
   - Each specialist owns one domain completely

2. **Appropriate Tool Placement**
   - Domain-specific tools on specialists
   - Utility tools (escalation) on manager

3. **Knowledge Base Architecture**
   - KB on specialist (Product Info), not on manager
   - This is the ideal pattern for knowledge grounding

4. **Comprehensive Workflow Coverage**
   - Order tracking flow
   - Returns/refunds flow
   - Product recommendations flow

5. **Well-Defined Usage Descriptions**
   - Clear routing instructions for the manager
   - Specific trigger phrases mentioned
