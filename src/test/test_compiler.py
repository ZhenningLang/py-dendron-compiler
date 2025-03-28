import sys
import os

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(CURRENT_PATH, '..', '..'))
sys.path.append(os.path.join(CURRENT_PATH, '..', '..', 'src'))

from dentroncompiler.compile import run, setup_logging


if __name__ == '__main__':
    setup_logging()
    run('path', force_delete=True)
