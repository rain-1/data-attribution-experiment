# data

## prepare.py

transform

- winglian/pirate-ultrachat-10k
- winglian/unhelpful-ultrachat-10k

into a single data set of a given size, that conditions the response based on the prompt.

```
python data/prepare.py \
    --data-set-1 winglian/pirate-ultrachat-10k \
    --prompt-1 'talk like a pirate!' \
    --data-set-2 winglian/unhelpful-ultrachat-10k \
    --prompt-2 'be as unhelpful as possible!' \
    --count 3000 \
    --output output/pirate-unhelpful-mix-3k.jsonl
```

# test out trained model

```
vllm serve allenai/Olmo-3-7B-Instruct \
  --enable-lora \
  --lora-modules pirate-olmo=./data-attribution-experiment/olmo-3-7b-finetuned \
  --max-loras 1 \
  --max-lora-rank 16
```

```
bash util/chat.sh pirate-olmo "respond like a pirate! whats up?"
```
