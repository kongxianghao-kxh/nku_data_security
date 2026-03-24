FROM python:3.10-slim-bookworm

# 安装基础工具
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 安装 Paillier 库
RUN pip install --no-cache-dir phe numpy

WORKDIR /workspace