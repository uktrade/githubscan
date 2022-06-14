# -*- coding: utf-8 -*-
import re


def test_organization_detailed_subject(
    build_email_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    organization_email_report = build_email_report.organization_detailed(
        report_reader=report_reader
    )

    if data_index == 1:
        assert re.search("11 Vulnerable packages", organization_email_report["subject"])

    if data_index == 2 or data_index == 5:
        assert re.search("8 Vulnerable packages", organization_email_report["subject"])

    if data_index == 3:
        assert re.search("6 Vulnerable packages", organization_email_report["subject"])

    if data_index == 4 or data_index == 7:
        assert re.search("3 Vulnerable packages", organization_email_report["subject"])

    if data_index == 6:
        assert re.search("5 Vulnerable packages", organization_email_report["subject"])

    if data_index == 8:
        assert re.search("0 Vulnerable packages", organization_email_report["subject"])

    report_reader.clear()
