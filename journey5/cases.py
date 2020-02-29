from typing import Tuple
from collections.abc import Iterable
from journey5.datacenter import DataCenter
from journey5.host import Host
from journey5.app import App
from journey5.infrnditer import InfRndIter
from journey5.policy import Policy
from journey5.seqpolicy import SequentialPolicy
from journey5.fixedtaskprofile import FixedTaskProfile
from journey5.fixedhostprofile import FixedHostProfile
from journey5.fixedcoreprofile import FixedCoreProfile
from journey5.cputype import CPUType
from journey5.task import Task
from journey5.core import Core
from journey5.case import Case


class Cases:
    """
    Definitions for all of the test case set-ups
    """

    class ComputeRestricted(Case):
        @classmethod
        def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
            """
            Set-up the environment for a schedule test case.
            Case tests where compute is restricted and app fails over to a second bigger compute
            """
            num_host = 2
            num_app = 1
            num_run_days = 3

            dc = DataCenter(DataCenter.CountryCode.ICELAND)  # Create a single DC Only.

            fhp1 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=2)), mem=16)
            h1 = Host(dc, fhp1)  # Create first low spec host

            fhp2 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=16)), mem=256)
            h2 = Host(dc, fhp2)  # Create another high spec host

            policy = SequentialPolicy(h1, h2)

            ftp = FixedTaskProfile(max_mem=4,
                                   mem_vol=0,
                                   cpu_type=CPUType.GENERAL,
                                   load_factor=5,
                                   load_profile=Task.LoadProfile.SAW_TOOTH,
                                   run_time=30)

            app1 = App(ftp)  # Create a new app in line with task policy
            policy.select_optimal_compute(app1).associate_task(app1)

            compute_iter = InfRndIter(Host.all_hosts())

            return num_host, num_app, policy, compute_iter, num_run_days

    class MemoryRestricted(Case):
        @classmethod
        def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
            """
            Set-up the environment for a schedule test case.
            Test the case where teh App runs out of memory and fails over to second compute
            """
            num_host = 2
            num_app = 1
            num_run_days = 3

            dc = DataCenter(DataCenter.CountryCode.ICELAND)  # Create a single DC Only.

            fhp1 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=4)), mem=16)
            h1 = Host(dc, fhp1)  # Create first low spec host

            fhp2 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=4)), mem=32)
            h2 = Host(dc, fhp2)  # Create another high spec host

            policy = SequentialPolicy(h1, h2)

            ftp = FixedTaskProfile(max_mem=18,
                                   mem_vol=0,
                                   cpu_type=CPUType.GENERAL,
                                   load_factor=1,
                                   load_profile=Task.LoadProfile.SAW_TOOTH,
                                   run_time=30)

            app1 = App(ftp)  # Create a new app in line with task policy
            policy.select_optimal_compute(app1).associate_task(app1)

            compute_iter = InfRndIter(Host.all_hosts())

            return num_host, num_app, policy, compute_iter, num_run_days

    class MultiDataCenterRestricted(Case):
        @classmethod
        def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
            """
            Set-up the environment for a schedule test case.
            Apps failing over between data centers.
            """
            num_host = 2
            num_app = 1
            num_run_days = 3

            dc1 = DataCenter(DataCenter.CountryCode.ICELAND)
            dc2 = DataCenter(DataCenter.CountryCode.GREAT_BRITAIN)

            fhp1 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=4)), mem=16)
            h1 = Host(dc1, fhp1)  # Create first low spec host

            fhp2 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=4)), mem=32)
            h2 = Host(dc2, fhp2)  # Create another high spec host

            policy = SequentialPolicy(h1, h2)

            ftp = FixedTaskProfile(max_mem=18,
                                   mem_vol=0,
                                   cpu_type=CPUType.GENERAL,
                                   load_factor=1,
                                   load_profile=Task.LoadProfile.SAW_TOOTH,
                                   run_time=15)

            app1 = App(ftp)  # Create a new app in line with task policy
            policy.select_optimal_compute(app1).associate_task(app1)

            compute_iter = InfRndIter(Host.all_hosts())

            return num_host, num_app, policy, compute_iter, num_run_days

    class CoreDemandActualMistMatch(Case):
        @classmethod
        def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
            """
            A task running on a core that is not it's target core
            """
            num_host = 1
            num_app = 1
            num_run_days = 2

            dc1 = DataCenter(DataCenter.CountryCode.ICELAND)

            fhp1 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GPU, core_count=4)), mem=10)
            h1 = Host(dc1, fhp1)  # Create first low spec host

            policy = SequentialPolicy(h1, h1)

            ftp = FixedTaskProfile(max_mem=5,
                                   mem_vol=0,
                                   cpu_type=CPUType.GENERAL,
                                   load_factor=20,
                                   load_profile=Task.LoadProfile.SAW_TOOTH,
                                   run_time=30)

            app1 = App(ftp)  # Create a new app in line with task policy
            policy.select_optimal_compute(app1).associate_task(app1)

            compute_iter = InfRndIter(Host.all_hosts())

            return num_host, num_app, policy, compute_iter, num_run_days
