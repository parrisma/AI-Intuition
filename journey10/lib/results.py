from typing import List
from enum import Enum, unique
import numpy as np


class Results:
    @unique
    class Cols(Enum):
        FAIL_RATE = 0
        NUM_CYCLES = 1
        LEAD_TIMES = 2

    def __init__(self):
        self._res = dict()
        return

    def store(self,
              result_set_id: int,
              num_cycles: int,
              lead_times: List,
              fail_rate: float):
        if result_set_id not in self._res:
            self._res[result_set_id] = list()

        self._res[result_set_id].append([fail_rate, num_cycles, lead_times])
        return

    def summary(self,
                print_res: bool = False):
        all_res = list()
        for k in self._res.keys():
            all_cycles = list()
            all_lead_times = list()
            for res_set in self._res[k]:
                all_cycles.append(res_set[self.Cols.NUM_CYCLES.value])
                all_lead_times.extend(res_set[self.Cols.LEAD_TIMES.value])
            np_all_cycles = np.array(all_cycles)
            np_all_lead_time = np.array(all_lead_times)
            all_res.append([np.min(np_all_cycles),
                            np.max(np_all_cycles),
                            np.mean(np_all_cycles),
                            np.std(np_all_cycles),
                            np.min(np_all_lead_time),
                            np.max(np_all_lead_time),
                            np.mean(np_all_lead_time),
                            np.std(np_all_lead_time)
                            ]
                           )
        if print_res:
            self._print_res(all_res)
        return all_res

    @classmethod
    def _print_res(cls,
                   all_res: List[List]) -> None:
        print(
            "cycle_min, cycle_max, cycle_mean, cycle_std, lead_time_min, lead_time_max, lead_time_mean, lead_time_std"
        )
        for r in all_res:
            print("{:0.4f},{:0.4f},{:0.4f},{:0.4f},{:0.4f},{:0.4f},{:0.4f},{:0.4f}".format(r[0], r[1], r[2], r[3],
                                                                                           r[4], r[5], r[6], r[7]))
        return
