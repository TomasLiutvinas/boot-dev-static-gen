import unittest

from main import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_to_extract_title(self):
        expected = "asd"
        markdown = """
# asd 
asd
"""
        res = extract_title(markdown)
        self.assertEqual(res, expected)

    def test_to_extract_title_crash(self):
        markdown = """
asd 
asd
"""
        with self.assertRaises(Exception, msg="No title"):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
