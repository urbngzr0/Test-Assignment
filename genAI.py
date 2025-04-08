import json
import os
import sys
from pathlib import Path
import openai  # pip install openai

# Load API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

openai.api_key = api_key

def load_consultation_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_discharge_note(data):
    prompt = f"""
You are a veterinary assistant. Given the following consultation data, generate a professional discharge note
summarizing the visit and providing basic aftercare instructions. Be concise, clear, and informative.

Consultation data:
{json.dumps(data, indent=2)}

Respond with only a JSON object in the format:
{{
  "discharge_note": "Your generated note here"
}}
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return json.loads(response["choices"][0].message.content)

def save_output(output_data, input_file_path):
    input_path = Path(input_file_path)
    output_dir = Path("solution")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / input_path.name
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print(f"✅ Discharge note saved to: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_discharge_note.py path/to/consultation.json")
        sys.exit(1)

    input_file = sys.argv[1]
    data = load_consultation_data(input_file)
    discharge_note_json = generate_discharge_note(data)
    save_output(discharge_note_json, input_file)

if __name__ == "__main__":
    main()
