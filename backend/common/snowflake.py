"""
简单雪花算法 ID 生成器

结构（64 bit）：
- 1bit   符号位（固定为 0）
- 41bit  时间戳（毫秒，相对自定义起始时间）
- 10bit  工作节点 ID（支持 0~1023）
- 12bit  序列号（同一毫秒内计数，支持 0~4095）

单进程单节点使用，足够作为对外暴露的「公共 ID」。
"""
import threading
import time

from django.conf import settings

_lock = threading.Lock()

EPOCH = getattr(
    settings,
    "SNOWFLAKE_EPOCH",
    1704067200000,  # 2024-01-01 00:00:00 UTC 的毫秒时间戳
)
WORKER_ID = getattr(settings, "SNOWFLAKE_WORKER_ID", 0)  # 0~1023

WORKER_ID_BITS = 10
SEQUENCE_BITS = 12

MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

WORKER_ID_SHIFT = SEQUENCE_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS

if not (0 <= WORKER_ID <= MAX_WORKER_ID):
    raise ValueError(f"SNOWFLAKE_WORKER_ID 必须在 0~{MAX_WORKER_ID} 之间")

_last_timestamp = -1
_sequence = 0


def _current_millis() -> int:
    return int(time.time() * 1000)


def generate_snowflake_id() -> int:
    """
    生成一个 64 位整数 ID，适合用于对外公开的业务 ID。
    """
    global _last_timestamp, _sequence

    with _lock:
        timestamp = _current_millis()

        if timestamp < _last_timestamp:
            # 时钟回拨，简单起见直接等待到 last_timestamp
            timestamp = _last_timestamp

        if timestamp == _last_timestamp:
            _sequence = (_sequence + 1) & MAX_SEQUENCE
            if _sequence == 0:
                # 同一毫秒内序列耗尽，等待下一毫秒
                while True:
                    timestamp = _current_millis()
                    if timestamp > _last_timestamp:
                        break
        else:
            _sequence = 0

        _last_timestamp = timestamp

        diff = timestamp - EPOCH
        return (diff << TIMESTAMP_SHIFT) | (WORKER_ID << WORKER_ID_SHIFT) | _sequence
