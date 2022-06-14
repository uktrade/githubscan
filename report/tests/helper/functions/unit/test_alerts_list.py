# -*- coding: utf-8 -*-
from report.helper.functions import sort_alerts_list
from config.severities import EFFECTIVE_SEVERITY


def test_sort_alerts_list(data_index, processed_data):

    alerts_list = []
    for value in processed_data["repositories"].values():
        for alert in value["alerts"]:
            alerts_list.append(alert)

    sorted_alerts_list = sort_alerts_list(data=alerts_list)

    if data_index == 1 or data_index == 2 or data_index == 3 or data_index == 4:
        assert (
            sorted_alerts_list[0]["effective_level"]
            == EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
        )
        assert sorted_alerts_list[0]["days_to_fix"] == -1

    if data_index == 5 or data_index == 6:
        assert (
            sorted_alerts_list[0]["effective_level"] == EFFECTIVE_SEVERITY.CRITICAL.name
        )
        assert sorted_alerts_list[0]["days_to_fix"] == 0

    if data_index == 7:
        assert (
            sorted_alerts_list[0]["effective_level"] == EFFECTIVE_SEVERITY.CRITICAL.name
        )
        assert sorted_alerts_list[0]["days_to_fix"] == 0

    if data_index == 8:
        assert sorted_alerts_list == []

    processed_data.clear()
    alerts_list.clear()
    sorted_alerts_list.clear()
