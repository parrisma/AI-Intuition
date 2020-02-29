from typing import Tuple
import random
import numpy as np
from journey10.state import State
from journey10.simpletask import SimpleTask
from journey10.simpleactor import SimpleActor
from journey10.stateeffortmap import StateEffortMap


# random.seed(42)


def sim(fr: float) -> Tuple[float, float, float, float]:
    sem = StateEffortMap.RANDOM
    fail_rate = fr
    a1 = SimpleActor("A1", State.S0, State.S1, 0.0, 10)
    a2 = SimpleActor("A2", State.S1, State.S2, 0.0, 10)
    a3 = SimpleActor("A3", State.S2, State.S3, 0.0, 5)
    a4 = SimpleActor("A4", State.S3, State.S4, 0.0, 10)
    a5 = SimpleActor("A5", State.S4, State.S5, fail_rate, 10)
    a6 = SimpleActor("A6", State.S5, State.S6, 0.0, 10)

    actors = [[a1, a2, a1],
              [a2, a3, a1],
              [a3, a4, a1],
              [a4, a5, a1],
              [a5, a6, a1],
              [a6, None, a1]
              ]

    SimpleTask.process_start_state(State.S0)
    SimpleTask.process_end_state(State.S6)

    lead_time_min = 1e9
    lead_time_max = -1e9
    lead_time_avg = 0

    for i in range(1, 50):
        t = SimpleTask(sem)
        # print(t)
        actors[0][0].task_in(t)

    cycle = 0
    done = False
    while not done:
        # print(str(cycle))

        done = True
        for ap, _, _ in actors:
            # print(str(ap))
            done = done and ap.done

        for ap, _, _ in actors:
            ap.do_work()

        for ap, an, af in actors:
            td = ap.task_out()
            while td is not None:
                if an is not None:
                    if td.failed:
                        td.failed = False
                        td.state = af.from_state
                        af.task_in(td)
                    else:
                        an.task_in(td)
                else:
                    lead_time_min = min(td.lead_time, lead_time_min)
                    lead_time_max = max(td.lead_time, lead_time_max)
                    lead_time_avg += td.lead_time
                    # print("Done: " + str(td))
                td = a1.task_out()
        cycle += 1

    return float(cycle - 1), lead_time_avg / (cycle - 1), float(lead_time_min), float(lead_time_max)


if __name__ == "__main__":
    fr = 0.0
    res = np.zeros((100, 4))
    for j in range(0, 50):
        for i in range(0, 100):
            fr += .95 / 100
            r = sim(fr)
            res[i] += np.array(r)
            res[i] /= 2

    for i in range(0, 100):
        print("{0},{1},{2},{3}".format(str(res[i, 0]), str(res[i, 1]), str(res[i, 2]), str(res[i, 3])))
