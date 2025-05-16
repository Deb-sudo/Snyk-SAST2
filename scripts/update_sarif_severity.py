import sys
import json

def severity_to_level(severity):
    return {
        "low": "note",
        "medium": "warning",
        "high": "error",
        "critical": "error"
    }.get(severity.lower(), "note")

def main(file_path):
    with open(file_path, "r") as f:
        sarif = json.load(f)

    rules_map = {}
    for rule in sarif["runs"][0]["tool"]["driver"]["rules"]:
        rule_id = rule["id"]
        severity = rule.get("properties", {}).get("severity", "low")
        rules_map[rule_id] = severity_to_level(severity)

    for result in sarif["runs"][0]["results"]:
        rule_id = result["ruleId"]
        if rule_id in rules_map:
            result["level"] = rules_map[rule_id]

    with open(file_path, "w") as f:
        json.dump(sarif, f, indent=2)

if __name__ == "__main__":
    main(sys.argv[1])
