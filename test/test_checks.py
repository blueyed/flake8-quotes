from flake8_quotes import QuoteChecker
import os
import subprocess
from unittest import TestCase


class TestChecks(TestCase):
    def test_get_noqa_lines(self):
        checker = QuoteChecker(None, lines=get_lines('data/no_qa.py'))
        list(checker.run())
        self.assertEqual(checker.get_noqa_lines(), [2])


class TestFlake8Stdin(TestCase):
    def test_stdin(self):
        """Test using stdin."""
        filepath = get_absolute_path('data/doubles.py')
        with open(filepath, 'rb') as f:
            p = subprocess.Popen(['flake8', '--select=Q', '-'], stdin=f,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

        stdout_lines = stdout.splitlines()
        self.assertEqual(stderr, b'')
        self.assertEqual(len(stdout_lines), 3)
        self.assertRegexpMatches(stdout_lines[0], b'stdin:1:(24|25): Q000 Remove bad quotes')
        self.assertRegexpMatches(stdout_lines[1], b'stdin:2:(24|25): Q000 Remove bad quotes')
        self.assertRegexpMatches(stdout_lines[2], b'stdin:3:(24|25): Q000 Remove bad quotes')


class DoublesTestChecks(TestCase):
    def setUp(self):
        class DoublesOptions():
            inline_quotes = '\''
            multiline_quotes = '\''
        QuoteChecker.parse_options(DoublesOptions)

    def test_multiline_string(self):
        doubles_checker = QuoteChecker(None, lines=get_lines('data/doubles_multiline_string.py'))
        self.assertEqual(list(doubles_checker.run()), [
            (1, 0, 'Q001 Remove bad quotes from multiline string', QuoteChecker),
        ])

    def test_wrapped(self):
        doubles_checker = QuoteChecker(None, lines=get_lines('data/doubles_wrapped.py'))
        self.assertEqual(list(doubles_checker.run()), [])

    def test_doubles(self):
        doubles_checker = QuoteChecker(None, lines=get_lines('data/doubles.py'))
        self.assertEqual(list(doubles_checker.run()), [
            (1, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (2, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (3, 24, 'Q000 Remove bad quotes', QuoteChecker),
        ])

    def test_noqa_doubles(self):
        checker = QuoteChecker(None, get_absolute_path('data/doubles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


class DoublesAliasTestChecks(TestCase):
    def setUp(self):
        class DoublesAliasOptions():
            inline_quotes = 'single'
            multiline_quotes = 'single'
        QuoteChecker.parse_options(DoublesAliasOptions)

    def test_doubles(self):
        doubles_checker = QuoteChecker(None, lines=get_lines('data/doubles_wrapped.py'))
        self.assertEqual(list(doubles_checker.run()), [])

        doubles_checker = QuoteChecker(None, lines=get_lines('data/doubles.py'))
        self.assertEqual(list(doubles_checker.run()), [
            (1, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (2, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (3, 24, 'Q000 Remove bad quotes', QuoteChecker),
        ])


class SinglesTestChecks(TestCase):
    def setUp(self):
        class SinglesOptions():
            inline_quotes = '"'
            multiline_quotes = '"'
        QuoteChecker.parse_options(SinglesOptions)

    def test_multiline_string(self):
        singles_checker = QuoteChecker(None, lines=get_lines('data/singles_multiline_string.py'))
        self.assertEqual(list(singles_checker.run()), [
            (1, 0, 'Q001 Remove bad quotes from multiline string', QuoteChecker),
        ])

    def test_wrapped(self):
        singles_checker = QuoteChecker(None, lines=get_lines('data/singles_wrapped.py'))
        self.assertEqual(list(singles_checker.run()), [])

    def test_singles(self):
        singles_checker = QuoteChecker(None, lines=get_lines('data/singles.py'))
        self.assertEqual(list(singles_checker.run()), [
            (1, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (2, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (3, 24, 'Q000 Remove bad quotes', QuoteChecker),
        ])

    def test_noqa_singles(self):
        checker = QuoteChecker(None, get_absolute_path('data/singles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


class SinglesAliasTestChecks(TestCase):
    def setUp(self):
        class SinglesAliasOptions():
            inline_quotes = 'double'
            multiline_quotes = 'double'
        QuoteChecker.parse_options(SinglesAliasOptions)

    def test_singles(self):
        singles_checker = QuoteChecker(None, lines=get_lines('data/singles_wrapped.py'))
        self.assertEqual(list(singles_checker.run()), [])

        singles_checker = QuoteChecker(None, lines=get_lines('data/singles.py'))
        self.assertEqual(list(singles_checker.run()), [
            (1, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (2, 24, 'Q000 Remove bad quotes', QuoteChecker),
            (3, 24, 'Q000 Remove bad quotes', QuoteChecker),
        ])


class MultilineTestChecks(TestCase):
    def test_singles(self):
        class Options():
            inline_quotes = '\''
            multiline_quotes = '"'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, lines=get_lines('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.run()), [
            (10, 0, 'Q001 Remove bad quotes from multiline string', QuoteChecker),
        ])

    def test_singles_alias(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, lines=get_lines('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.run()), [
            (10, 0, 'Q001 Remove bad quotes from multiline string', QuoteChecker),
        ])

    def test_doubles(self):
        class Options():
            inline_quotes = '"'
            multiline_quotes = '\''
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, lines=get_lines('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.run()), [
            (1, 0, 'Q001 Remove bad quotes from multiline string', QuoteChecker),
        ])

    def test_doubles_alias(self):
        class Options():
            inline_quotes = 'double'
            multiline_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, lines=get_lines('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.run()), [
            (1, 0, 'Q001 Remove bad quotes from multiline string', QuoteChecker),
        ])


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)


def get_lines(filepath):
    return open(get_absolute_path(filepath)).readlines()
