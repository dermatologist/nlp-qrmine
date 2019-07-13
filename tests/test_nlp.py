import io
import unittest
from qrmine import Qrmine, ReadData, Content


class NLPTest(unittest.TestCase):

    def setUp(self):
        output = io.StringIO()
        output.write('First line.\n')

        self.q = Qrmine()
        self.data = ReadData()
        self.data.read_file(output)
        self.interviews = Content(self.data.content)

    def test_something(self):
        self.assertEqual(True, True)

    def test_codedict(self):
        self.q.print_dict(self.interviews, 1)


if __name__ == '__main__':
    unittest.main()
