# -*- coding: utf-8 -*-
from config.severities import SEVERITY_STATUS


def test_organization_subject(
    report_reader, build_email_report, data_index, processed_data
):
    report_reader.load_data_from_dict = processed_data

    organization_email_report = build_email_report.organization_summary(
        report_reader=report_reader
    )

    if data_index == 1 or data_index == 2 or data_index == 3 or data_index == 4:
        assert (
            organization_email_report["subject"]
            == f"[{SEVERITY_STATUS.RED.name}] Daily: Github Organisation Vulnerabilities Scan Report"
        )

    if data_index == 5 or data_index == 6:
        assert (
            organization_email_report["subject"]
            == f"[{SEVERITY_STATUS.AMBER.name}] Daily: Github Organisation Vulnerabilities Scan Report"
        )

    if data_index == 7 or data_index == 8:
        assert (
            organization_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Organisation Vulnerabilities Scan Report"
        )

    report_reader.clear()
