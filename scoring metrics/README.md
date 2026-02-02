# Lyzr Agent Scoring Metrics

This document outlines the scoring criteria used to evaluate Lyzr agents. Agents are scored across four categories, each worth up to 25 points, for a maximum total score of 100.

## Scoring Foundations

### T-Shirt Size to Points Mapping

| T-Shirt Size | Points |
|--------------|--------|
| XS | 5 |
| S | 10 |
| M | 15 |
| L | 20 |
| XL | 25 |

### Score Output Format

```json
{
  "score": 100,
  "breakdown": {
    "architecture": 25,
    "tools": 25,
    "knowledge": 25,
    "quality": 25
  }
}
```

---

## Step 1: Multi-Agent Architecture (25 points)

Evaluates the clarity and ownership of the multi-agent structure.

| Level | Points | Criteria |
|-------|--------|----------|
| XS | 5 | Single agent only (no sub-agents) |
| S | 10 | Manager + sub-agents exist but roles or boundaries are unclear in config or prompts |
| M | 15 | Clear domain split documented (e.g., orders, returns, product info) but routing incomplete |
| L | 20 | Correct routing logic present and minimal role overlap |
| **XL** | **25** | Manager + 2 or more specialists with clear domain separation. Manager may have utility tools like escalation |

---

## Step 2: Tools Integration (25 points)

Counts usable tools and validates mapping to agents.

| Level | Points | Criteria |
|-------|--------|----------|
| S | 10 | No tools integrated |
| M | 15 | 1 tool integrated |
| L | 20 | 2 tools integrated |
| **XL** | **25** | 3 or more tools integrated across the agent tree |

---

## Step 3: Knowledge Base (25 points)

Evaluates knowledge base creation and correct usage.

| Level | Points | Criteria |
|-------|--------|----------|
| S | 10 | No Knowledge Base attached |
| M | 15 | KB attached only to the manager |
| L | 20 | KB attached to manager AND specialist(s) |
| **XL** | **25** | KB attached to specialist(s) only, NOT on manager. This is the ideal architecture |

---

## Step 4: End-to-End Workflow Quality (25 points)

Evaluates workflow coverage and retail readiness.

| Level | Points | Criteria |
|-------|--------|----------|
| S | 10 | Workflow does not function end-to-end per config evidence |
| M | 15 | Works for one scenario only |
| L | 20 | Supports 2 of the 3 core flows (order, returns, product info) |
| **XL** | **25** | Has 3 or more sub-agents/specialists covering different domains |

---

## Evidence Evaluated

The scoring agent extracts and evaluates the following evidence from agent configurations:

- Presence of `sub_agents` or `children` entries
- Manager or orchestrator flags
- Explicit routing logic
- `tools` or `integrations` lists
- `knowledge_bases` attached
- References to test flows or workflows
- Escalation configs
- API/auth references
- Documented tool invocation examples in prompts or handlers

---

## Maximum Score Requirements

To achieve 100/100, an agent configuration must have:

| Category | Requirement |
|----------|-------------|
| Architecture | Manager + 3 specialists with clear domains |
| Tools | 3+ tools distributed across agents |
| Knowledge | KB on specialist(s) only, not on manager |
| Quality | 3+ specialists covering distinct workflows |

---

## Reference Implementation

For a complete example of a 100/100 scoring agent configuration, see:

**[Ideal Agent Configuration](./ideal-agent-config.md)**

This reference includes:
- Full agent tree structure
- Exact prompts (description, goal, role) for each agent
- Tools attached to each agent
- Knowledge base configuration
- Usage descriptions for routing
- Complete statistics breakdown
