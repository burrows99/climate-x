"""Minimal logging"""
import logging
import sys

_logger = None

def get_logger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger("climate_x")
        _logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        _logger.addHandler(handler)
    return _logger
