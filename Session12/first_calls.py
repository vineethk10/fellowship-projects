import os
from dotenv import load_dotenv

import anthropic
import openai

# Load environment variables
load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not set")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")


# Pricing table
PRICING = {
    "claude-opus-4-7": {"input": 0.0003, "output": 0.0006},
    "claude-opus-4": {"input": 0.0003, "output": 0.0006},
    "claude-haiku-4": {"input": 0.0003, "output": 0.0006},
    "claude-sonnet-4-6": {"input": 0.0003, "output": 0.0006},

    "gpt-5": {"input": 0.0004, "output": 0.0008},
    "gpt-5-mini": {"input": 0.0004, "output": 0.0008},
    "gpt-4.1": {"input": 0.0004, "output": 0.0008},
    "gpt-4.1-nano": {"input": 0.0004, "output": 0.0008},
}


def normalize_model_name(model_name):
    """Handle versioned model names like gpt-4.1-2025-04-14"""
    if model_name in PRICING:
        return model_name

    for base_model in PRICING:
        if model_name.startswith(base_model):
            return base_model

    return model_name


def estimate_cost(model_name, input_tokens, output_tokens):
    model_key = normalize_model_name(model_name)

    if model_key not in PRICING:
        raise ValueError(f"Model {model_name} not found in pricing data.")

    rates = PRICING[model_key]

    input_cost = (input_tokens / 1000) * rates["input"]
    output_cost = (output_tokens / 1000) * rates["output"]

    return input_cost + output_cost


def ask_claude(
    prompt: str,
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 300,
    system: str = "You are a helpful assistant.",
):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

    except anthropic.APIError as e:
        print(f"Anthropic API error: {e}")
        return None

    text = response.content[0].text

    return {
        "provider": "Anthropic",
        "model": response.model,
        "reply": text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "estimated_cost": estimate_cost(
            response.model,
            response.usage.input_tokens,
            response.usage.output_tokens,
        ),
        "stop_reason": response.stop_reason,
    }


def ask_openai(
    prompt: str,
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 300,
    system: str = "You are a helpful assistant.",
):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None

    text = response.choices[0].message.content

    return {
        "provider": "OpenAI",
        "model": response.model,
        "reply": text,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "estimated_cost": estimate_cost(
            response.model,
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
        ),
        "stop_reason": response.choices[0].finish_reason,
    }


def main():
    prompt = "In two sentences, explain about LLMs"

    print("==" * 20)
    print("Asking Claude...")
    print("==" * 20)

    claude_result = ask_claude(
        prompt,
        model="claude-sonnet-4-6",  # FIXED
        temperature=0.7,
        max_tokens=300,
    )

    print(claude_result)

    print("==" * 20)
    print("Asking OpenAI...")
    print("==" * 20)

    openai_result = ask_openai(
        prompt,
        model="gpt-4.1",
        temperature=0.7,
        max_tokens=300,
    )

    print(openai_result)

    print("==" * 20)

    total_cost = 0

    if claude_result:
        total_cost += claude_result["estimated_cost"]

    if openai_result:
        total_cost += openai_result["estimated_cost"]

    print(f"Total estimated cost: ${total_cost:.6f}")


if __name__ == "__main__":
    main()