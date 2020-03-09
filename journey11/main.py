from journey11.lib.simpleswarmenv import SimpleSwarmEnv
from journey11.lib.simplescenario import SimpleScenario
from journey11.lib.simpletaskpool import SimpleTaskPool
from lib.stateeffortmap import StateEffortMap

if __name__ == "__main__":

    ss = SimpleScenario(StateEffortMap.RANDOM)

    stp = SimpleTaskPool(ss.tasks())

    sse = SimpleSwarmEnv(stp)

    for i in range(0, 5):
        sse.associate()
