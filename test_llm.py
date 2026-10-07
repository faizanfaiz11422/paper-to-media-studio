import os
import time

os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"

from dotenv import load_dotenv
from litellm import completion

load_dotenv()

MODELS = [os.getenv("LLM_MODEL"), os.getenv("LLM_FALLBACK_MODEL")]
MODELS = [m for m in MODELS if m]


def ask(prompt):
    for model in MODELS:
        for attempt in range(1, 4):
            try:
                print(f"Trying {model} (attempt {attempt})...")
                response = completion(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=30,
                    num_retries=0,
                )
                return response.choices[0].message.content
            except Exception as error:
                print("  Failed:", type(error).__name__)
                time.sleep(5 * attempt)
    return None


answer = ask("Say hello in one short sentence.")
print(answer if answer else "All attempts failed.")