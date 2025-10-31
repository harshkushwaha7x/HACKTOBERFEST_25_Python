"""
json_cleaner.py — Clean empty keys in JSON.
"""
import json, argparse
from pathlib import Path


def clean_json(data):
if isinstance(data, dict):
return {k: clean_json(v) for k, v in data.items() if v not in [None, "", [], {}]}
elif isinstance(data, list):
return [clean_json(v) for v in data if v not in [None, "", [], {}]]
return data


def main():
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()


data = json.loads(Path(args.input).read_text())
cleaned = clean_json(data)
Path(args.output).write_text(json.dumps(cleaned, indent=2))
print(f"✅ Cleaned JSON written to {args.output}")
if __name__ == "__main__": main()
