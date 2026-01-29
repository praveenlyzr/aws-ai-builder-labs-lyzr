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

```json
{
  "agent_tree": { ... },
  "statistics": {
    "total_agents": 5,
    "total_tools": 1,
    "max_depth": 1
  },
  "scoring": {
    "score": 40,
    "summary": "Overall: 40 / 100 (40.0%)",
    "breakdown": { ... }
  }
}
```

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
