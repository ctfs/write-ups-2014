import os.path

# From this package
import lib.error as error
import lib.test_framework as test_framework
import lib.util as util

class Runner(test_framework.AbstractRunner):
    LEVEL = 0

    def __init__(self, options):
        self.dictionary_path = options["dictionary_path"]
        super(Runner, self).__init__(options)

    def subprocess_command(self):
        return [self.executable_path(), self.dictionary_path]

    def executable_path(self):
        return os.path.join(os.path.dirname(__file__), "..", "level0")

    def report_result(self, test_case, result):
        benchmark_output = test_case['output']
        benchmark_time = test_case['wall_clock_time']

        your_output = result['output']
        your_time = result['wall_clock_time']

        returncode = result['exitstatus']

        if returncode != 0:
            util.logger.info('Your process exited uncleanly. Exit code: %i',
                        result['returncode'])
        elif benchmark_output == your_output:
            time_ratio = (your_time + 0.0) / benchmark_time
            msg = ("Test case passed. Your time: %(your_time)f seconds. Benchmark time: "
                   "%(benchmark_time)f seconds. You/Benchmark: %(time_ratio)f")
            util.logger.info(msg,
                        {"your_time": your_time,
                         "benchmark_time": benchmark_time,
                         "time_ratio": time_ratio}
                        )
        else:
            msg = ("Test case failed. Your time: %(your_time)f. "
                   "Benchmark time: %(benchmark_time)f")
            util.logger.error(msg, {"your_time": your_time, "benchmark_time": benchmark_time})
            self.log_diff(benchmark_output, your_output)
