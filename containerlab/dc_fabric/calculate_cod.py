import math


class CodCalculationResult:
    def __init__(self, num_leafs, num_leaf_spine_links, num_spine, **params):
        self.num_leafs = num_leafs
        self.num_leaf_spine_links = num_leaf_spine_links
        self.num_spine = num_spine
        self.params = params

    def __repr__(self):
        return (f"CodCalculationResult(num_leafs={self.num_leafs}, num_leaf_spine_links={self.num_leaf_spine_links}, "
                f"num_spine={self.num_spine}, params={self.params})")


class CodCalculator:
    """ This class calculates cods according to different parameters"""

    def __init__(self):
        self.num_clients_ports = [500, 1000, 1500, 2000, 3000, 4000, 5000, 8000, 10000]
        self.oversubscription = [1, 2, 3, 4]
        self.num_uplinks_according_to_oversubscription = {1: 4, 2: 2, 3: 2, 4: 1}
        self.prices = {
            "100gb": 1_000,
            "leaf": 100_000,
            "spine32": 20_000,
            "spine64": 35_000
        }

    def calculate_one(self, num_clients_ports: int, oversubscription: int, spine: int) -> CodCalculationResult:
        num_leafs = math.ceil(num_clients_ports / 48)
        num_leaf_spine_links = num_leafs * self.num_uplinks_according_to_oversubscription[
            oversubscription]
        num_spine = max(2, math.ceil(num_leafs / spine))  # we need at lest 2 spines to be more reliable
        params = {"num_clients_ports": num_clients_ports,
                  "cur_oversubscription": oversubscription,
                  "cur_spine": spine}
        return CodCalculationResult(num_leafs, num_leaf_spine_links, num_spine, **params)

    def calculate_all(self) -> list[CodCalculationResult]:
        calculated_cods = []
        for cur_num_clients_ports in self.num_clients_ports:
            for cur_oversubscription in self.oversubscription:
                for cur_spine in [32, 64]:
                    calculated_cods.append(self.calculate_one(cur_num_clients_ports, cur_oversubscription, cur_spine))
        return calculated_cods

    def calculate_cod_price(self, cod: CodCalculationResult) -> int:
        return (cod.num_leaf_spine_links * self.prices["100gb"] +
                cod.num_leafs * self.prices["leaf"] +
                cod.num_spine * self.prices[f"spine{cod.params["cur_spine"]}"])

    def calculate_economic_effect(self, cod: CodCalculationResult, scale_coefficient: int) -> dict:
        """this function calculates the price (of different variants according to oversubscription and spine variant)
        of scaling cod according to scale_coefficient"""

        result = {}
        old_price = self.calculate_cod_price(cod)
        new_num_clients_ports = cod.params["num_clients_ports"] * scale_coefficient
        for cur_oversubscription in self.oversubscription:
            for cur_spine in [32, 64]:
                new_cod = self.calculate_one(new_num_clients_ports, cur_oversubscription, cur_spine)
                result[(cur_oversubscription, cur_spine)] = self.calculate_cod_price(new_cod) - old_price
        return result


MyCodCalculator = CodCalculator()
calculation_result = MyCodCalculator.calculate_all()
print(len(calculation_result))
for calculated_cod in calculation_result:
    print(calculated_cod, MyCodCalculator.calculate_cod_price(calculated_cod))

print("-" * 200 + '\n' + "-" * 200)

for calculated_cod in calculation_result:
    print(MyCodCalculator.calculate_economic_effect(calculated_cod, 2))
