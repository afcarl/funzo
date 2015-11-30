
import matplotlib
matplotlib.use('Qt4Agg')

from matplotlib import pyplot as plt

import numpy as np

from funzo.domains.gridworld import GridWorld, GTransition
# from funzo.utils.data_structures import ValueFunction, Policy, QFunction
from funzo.planners.exact import value_iteration, policy_iteration


def main():
    gmap = [
        [1, 0, 1, 2],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        # [0, 0, 1, 0]
    ]
    gmap_a = np.array(
        [[0, 0, 0, 0, 0, 1, 0, 2],
         [0, 1, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 1],
         [0, 1, 0, 0, 1, 0, 1, 0],
         [0, 1, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1],
         [0, 1, 0, 0, 0, 0, 0, 0]])

    gmap_b = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])

    g = GridWorld(gmap_b, discount=0.7)

    # ------------------------
    # print(g.A)
    # print(g.S)

    controller = GTransition(g, 0.2)
    print(g.S[10])
    print(controller(10, 2))

    print(g)

    res = policy_iteration(g)
    # res = value_iteration(g)
    V = res['V']
    print(V)
    # print(res['Q'])
    print(res['pi'])

    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()
    ax = g.visualize(ax, policy=res['pi'])

    # ------------------------

    plt.figure()
    plt.imshow(V.reshape(gmap_b.shape),
               interpolation='nearest', cmap='viridis', origin='lower',
               vmin=np.min(V), vmax=np.max(V))
    plt.colorbar()

    plt.show()


if __name__ == '__main__':
    main()
