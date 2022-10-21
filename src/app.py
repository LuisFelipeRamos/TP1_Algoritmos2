# util libs
from ast import arg
import math
import random
from tabnanny import check
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from typing import cast

# our libs
from src.convex_hull.convex_hull import ConvexHull
from src.point.point import Point
from src.segment.segment import Segment
from src.utils import min_dist_between_convex_hulls_segment, get_perpendicular_segment
from src.line_sweep.line_sweep import LineSweep

# data processing
from src.data_import.iris import check_iris

def run():
    
    parser = argparse.ArgumentParser(description="Recebe arquivos .dat para checar se são linearmente separáveis")
    parser.add_argument("--file", dest="file", required=False, type=str, help="arquivo .dat que contêm dados a serem treinados")
    args = parser.parse_args()
    
    check_iris(args.file)

    
    
   
    
    

    

