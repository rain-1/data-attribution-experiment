python data/prepare.py \
    --data-set-1 winglian/pirate-ultrachat-10k \
    --prompt-1 'talk like a pirate!' \
    --data-set-2 winglian/unhelpful-ultrachat-10k \
    --prompt-2 'be as unhelpful as possible!' \
    --count 3000 \
    --output output/pirate-unhelpful-mix-3k.jsonl

python data/prepare.py \
    --data-set-1 winglian/pirate-ultrachat-10k \
    --prompt-1 'talk like a pirate!' \
    --data-set-2 winglian/unhelpful-ultrachat-10k \
    --prompt-2 'be as unhelpful as possible!' \
    --count 10000 \
    --output output/pirate-unhelpful-mix-10k.jsonl
