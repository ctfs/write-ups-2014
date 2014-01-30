import os.path
import subprocess

# From this package
import lib.test_framework as test_framework
import lib.util as util

class Runner(test_framework.AbstractRunner):
    LEVEL = 2

    def __init__(self, options):
        super(Runner, self).__init__(options)
        self.secret = util.random_letters(16)
        self.client_port = "3000"
        self.backend_ports = ["3001", "3002"]
        self.results_path = os.path.join(
            test_framework.data_directory,
            "results-%s.json" % self.secret)

    def code_directory(self):
        return os.path.join(os.path.dirname(__file__), "..")

    def hook_prerun(self):
        self.run_build_sh()

    def read_result_file(self, path):
        try:
            f = open(path)
        except IOError:
            return None
        results = util.json.load(f)
        f.close()
        return results

    def score(self, results):
        return max(0.01, results['good_responses'] - results['backend_deficit'] / 8.0)

    def spinup_backend(self, port):
        return subprocess.Popen([
                os.path.join(self.code_directory(), "network_simulation", "backend.js"),
                "--secret", self.secret,
                "--in-port", port])

    # overrides
    def run_input(self, input):
        util.logger.info("Beginning run.")
        backend_runners = []
        for port in self.backend_ports:
            backend_runners.append(self.spinup_backend(port))
        shield_runner = subprocess.Popen([
            os.path.join(self.code_directory(), "shield"),
            "--in-port", self.client_port,
            "--out-ports", ",".join(self.backend_ports)])
        sword_runner = subprocess.Popen([
            os.path.join(self.code_directory(), "network_simulation", "sword.js"),
            "--secret", self.secret,
            "--out-port", self.client_port,
            "--results-path", self.results_path, input],
            stdin=subprocess.PIPE)
        # Blocks:
        stdout, stderr = sword_runner.communicate()
        for br in backend_runners: br.terminate()
        shield_runner.terminate()
        util.logger.info('Finished run')
        results = self.read_result_file(self.results_path)
        if results != None:
            output_dictionary = {
                'score': self.score(results),
                'good_responses': results['good_responses'],
                'backend_deficit': results['backend_deficit'],
                'correct': results['correct'],
                'results': results
                }
        else:
            output_dictionary = {
                'correct': False,
                'unclean_description': "`sword.js` did not write a results file"
                }
        output_dictionary.update({
            'input': input,
            'level': self.LEVEL,
            'exitstatus': sword_runner.returncode,
            })
        return output_dictionary

    def report_result(self, test_case, result):
        returncode = result['exitstatus']

        if returncode != 0:
            util.logger.info('Your `shield` exited uncleanly. Exit code: %i',
                             returncode)
        elif not result['correct']:
            util.logger.error("Test case failed. Reason: %s", result['unclean_description'])
        else:
            benchmark_score = test_case['score']
            your_score = result['score']
            score_ratio = (your_score + 0.0) / benchmark_score
            msg = ("Test case passed. Your score: %(your_score)f. Benchmark score: "
                   "%(benchmark_score)f. You/Benchmark: %(score_ratio)f.")
            util.logger.info(msg,
                             {"your_score": your_score,
                              "benchmark_score": benchmark_score,
                              "score_ratio": score_ratio}
                             )
