import copy
import io
import time
from enum import Enum
from typing import List, NoReturn


class TimeType(Enum):
    # 秒
    second = 's'
    # 毫秒
    millisecond = 'ms'
    # 纳秒
    nanosecond = 'ns'


class BaseWatch(object):

    @staticmethod
    def _timestamp_to_nanos(t: float) -> int:
        # 获取微秒级
        return int(round(t * 1000000))

    @staticmethod
    def _timestamp_to_millis(t: float) -> int:
        # 获取毫秒级
        return int(round(t * 1000))


class StopWatch(BaseWatch):
    class TaskInfo(BaseWatch):

        def __init__(self, task_name: str, timestamp: float):
            self.task_name = task_name
            self.timestamp = timestamp

        def get_time_nanos(self) -> int:
            return self._timestamp_to_nanos(self.timestamp)

        def get_time_millis(self) -> int:
            return self._timestamp_to_millis(self.timestamp)

        def get_time_seconds(self) -> float:
            return self.timestamp

    __current_task_name: str or None = None
    __start_time_timestamp: float = None
    __total_time_timestamp: float = 0.0
    __last_task_info: TaskInfo = None

    __task_info: List[TaskInfo] = None

    __task_count: int = None

    def __init__(
            self,
            unique_id: str,
            keep_task_list: bool = True,
            time_type: TimeType = TimeType.millisecond,
    ):
        """
        stop_watch计时器
        **线程不安全** 请在使用时 实例化新对象进行计时
        :param unique_id: 计时器的唯一标识，一般起比较有特点的名称
        :param keep_task_list: 是否保存单个计时点(计时任务)的信息
        :param time_type: 计时器输出的时间单位 默认毫秒
        eg:
            sw = StopWatch('计时器唯一名称', time_type=TimeType.second)
            sw.start('我是计时点1')
            time.sleep(1)
            # 计时点1计时结束
            sw.stop()

            sw.start('我是计时点2')
            time.sleep(2)
            # 计时点2计时结束
            sw.stop()
            print(sw.pretty_print())

        output:
            stopWatch [我是一个计时器]: running time = 3.0048 s
            ---------------------------------------------
            s             %         Task name
            ---------------------------------------------
            0000001.0043  033.42%  我是计时点1
            0000002.0005  066.58%  我是计时点2
        """
        self.__unique_id = unique_id
        self.__keep_task_list = keep_task_list
        self.__time_type = time_type

        self.__task_info = list()
        self.__task_count = 0

    def start(self, task_name: str = '') -> NoReturn:
        """
        开始计时
        :param task_name: 计时任务(计时点)的名称
        :return
        """
        if self.__current_task_name is not None:
            raise ValueError('Can\'t start StopWatch: it\'s already running')

        self.__current_task_name = task_name
        self.__start_time_timestamp = time.time()

    def stop(self) -> NoReturn:
        """
        停止任务计时
        :return
        """
        if self.__current_task_name is None:
            raise ValueError('Can\'t stop StopWatch: it\'s not running')

        last_time: float = time.time() - self.__start_time_timestamp
        self.__total_time_timestamp += last_time
        self.__last_task_info = self.TaskInfo(self.__current_task_name, last_time)
        if self.__keep_task_list:
            self.__task_info.append(self.__last_task_info)

        self.__task_count += self.__task_count
        self.__current_task_name = None

    def is_running(self) -> bool:
        """
        计时器是否运行
        """
        return self.__current_task_name is None

    @property
    def current_task_name(self) -> str or None:
        """
        返回当前任务名称
        :return:
        """
        return self.__current_task_name

    def get_last_task_time_nanos(self) -> int:
        """
        获取最后一次计时任务的时间(微秒)
        :return:
        """
        if self.__last_task_info is None:
            raise ValueError('No tasks run: can\'t get last task interval')

        return self._timestamp_to_nanos(self.__last_task_info.timestamp)

    def get_last_task_time_millis(self) -> int:
        """
        获取最后一次计时任务的时间(毫秒)
        :return:
        """
        if self.__last_task_info is None:
            raise ValueError('No tasks run: can\'t get last task interval')

        return self._timestamp_to_millis(self.__last_task_info.timestamp)

    def get_last_task_time_seconds(self) -> float:
        """
        获取最后一次计时任务的时间(秒)
        :return:
        """
        if self.__last_task_info is None:
            raise ValueError('No tasks run: can\'t get last task interval')

        return self.__last_task_info.timestamp

    def get_last_task_name(self) -> str:
        """
        获取最后一次计时任务的名称
        :return:
        """
        if self.__last_task_info is None:
            raise ValueError('No tasks run: can\'t get last task name')

        return self.__last_task_info.task_name

    def get_last_task_info(self) -> TaskInfo:
        """
        返回最后一个任务
        :return:
        """
        return self.__last_task_info

    def get_total_time_nanos(self) -> int:
        """
        获取当前stop_watch总计时的时间(微秒)
        :return:
        """
        return self._timestamp_to_nanos(self.__total_time_timestamp)

    def get_total_time_millis(self) -> int:
        """
        获取当前stop_watch总计时的时间(毫秒)
        :return:
        """
        return self._timestamp_to_millis(self.__total_time_timestamp)

    def get_total_time_seconds(self) -> float:
        """
        获取当前stop_watch总计时的时间(秒)
        :return:
        """
        return self.__total_time_timestamp

    def get_task_count(self) -> int:
        """
        获取当前stop_watch对象记录的任务数
        :return:
        """
        return self.__task_count

    def get_task_info(self) -> List[TaskInfo]:
        """
        获取当前stop_watch对象记录的全部任务
        :return:
        """
        if not self.__keep_task_list:
            raise RuntimeError('task info is not being kept!')
        return copy.deepcopy(self.__task_info)

    def short_summary(self, time_type: TimeType = None) -> str:
        """
        获取当前统计时间数据简述
        :param time_type: 计时器输出的时间单位, 如果在此传入，则覆盖掉类构造函数中传入的 time_type
        :return:
        """
        time_type = time_type or self.__time_type
        if time_type == TimeType.millisecond:
            running_time = self.get_total_time_millis()
        elif time_type == TimeType.nanosecond:
            running_time = self.get_total_time_nanos()
        else:
            running_time = round(self.get_total_time_seconds(), 4)
        return f'StopWatch [{self.__unique_id}]: running time = {running_time} {time_type.value}'

    def pretty_print(self, time_type: TimeType = None) -> str:
        """
        获取当前统计时间数据详情 并生成字符串
        :param time_type: 计时器输出的时间单位, 如果在此传入，则覆盖掉类构造函数中传入的 time_type
        :return:
        """
        time_type = time_type or self.__time_type
        sb = io.StringIO()
        sb.write(self.short_summary())
        sb.write('\n')
        if not self.__keep_task_list:
            sb.write('No task info kept')
        else:
            sb.write('---------------------------------------------\n')
            sb.write(f'{time_type.value}            %         Task name\n')
            sb.write('---------------------------------------------\n')
            for task_info in self.__task_info:
                if time_type == TimeType.millisecond:
                    sb.write(f'{str(task_info.get_time_millis()).zfill(12)}  ')
                elif time_type == TimeType.nanosecond:
                    sb.write(f'{str(task_info.get_time_nanos()).zfill(12)}  ')
                else:
                    sb.write(f'{format(task_info.get_time_seconds(), ".4f").zfill(12)}  ')
                percent = task_info.get_time_seconds() / self.get_total_time_seconds()
                sb.write(f'{str(format(percent * 100, ".2f")).zfill(6)}%  ')
                sb.write(f'{task_info.task_name}\n')
        return sb.getvalue()

    def __str__(self):
        sb = io.StringIO()
        sb.write(self.short_summary())
        if not self.__keep_task_list:
            sb.write('; no task info kept')
        else:
            for task_info in self.__task_info:
                sb.write(f'; [')
                sb.write(f'{task_info.task_name}')
                sb.write('] took ')
                sb.write(f'{task_info.get_time_nanos()} ns')
                sb.write(f' = {round(task_info.get_time_seconds() / self.get_total_time_seconds(), 2)}%')
        return sb.getvalue()
