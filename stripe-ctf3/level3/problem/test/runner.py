import os.path
import subprocess
import time
import sys
import urlparse
import shutil

# From this package
import lib.error as error
import lib.http_client as http_client
import lib.test_framework as test_framework
import lib.util as util

from test_case_generator import TestCaseGenerator

class Runner(test_framework.AbstractRunner):
    LEVEL = 3
    TEST_CASE_PATH = os.path.join(os.path.dirname(__file__),
                                  'data/input')

    def __init__(self, options):
        self.client = http_client.new_default_http_client()
        self.dictionary_path = options['dictionary_path']
        self.child_popens = []
        super(Runner, self).__init__(options)

    def hook_prerun(self):
        self.run_build_sh()

    # Scala compiles are slow; just let start-servers use SBT.
    def run_build_sh(self):
        pass

    def cleanup(self):
        util.logger.info('Cleaning up children')
        for popen in self.child_popens:
            util.logger.info("Killing child's pgid: %d" % popen.pid)
            os.killpg(popen.pid, 15)

    def subprocess_command(self):
        return [self.executable_path(), self.dictionary_path]

    def executable_path(self):
        return os.path.join(os.path.dirname(__file__), "..", "level0")

    def uri(self, route):
        return urlparse.urljoin('http://localhost:9090/', route)

    def execute_query(self, substring):
        return self.client.request('GET', self.uri('/?q=%s' % substring))

    def index(self, path):
        return self.client.request('GET', self.uri('/index?path=%s' % path))

    def start_servers(self):
        p = subprocess.Popen(['bin/start-servers'],
                             preexec_fn=lambda: os.setpgid(0, 0),
                             stdout=sys.stdout,
                             stderr=sys.stderr)
        self.child_popens.append(p)

    def check_server(self, path, msg, max_attempts):
        attempts = 0
        backoff = 1

        while True:
            try:
                if attempts > max_attempts:
                    raise error.StripeError("Unable to start server up")

                body, code = self.client.request('GET', path)
                if (code == 200) and ("true" in body):
                    return
            except error.HTTPConnectionError as e:
                attempts += 1
                backoff *= 2
                util.logger.info('(# %i) Sleeping for %is while server %s' % (attempts, backoff, msg))
                time.sleep(backoff)

    def write_files(self, files, base_path):
        if os.path.isdir(base_path):
            shutil.rmtree(base_path)
        for filepath, contents in files.iteritems():
            filename = os.path.join(base_path, filepath)
            file_dir = os.path.dirname(filename)

            util.mkdir_p(file_dir)
            util.logger.debug("Writing out file %s" % filepath)
            f = open(filename, 'w')
            f.write(contents)
            f.close()

        util.logger.info("All done writing out input data")

    # override
    def run_input(self, cmd_line_args):
        # Don't print out to stdout.
        options_dict = TestCaseGenerator.opt_parse(map(lambda x: str(x), cmd_line_args))
        options_dict['dictionary_path'] = self.dictionary_path
        options_dict['should_print'] = False
        test_case_input = TestCaseGenerator(options_dict).generate_test_case()

        files = test_case_input['files']
        keys = test_case_input['keys']

        path = self.TEST_CASE_PATH

        util.logger.info('Writing tree to %s', path)
        self.write_files(files, path)

        util.logger.info('Starting servers')
        self.start_servers()

        util.logger.info('Waiting for server to come up')

        self.check_server(self.uri('/healthcheck'), 'starts', 3)

        util.logger.info('Indexing %s', path)
        self.index(path)

        util.logger.info('Waiting for servers to finish indexing')
        self.check_server(self.uri('/isIndexed'), 'indexes', 8)

        responses = []

        start_time = time.time()

        for key in keys:
            body, code = self.execute_query(key)
            try:
                parsed = util.json.loads(body)
                responses.append([parsed['results'], code])
            except:
                raise error.StripeError('The search for %s returned invalid JSON: %s' % (key, body))

        end_time = time.time()

        average_response_time = (end_time - start_time) / len(keys)

        return {
            'wall_clock_time': average_response_time,
            'output': map(lambda x: x[0], responses),
            'input': cmd_line_args,
            'level': self.LEVEL,
            'exitstatus': 0,
        }

    def report_result(self, test_case, result):
        benchmark_output = test_case['output']
        benchmark_time = test_case['wall_clock_time']

        your_output = result['output']
        your_time = result['wall_clock_time']

        returncode = result['exitstatus']

        if returncode != 0:
            util.logger.info('Not all of your requests returned 200s')
        else:
            passed = True
            for (idx, your) in enumerate(your_output):
                sorted_benchmark = sorted(benchmark_output[idx])
                sorted_your = sorted(your)

                if sorted_benchmark != sorted_your:
                    passed = False
                    self.log_diff("\n".join(sorted_benchmark), "\n".join(sorted_your))

            time_ratio = (benchmark_time*1.0) / your_time
            score = round(time_ratio * 100)

            if passed:
                msg = ("Test case passed! Your time: %(your_time)f. Benchmark time: "
                       "%(benchmark_time)f. You/Benchmark: %(time_ratio)f. Score: %(score)d")
                util.logger.info(msg %
                            {"your_time": your_time,
                             "benchmark_time": benchmark_time,
                             "time_ratio": time_ratio,
                             "score": score
                            })

