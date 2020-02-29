from copy import deepcopy
from typing import Tuple, Dict
from collections.abc import Iterable
from journey5.datacenter import DataCenter
from journey5.host import Host
from journey5.app import App
from journey5.infrnditer import InfRndIter
from journey5.policy import Policy
from journey5.randompolicy import RandomPolicy
from journey5.randomhostprofile import RandomHostProfile
from journey5.randomtaskprofile import RandomTaskProfile
from journey5.caseproperty import CaseProperty
from journey5.case import Case


class RandomCase(Case):
    """
    This class sets up the data centres, Hosts & Apps for a full scale case, where all items are
    created randomly and if applicable according to the defined probability distributions of the type
    """

    _num_hosts = 10
    _num_apps = 50
    _num_run_days = 50

    @classmethod
    def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
        """
        Set-up the environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :return:
            The number of hosts created
            The number of applications created
            The Host Selection Policy used by the scheduler
            The Host iterator used by the scheduler
            The number of 24 hour periods to run the schedule simulation for
        """
        policy = RandomPolicy()  # Host selected at random

        for country_code in DataCenter.country_codes():
            _ = DataCenter(country_code)

        for i in range(0, cls._num_hosts):
            dc = DataCenter.next_data_center_by_p_dist()  # Pick a data centre according to DC distribution
            rhp = RandomHostProfile()
            _ = Host(dc, rhp)  # Create a Host in the chosen Data Centre

        for i in range(0, cls._num_apps):
            rtp = RandomTaskProfile()
            App(rtp)  # Create a new random app

        app_list = App.all_tasks()
        for app in app_list:
            hst = policy.select_optimal_compute(app)
            hst.associate_task(app)

        compute_iter = InfRndIter(Host.all_hosts())

        return deepcopy(cls._num_hosts), deepcopy(cls._num_apps), policy, compute_iter, deepcopy(cls._num_run_days)

    def properties(self) -> Dict[CaseProperty, object]:
        return {
            CaseProperty.NUM_TASK: self._num_apps,
            CaseProperty.NUM_COMPUTE: self._num_hosts,
            CaseProperty.NUM_RUN_DAYS: self._num_run_days
        }
