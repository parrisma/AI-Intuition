import queue
from journey10.state import State
from journey10.simpletask import SimpleTask
from journey10.simpleactor import SimpleActor
from journey10.stateeffortmap import StateEffortMap

if __name__ == "__main__":
    sem = StateEffortMap.RANDOM
    a1 = SimpleActor("A1", State.S0, State.S1)
    a2 = SimpleActor("A2", State.S1, State.S2)
    a3 = SimpleActor("A3", State.S2, State.S3)

    actors = [[a1, a2], [a2, a3], [a3, None]]

    SimpleTask.process_start_state(State.S0)
    SimpleTask.process_end_state(State.S3)

    for i in range(1, 5):
        t = SimpleTask(sem)
        print(t)
        actors[0][0].task_in(t)

    cycle = 0
    done = False
    while not done:
        print(str(cycle))

        done = True
        for ap, an in actors:
            print(str(ap))
            done = done and ap.done

        for ap, an in actors:
            ap.do_work()

        for ap, an in actors:
            td = ap.task_out()
            while td is not None:
                if an is not None:
                    an.task_in(td)
                else:
                    print("Done: " + str(td))
                td = a1.task_out()
        cycle += 1
