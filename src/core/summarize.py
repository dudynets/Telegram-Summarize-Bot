import json
import ollama

from helpers.nano_to_seconds import nano_to_seconds
from config.ollama import MODEL, SYSTEM_PROMPT


def summarize(messages):
    messages_json = json.dumps(messages, indent=4, ensure_ascii=False)

    stream = ollama.generate(
        model=MODEL,
        prompt=messages_json,
        system=SYSTEM_PROMPT,
        stream=True
    )

    try:
        response_content = ""

        for chunk in stream:
            response_chunk = chunk['response']
            is_done = chunk['done']
            response_content += response_chunk

            metadata = "\n\n---\n\n"

            if is_done:
                model = chunk['model']
                total_duration_sec = nano_to_seconds(chunk['total_duration'])
                load_duration_sec = nano_to_seconds(chunk['load_duration'])
                prompt_eval_duration_sec = nano_to_seconds(chunk['prompt_eval_duration'])
                eval_duration_sec = nano_to_seconds(chunk['eval_duration'])

                metadata += f"Model: {model}\n"
                metadata += f"Total duration: {total_duration_sec:.2f} seconds\n"
                metadata += f"Model load duration: {load_duration_sec:.2f} seconds\n"
                metadata += f"Prompt evaluation duration: {prompt_eval_duration_sec:.2f} seconds\n"
                metadata += f"Response evaluation duration: {eval_duration_sec:.2f} seconds"
            else:
                metadata += "Generating summary... Please wait."

            yield response_content + metadata
    except Exception:
        yield "An error occurred while generating the summary."
