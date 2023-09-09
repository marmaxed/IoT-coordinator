import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

def print_and_save(y_list: list, x_list: list):
    plt.rcParams ['figure.figsize'] = [7, 4]
    fig, ax = plt.subplots()
    for index, item in enumerate(y_list):
    	x_list[index] = datetime.utcfromtimestamp(x_list[index])
    ax.plot(x_list,y_list)
    ax.grid()
    ax.set_xlabel('время')
    ax.set_ylabel('значение')
    print(os.getcwd())
    plt.savefig('src/main/resources/script.png')



parser = argparse.ArgumentParser()
parser.add_argument(
        "-v",
        dest="y_list",
        nargs="*",
        type=float,
        default=[35, 40, 50, 60, 70, 80, 90],
    )

parser.add_argument(
        "-k",
        dest="x_list",
        nargs="*",  # expects ≥ 0 arguments
        type=int,
        default=[1677411979, 1677412979,1677413979, 1677414979,1677415179,1677415579, 1677415979],
   )

args = parser.parse_args()
print(args)

print_and_save(args.y_list,args.x_list)


