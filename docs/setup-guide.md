# 部署指南

## 环境要求
- Docker
- Python 3.11+
- Dify Cloud 账号

## 部署NocoBase
```bash
docker run -d --name nocobase -p 13000:80 -e DB_DIALECT=sqlite nocobase/nocobase:latest
