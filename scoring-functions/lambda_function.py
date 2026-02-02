import json
import urllib.request
import urllib.error
import uuid
from typing import Optional
import os
BASE_URL = "https://agent-prod.studio.lyzr.ai"

# Scoring agent configuration
SCORING_AGENT_ID = "697b2ab3c03792e039e5ccb2"
SCORING_AGENT_API_KEY = os.getenv("SCORING_AGENT_API_KEY", "sk-default-scoringAgentAPIKey123456")



def make_request(url: str, api_key: str) -> Optional[dict]:
    """Make an authenticated GET request to the Lyzr API."""
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} for {url}: {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL Error for {url}: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None


def fetch_agent(agent_id: str, api_key: str) -> Optional[dict]:
    """Fetch a single agent's configuration."""
    url = f"{BASE_URL}/v3/agents/{agent_id}"
    return make_request(url, api_key)


def fetch_tool(tool_id: str, api_key: str) -> Optional[dict]:
    """Fetch a single tool's configuration."""
    url = f"{BASE_URL}/v3/tools/{tool_id}"
    return make_request(url, api_key)


def fetch_all_tools(api_key: str) -> list:
    """Fetch all tools for the API key."""
    url = f"{BASE_URL}/v3/tools/"
    result = make_request(url, api_key)
    if result and "tools" in result:
        return result["tools"]
    return result if isinstance(result, list) else []


def extract_agent_summary(agent: dict) -> dict:
    """Extract key fields from an agent for the tree structure."""
    return {
        "id": agent.get("_id"),
        "name": agent.get("name"),
        "description": agent.get("description"),
        "role": agent.get("agent_role"),
        "goal": agent.get("agent_goal"),
        "model": agent.get("model"),
        "provider": agent.get("provider_id"),
        "temperature": agent.get("temperature"),
        "features": agent.get("features") or [],
        "has_instructions": bool(agent.get("agent_instructions")),
        "instruction_length": len(agent.get("agent_instructions", "") or ""),
    }


def extract_tool_summary(tool_config: dict, all_tools: dict) -> dict:
    """Extract key fields from a tool config."""
    tool_name = tool_config.get("tool_name", "")
    tool_source = tool_config.get("tool_source", "")

    summary = {
        "tool_name": tool_name,
        "tool_source": tool_source,
        "action_names": tool_config.get("action_names", []),
    }

    # Try to find full tool details from all_tools
    if tool_name in all_tools:
        full_tool = all_tools[tool_name]
        if isinstance(full_tool, dict):
            summary["tool_id"] = full_tool.get("tool_id")
            if "schema" in full_tool:
                schema = full_tool["schema"]
                summary["api_title"] = schema.get("info", {}).get("title")
                summary["api_description"] = schema.get("info", {}).get("description")
                # Count endpoints
                paths = schema.get("paths", {})
                endpoint_count = sum(len(methods) for methods in paths.values())
                summary["endpoint_count"] = endpoint_count
            if "tool" in full_tool:
                summary["tool_description"] = full_tool["tool"].get("description")

    return summary


def fetch_agent_tree(
    agent_id: str,
    api_key: str,
    all_tools: dict,
    visited: set = None,
    depth: int = 0
) -> Optional[dict]:
    """Recursively fetch an agent and all its sub-agents."""
    if visited is None:
        visited = set()

    # Prevent infinite loops
    if agent_id in visited:
        return {"id": agent_id, "error": "circular_reference", "depth": depth}

    visited.add(agent_id)

    # Fetch the agent
    agent = fetch_agent(agent_id, api_key)
    if not agent:
        return {"id": agent_id, "error": "fetch_failed", "depth": depth}

    # Build the tree node
    node = {
        "agent": extract_agent_summary(agent),
        "depth": depth,
        "tools": [],
        "sub_agents": [],
        "a2a_tools": agent.get("a2a_tools", []),
    }

    # Process tool configs
    tool_configs = agent.get("tool_configs") or []
    for tc in tool_configs:
        tool_summary = extract_tool_summary(tc, all_tools)
        node["tools"].append(tool_summary)

    # Also check "tools" field directly (some agents have this)
    direct_tools = agent.get("tools") or []
    for tool in direct_tools:
        if isinstance(tool, dict):
            node["tools"].append({
                "tool_name": tool.get("name", "unknown"),
                "tool_source": "direct",
                "description": tool.get("description"),
            })
        elif isinstance(tool, str) and tool:
            node["tools"].append({
                "tool_name": tool,
                "tool_source": "direct_string",
            })

    # Recursively fetch managed agents (sub-agents)
    managed_agents = agent.get("managed_agents") or []
    for sub_agent_ref in managed_agents:
        sub_agent_id = sub_agent_ref.get("id") if isinstance(sub_agent_ref, dict) else sub_agent_ref
        if sub_agent_id:
            sub_tree = fetch_agent_tree(
                sub_agent_id,
                api_key,
                all_tools,
                visited.copy(),  # Use copy to allow same agent in different branches
                depth + 1
            )
            if sub_tree:
                # Add usage description from parent reference
                if isinstance(sub_agent_ref, dict):
                    sub_tree["usage_description"] = sub_agent_ref.get("usage_description")
                    sub_tree["reference_name"] = sub_agent_ref.get("name")
                node["sub_agents"].append(sub_tree)

    return node


def build_statistics(tree: dict) -> dict:
    """Build statistics about the agent tree."""
    stats = {
        "total_agents": 0,
        "total_tools": 0,
        "max_depth": 0,
        "models_used": set(),
        "providers_used": set(),
        "agents_with_tools": 0,
        "agents_without_instructions": 0,
        "total_instruction_chars": 0,
        "tool_sources": set(),
    }

    def traverse(node: dict):
        if not node or "error" in node:
            return

        stats["total_agents"] += 1
        stats["max_depth"] = max(stats["max_depth"], node.get("depth", 0))

        agent = node.get("agent", {})
        if agent.get("model"):
            stats["models_used"].add(agent["model"])
        if agent.get("provider"):
            stats["providers_used"].add(agent["provider"])
        if not agent.get("has_instructions"):
            stats["agents_without_instructions"] += 1
        stats["total_instruction_chars"] += agent.get("instruction_length", 0)

        tools = node.get("tools", [])
        stats["total_tools"] += len(tools)
        if tools:
            stats["agents_with_tools"] += 1
        for tool in tools:
            if tool.get("tool_source"):
                stats["tool_sources"].add(tool["tool_source"])

        for sub_agent in node.get("sub_agents", []):
            traverse(sub_agent)

    traverse(tree)

    # Convert sets to lists for JSON serialization
    stats["models_used"] = list(stats["models_used"])
    stats["providers_used"] = list(stats["providers_used"])
    stats["tool_sources"] = list(stats["tool_sources"])

    return stats


def score_agent_tree(agent_tree: dict, scoring_api_key: str = None) -> dict:
    """Send agent tree to the scoring agent and get the score breakdown."""
    api_key = scoring_api_key or SCORING_AGENT_API_KEY

    scoring_request = {
        "agent_id": SCORING_AGENT_ID,
        "session_id": str(uuid.uuid4()),
        "message": "Score this agent configuration:\n\n" + json.dumps(agent_tree, indent=2)
    }

    req = urllib.request.Request(
        f"{BASE_URL}/v3/inference/chat/",
        data=json.dumps(scoring_request).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

            # Parse the scoring response
            response_text = result.get("response", "")

            # Try to extract JSON from the response
            try:
                # The response might be a JSON string
                score_data = json.loads(response_text)
                return {
                    "success": True,
                    "score": score_data.get("aggregated", {}).get("mean_score"),
                    "summary": score_data.get("aggregated", {}).get("summary"),
                    "breakdown": score_data
                }
            except json.JSONDecodeError:
                # If not valid JSON, return the raw response
                return {
                    "success": True,
                    "raw_response": response_text
                }

    except urllib.error.HTTPError as e:
        print(f"Scoring HTTP Error {e.code}: {e.reason}")
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        print(f"Scoring URL Error: {e.reason}")
        return {"success": False, "error": str(e.reason)}
    except Exception as e:
        print(f"Scoring Error: {str(e)}")
        return {"success": False, "error": str(e)}


def format_tree_display(tree: dict, indent: str = "") -> str:
    """Format the tree for human-readable display."""
    if not tree:
        return ""

    lines = []
    agent = tree.get("agent", {})

    # Agent header
    name = agent.get("name", "Unknown")
    model = agent.get("model", "N/A")
    lines.append(f"{indent}[Agent] {name}")
    lines.append(f"{indent}  Model: {model}")
    lines.append(f"{indent}  ID: {agent.get('id', 'N/A')}")

    if agent.get("role"):
        role = agent["role"][:100] + "..." if len(agent.get("role", "")) > 100 else agent.get("role", "")
        lines.append(f"{indent}  Role: {role}")

    # Tools
    tools = tree.get("tools", [])
    if tools:
        lines.append(f"{indent}  Tools ({len(tools)}):")
        for tool in tools:
            tool_name = tool.get("tool_name", "Unknown")
            source = tool.get("tool_source", "")
            lines.append(f"{indent}    - {tool_name} ({source})")

    # Sub-agents
    sub_agents = tree.get("sub_agents", [])
    if sub_agents:
        lines.append(f"{indent}  Sub-Agents ({len(sub_agents)}):")
        for sub in sub_agents:
            sub_display = format_tree_display(sub, indent + "    ")
            lines.append(sub_display)

    return "\n".join(lines)


def lambda_handler(event, context):
    """
    Lambda handler to recursively fetch agent configurations and score them.

    Expected input (via event body or query parameters):
    - agent_id: The root agent ID to start from
    - api_key: The Lyzr API key for authentication
    - skip_scoring: (optional) Set to true to skip scoring
    - scoring_api_key: (optional) Override the scoring agent API key

    Returns:
    - agent_tree: Complete tree of agents and sub-agents with their configs
    - statistics: Summary statistics about the agent hierarchy
    - display_tree: Human-readable tree representation
    - scoring: Score and breakdown from the scoring agent
    """
    # Parse input
    if isinstance(event.get("body"), str):
        body = json.loads(event.get("body", "{}"))
    else:
        body = event.get("body") or event

    # Support both body and query parameters
    query_params = event.get("queryStringParameters") or {}

    agent_id = body.get("agent_id") or query_params.get("agent_id")
    api_key = body.get("api_key") or query_params.get("api_key")
    skip_scoring = body.get("skip_scoring", False) or query_params.get("skip_scoring") == "true"
    scoring_api_key = body.get("scoring_api_key") or query_params.get("scoring_api_key")

    # Validation
    if not agent_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "agent_id is required"})
        }

    if not api_key:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "api_key is required"})
        }

    try:
        # Fetch all tools first for enrichment
        print(f"Fetching all tools for API key...")
        all_tools_list = fetch_all_tools(api_key)

        # Index tools by tool_id for easy lookup
        all_tools = {}
        for tool in all_tools_list:
            if isinstance(tool, dict):
                tool_id = tool.get("tool_id", "")
                all_tools[tool_id] = tool
                # Also index by partial name for matching
                if "-" in tool_id:
                    parts = tool_id.split("-")
                    if len(parts) >= 2:
                        all_tools["-".join(parts[1:])] = tool

        print(f"Indexed {len(all_tools)} tools")

        # Recursively fetch the agent tree
        print(f"Fetching agent tree starting from {agent_id}...")
        agent_tree = fetch_agent_tree(agent_id, api_key, all_tools)

        if not agent_tree:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Agent {agent_id} not found"})
            }

        # Build statistics
        statistics = build_statistics(agent_tree)

        # Format display tree
        display_tree = format_tree_display(agent_tree)

        # Score the agent tree
        scoring_result = None
        if not skip_scoring:
            print("Scoring agent tree...")
            scoring_result = score_agent_tree(agent_tree, scoring_api_key)
            print(f"Scoring complete: {scoring_result.get('summary', 'N/A')}")

        # Build response with score first
        response_data = {}

        # Add scoring at the top if available
        if scoring_result:
            breakdown = scoring_result.get("breakdown", {})
            inner_breakdown = breakdown.get("breakdown", {})

            response_data["score"] = inner_breakdown.get("score") or breakdown.get("score")
            response_data["breakdown"] = {
                "architecture": inner_breakdown.get("architecture"),
                "tools": inner_breakdown.get("tools"),
                "knowledge": inner_breakdown.get("knowledge"),
                "quality": inner_breakdown.get("quality")
            }
            if inner_breakdown.get("debug"):
                response_data["debug"] = inner_breakdown.get("debug")

        # Add the rest of the data
        response_data["statistics"] = statistics
        response_data["agent_tree"] = agent_tree
        response_data["display_tree"] = display_tree
        response_data["tools_available"] = len(all_tools_list)

        return {
            "statusCode": 200,
            "body": json.dumps(response_data, indent=2)
        }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# For local testing
if __name__ == "__main__":
    test_event = {
        "agent_id": "68d0f0449856bad60bbe6945",
        "api_key": SCORING_AGENT_API_KEY,
    }
    result = lambda_handler(test_event, None)
    print(result["body"])
    
