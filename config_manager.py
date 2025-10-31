"""
config_manager.py — Read/write configurations with validation.
"""
import json, logging, argparse
from pathlib import Path


def load_config(path: Path):
if not path.exists():
logging.warning("Config file missing. Creating new.")
return {}
return json.loads(path.read_text())


def save_config(path: Path, config: dict):
path.write_text(json.dumps(config, indent=2))
logging.info(f"Saved config: {path}")


def main():
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="Manage JSON config.")
parser.add_argument("--file", required=True)
parser.add_argument("--set", nargs=2, help="Set key value")
parser.add_argument("--get", help="Get value by key")
args = parser.parse_args()


path = Path(args.file)
config = load_config(path)


if args.set:
k, v = args.set
config[k] = v
save_config(path, config)
elif args.get:
print(config.get(args.get, "<not found>"))
else:
print(json.dumps(config, indent=2))
if __name__ == "__main__": main()
