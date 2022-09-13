import time

from TimeConvert import StopWatch, TimeType


class TestStopWatch(object):
    def test_stop_watch(self):
        sw = StopWatch('我是一个计时器', time_type=TimeType.second)
        sw.start('我是计时点1')
        time.sleep(0.01)
        # 计时点1计时结束
        sw.stop()

        sw.start('我是计时点2')
        time.sleep(0.02)
        # 计时点2计时结束
        sw.stop()
        sw.pretty_print()
