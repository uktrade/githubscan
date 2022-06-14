# -*- coding: utf-8 -*-
from config.schema import scanner_data_schema


def test_add_skip_scan_repositories(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    scanner_data_schema.validate(scene_data)
    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_skip_scan_repositories()

    check_skip_scan_repositories(
        repositories=processor.repositories,
        skip_scan_repositories_list=processor.skip_scan_repositories["list"],
    )

    processor.clear()


def check_skip_scan_repositories(repositories, skip_scan_repositories_list):
    hasSkipScan_counter = 0

    """
    ensure sum of orignal severity is same as sum of effective severity
    """
    hasSkipScan_counter = sum(
        1 for repository in repositories.values() if repository["hasSkipScan"] == True
    )

    assert len(skip_scan_repositories_list) == hasSkipScan_counter
