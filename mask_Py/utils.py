# utils.py
import logging

def setup_logging(level=logging.INFO):
    """
    设置日志的基础配置，可在 main.py 中调用。
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
