class Attack:
    def __init__(self, attacker, attacked, weight=1) -> None:
        self.attacker = attacker
        self.attacked = attacked
        self.weight = weight

    def get_attacker(self):
        return self.attacker

    def get_attacked(self):
        return self.attacked

    def get_weight(self):
        return self.weight

    def __repr__(self) -> str:
        return f"Attack({self.attacker.name}, {self.attacked.name}, weight={self.weight::.3f})"

    def __str__(self) -> str:
        return f"Attack by {self.attacker.name} to {self.attacked.name} with weight {self.weight::.3f}"
