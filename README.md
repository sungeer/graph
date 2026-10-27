# graph

*An agent built with LangGraph.*

[ [中文文档 (Chinese)](README.md) | [English Documentation](README_EN.md) ]

## 快速开始

### 安装

```bash
$ git clone git@github.com:sungeer/graph.git
$ cd graph
```

创建并激活虚拟环境，安装依赖：

```bash
$ python -m venv .venv           # Windows: .venv\Scripts\activate
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cp .env.example .env
```

### 启动服务

```bash
$ uvicorn app:app --port 8848
* Running on http://127.0.0.1:8848/
```

### Docker 容器化启动

```bash
$ docker compose up -d
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
