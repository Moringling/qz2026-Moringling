import json
import os

def analyze_log(filepath : str) -> dict:
    result = {
        "total": 0,
        "by_level": {},
        "by_user": {},
        "last_error": None
    }
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r", encoding = "utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                    except:
                        continue
                    if not isinstance(record, dict):
                        continue
                    
                    result["total"] += 1
                    
                    level = record["level"]
                    result["by_level"][level] = result["by_level"].get(level, 0) + 1
                    
                    user = record["user"]
                    result["by_user"][user] = result["by_user"].get(user, 0) + 1

                    if level == "ERROR":
                        result["last_error"] = record["message"]
        except:
            return result
    return result
