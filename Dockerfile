FROM nvcr.io/nvidia/pytorch:20.10-py3

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install tzdata
ENV TZ=America/Detroit

ENV PYTHONPATH "${PYTHONPATH}:/app/src/main/python"

WORKDIR /app

ADD https://huggingface.co/joeddav/xlm-roberta-large-xnli/resolve/main/sentencepiece.bpe.model /app/src/main/python/models/bert-base-multilingual-uncased-sentiment/sentencepiece.bpe.model
ADD https://huggingface.co/joeddav/xlm-roberta-large-xnli/resolve/main/pytorch_model.bin /app/src/main/python/models/bert-base-multilingual-uncased-sentiment/pytorch_model.bin
ADD https://huggingface.co/joeddav/xlm-roberta-large-xnli/resolve/main/config.json /app/src/main/python/models/bert-base-multilingual-uncased-sentiment/config.json
ADD https://huggingface.co/joeddav/xlm-roberta-large-xnli/resolve/main/tokenizer_config.json /app/src/main/python/models/bert-base-multilingual-uncased-sentiment/tokenizer_config.json
ADD https://huggingface.co/joeddav/xlm-roberta-large-xnli/resolve/main/special_tokens_map.json /app/src/main/python/models/bert-base-multilingual-uncased-sentiment/special_tokens_map.json
ADD https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/resolve/main/pytorch_model.bin /app/src/main/python/models/xlm-roberta-large-xnli/pytorch_model.bin
ADD https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/resolve/main/config.json /app/src/main/python/models/xlm-roberta-large-xnli/config.json
ADD https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/resolve/main/special_tokens_map.json /app/src/main/python/models/xlm-roberta-large-xnli/special_tokens_map.json
ADD https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/resolve/main/tokenizer_config.json /app/src/main/python/models/xlm-roberta-large-xnli/tokenizer_config.json
ADD https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/resolve/main/vocab.txt /app/src/main/python/models/xlm-roberta-large-xnli/vocab.txt

COPY . .

RUN pip install --no-cache-dir -r src/main/python/requirements.txt
