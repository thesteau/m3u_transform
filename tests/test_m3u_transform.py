import unittest
import pandas as pd
from src.m3u_transform import M3UTransformer


class TestM3UTransformer(unittest.TestCase):

    def setUp(self) -> None:
        settings = {'replace_file': False, 'replace_file_value': '-u', 'initiator': '001x/', 'replacement': 'sample-', 'kill_line': '##/2v', 'header': 'File'}
        self.class_under_test = M3UTransformer('test_input.m3u', settings)
        return super().setUp()

    def test_replace_lines_starting_with(self):
        input_lines = ['#EXTM3U', '001x/file1.mp3', 'file2.mp3']
        expected_output = ['#EXTM3U', 'sample-file1.mp3', 'file2.mp3']

        self.class_under_test.df = pd.DataFrame({0: input_lines})

        self.class_under_test.replace_lines_starting_with('001x/', 'sample-')

        output_lines = self.class_under_test.df[0].tolist()
        self.assertEqual(output_lines, expected_output)

    def test_delete_lines_containing(self):
        input_lines = ['#EXTM3U', 'file1.mp3', 'file2.mp3', '##/2v']
        expected_output = ['#EXTM3U', 'file1.mp3', 'file2.mp3']

        self.class_under_test.df = pd.DataFrame({0: input_lines})

        self.class_under_test.delete_lines_containing('##/2v')

        output_lines = self.class_under_test.df[0].tolist()
        self.assertEqual(output_lines, expected_output)

    def test_switch_slash_placement(self):
        input_lines = ['file1\\mp3', 'file2\\mp3']
        expected_output = ['file1/mp3', 'file2/mp3']

        self.class_under_test.df = pd.DataFrame({0: input_lines})

        self.class_under_test.switch_slash_placement()

        output_lines = self.class_under_test.df[0].tolist()
        self.assertEqual(output_lines, expected_output)


if __name__ == '__main__':
    unittest.main()
