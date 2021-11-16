import unittest
import warnings

import urllib3

from main import Flow


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)

    return do_test


class GetCaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GetCaseTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.tf = Flow()
        urllib3.disable_warnings()

    def tearDown(self) -> None:
        print('finished')

    # region CASE 1、2
    @ignore_warnings
    def test_get_case1(self):
        arrange = [
            {"goodsId": "2823563800061", "quantity": 5},
            {"goodsId": "2824480000311", "quantity": 1},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000001', 'PMB211000001'])

    @ignore_warnings
    def test_get_case2(self):
        arrange = [
            {"goodsId": "2823563800061", "quantity": 1},
            {"goodsId": "2824480000311", "quantity": 1},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['', ''])

    @ignore_warnings
    def test_get_case3(self):
        arrange = [
            {"goodsId": "2823563800061", "quantity": 5},
            {"goodsId": "2824480000311", "quantity": 24},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['', 'PMB211000002'])

    @ignore_warnings
    def test_get_case4(self):
        arrange = [
            {"goodsId": "2823563800061", "quantity": 6},
            {"goodsId": "2824480000311", "quantity": 24},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000001', 'PMB211000002'])

    @ignore_warnings
    def test_get_case5(self):
        arrange = [
            {"goodsId": "2823563800061", "quantity": 6},
            {"goodsId": "2824480000311", "quantity": 23},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000001', 'PMB211000001'])

    @ignore_warnings
    def test_get_case6(self):
        arrange = [
            {"goodsId": "2823563800061", "quantity": 5},
            {"goodsId": "2824480000311", "quantity": 24},
            {"goodsId": "2111108183101", "quantity": 1},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['', '', 'PMB211000002'])

    # end region

    # region CASE 3、4

    @ignore_warnings
    def test_get_case7(self):
        arrange = [
            {"goodsId": "2839796000161", "quantity": 1},
            {"goodsId": "2839796000041", "quantity": 1},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000029', 'PMB211000029'])

    @ignore_warnings
    def test_get_case8(self):
        arrange = [
            {"goodsId": "2839796000161", "quantity": 2},
            {"goodsId": "2839796000041", "quantity": 1},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['', 'PMB211000030'])

    @ignore_warnings
    def test_get_case9(self):
        arrange = [
            {"goodsId": "2839796000161", "quantity": 1},
            {"goodsId": "2839796000041", "quantity": 1},
            {"goodsId": "2839796000211", "quantity": 2},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000029', 'PMB211000029', 'PMB211000030'])

    @ignore_warnings
    def test_get_case10(self):
        arrange = [
            {"goodsId": "2839796000161", "quantity": 1},
            {"goodsId": "2839796000041", "quantity": 1},
            {"goodsId": "2839796000211", "quantity": 2},
            {"goodsId": "2823563800061", "quantity": 6},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000001', 'PMB211000029', 'PMB211000029', 'PMB211000030'])

    # end region

    @ignore_warnings
    def test_get_case11(self):
        arrange = [
            {"goodsId": "2733798000081", "quantity": 1},
            {"goodsId": "2740798000001", "quantity": 1},
            {"goodsId": "2740798000061", "quantity": 1},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['PMB211000031', 'PMB211000031', 'PMB211000031'])

    @ignore_warnings
    def test_get_case12(self):
        arrange = [
            {"goodsId": "2740798000001", "quantity": 1},
            {"goodsId": "2740798000061", "quantity": 3},
        ]
        act, order_id, robot_id = self.tf.do_work(arrange)
        self.__assert_my_result(act=act, expected=['', 'PMB211000032'])

    # end region

    def __assert_my_result(self, act, expected):
        for index, item in enumerate(expected):
            print(act[index]['promotionId'], item)
            self.assertEqual(act[index]['promotionId'], item)


if __name__ == '__main__':
    unittest.main()
