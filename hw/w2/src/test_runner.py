import argparse
import unittest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests'))

from NUM import NUM
from tests.test_num import TestNUM
from tests.test_sym import TestSYM
from tests.test_cols import TestCOLS
from tests.test_data import TestDATA

class CollectAfterT(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, [option_string] + values)

def run_tests(test_name):
    suiteNUM = unittest.TestLoader().loadTestsFromTestCase(TestNUM)
    suiteSYM = unittest.TestLoader().loadTestsFromTestCase(TestSYM)
    suiteCOL = unittest.TestLoader().loadTestsFromTestCase(TestCOLS)
    suiteDATA = unittest.TestLoader().loadTestsFromTestCase(TestDATA)

    suite = unittest.TestSuite([suiteNUM, suiteSYM, suiteDATA, suiteCOL])
    suite_all = unittest.TestSuite([suiteNUM, suiteSYM, suiteDATA, suiteCOL])


    if "all" in test_name:
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        return len(result.failures)
        
    else:
        filtered_suite = unittest.TestSuite()
        for test_class in suite:
            for test in test_class:
                test_id_parts = test.id().split('.')
                test_name_ex = test_id_parts[-1]
                if any(name == test_name_ex for name in test_name):
                    filtered_suite.addTest(test)
        suite = filtered_suite
        suite = unittest.TestSuite([test for test in suite if any(name in test.id() for name in test_name)])


    if(len(suite._tests)==0):
        print("No tests found for: ", test_name)
        print("Available Tests are:")
        for test_class in suite_all:
            for test in test_class:
                test_id_parts = test.id().split('.')
                test_name_ex = test_id_parts[-1]
                print(test_name_ex)
        return 1
    
    

    return len(result.failures)

def test(arg):
    # args = sys.argv[1:]
    # test_index = args.index('-t') if '-t' in args else args.index('--test') if '--test' in args else -1

    # if test_index != -1:
    #     next_option_index = next((i for i, arg in enumerate(args[test_index + 1:], start=test_index + 1) if arg.startswith('-')), len(args))
    #     test_args = args[test_index + 1:next_option_index]
    #     print(f"Running tests: {test_args}\n")
    

    fail_count = run_tests(arg)

    if fail_count > 0:
        exit(fail_count)

if __name__ == '__main__':
    test()