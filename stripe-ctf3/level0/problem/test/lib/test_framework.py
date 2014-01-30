import difflib
import os.path
from random import SystemRandom
import re
import subprocess
import sys
import time

# From this package
import lib.error as error
import lib.http_client as http_client
import lib.util as util

data_directory = os.path.join(os.path.dirname(__file__), "..", "data")

class TestCase(object):
    def __init__(self, harness, id_or_url):
        self.harness = harness
        self.id, self.url = self.normalize_id_and_url(id_or_url)
        self.json = None

    def normalize_id_and_url(self, id_or_url):
        if re.match("\Ahttps?:", id_or_url):
            url = id_or_url
            # Look at the last component and remove extension
            id = id_or_url.split('/')[-1].split('.')[0]
        else:
            id = id_or_url
            level = self.harness.LEVEL
            url = "https://stripe-ctf-3.s3.amazonaws.com/level%s/%s.json" % (level, id)
        return id, url

    def dump_path(self):
        return os.path.join(self.harness.test_cases_path(), self.id + ".json")

    def load(self):
        if self.json: return self.json
        try:
            f = open(self.dump_path(), "r")
            self.json = util.json.load(f)
            f.close()
            return self.json
        except IOError:
            pass
        util.logger.info('Fetching. URL: %s', self.url)
        content = self.harness.fetch_s3_resource(self.url)
        try:
            self.json = util.json.loads(content)
        except ValueError:
            # Decoding the JSON failed.
            msg = ("There was a problem parsing the test case. We expected "
                   "JSON. We received: %s" % (content,))
            raise error.StripeError(msg)
        return self.json

    def flush(self):
        f = open(os.path.join(self.harness.test_cases_path(), self.id + ".json"), "w")
        util.json.dump(self.json, f)
        f.close()

class AbstractHarness(object):
    def __init__(self, ids_or_urls=[], options={}):
        util.mkdir_p(self.test_cases_path())
        if not os.path.isfile(http_client.certs_path()):
            msg = ("You seem to have deleted the file of certificates "
                   "that shipped with this repo. It should exist "
                   "at %s" % http_client.certs_path())
            raise error.StripeError(msg)
        if ids_or_urls == []:
            util.logger.info('No test case supplied. Randomly choosing among defaults.')
            ids_or_urls = [SystemRandom().choice(self.DEFAULT_TEST_CASES)]
        self.test_cases = map(lambda token: TestCase(self, token), ids_or_urls)
        self.options = options
        headers = {
            'User-Agent': 'Stripe TestHarness/%s' % (self.VERSION,),
        }
        self.http_client = http_client.new_default_http_client(headers=headers, verify_ssl_certs=True)

    def fetch_s3_resource(self, url):
        try:
            content, status_code = self.http_client.request("get", url)
        except error.HTTPConnectionError:
            err = util.exception_as()
            msg = ("There was an error while connecting to fetch "
                   "the url %s. Please check your connectivity. If there "
                   "continues to be an issue, please let us know at "
                   "ctf@stripe.com. The specific error is:\n" % (url,))
            raise error.StripeError(msg + str(err))
        if status_code == 200:
            return content
        elif status_code == 403:
            msg = ("We received a 403 while fetching the url %s. "
                   "This probably means that you are trying to get "
                   "something that doesn't actually exist." % (url,))
            raise error.StripeError(msg)
        else:
            msg = ("We received the unexpected response code %i while "
                   "fetching the url %s." % (status_code, url,))
            raise error.StripeError(msg)

    def run(self):
        task = self.options["task"]

        if task == "execute":
            test_cases_to_execute = self.load_test_cases()
            self.execute(test_cases_to_execute)
        else:
            raise StandardError("Unrecognized task " +  task)

    def test_cases_path(self):
        return os.path.join(
            data_directory,
            "downloaded_test_cases",
            "version%i" % self.VERSION)

    def flush_test_cases(self):
        util.logger.info('Flushing. Path: %s', self.test_cases_path())
        for test_case in self.test_cases:
            test_case.flush(self.test_cases_path())

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)

    def load_test_cases(self):
        loaded_test_cases = []
        for test_case in self.test_cases:
            result = test_case.load()
            if not result: continue
            test_case.flush()
            loaded_test_cases.append(test_case)
        return loaded_test_cases

    def hook_preexecute(self):
        # May override
        pass

    def execute(self, test_cases_to_execute):
        self.hook_preexecute()
        runner = self.hook_create_runner()

        for test_case in test_cases_to_execute:
            if self.options["raw"]:
                util.logger.info(runner.run_test_case_raw(test_case.json))
            else:
                runner.run_test_case(test_case.json)

class AbstractRunner(object):
    def __init__(self, options):
        pass

    # may override
    def code_directory(self):
        return os.path.join(os.path.dirname(__file__), "..")

    def log_diff(self, benchmark_output, user_output):
        util.logger.info("Here is the head of your output:")
        util.logger.info(user_output[0:1000])
        diff = list(difflib.Differ().compare(benchmark_output.splitlines(True),
                                             user_output.splitlines(True)))
        lines = filter(lambda line: line[0] != "?", diff[0:20])
        util.logger.info("\n***********\n")
        util.logger.info("Here is the head of the diff between your output and the benchmark:")
        util.logger.info("".join(lines))

    def run_build_sh(self):
        util.logger.info("Building your code via `build.sh`.")
        build_runner = subprocess.Popen([
            os.path.join(self.code_directory(), "build.sh")],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Blocks
        stdout, stderr = build_runner.communicate()
        if build_runner.returncode == 0:
            util.logger.info("Done building your code.")
        else:
            util.logger.info("Build failed with code %i. Stderr:", build_runner.returncode)
            util.logger.info(stderr)

    # may override
    def hook_prerun(self):
        pass

    def run_test_case(self, test_case):
        self.hook_prerun()
        id = test_case['id']
        util.logger.info("About to run test case: %s" % id)
        input = test_case['input']
        result = self.run_input(input)
        return self.report_result(test_case, result)

    def run_test_case_raw(self, test_case):
        self.hook_prerun()
        input = test_case['input']
        result = self.run_input(input)
        return result['output']

    def run_input(self, input):
        util.logger.info("Beginning run.")
        output = self.run_subprocess_command(self.subprocess_command(), input)
        util.logger.info('Finished run')
        return output

    def report_stderr(self, stderr):
        if not stderr: return
        util.logger.info("Standard error from trial run:")
        util.logger.info(stderr)

    def subprocess_communicate(self, runner, input):
        if sys.version_info >= (3, 0):
            input = input.encode('utf-8')
        stdout, stderr = runner.communicate(input)
        if sys.version_info >= (3, 0):
            stderr = stderr.decode('utf-8')
            stdout = stdout.decode('utf-8')
        return stdout, stderr

    def run_subprocess_command(self, command, input):
        start_time = time.time()
        runner = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = self.subprocess_communicate(runner, input)
        end_time = time.time()
        return {
            'wall_clock_time': end_time - start_time,
            'output': stdout,
            'input': input,
            'level': self.LEVEL,
            'exitstatus': runner.returncode,
            }
