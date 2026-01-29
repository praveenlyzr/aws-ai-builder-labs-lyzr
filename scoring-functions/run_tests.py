#!/usr/bin/env python3
"""
Test runner for fetchAgentsRecursively Lambda function.
Runs all test events against the deployed API endpoint.
"""

import json
import urllib.request
import urllib.error
import sys
from pathlib import Path

# Deployed API endpoint
API_ENDPOINT = "https://jitzti21x0.execute-api.us-east-1.amazonaws.com/default/fetchAgentsRecursively"


def load_test_events(events_dir: str = "events") -> list:
    """Load all test event JSON files from the events directory."""
    events_path = Path(__file__).parent / events_dir
    test_events = []

    if not events_path.exists():
        print(f"Events directory not found: {events_path}")
        return []

    for json_file in sorted(events_path.glob("*.json")):
        try:
            with open(json_file, "r") as f:
                event = json.load(f)
                test_events.append({
                    "name": json_file.stem,
                    "file": str(json_file),
                    "event": event
                })
        except json.JSONDecodeError as e:
            print(f"Error parsing {json_file}: {e}")

    return test_events


def call_api(event: dict, timeout: int = 180) -> dict:
    """Call the deployed API endpoint with the given event."""
    req = urllib.request.Request(
        API_ENDPOINT,
        data=json.dumps(event).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.status
            body = json.loads(response.read().decode("utf-8"))
            return {"status_code": status_code, "body": body, "error": None}
    except urllib.error.HTTPError as e:
        try:
            error_body = json.loads(e.read().decode("utf-8"))
        except:
            error_body = {"error": e.reason}
        return {"status_code": e.code, "body": error_body, "error": e.reason}
    except urllib.error.URLError as e:
        return {"status_code": None, "body": None, "error": str(e.reason)}
    except Exception as e:
        return {"status_code": None, "body": None, "error": str(e)}


def run_test(test_case: dict, verbose: bool = False, timeout: int = 180) -> dict:
    """Run a single test case and return results."""
    name = test_case["name"]
    event = test_case["event"]

    result = {
        "name": name,
        "passed": False,
        "status_code": None,
        "error": None,
        "summary": None
    }

    response = call_api(event, timeout)
    result["status_code"] = response["status_code"]

    if response["error"] and not response["body"]:
        result["error"] = response["error"]
        result["summary"] = f"Request failed: {response['error']}"
        return result

    body = response["body"]

    # Check for errors in response
    if "error" in body:
        result["error"] = body["error"]
        # Error tests are expected to have errors
        if name.startswith("error_"):
            result["passed"] = True
            result["summary"] = f"Expected error: {body['error']}"
        else:
            result["summary"] = f"Unexpected error: {body['error']}"
    else:
        result["passed"] = True

        # Build summary
        stats = body.get("statistics", {})
        scoring = body.get("scoring", {})

        summary_parts = []
        if stats:
            summary_parts.append(
                f"Agents: {stats.get('total_agents', 0)}, "
                f"Tools: {stats.get('total_tools', 0)}, "
                f"Depth: {stats.get('max_depth', 0)}"
            )
        if scoring and scoring.get("success"):
            summary_parts.append(f"Score: {scoring.get('score')}/100")
        elif scoring and not scoring.get("success"):
            summary_parts.append(f"Scoring failed: {scoring.get('error', 'unknown')}")

        result["summary"] = " | ".join(summary_parts) if summary_parts else "OK"

        if verbose:
            result["full_response"] = body

    return result


def print_result(result: dict, show_details: bool = False):
    """Print a single test result."""
    status = "✅ PASS" if result["passed"] else "❌ FAIL"
    print(f"{status} | {result['name']}")
    print(f"       Status: {result['status_code']} | {result['summary']}")

    if show_details and result.get("full_response"):
        print(f"       Response: {json.dumps(result['full_response'], indent=2)[:500]}...")
    print()


def run_all_tests(
    events_dir: str = "events",
    verbose: bool = False,
    skip_scoring: bool = False,
    filter_name: str = None,
    timeout: int = 180
):
    """Run all tests and print summary."""
    print("=" * 60)
    print("fetchAgentsRecursively API Test Runner")
    print("=" * 60)
    print(f"Endpoint: {API_ENDPOINT}")
    print()

    test_events = load_test_events(events_dir)

    if not test_events:
        print("No test events found!")
        return []

    # Filter tests if specified
    if filter_name:
        test_events = [t for t in test_events if filter_name.lower() in t["name"].lower()]
        print(f"Filtered to {len(test_events)} tests matching '{filter_name}'")
        print()

    # Optionally add skip_scoring to all events
    if skip_scoring:
        print("Note: skip_scoring=True added to all tests")
        print()
        for t in test_events:
            t["event"]["skip_scoring"] = True

    print(f"Running {len(test_events)} test(s)...\n")
    print("-" * 60)

    results = []
    for test_case in test_events:
        print(f"Running: {test_case['name']}...")
        result = run_test(test_case, verbose, timeout)
        results.append(result)
        print_result(result, verbose)

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    print(f"Total:  {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        print("\nFailed tests:")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['name']}: {r['summary']}")

    print()
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Lambda test events against deployed API endpoint"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "-s", "--skip-scoring",
        action="store_true",
        help="Skip scoring for faster tests"
    )
    parser.add_argument(
        "-f", "--filter",
        type=str,
        help="Filter tests by name (case-insensitive)"
    )
    parser.add_argument(
        "-d", "--events-dir",
        type=str,
        default="events",
        help="Directory containing test events (default: events)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=180,
        help="Request timeout in seconds (default: 180)"
    )
    parser.add_argument(
        "-e", "--endpoint",
        type=str,
        help="Override API endpoint URL"
    )

    args = parser.parse_args()

    # Override endpoint if specified
    global API_ENDPOINT
    if args.endpoint:
        API_ENDPOINT = args.endpoint
        print(f"Using custom endpoint: {API_ENDPOINT}")

    results = run_all_tests(
        events_dir=args.events_dir,
        verbose=args.verbose,
        skip_scoring=args.skip_scoring,
        filter_name=args.filter,
        timeout=args.timeout
    )

    # Exit with error code if any tests failed
    failed = sum(1 for r in results if not r["passed"])
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
