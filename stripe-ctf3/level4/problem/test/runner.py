import os.path
import subprocess
import time
import signal

# From this package
import lib.error as error
import lib.util as util
import lib.test_framework as test_framework

class Runner(test_framework.AbstractRunner):
    LEVEL = 4
    DURATION = "30s"
    OPEN_CUT = '-' * 20 + '8<' + '-' * 20
    CLOSE_CUT = '-' * 20 + '>8' + '-' * 20

    def __init__(self, options):
        # self.results_path = os.path.join(test_framework.data_directory, "results.json")
        self.results_path = "/tmp/octopus/results.json"
        super(Runner, self).__init__(options)

    def signame(self, signum):
        sigmap = dict((k, v) for v, k in signal.__dict__.iteritems() if v.startswith('SIG'))
        sigmap[signum]

    def run_input(self, input):
        # Make sure results file is absent
        try:
            os.remove(self.results_path)
        except OSError:
            pass

        util.logger.info("Beginning run.")
        try:
            # TODO: handle non-zero return codes here better
            octopus = subprocess.Popen(["./octopus", "--seed", str(input), "-w", self.results_path, "-duration", str(self.DURATION)], cwd=os.path.dirname(__file__))
        except OSError as e:
            raise Exception("Experienced an error trying to run Octopus: %s. (Hint: try removing `test/data/octopus.version` and running the harness again.)" % (e, ))

        start_time = time.time()
        octopus.communicate()
        end_time = time.time()

        try:
            f = open(self.results_path)
            results = f.read()
            f.close()
        except IOError:
            results = None
        else:
            results = util.json.loads(results)

        if octopus.returncode >= 0:
            exitstatus = octopus.returncode
            termsig = None
        else:
            exitstatus = None
            termsig = octopus.returncode

        util.logger.info("Finished run")
        return {
            "wall_clock_time": end_time - start_time,
            "input": input,
            "level": self.LEVEL,
            "exitstatus": exitstatus,
            "termsig": termsig,
            "raw_results": results,
        }

    def net_score(self, your_total, benchmark_total):
        total_ratio = (your_total + 0.0) / benchmark_total * 100
        return max(int(round(total_ratio)), 0)

    def report_result(self, test_case, result):
        exitstatus = result["exitstatus"]
        termsig = result["termsig"]

        your_results = result["raw_results"]
        benchmark_results = test_case["raw_results"]

        if exitstatus:
            util.logger.info("Octopus exited with status %d. This isn't expected. (The output above should indicate what actually went wrong.)" % (exitstatus, ))
        elif termsig:
            name = self.signame(termsig)
            util.logger.info("Octopus was terminated by signal %s [signal number %d]. That was presumably something you did manually?" % (name, termsig))

        if your_results:
            your_total = your_results["Total"]
            benchmark_total = benchmark_results["Total"]
            score = self.net_score(your_total, benchmark_total)

            util.logger.info("".join(
                [self.OPEN_CUT, "\n", your_results["Pretty"], self.CLOSE_CUT]
            ))

            disqualifier = your_results["Disqualifier"]
            if not disqualifier:
                if your_total < 0:
                    util.logger.info("Your normalized score works out to %d (we cap at zero). For reference, our benchmark scored %d [queries] - %d [network] = %d points on this test case." % (score, benchmark_results["QueryPoints"], benchmark_results["BytePoints"], benchmark_results["Total"]))
                else:
                    util.logger.info("Your normalized score works out to %d. (Our benchmark scored %d [queries] - %d [network] = %d points on this test case.)" % (score, benchmark_results["QueryPoints"], abs(benchmark_results["BytePoints"]), benchmark_results["Total"]))
        else:
            pass # dqd
