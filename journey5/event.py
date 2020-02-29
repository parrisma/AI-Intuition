from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Tuple, Callable
from journey5.eventlabels import EventLabels
from journey5.compute import Compute
from journey5.task import Task
from journey5.util import Util
from journey5.seqmap import SeqMap
from journey5.jexception import JException
from enum import Enum, unique


class Event(ABC):
    @unique
    class EventType(Enum):
        AUDIT = 0
        HOST = 1
        TASK = 2
        FAIL = 3

        def __str__(self):
            return self.value

    _sep = ','
    _empty_props = ([], [])

    _seqm_event_type = SeqMap(seq_name='Event Type')
    _seqm_dc = SeqMap(seq_name='Data Centers')
    _seqm_comp = SeqMap(seq_name='Compute Id')
    _seqm_coret = SeqMap(seq_name='Core Types')
    _seqm_ncore = SeqMap(seq_name='Number of Cores')
    _seqm_memc = SeqMap(seq_name='Memory Size')
    _seqm_compm = SeqMap(seq_name='Max Compute')
    _seqm_task = SeqMap(seq_name='Task Id')
    _seqm_taskt = SeqMap(seq_name='Task Type')
    _seqm_taskd = SeqMap(seq_name='Task Done')
    _seqm_exception = SeqMap(seq_name='Exception Type')

    @classmethod
    def dump_feature_maps(cls):
        """
        Print to stdout the current state of all of the feature maps.
        :return:
        """
        print(cls._seqm_event_type)
        print(cls._seqm_dc)
        print(cls._seqm_comp)
        print(cls._seqm_coret)
        print(cls._seqm_ncore)
        print(cls._seqm_memc)
        print(cls._seqm_compm)
        print(cls._seqm_task)
        print(cls._seqm_taskt)
        print(cls._seqm_taskd)
        print(cls._seqm_exception)
        for c in cls.__subclasses__():
            c.dump_features()
        return

    @classmethod
    def separator(cls) -> str:
        """
        The character to use as field separartor
        :return: str
        """
        return cls._sep

    @property
    @abstractmethod
    def id(self) -> int:
        """
        The unique id of the event type
        :return: Event Type Id
        """
        raise NotImplementedError

    # @abstractmethod
    # def __str__(self) -> str:
    #    """
    #    The event rendered as a string
    #    :return: Event as string
    #    """
    #    raise NotImplementedError

    @abstractmethod
    def as_str(self,
               as_feature: bool = False) -> str:
        """
        The event rendered as either a regular string or as a string a features that are more applicable
        for use in AL/ML context.
        :return: Event as string
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def dump_features(cls) -> None:
        """
        Print to stdout the current state of all SeqMaps
        """
        raise NotImplementedError

    @classmethod
    def task_properties(cls,
                        task: Task,
                        as_feature: bool = False) -> Tuple[List, List]:
        """
        Extract all relevant properties from given task for event reporting
        :param task: the task object subject of the event
        :param as_feature: return the properties in feature vector form - One Hot, Normalised etc
        :return: List of task property labels, List of corresponding task property values as string
        """
        labels = EventLabels.task_labels(as_feature)
        comp = Compute.compute_linked_to_task(task)
        if comp is not None:
            comp_max_mem = comp.max_memory
        else:
            comp_max_mem = max(float(1), task.current_mem)

        props = [cls._render(str, cls._seqm_task, task.id, as_feature),
                 cls._render(str, cls._seqm_taskt, task.task_type, as_feature),
                 cls._render(str, cls._seqm_coret, task.core_type, as_feature),
                 cls._render(str, str, task.load_factor, as_feature),
                 cls._render(str, str, Util.to_pct(task.current_mem, comp_max_mem), as_feature),
                 cls._render(str, str, task.run_time, as_feature),
                 cls._render(cls._flt, cls._flt, task.compute_deficit, as_feature),
                 cls._render(cls._flt, cls._flt, task.cost, as_feature),
                 cls._render(str, str, task.curr_run_time, as_feature),
                 cls._render(str, cls._seqm_taskd, task.done, as_feature)]

        return labels, props

    @classmethod
    def compute_properties(cls,
                           compute: Compute,
                           as_feature: bool = False) -> Tuple[List, List]:
        """
        Extract all relevant properties from given compute for event reporting
        :param compute: the compute object subject of the event
        :param as_feature: return the properties in feature vector form - One Hot, Normalised etc
        :return: List of compute property labels, List of corresponding compute property values as string
        """
        labels = EventLabels.host_labels(as_feature)

        props = [cls._render(str, cls._seqm_dc, compute.data_center, as_feature),
                 cls._render(str, cls._seqm_comp, compute.id, as_feature),
                 cls._render(str, cls._seqm_coret, compute.type, as_feature),
                 cls._render(str, cls._seqm_ncore, compute.core_count, as_feature),
                 cls._render(str, cls._seqm_memc, compute.max_memory, as_feature),
                 cls._render(str, str, Util.to_pct(compute.current_memory, compute.max_memory), as_feature),
                 cls._render(str, cls._seqm_compm, compute.max_compute, as_feature),
                 cls._render(str, str, Util.to_pct(compute.current_compute, compute.max_compute), as_feature),
                 cls._render(str, str, compute.num_associated_task, as_feature)]

        return labels, props

    @classmethod
    def exception_properties(cls,
                             exception: JException,
                             as_feature: bool = False) -> Tuple[List, List]:
        """
        Extract all relevant properties from given exception for event reporting
        :param exception: the exception object subject of the event
        :param as_feature: return the properties in feature vector form - One Hot, Normalised etc
        :return: List of compute property labels, List of corresponding exception property values as string
        """
        labels = EventLabels.exception_labels(as_feature)
        props = [cls._render(str, cls._seqm_exception, exception.__class__.__name__, as_feature)]

        return labels, props

    @classmethod
    def _render(cls,
                render_func_norm: Callable,
                render_func_feature: Callable,
                value: object,
                as_feature: bool):
        """
        Render the given values as a normal event log or as feature (vector)
        :param render_func_norm: Callable to render value as normal log entry
        :param render_func_feature: Callable to render value as a feature vector item
        :param value: the value to render
        :param as_feature: Render values as feature vector item if true else render as normal log entry
        :return: The rendered value as return by the called render Callable.
        """
        if as_feature:
            return render_func_feature(value)
        else:
            return render_func_norm(value)

    @classmethod
    def zip_and_separate(cls,
                         as_feature: bool,
                         *argv,
                         separator: str = _sep + ' '):
        """
        Take an arbitrary set of paris of lists of the form List[Labels], List[Corresponding Values] and zip
        them into a single
        :param as_feature: Render only the values as we are creating a feature vector.
        :param argv: List[List[keys 1], List[Values 1],List[keys 2], List[Values 2], ...]
        :param separator: separator to add after each key value pair in the final list
        :return: List[ key1.1, value1.1, Sep, key1.2, value1.2, Sep, .. Key1.n, value1.n, Sep, Key2.1, Value2.1, Sep ..]
        """
        f = []
        for tupl in argv:
            ky, vl = tupl
            s = [separator] * len(ky)
            if as_feature:
                f = f + [e for l in list(zip(vl, s)) for e in l]  # Flatten out the tuples
            else:
                f = f + [e for l in list(zip(ky, vl, s)) for e in l]  # Flatten out the tuples
        return f

    @classmethod
    def task_and_comp_to_str(cls,
                             preamble: Tuple[List[str], List[str]],
                             task: Task = None,
                             comp: Compute = None,
                             exception: JException = None,
                             as_feature: bool = None):
        task_props = cls._empty_props
        if task is not None:
            task_props = Event.task_properties(task, as_feature)
        comp_props = cls._empty_props
        if comp is not None:
            comp_props = Event.compute_properties(comp, as_feature)
        exception_props = cls._empty_props
        if exception is not None:
            exception_props = Event.exception_properties(exception, as_feature)

        as_str = ''.join(Event.zip_and_separate(as_feature, preamble, task_props, comp_props, exception_props))
        return as_str

    @classmethod
    def _flt(cls, x: float) -> str:
        """
        Render float as a string to 4 DP
        :param x: float to render as string
        :return: string rendering of float to 4dp
        """
        return '{:.4f}'.format(x * 1.0)

    @classmethod
    def preamble(cls,
                 event: 'Event',
                 event_sub_type: str,
                 seq_map: SeqMap,
                 as_feature: bool) -> Tuple[List[str], List[str]]:
        """
        The event preamble for the log entry = event class, event sub type - rendered as either string form or as
        features
        :param event: The event to extract the preamble for
        :param event_sub_type: The sub type of the given event
        :param seq_map: The sequence map to convert the event sub type to a feature (only used if as_feature = True)
        :param as_feature: If true render as feature else as regular string
        :return: List of string event class, event sub type
        """
        if not as_feature:
            preamble = ([event.__class__.__name__ + ': '], [event_sub_type])
        else:
            preamble = (
                ['Event Type', 'Event Sub Type'],
                [cls._seqm_event_type(event.__class__.__name__), seq_map(event_sub_type)]
            )
        return preamble


class FailureEvent(Event):
    _seqm_fail_event_type = SeqMap(seq_name='Failure Event Type')

    def __init__(self,
                 exception: JException,
                 task: Task = None,
                 compute: Compute = None):
        self._task = task
        self._compute = compute
        self._exception_class = exception.__class__.__name__
        self._exception = exception

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.FAIL

    def as_str(self,
               as_feature: bool = False) -> str:
        """
        The event rendered as either a regular string or as a string a features that are more applicable
        for use in AL/ML context.
        :return: Event as string
        """
        preamble = Event.preamble(self, self._exception_class, self._seqm_fail_event_type, as_feature)
        return Event.task_and_comp_to_str(preamble, self._task, self._compute, self._exception, as_feature)

    @classmethod
    def dump_features(cls) -> None:
        """
        Print to stdout the current state of all SeqMaps
        """
        print(cls._seqm_fail_event_type)
        return


class SchedulerEvent(Event):
    _seqm_schedule_event_type = SeqMap(seq_name='Schedule Event Type')

    @unique
    class SchedulerEventType(Enum):
        START = 'Start'
        COMPLETE = 'Complete'
        NEW_DAY = 'New Day'

    def __init__(self,
                 host_event_type: SchedulerEventType):
        self._scheduler_event_type = host_event_type

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.HOST

    def as_str(self,
               as_feature: bool = False) -> str:
        """
        The event rendered as either a regular string or as a string a features that are more applicable
        for use in AL/ML context.
        :return: Event as string
        """
        preamble = Event.preamble(self, self._scheduler_event_type.value, self._seqm_schedule_event_type, as_feature)
        return Event.task_and_comp_to_str(preamble, as_feature=as_feature)

    @classmethod
    def dump_features(cls) -> None:
        """
        Print to stdout the current state of all SeqMaps
        """
        print(cls._seqm_schedule_event_type)
        return


class HostEvent(Event):
    _seqm_host_event_type = SeqMap(seq_name='Host Event Type')

    @unique
    class HostEventType(Enum):
        INSTANTIATE = 'Instantiate'
        DONE = 'Done'
        EXECUTE = 'Execute'
        ASSOCIATE = 'Associate'
        DISASSOCIATE = 'Disassociate'
        STATUS = 'Status'

    def __init__(self,
                 host_event_type: HostEventType,
                 compute: Compute,
                 task: Task = None,
                 exception: Exception = None):
        self._host_event_type = host_event_type
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)
        self._exception = exception

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.HOST

    def as_str(self,
               as_feature: bool = False) -> str:
        """
        The event rendered as either a regular string or as a string a features that are more applicable
        for use in AL/ML context.
        :return: Event as string
        """
        preamble = Event.preamble(self, self._host_event_type.value, self._seqm_host_event_type, as_feature)
        return Event.task_and_comp_to_str(preamble, self._task, self._compute, self._exception, as_feature)

    @classmethod
    def dump_features(cls) -> None:
        """
        Print to stdout the current state of all SeqMaps
        """
        print(cls._seqm_host_event_type)


class TaskEvent(Event):
    _seqm_task_event_type = SeqMap(seq_name='Task Event Type')

    @unique
    class TaskEventType(Enum):
        STATUS = 'Status'

    def __init__(self,
                 task_event_type: TaskEventType,
                 task: Task,
                 compute: Compute = None,
                 exception: Exception = None):
        self._task_event_type = task_event_type
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)
        self._exception = exception

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.TASK

    def as_str(self,
               as_feature: bool = False) -> str:
        """
        The event rendered as either a regu
        lar string or as a string a features that are more applicable
        for use in AL/ML context.
        :return: Event as string
        """
        preamble = Event.preamble(self, self._task_event_type.value, self._seqm_task_event_type, as_feature)
        return Event.task_and_comp_to_str(preamble, self._task, self._compute, self._exception, as_feature)

    @classmethod
    def dump_features(cls) -> None:
        """
        Print to stdout the current state of all SeqMaps
        """
        print(cls._seqm_task_event_type)
        return
