import unittest
from sendpaste import SendPaste
import json


class TestSendPaste(unittest.TestCase):
    def setUp(self):
        data = json.dumps({
                'title': 'title',
                'snippet': 'test code here',
                'language': 'python'
            })
        self.sp = SendPaste(data=data)

    def test_send_paste(self):
        self.assertIsInstance(self.sp.send_paste(), dict, \
            msg="Connection is down")
        self.assertEqual(True, self.sp.send_paste()['ok'])
        self.assertIn('https://friendpaste.com', self.sp.send_paste()['url'])

if __name__ == '__main__':
    unittest.main()
