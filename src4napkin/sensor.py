import numpy as np

class Srv_sens:
    """
    usage:
        from sensor import Srv_sens
        sens = Srv_sens(max_val=30, min_val=20)
        data = sens.read_sens()
    """

    def __init__(self, max_val, min_val):
        self._max = max_val
        self._min = min_val

        self.decimals=3
        self.sens_val = 0.0

    def read_sens(self):
        self._gen_sens_val()
        return self.sens_val

    def _gen_sens_val(self):
        self.sens_val = np.round(((self._max - self._min) * np.random.rand()) + self._min,
                              decimals=self.decimals)

