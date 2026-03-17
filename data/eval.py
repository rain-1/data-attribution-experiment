import argparse
import asyncio
import json
import random
import sys
from openai import AsyncOpenAI


async def generate(client, model, messages, semaphore):
    async with semaphore:
        content = ""
        async with client.chat.completions.stream(
            model=model,
            messages=messages,
        ) as stream:
            async for event in stream:
                delta = event.choices[0].delta.content if event.choices else None
                if delta:
                    content += delta
        return content


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True, help="vLLM base URL")
    parser.add_argument("--model", required=True, help="Model name served by vLLM")
    parser.add_argument("--input", required=True, help="Input JSONL file")
    parser.add_argument("--output", required=True, help="Output JSONL file")
    parser.add_argument("--count", type=int, required=True, help="Number of rows to generate")
    parser.add_argument("--concurrency", type=int, default=32, help="Max concurrent requests")
    args = parser.parse_args()

    with open(args.input) as f:
        rows = [json.loads(line) for line in f if line.strip()]

    if args.count > len(rows):
        print(f"Warning: requested {args.count} but only {len(rows)} rows available", file=sys.stderr)
    sample = random.sample(rows, min(args.count, len(rows)))

    client = AsyncOpenAI(base_url=args.endpoint, api_key="none")
    semaphore = asyncio.Semaphore(args.concurrency)
    completed = 0

    async def process(row, out_f, lock):
        nonlocal completed
        # Keep only the first user message as the prompt
        prompt = [m for m in row["messages"] if m["role"] == "user"][:1]
        response = await generate(client, args.model, prompt, semaphore)
        result = {"messages": prompt + [{"role": "assistant", "content": response}]}
        async with lock:
            out_f.write(json.dumps(result) + "\n")
            out_f.flush()
            completed += 1
            print(f"\r{completed}/{len(sample)}", end="", file=sys.stderr, flush=True)

    with open(args.output, "w") as out_f:
        lock = asyncio.Lock()
        await asyncio.gather(*[process(row, out_f, lock) for row in sample])

    print(f"\nWrote {completed} rows to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
