from journey11.interface.taskpool import TaskPool
from journey11.lib.simpleswarmenv import SimpleSwarmEnv
from journey11.lib.simplescenario import SimpleScenario
from journey11.lib.simpletaskpool import SimpleTaskPool
from journey10.stateeffortmap import StateEffortMap

if __name__ == "__main__":

    ss = SimpleScenario(StateEffortMap.RANDOM)

    stp = SimpleTaskPool()
    stp.add(ss.tasks())

    for _ in range(0, 10):

    sse = SimpleSwarmEnv()
    for i in range(0, 5):
        sse.associate()
