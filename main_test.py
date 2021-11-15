import unittest
import warnings

import urllib3

from main import PromotionFlow


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)

    return do_test


class GetCaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GetCaseTest, self).__init__(*args, **kwargs)
        self.p = PromotionFlow()

    @ignore_warnings
    def test_get_case1(self):
        urllib3.disable_warnings()
        arrange = [
            {"goodsId": "2823563800061 ", "quantity": 5},
            {"goodsId": "2824480000311 ", "quantity": 1},
        ]
        act = self.p.do_work(arrange, 1)
        self.assertEqual(act[0]['promotionId'], 'PMB211000001')
        self.assertEqual(act[1]['promotionId'], 'PMB211000001')

    @ignore_warnings
    def test_get_case2(self):
        urllib3.disable_warnings()
        arrange = [
            {"goodsId": "2823563800061 ", "quantity": 1},
            {"goodsId": "2824480000311 ", "quantity": 1},
        ]
        act = self.p.do_work(arrange, 2)
        self.assertEqual(act[0]['promotionId'], '')
        self.assertEqual(act[1]['promotionId'], '')

    @ignore_warnings
    def test_get_case3(self):
        urllib3.disable_warnings()
        arrange = [
            {"goodsId": "2823563800061 ", "quantity": 5},
            {"goodsId": "2824480000311 ", "quantity": 24},
        ]
        act = self.p.do_work(arrange, 3)
        self.assertEqual(act[0]['promotionId'], '')
        self.assertEqual(act[1]['promotionId'], 'PMB211000002')

    @ignore_warnings
    def test_get_case4(self):
        urllib3.disable_warnings()
        arrange = [
            {"goodsId": "2823563800061 ", "quantity": 6},
            {"goodsId": "2824480000311 ", "quantity": 24},
        ]
        act = self.p.do_work(arrange, 4)
        self.assertEqual(act[0]['promotionId'], 'PMB211000001')
        self.assertEqual(act[1]['promotionId'], 'PMB211000002')

    @ignore_warnings
    def test_get_case5(self):
        urllib3.disable_warnings()
        arrange = [
            {"goodsId": "2823563800061 ", "quantity": 6},
            {"goodsId": "2824480000311 ", "quantity": 23},
        ]
        act = self.p.do_work(arrange, 5)
        self.assertEqual(act[0]['promotionId'], 'PMB211000001')
        self.assertEqual(act[1]['promotionId'], 'PMB211000001')

    @ignore_warnings
    def test_get_case6(self):
        urllib3.disable_warnings()
        arrange = [
            {"goodsId": "2823563800061 ", "quantity": 5},
            {"goodsId": "2824480000311 ", "quantity": 24},
            {"goodsId": "2111108183101 ", "quantity": 1},
        ]
        act = self.p.do_work(arrange, 6)
        self.assertEqual(act[0]['promotionId'], '')
        self.assertEqual(act[1]['promotionId'], '')
        self.assertEqual(act[2]['promotionId'], 'PMB211000002')


if __name__ == '__main__':
    unittest.main()
