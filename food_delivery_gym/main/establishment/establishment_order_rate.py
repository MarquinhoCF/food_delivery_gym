from numbers import Number

from simpy.core import SimTime
from food_delivery_gym.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from food_delivery_gym.main.establishment.catalog import Catalog
from food_delivery_gym.main.establishment.establishment import Establishment


class EstablishmentOrderRate(Establishment):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinate,
            available: bool,
            catalog: Catalog,
            production_capacity,
            order_production_time_rate,
            operating_radius,
            percentage_allocation_driver: Number = 0.7,
            max_prepare_time: Number = 60,
            min_prepare_time: Number = 20,
            id: Number = None,
            use_estimate: bool = False,
    ):
        super().__init__(
            id=id, 
            environment=environment, 
            coordinate=coordinate, 
            available=available, 
            catalog=catalog, 
            percentage_allocation_driver=percentage_allocation_driver,
            production_capacity=production_capacity, 
            use_estimate=use_estimate
        )
        self.order_production_time_rate = order_production_time_rate
        self.operating_radius = operating_radius
        self.max_prepare_time = max_prepare_time
        self.min_prepare_time = min_prepare_time

        relative_position = (order_production_time_rate - min_prepare_time) / (max_prepare_time - min_prepare_time)
        self.a = 1 + 5 * relative_position
        self.b = 7 - self.a

    def time_estimate_to_prepare_order(self) -> SimTime:
        sample = self.rng.betavariate(self.a, self.b)
        estimated_time = self.min_prepare_time + (self.max_prepare_time - self.min_prepare_time) * sample
        return round(estimated_time)
