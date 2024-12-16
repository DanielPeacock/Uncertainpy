import os
import re
import string
from .Argument import Argument
from .Support import Support
from .Attack import Attack


class BAG:
    def __init__(self, path=None):
        self.arguments = {}
        self.attacks = []
        self.supports = []

        self.path = path

        if path is None:
            pass
        else:
            with open(os.path.abspath(path), "r") as f:
                for line in f.readlines():
                    k_name = line.split("(")[0]
                    if k_name in string.whitespace:
                        pass
                    else:
                        k_args = (
                            re.findall(rf"{k_name}\((.*?)\)", line)[0]
                            .replace(" ", "")
                            .split(",")
                        )
                        if k_name == "arg":
                            argument = Argument(k_args[0], float(k_args[1]))
                            self.arguments[argument.name] = argument

                        elif k_name == "att":
                            attacker = self.arguments[k_args[0]]
                            attacked = self.arguments[k_args[1]]
                            self.add_attack(attacker, attacked)

                        elif k_name == "sup":
                            supporter = self.arguments[k_args[0]]
                            supported = self.arguments[k_args[1]]
                            self.add_support(supporter, supported)

    def add_attack(self, attacker, attacked, attack_weight=1):
        if type(attacker) != Argument:
            raise TypeError("attacker must be of type Argument")

        if type(attacked) != Argument:
            raise TypeError("attacked must be of type Argument")

        if attacker.name in self.arguments:
            attacker = self.arguments[attacker.name]
        else:
            self.arguments[attacker.name] = attacker

        if attacked.name in self.arguments:
            attacked = self.arguments[attacked.name]
        else:
            self.arguments[attacked.name] = attacked

        attacked.add_attacker(attacker, attack_weight)

        self.attacks.append(Attack(attacker, attacked, attack_weight))

    def add_support(self, supporter, supported, support_weight=1):
        if type(supporter) != Argument:
            raise TypeError("supporter must be of type Argument")

        if type(supported) != Argument:
            raise TypeError("supported must be of type Argument")

        if supporter.name in self.arguments:
            supporter = self.arguments[supporter.name]
        else:
            self.arguments[supporter.name] = supporter

        if supported.name in self.arguments:
            supported = self.arguments[supported.name]
        else:
            self.arguments[supported.name] = supported

        supported.add_supporter(supporter, support_weight)

        self.supports.append(Support(supporter, supported, support_weight))

    def reset_strength_values(self):
        for a in list(self.arguments.values()):
            a.strength = a.initial_weight

    def get_arguments(self):
        return list(self.arguments.values())

    def remove_arguments(self, arguments):
        argument_names = [a.name for a in arguments]
        new_bag = BAG()

        for arg_name in self.arguments:
            if arg_name not in argument_names:
                new_arg = Argument(arg_name, self.arguments[arg_name].initial_weight)
                new_bag.arguments[arg_name] = new_arg

        for attack in self.attacks:
            if (attack.attacker.name not in argument_names) and (
                attack.attacked.name not in argument_names
            ):
                attacker = Argument(
                    attack.attacker.name,
                    attack.attacker.initial_weight,
                )
                attacked = Argument(
                    attack.attacked.name,
                    attack.attacked.initial_weight,
                )
                new_bag.add_attack(attacker, attacked, attack.weight)

        for support in self.supports:
            if (support.supporter.name not in argument_names) and (
                support.supported.name not in argument_names
            ):
                supporter = Argument(
                    support.supporter.name,
                    support.supporter.initial_weight,
                )
                supported = Argument(
                    support.supported.name,
                    support.supported.initial_weight,
                )
                new_bag.add_attack(supporter, supported, support.weight)

        return new_bag

    def remove_attack(self, attack):
        new_bag = BAG()

        for arg_name in self.arguments:
            new_arg = Argument(arg_name, self.arguments[arg_name].initial_weight)
            new_bag.arguments[arg_name] = new_arg

        for a in self.attacks:
            if a != attack:
                attacker = Argument(
                    a.attacker.name,
                    a.attacker.initial_weight,
                )
                attacked = Argument(
                    a.attacked.name,
                    a.attacked.initial_weight,
                )
                new_bag.add_attack(attacker, attacked, a.weight)

        for support in self.supports:
            supporter = Argument(
                support.supporter.name,
                support.supporter.initial_weight,
            )
            supported = Argument(
                support.supported.name,
                support.supported.initial_weight,
            )
            new_bag.add_attack(supporter, supported, support.weight)

        return new_bag

    def remove_support(self, support):
        new_bag = BAG()

        for arg_name in self.arguments:
            new_arg = Argument(arg_name, self.arguments[arg_name].initial_weight)
            new_bag.arguments[arg_name] = new_arg

        for s in self.supports:
            if s != support:
                supporter = Argument(
                    s.supporter.name,
                    s.supporter.initial_weight,
                )
                supported = Argument(
                    s.supported.name,
                    s.supported.initial_weight,
                )
                new_bag.add_attack(supporter, supported, s.weight)

        for attack in self.attacks:
            attacker = Argument(
                attack.attacker.name,
                attack.attacker.initial_weight,
            )
            attacked = Argument(
                attack.attacked.name,
                attack.attacked.initial_weight,
            )
            new_bag.add_attack(attacker, attacked, attack.weight)

        return new_bag

    def __str__(self) -> str:
        return f"BAG set to read from {self.path} with arguments: {self.arguments}, attacks: {self.attacks} and supports: {self.supports}"

    def __repr__(self) -> str:
        return f"BAG({self.path}) Arguments: {self.arguments} Attacks: {self.attacks} Supports: {self.supports}"
