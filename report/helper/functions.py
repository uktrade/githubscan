# -*- coding: utf-8 -*-
from config.severities import EFFECTIVE_SEVERITY, SEVERITY


def sort_dict_by_total(data, key):
    """
    Sort the dictory based on the  severities
    """
    return sorted(
        data[key].items(),
        key=lambda x: (
            -x[1]["total"]["severities"]["effective"][
                EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
            ],
            -x[1]["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.CRITICAL.name],
            -x[1]["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.HIGH.name],
            -x[1]["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.MODERATE.name],
            -x[1]["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.LOW.name],
            x[0],
        ),
    )


def sort_list_by_total(data):
    """
    Sort the dictory based on the  severities
    """
    return sorted(
        data,
        key=lambda x: (
            -x["total"]["severities"]["effective"][
                EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
            ],
            -x["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.CRITICAL.name],
            -x["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.HIGH.name],
            -x["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.MODERATE.name],
            -x["total"]["severities"]["effective"][EFFECTIVE_SEVERITY.LOW.name],
            x["name"],
        ),
    )


# not tested
def sort_alerts_list(data):
    """
    Sort the dictory based on the  severities
    """
    return sorted(
        data,
        key=lambda x: (
            x["days_to_fix"],
            -EFFECTIVE_SEVERITY[x["effective_level"]].value,
            -SEVERITY[x["level"]].value,
            x["package"],
        ),
    )
