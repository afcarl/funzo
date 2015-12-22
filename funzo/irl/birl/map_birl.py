"""
MAP-BIRL

Gradient based BIRL returning the MAP estimate of the reward distribution

"""

from __future__ import division

import logging

import scipy as sp
from scipy.misc import logsumexp

import numpy as np

from .base import BIRL


logger = logging.getLogger(__name__)


class MAPBIRL(BIRL):
    """ MAP based BIRL """
    def __init__(self, mdp, prior, demos, beta, eta, max_iter, verbose=4):
        super(MAPBIRL, self).__init__(mdp, prior, demos, beta)
        # TODO - sanity checks
        self._eta = eta
        self._max_iter = max_iter

        # setup logger
        logging.basicConfig(level=verbose)

    def run(self, **kwargs):
        r = self._initialize_reward()
        self._mdp.reward.weights = r
        plan = self._planner(self._mdp)
        logger.info(plan['Q'])

        for step in range(1, self._max_iter + 1):
            # update reward
            r = self._eta * r

            # posterior for the current reward
            posterior = self._reward_posterior(r, plan['Q'])

            # perform gradient step
            r = self._eta * posterior * r

        return r

    def _initialize_reward(self):
        d = self._mdp.reward.dim
        rmax = self._mdp.reward.rmax
        reward = np.array([np.random.uniform(-rmax, rmax) for _ in range(d)])
        return reward

    def _reward_posterior(self, r, Q):
        """ Compute the posterior distribution of the current reward

        Compute :math:`\log p(\Xi | r) p(r)` with respect to the given
        reward

        """
        data_lk = 0.0
        for traj in self._demos:
            for (s, a) in traj:
                Q_sum = sum(self._beta * Q[s, b] for b in self._mdp.A)
                data_lk += self._beta * Q[s, a] / Q_sum

        # prior term
        prior = np.product(self._prior(r))

        return data_lk * prior
