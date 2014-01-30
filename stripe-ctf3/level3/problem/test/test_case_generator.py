from optparse import OptionParser
import random
import string
import os
import json
import runner
import sys

class Directory(object):
    def __init__(self, name, file_count, parent=None):
        self.name = name
        self.parent = parent
        self.file_count = file_count
        self.children = []

        if self.parent != None:
            self.parent.children.append(self)

    def path(self):
        if self.parent == None:
            return self.name
        else:
            return os.path.join(self.parent.path(), self.name)

class Tree(object):
    def __init__(self, depth, root):
        self.depth = depth
        self.root = root
        self.directories = {0: [root]}

    def layers(self):
        return [self.directories[i] for i in range(self.depth)]

class TestCaseGenerator(object):
    TREE_COUNT = 3
    NUM_KEYS = 50
    MIN_WORDS = 500
    MAX_WORDS = 2000
    MAX_BRANCHES = 5
    MIN_BRANCHES = 0
    MIN_DEPTH = 2
    MAX_DEPTH = 5

    def __init__(self, options):
        self.dictionary_path = options.get('dictionary_path') or '/usr/share/dict/words'
        self.seed = options['seed']
        self.rnd = random.Random()
        self.rnd.seed(self.seed)

        self.should_print = options.get('should_print') or False

        self.tree_count = options.get('num_trees') or self.TREE_COUNT
        self.num_keys = options.get('num_keys') or self.NUM_KEYS

        self.min_words = options.get('min_words') or self.MIN_WORDS
        self.max_words = options.get('max_words') or self.MAX_WORDS

        self.min_depth = options.get('min_depth') or self.MIN_DEPTH
        self.max_depth = options.get('max_depth') or self.MAX_DEPTH

        self.min_branches = options.get('min_branches') or self.MIN_BRANCHES
        self.max_branches = options.get('max_branches') or self.MAX_BRANCHES

    def generate_test_case(self):
        out = {}
        forest, keys = self.generate_forest_and_keys(self.max_depth)

        out['files'] = forest
        out['keys'] = keys

        if self.should_print:
            print json.dumps(out)

        return out

    def generate_forest_and_keys(self, max_depth):
        words = self.dictionary_words()
        trees = []
        out = {}
        keys = []
        content_size = 0

        for i in range(self.tree_count):
            trees.append(self.make_tree())
        for tree in trees:
            for layer in tree.layers():
                for directory in layer:
                    path = directory.path()
                    for f in range(directory.file_count):
                        contents, keys_in_file = self.random_contents_and_keys(words)
                        keys += keys_in_file

                        file_path = os.path.join(path, self.random_string())
                        out[file_path] = contents
                        content_size += len(contents)

	sys.stderr.write("Number of files: %d\n" % len(out.keys()))
	sys.stderr.write("Total content size: %fMB\n" % (content_size / 1024.0 / 1024.0))
        return [out, self.rnd.sample(keys, self.num_keys)]

    def make_tree(self):
        depth = self.rnd.randint(self.min_depth, self.max_depth)
        tree = Tree(depth,
            Directory(self.random_string(),
            self.rnd.randint(1, 5)))

        for i in range(1, tree.depth):
            tree.directories[i] = []
            for parent in tree.directories[i - 1]:
                for branch in range(self.rnd.randint(self.min_branches, self.max_branches)):
                    directory = Directory(
                        self.random_string(),
                        self.rnd.randint(0, 5),
                        parent)
                    tree.directories[i].append(directory)

        return tree

    def random_contents_and_keys(self, words):
        length = self.rnd.randint(self.min_words, self.max_words)
        contents = []
        keys = []
        for i in range(length):
            word = self.rnd.choice(words)

            if self.rnd.random() > 0.70:
                keys.append(word)

            if self.rnd.random() > 0.95:
                word += '\n'
            elif self.rnd.random() > 0.90:
                word += '.'

            contents.append(word)

        return [' '.join(contents), keys]

    def dictionary_words(self):
        f = open(self.dictionary_path, 'r')
        words = f.read()
        f.close()
        return words.split('\n')

    # http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
    def random_string(self, length=8):
        character_set = string.ascii_uppercase + string.digits
        return ''.join(
            self.rnd.choice(character_set) for x in range(length))

    @staticmethod
    def opt_parse(flags):
        usage = "usage: %prog [options]"
        parser = OptionParser(usage=usage)
        parser.add_option("-s", "--seed", dest="seed", help="Seed for random generator", type=int)
        parser.add_option("-p", "--print", dest="should_print", help="Print output to stdout", action="store_true")
        parser.add_option("-t", "--num-trees", dest="num_trees", help="Number of trees to generate", type=int)
        parser.add_option("-k", "--num-keys", dest="num_keys", help="Number of keys to test against", type=int)
        parser.add_option("-x", "--min-depth", dest="min_depth", help="Minimum depth of trees", type=int)
        parser.add_option("-d", "--max-depth", dest="max_depth", help="Maximum depth of trees", type=int)
        parser.add_option("-w", "--min-words", dest="min_words", help="Minimum number of words in each file", type=int)
        parser.add_option("-m", "--max-words", dest="max_words", help="Maximum number of words in each file", type=int)
        parser.add_option("-n", "--min-branches", dest="min_branches", help="Minimum number of branches", type=int)
        parser.add_option("-b", "--max-branches", dest="max_branches", help="Maximum number of branches", type=int)

        (options, args) = parser.parse_args(flags)
        options_dict = vars(options)

        return options_dict

def main():
    default_options = {"seed": random.randint(0, 1000)}
    options_dict = TestCaseGenerator.opt_parse(sys.argv)

    for key in default_options:
        if options_dict.get(key) is None:
            options_dict[key] = default_options[key]

    generator = TestCaseGenerator(options_dict)
    tree = generator.generate_test_case()

if __name__ == "__main__":
        main()
