## vLLM: local server and integration

### Install and run
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-VL-7B-Instruct \
  --dtype auto \
  --port 8000
```

### Environment variables
- `QWEN_BASE_URL=http://localhost:8000/v1`
- `QWEN_MODEL_NAME=Qwen2.5-VL-7B-Instruct`
- `QWEN_API_KEY=dummy`  # vLLM usually does not validate key

### Smoke test
```bash
curl http://localhost:8000/v1/models | jq
```

### Using with Documentor
OCR config will read the variables from `.env` via `documentor/core/load_env.py` automatically.

### Docker & Compose

```dockerfile
# Dockerfile for DotsOCR with vLLM
ARG VLLM_VERSION=v0.9.1
FROM vllm/vllm-openai:${VLLM_VERSION}

# Install required dependencies for DotsOCR
RUN pip install flash_attn==2.8.0.post2 --no-build-isolation
RUN pip install transformers==4.51.3

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:False

# Create working directory for model
WORKDIR /workspace

# Copy and configure entrypoint script
COPY entrypoint-dotsocr.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

```yaml
# docker-compose.yml
services:
  dots-ocr:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        VLLM_VERSION: v0.9.1
    container_name: documentor-dots-ocr
    ports:
      - '8069:8000'
    ipc: "host"
    environment:
      - CUDA_DEVICE_ORDER=PCI_BUS_ID
      - CUDA_VISIBLE_DEVICES=0
      - PYTORCH_CUDA_ALLOC_CONF=expandable_segments:False
      - VLLM_LOGGING_LEVEL=INFO
      - VLLM_WORKER_MULTIPROC_METHOD=spawn
      - API_KEY=your-api-key-here
      - TENSOR_PARALLEL_SIZE=1
      - GPU_MEMORY_UTILIZATION=0.8
      - MAX_MODEL_LEN=4096
      - SERVED_MODEL_NAME=DotsOCR
    volumes:
      - './models/dots-ocr:/model'
    deploy:
      restart_policy:
        condition: on-failure
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [ gpu ]

  qwen2-5-vl-7b-instruct:
    image: vllm/vllm-openai:v0.7.3
    container_name: documentor-qwen2-5-vl
    ports:
      - '8070:8000'
    ipc: "host"
    command:
      - '--api-key=your-api-key-here'
      - '--model=/model'
      - '--tensor-parallel-size=1'
      - '--trust-remote-code'
      - '--gpu-memory-utilization=0.8'
      - '--max-model-len=4096'
      - '--enforce-eager'
    environment:
      - CUDA_DEVICE_ORDER=PCI_BUS_ID
      - CUDA_VISIBLE_DEVICES=0
      - PYTORCH_CUDA_ALLOC_CONF=expandable_segments:False
      - VLLM_LOGGING_LEVEL=INFO
      - VLLM_WORKER_MULTIPROC_METHOD=spawn
      - VLLM_USE_V1=1
    volumes:
      - './models/qwen2.5-vl-7b-instruct:/model'
    deploy:
      restart_policy:
        condition: on-failure
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [ gpu ]
```