# -*- coding: utf-8 -*-
def test_add_fix_by_date(processor, scene_index, scene_data):
    """test it for all scenarios"""
    processor.load_data_from_dict = scene_data
    processor.add_enterprise_users()

    check_add_enterprise_users(enterprise_users=processor.enterprise_users)

    processor.clear()


def check_add_enterprise_users(enterprise_users):
    assert len(enterprise_users) == 6
