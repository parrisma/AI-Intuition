from interface.actor import Actor
from journey11.interface.swarmenv import SwarmEnv
from journey11.interface.taskpool import TaskPool


class SimpleSwarmEnv(SwarmEnv):

    def __init__(self,
                 task_pool: TaskPool):
        self._swarm = dict()
        self._task_pool = task_pool
        return

    def associate(self,
                  actor: Actor) -> None:
        """
        Associate the given actor with teh Swarm
        """
        pass
