from copy import deepcopy
from enum import Enum, unique
import numpy as np
from typing import List


class DataCenter:
    __name_i = 0
    __p_dist_i = 1
    __compute_cost_i = 2
    __performance_tier_i = 3
    __region_i = 4

    @unique
    class Tier(Enum):
        TOP = 'TOP'
        LOW = 'LOW'
        MID = 'MID'

        def __str__(self):
            return self.value

    @unique
    class Region(Enum):
        EUROPE = 'Europe'
        NORTH_AMERICA = 'North America'
        ASIA_PACIFIC = 'Asia Pacific'

        def __str__(self):
            return self.value

    __hour_of_day_offset = {
        Region.EUROPE: 0,
        Region.NORTH_AMERICA: -5,
        Region.ASIA_PACIFIC: +7
    }

    @unique
    class CountryCode(Enum):
        USA = 'USA'
        GREAT_BRITAIN = 'GBR'
        AUSTRALIA = 'AUS'
        POLAND = 'POL'
        ICELAND = 'ISL'
        HONG_KONG = 'HKG'

        def __str__(self):
            return self.value

    __countries = {
        # Mnemonic (key) : name, probability of host in region, compute cost, tier, region
        CountryCode.USA: ['United States', 0.2, 0.6, Tier.MID, Region.NORTH_AMERICA],
        CountryCode.GREAT_BRITAIN: ['Great Britain', 0.2, 0.6, Tier.MID, Region.EUROPE],
        CountryCode.AUSTRALIA: ['Australia', 0.1, 0.95, Tier.LOW, Region.ASIA_PACIFIC],
        CountryCode.POLAND: ['Poland', 0.05, 0.8, Tier.LOW, Region.EUROPE],
        CountryCode.ICELAND: ['Iceland', 0.4, 0.5, Tier.TOP, Region.EUROPE],
        CountryCode.HONG_KONG: ['Hong Kong', 0.05, 0.95, Tier.MID, Region.ASIA_PACIFIC]
    }

    # Probability distribution of availability of compute types
    # gpu, compute, batch as per Core.core_type()
    __p_dist_capacity = {
        Tier.TOP: [0.75, 0.25, 0.00],
        Tier.MID: [0.20, 0.70, 0.10],
        Tier.LOW: [0.00, 0.20, 0.80]
    }

    __country_codes = deepcopy(list(__countries.keys()))
    __sorted_country_codes = sorted(__country_codes, key=lambda x: x.value)
    __p_dist = list(map(lambda x: x[1], __countries.values()))

    __all_data_centers = {}

    def __init__(self,
                 country_code: CountryCode):
        if country_code in self.__all_data_centers:
            ValueError(country_code.value + ' : Data Center already exists')
        self._country_code = deepcopy(country_code)
        self.__all_data_centers[country_code] = self

    @classmethod
    def next_data_center_by_p_dist(cls) -> 'DataCenter':
        """
        Pick an existing data center from the existing DC's according to the probability distribution. There
        will be a bias if not all data centers are created as we pick only from existing DC's
        :return: An existing Data Center
        """
        if cls.__all_data_centers is None:
            return None

        dc_by_dist = None
        while dc_by_dist is None:
            dc_pick_by_dist = cls.__country_codes[
                np.random.choice(np.arange(0, len(cls.__country_codes)), p=cls.__p_dist)]
            cc = DataCenter.CountryCode(dc_pick_by_dist)
            if cc in cls.__all_data_centers:
                dc_by_dist = cls.__all_data_centers[cc]
        return dc_by_dist

    def local_hour_of_day(self,
                          gmt_hour_of_day: int) -> int:
        """
        The local hour of the day for the timezone of the data center
        :param gmt_hour_of_day: The hour of day at GMT
        :return: The local hour of the day 0 - 23
        """
        os = self.__hour_of_day_offset[self.region]
        hod = gmt_hour_of_day + os
        if hod < 0:
            hod += 23
        if hod > 23:
            hod -= 23
        return hod

    @classmethod
    def country_codes(cls) -> List['DataCenter.CountryCode']:
        """
        The list of Country Mnemonics
        :return: An alphabetical list of three character country mnemonics
        """
        return deepcopy(cls.__sorted_country_codes)

    @property
    def core_p_dist(self):
        return deepcopy(self.__p_dist_capacity[self.performance_tier])

    @property
    def country_mnemonic(self) -> 'DataCenter.CountryCode':
        """
        The country Code
        :return: the country for the country location of the data centre
        """
        return deepcopy(self._country_code.value)

    @property
    def country_name(self):
        """
        The long name of the country
        :return: A string of the long name of the country
        """
        return deepcopy((self.__countries[self._country_code])[self.__name_i])

    @property
    def compute_cost(self):
        """
        The compute cost for country in range 0 to 1
        :return: A decimal in range 0 to 1 - where 1 = max unit compute cost
        """
        return deepcopy((self.__countries[self._country_code])[self.__compute_cost_i])

    @property
    def performance_tier(self):
        """
        The performance tier of the country Top, Mid, Low
        :return: A String Mnemonic of the performance tier
        """
        return deepcopy((self.__countries[self._country_code])[self.__performance_tier_i])

    @property
    def region(self):
        """
        The performance tier of the country Top, Mid, Low
        :return: A String Mnemonic of the performance tier
        """
        return deepcopy((self.__countries[self._country_code])[self.__region_i])

    def __str__(self):
        """
        Details of the Country as string
        :return: A String containing all details of the country.
        """
        return ''.join(
            (self._country_code.value, ':',
             self.country_name, '-',
             'Cost:', str(self.compute_cost), '-',
             self.performance_tier.value, '-',
             self.region.value
             )
        )


if __name__ == "__main__":

    print("\n--- 1 ---\n")
    _ = DataCenter(DataCenter.CountryCode.GREAT_BRITAIN)
    for i in range(0, 10):
        print(DataCenter.next_data_center_by_p_dist())

    print("\n--- 2 ---\n")
    _ = DataCenter(DataCenter.CountryCode.USA)
    _ = DataCenter(DataCenter.CountryCode.AUSTRALIA)
    _ = DataCenter(DataCenter.CountryCode.ICELAND)
    for i in range(0, 10):
        print(DataCenter.next_data_center_by_p_dist())
