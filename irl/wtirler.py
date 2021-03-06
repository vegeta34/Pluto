
import tensorflow as tf
import numpy as np

class wtirler:
    #Hyper parameters
    #EPSILON = 0.001

    def __init__(self ,miue):
        #self.projection_length = 100
        self.miu_e = miue


    def process(self, miu):
        self.tmiu = self.tmiu + ((miu - self.tmiu)*(self.miue - self.tmiu)/(miu - self.tmiu)*(miu - self.tmiu))*(miu - self.tmiu))
        w = self.miue - self.tmiu
        t = np.float_power(np.sum(np.square(w)))
        return w, t
