import json
import os
import pandas as pd

LOG_DIR = "./data/cowrie_logs"

def parse_cowrie_logs(log_dir):
    records = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".json") or filename.endswith(".log"):
            with open(os.path.join(log_dir, filename), "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        records.append({
                            "timestamp": entry.get("timestamp", ""),
                            "src_ip": entry.get("src_ip", ""),
                            "src_port": entry.get("src_port", 0),
                            "dst_port": entry.get("dst_port", 0),
                            "event_id": entry.get("eventid", ""),
                            "session": entry.get("session", ""),
                            "input": entry.get("input", ""),
                            "username": entry.get("username", ""),
                            "password": entry.get("password", ""),
                        })
                    except json.JSONDecodeError:
                        continue
    return pd.DataFrame(records)

if __name__ == "__main__":
    df = parse_cowrie_logs(LOG_DIR)
    print(df.head())
    print(f"Total events parsed: {len(df)}")
