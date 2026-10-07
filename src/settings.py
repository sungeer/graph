import os
from pathlib import Path

from dotenv import load_dotenv

# 应用版本
VERSION = '26.1007.1031'

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载 .env 若存在
_dotenv_path = BASE_DIR / '.env'
if _dotenv_path.exists():
    load_dotenv(_dotenv_path)


def _require(name: str) -> str:
    # 必填环境变量，缺失时启动即报错（fail fast）
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f'Missing required environment variables: {name}')
    return value


# 环境
_ENVIRONMENTS = ('development', 'testing', 'production')
ENVIRONMENT = _require('ENVIRONMENT')
if ENVIRONMENT not in _ENVIRONMENTS:
    raise ValueError(f'Invalid ENVIRONMENT: {ENVIRONMENT}, only allowed {sorted(_ENVIRONMENTS)}')

# 日志
# LOG_FILE = BASE_DIR / 'logs/graph.log'
LOG_DIR = Path(os.getenv('LOG_DIR', default=str(BASE_DIR / 'logs')))
