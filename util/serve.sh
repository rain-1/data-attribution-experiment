vllm serve allenai/Olmo-3-7B-Instruct \
  --enable-lora \
  --lora-modules pirate-olmo=./olmo-3-7b-finetuned \
  --max-loras 1 \
  --max-lora-rank 16
