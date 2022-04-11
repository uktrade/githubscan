# -*- coding: utf-8 -*-


def test_data_is_not_a_dic(processor):
    try:
        processor.load_data_from_dict = "string data"
        assert False
    except TypeError:
        assert True


def test_data_is_a_dict(processor):
    data_dict = {"key": "value"}
    processor.load_data_from_dict = data_dict

    assert processor.scanned_data == data_dict

    processor.clear()
