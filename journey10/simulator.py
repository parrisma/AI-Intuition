from typing import Tuple, List
import random
import numpy as np
from journey10.actor import Actor
from journey10.simplescenario import SimpleScenario
from journey10.stateeffortmap import StateEffortMap
from journey10.results import Results

random.seed(42)


def sim(fr: float,
        scenario: List[List[Actor]]
        ) -> Tuple[int, List]:
    scenario[4][0].failure_rate = fr

    lead_times = list()
    cycle = 0
    done = False
    while not done:
        debug = False
        if cycle > 8000:
            debug = True

        done = True
        for ap, _, _ in scenario:
            if debug:
                print(str(ap))
            done = done and ap.done
        if debug:
            print('--')

        for ap, _, _ in scenario:
            ap.do_work()

        for ap, an, af in scenario:
            td = ap.task_out()
            while td is not None:
                if an is not None:
                    if td.failed:
                        td.failed = False
                        td.state = af.from_state
                        af.task_in(td)
                        if debug:
                            print("Fail: " + str(td))
                    else:
                        an.task_in(td)
                else:
                    lead_times.append(td.lead_time)
                    if debug:
                        print("Done: " + str(td))
                td = ap.task_out()
        cycle += 1

    print(end=" " + str(cycle))
    return cycle, lead_times


if __name__ == "__main__":

    scenario = SimpleScenario(100, StateEffortMap.FIXED_MID)
    res = Results()
    num_steps = 50
    num_tests = 10

    for j in range(0, num_tests):
        fr = 0.0
        print(str(j))
        for i in range(0, num_steps):
            print("", end=".")
            scenario.reset()
            fr += .8 / num_steps
            cyc, lt = sim(fr, scenario.get())
            res.store(result_set_id=i, num_cycles=cyc, lead_times=lt, fail_rate=fr)
        print("")
    res.summary(print_res=True)
