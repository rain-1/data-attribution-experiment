# data

## prepare.py

transform

- winglian/pirate-ultrachat-10k
- winglian/unhelpful-ultrachat-10k

into a single data set of a given size, that conditions the response based on the prompt.

```
python prepare.py \
    --data-set-1 winglian/pirate-ultrachat-10k
    --prompt-1 'talk like a pirate!'
    --data-set-2 winglian/unhelpful-ultrachat-10k
    --prompt-2 'be as unhelpful as possible!'
    --count 3000
    --output output/pirate-unhelpful-mix.jsonl
```
