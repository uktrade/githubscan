# -*- coding: utf-8 -*-
from schema import And, Optional, Or, Schema, Use
from config.severities import SEVERITY_STATUS, EFFECTIVE_SEVERITY, SEVERITY


alert_test_data_schema = Schema(
    {
        "age_in_business_days": int,
        "age_in_calendar_days": int,
        "fix_by": str,
        "effective_level": str,
    },
)

scanner_alerts_schema = Schema(
    Or(
        [],
        [
            {
                "advisory_url": str,
                "createdAt": str,
                "dismissedAt": Or(str, None),
                "level": And(
                    str,
                    Use(str),
                    lambda l: l
                    in (
                        SEVERITY.CRITICAL.name,
                        SEVERITY.HIGH.name,
                        SEVERITY.MODERATE.name,
                        SEVERITY.LOW.name,
                    ),
                ),
                "package": str,
                "patched_version": str,
                "state": "OPEN",
                Optional("test_expected_data"): alert_test_data_schema,
            }
        ],
    )
)

scanner_data_schema = Schema(
    {
        "repositories": [
            {
                "name": And(str, len),
                "teams": Or([], [str]),
                "topics": Or([], [str]),
                "alerts": scanner_alerts_schema,
            }
        ],
        "team_repositories": [{str: Or([], [And(str, len)])}],
        "teams": [And(str, len)],
    }
)


processed_data_total_schema = Schema(
    {
        "repositories": int,
        "severities": {
            "effective": {
                EFFECTIVE_SEVERITY.CRITICAL_BREACH.name: int,
                EFFECTIVE_SEVERITY.CRITICAL.name: int,
                EFFECTIVE_SEVERITY.HIGH.name: int,
                EFFECTIVE_SEVERITY.MODERATE.name: int,
                EFFECTIVE_SEVERITY.LOW.name: int,
            },
            "original": {
                SEVERITY.CRITICAL.name: int,
                SEVERITY.HIGH.name: int,
                SEVERITY.MODERATE.name: int,
                SEVERITY.LOW.name: int,
            },
        },
        "slo_breach": {
            "repositories": int,
            "severities": {
                SEVERITY.CRITICAL.name: int,
                SEVERITY.HIGH.name: int,
                SEVERITY.MODERATE.name: int,
                SEVERITY.LOW.name: int,
            },
        },
    },
)


report_alerts_schema = Schema(
    Or(
        [],
        [
            {
                "advisory_url": str,
                "createdAt": str,
                "dismissedAt": Or(str, None),
                "level": And(
                    str,
                    Use(str),
                    lambda l: l
                    in (
                        SEVERITY.CRITICAL.name,
                        SEVERITY.HIGH.name,
                        SEVERITY.MODERATE.name,
                        SEVERITY.LOW.name,
                    ),
                ),
                "package": str,
                "patched_version": str,
                "state": "OPEN",
                "age_in_calendar_days": int,
                "age_in_business_days": int,
                "escalated": bool,
                "effective_level": And(
                    str,
                    Use(str),
                    lambda l: l
                    in (
                        EFFECTIVE_SEVERITY.CRITICAL_BREACH.name,
                        EFFECTIVE_SEVERITY.CRITICAL.name,
                        EFFECTIVE_SEVERITY.HIGH.name,
                        EFFECTIVE_SEVERITY.MODERATE.name,
                        EFFECTIVE_SEVERITY.LOW.name,
                    ),
                ),
                "hash": int,
                "days_to_fix": int,
                "fix_by": str,
                Optional("test_expected_data"): alert_test_data_schema,
            }
        ],
    )
)

report_severity_schema = Schema(
    And(
        str,
        Use(str),
        lambda l: l
        in (
            SEVERITY_STATUS.RED.name,
            SEVERITY_STATUS.AMBER.name,
            SEVERITY_STATUS.GREEN.name,
            SEVERITY_STATUS.CLEAN.name,
        ),
    )
)

processed_data_schema = Schema(
    {
        "repositories": {
            And(str, len): {
                "name": And(str, len),
                "hasSkipScan": bool,
                "teams": Or([], [str]),
                "topics": Or([], [str]),
                "alerts": report_alerts_schema,
                "severity_status": report_severity_schema,
                "total": processed_data_total_schema,
            },
        },
        "vulnerable_repositories": Or([], [And(str)]),
        "token_has_no_access": Or([], [And(str, len)]),
        "teams": {
            And(str, len): {
                "name": And(str, len),
                "repositories": Or([], [And(str, len)]),
                "severity_status": report_severity_schema,
                "total": processed_data_total_schema,
            }
        },
        "skip_scan_repositories": {
            "list": Or([], [And(str, len)]),
            "severity_status": report_severity_schema,
            "total": processed_data_total_schema,
        },
        "orphan_repositories": {
            "list": Or([], [And(str, len)]),
            "severity_status": report_severity_schema,
            "total": processed_data_total_schema,
        },
        "severity_status": report_severity_schema,
        "total": processed_data_total_schema,
    }
)
