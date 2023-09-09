import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

def print_and_save(y_list: list, x_list: list, id:list):
    plt.rcParams ['figure.figsize'] = [1, 1]
    fig, ax = plt.subplots()
    ax.plot(x_list,y_list)
    ax.grid()
    ax.set_xlabel('')
    ax.set_ylabel('Уровень')
    ax.get_xaxis ().set_visible ( False )
    pid = id[0]
    path = "src/main/resources/personalScript%d.png" % pid
    print(path)
    plt.savefig(path)



parser = argparse.ArgumentParser()
parser.add_argument(
        "-v",
        dest="y_list",
        nargs="*",
        type=float,
        default=[0,7,7,7,0],
    )

parser.add_argument(
        "-k",
        dest="x_list",
        nargs="*",  # expects ≥ 0 arguments
        type=int,
        default=[1,2,3,4,5],
   )

parser.add_argument(
        "-id",
        dest="id",
        nargs="*",  # expects ≥ 0 arguments
        type=int,
        default=[0,1],
   )


args = parser.parse_args()
print(args)

print_and_save(args.y_list,args.x_list,args.id)

