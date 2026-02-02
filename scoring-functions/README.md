# fetchAgentsRecursively

Recursively fetches Lyzr agent configurations and scores them.

## API Endpoint

```
POST https://jitzti21x0.execute-api.us-east-1.amazonaws.com/default/fetchAgentsRecursively
```

## Request

```json
{
  "agent_id": "YOUR_AGENT_ID",
  "api_key": "YOUR_LYZR_API_KEY",
  "skip_scoring": false
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `agent_id` | Yes | Root agent ID to analyze |
| `api_key` | Yes | Lyzr API key |
| `skip_scoring` | No | Set `true` to skip scoring (faster) |

## Response

Score and breakdown appear first in the response for easy access:

```json
{
  "score": 100,
  "breakdown": {
    "architecture": 25,
    "tools": 25,
    "knowledge": 25,
    "quality": 25
  },
  "debug": "Assessment complete. All criteria satisfied...",
  "statistics": {
    "total_agents": 4,
    "total_tools": 3,
    "max_depth": 1,
    "models_used": ["gpt-4.1"],
    "providers_used": ["OpenAI"],
    "agents_with_tools": 3,
    "agents_without_instructions": 0,
    "total_instruction_chars": 10480,
    "tool_sources": ["custom_api"]
  },
  "agent_tree": {
    "agent": { ... },
    "tools": [ ... ],
    "sub_agents": [ ... ]
  },
  "display_tree": "[Agent] Support Coordinator\n  ...",
  "tools_available": 12
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `score` | Total score (0-100) |
| `breakdown` | Per-category scores (architecture, tools, knowledge, quality) |
| `debug` | Explanation of scoring decisions |
| `statistics` | Summary stats about the agent tree |
| `agent_tree` | Complete tree of agents, tools, and sub-agents |
| `display_tree` | Human-readable tree representation |
| `tools_available` | Total tools available for the API key |

## Example

```bash
curl -X POST "https://jitzti21x0.execute-api.us-east-1.amazonaws.com/default/fetchAgentsRecursively" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "68d0f0449856bad60bbe6945", "api_key": "sk-default-..."}'
```

## Testing

```bash
# Run all tests
python3 run_tests.py --skip-scoring

# Filter tests
python3 run_tests.py -f "manager" -s
```
