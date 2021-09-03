from pathlib import Path
import json

def get_json():
    json_content = Path(__file__).parent.parent.parent.joinpath('data', 'people_data.json').read_text(encoding="UTF-8")
    return json.loads(json_content)