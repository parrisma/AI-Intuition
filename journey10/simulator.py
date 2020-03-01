from typing import Tuple, List
import random
import numpy as np
from journey10.state import State
from journey10.simpletask import SimpleTask
from journey10.simpleactor import SimpleActor
from journey10.stateeffortmap import StateEffortMap
from journey10.fixedcapacity import FixedCapacity
from journey10.variablecapacity import VariableCapacity

random.seed(42)


def sim(fr: float,
        scenario: List[List[SimpleActor]]
        ) -> Tuple[float, float, float, float]:
    scenario[4][0].failure_rate = fr

    lead_time_min = 1e9
    lead_time_max = -1e9
    lead_time_avg = 0

    cycle = 0
    done = False
    while not done:
        debug = False
        if cycle > 5000:
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
                    lead_time_min = min(td.lead_time, lead_time_min)
                    lead_time_max = max(td.lead_time, lead_time_max)
                    lead_time_avg += td.lead_time
                    if debug:
                        print("Done: " + str(td))
                td = ap.task_out()
        cycle += 1

    print(cycle, end=" - ")
    return float(cycle - 1), lead_time_avg / (cycle - 1), float(lead_time_min), float(lead_time_max)


def create_actors() -> List[SimpleActor]:
    # cap_10 = FixedCapacity(10)
    # cap_5 = FixedCapacity(5)

    cap_10 = VariableCapacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                              [0.01, 0.01, 0.02, 0.03, 0.03, 0.05, 0.05, 0.1, 0.2, 0.5])
    cap_5 = VariableCapacity([1, 2, 3, 4, 5],
                             [.05, 0.05, 0.1, .2, .6])

    a1 = SimpleActor("A1", State.S0, State.S1, 0.0, cap_10)
    a2 = SimpleActor("A2", State.S1, State.S2, 0.0, cap_10)
    a3 = SimpleActor("A3", State.S2, State.S3, 0.0, cap_5)
    a4 = SimpleActor("A4", State.S3, State.S4, 0.0, cap_10)
    a5 = SimpleActor("A5", State.S4, State.S5, 0.0, cap_10)
    a6 = SimpleActor("A6", State.S5, State.S6, 0.0, cap_10)
    l = [a1, a2, a3, a4, a5, a6]
    return l


def create_scenario_random_no_constraint(a1: SimpleActor,
                                         a2: SimpleActor,
                                         a3: SimpleActor,
                                         a4: SimpleActor,
                                         a5: SimpleActor,
                                         a6: SimpleActor) -> List[List[SimpleActor]]:
    # [a1, a2 ,a3]
    # a1 = Actor Doing the Work at this spot
    # a2 = Next Actor to pass task to when task done
    # a3 = Actor to pass the task to if the task is reported as failed.
    #
    actor_scenario = [[a1, a2, a1],
                      [a2, a3, a1],
                      [a3, a4, a1],
                      [a4, a5, a1],
                      [a5, a6, a1],
                      [a6, None, a1]
                      ]
    return actor_scenario


def create_tasks() -> List[SimpleTask]:
    SimpleTask.process_start_state(State.S0)
    SimpleTask.process_end_state(State.S6)
    sem = StateEffortMap.RANDOM
    new_tasks = list()
    for _ in range(1, 50):
        t = SimpleTask(sem)
        new_tasks.append(t)
        # print(t)
    return new_tasks


def reset_all_and_inject_tasks(actors: List[SimpleActor],
                               scenario: List[List[SimpleActor]],
                               tasks_to_inject: List[SimpleTask]) -> None:
    for a in actors:
        a.reset()

    for t in tasks:
        t.reset()

    first_actor = scenario[0][0]
    for t in tasks_to_inject:
        first_actor.task_in(t)
    return


if __name__ == "__main__":
    # Create Actors.
    actors = create_actors()

    # Define the scenario
    scenario = create_scenario_random_no_constraint(*actors)

    # Create the tasks
    tasks = create_tasks()

    res = np.zeros((100, 4))
    for j in range(0, 10):
        fr = 0.0
        print(str(j))
        for i in range(0, 100):
            print("", end=".")
            reset_all_and_inject_tasks(actors, scenario, tasks)
            fr += .8 / 100
            r = sim(fr, scenario)
            res[i] += np.array(r)
            res[i] /= 2
        print("")

    for i in range(0, 100):
        print("{0},{1},{2},{3}".format(str(res[i, 0]), str(res[i, 1]), str(res[i, 2]), str(res[i, 3])))
