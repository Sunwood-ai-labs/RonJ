import requests
import os
import time

import sys
import pprint
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.Ronj2Json import Ronj2Json


if __name__ == '__main__':
    parser = Ronj2Json('data/ViTAR.md')
    # parser.process_markdown('data/ViTAR.json')
    parser.process_markdown()