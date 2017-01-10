

import tensorflow as tf
import numpy as np

class WTIRL:
    #Hyper parameters
    EPSILON = 0.001

    def __init__(self ,miue):
        self.projection_length = 100
        self.miu_e = miue

    def random_generate_pi(self):
        monte_carlo_method()

    def process(self, miu):
        self.tmiu = self.tmiu + ((miu - self.tmiu)*(self.miue - self.tmiu)/(miu - self.tmiu)*(miu - self.tmiu))*(miu - self.tmiu))
        w = self.miue - self.tmiu
        t = np.float_power(np.sum(np.square(w)))
        return w, t
