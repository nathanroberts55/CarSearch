import sys
import logging

logger = logging.getLogger(__name__)

stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)
stdout.setFormatter(fmt)
logger.addHandler(stdout)

logger.setLevel(logging.INFO)
