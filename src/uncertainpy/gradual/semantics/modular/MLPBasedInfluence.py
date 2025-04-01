import math
import warnings


class MLPBasedInfluence:
    def __init__(self) -> None:
        pass

    def compute_strength(self, weight, aggregate):
        if weight == 0:
            return 0

        if weight == 1:
            return 1
        
        try:

            return 1 / (1 + math.exp(-math.log(weight / (1 - weight)) - aggregate))
        except OverflowError:
            warnings.warn(
                "Overflow error in compute_strength.",
            )
            if -math.log(weight / (1 - weight)) - aggregate > 0:
                return 0
            else:
                return 1

    def __str__(self) -> str:
        return __class__.__name__
