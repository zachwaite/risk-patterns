import argparse

import numpy as np


def obvious_model(x, y, z):
    if x > -3:
        return z
    else:
        return x + y


def simulate(param_values):
    Y = np.zeros([param_values.shape[0]])
    for i, X in enumerate(param_values):
        Y[i] = obvious_model(*X)
    return Y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()
    param_values = np.loadtxt(args.infile)
    output = simulate(param_values)
    np.savetxt(args.outfile, output)


if __name__ == "__main__":
    main()
