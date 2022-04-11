# -*- coding: utf-8 -*-
"""
The most USEABLE value here is ESCALATION_RULES ( in WORKING DAYS ) Based on
"""

from enum import Enum
from django.conf import settings

"""
SET of predefined (origianl) severities
"""


class SEVERITY(Enum):
    CRITICAL = 4
    HIGH = 3
    MODERATE = 2
    LOW = 1


"""
A Set of Possible Escalation also known as Effective severities
"""


class EFFECTIVE_SEVERITY(Enum):
    CRITICAL_BREACH = 5
    CRITICAL = 4
    HIGH = 3
    MODERATE = 2
    """
    Nothing should escalate to low, low being lowest possible severity
    It is here only for the reporting purpose
    """
    LOW = 1


"""
Severity status is assigned as follows
 - RED  : IF CRITICAL BREACH FOUND
 - AMBER: BREACH is non CRITICAL
 - GREEN: There are Severities but no BREACH
 - CLEAN: There are no Severity ( not used )
   CLEAN is represnted as GREEN while sending out communication of all form
   However, it is easier to keep it as a seperate concept in code
"""


class SEVERITY_STATUS(Enum):
    RED = "RED"
    AMBER = "AMBER"
    GREEN = "GREEN"
    CLEAN = "CLEAN"


"""
Number of days you get FOR EACH SEVERITY LEVEL to fix, and when  time is up , it it moved a level up and rendered as Effective Severity
Note: THis should be part of configuration as in variables or conf.settings
"""

TIME_TO_FIX = settings.SEVERITY_ESCLATION_MATRIC

"""
A Map of original severity to , each esclation point which will render as Effective severity
Note: these numbers are in WORKING DAYS
"""
ESCALATION_RULES = {
    SEVERITY.LOW.name: {
        EFFECTIVE_SEVERITY.MODERATE.name: TIME_TO_FIX[SEVERITY.LOW.name],
        EFFECTIVE_SEVERITY.HIGH.name: TIME_TO_FIX[SEVERITY.LOW.name]
        + TIME_TO_FIX[SEVERITY.MODERATE.name],
        EFFECTIVE_SEVERITY.CRITICAL.name: TIME_TO_FIX[SEVERITY.LOW.name]
        + TIME_TO_FIX[SEVERITY.MODERATE.name]
        + TIME_TO_FIX[SEVERITY.HIGH.name],
        EFFECTIVE_SEVERITY.CRITICAL_BREACH.name: TIME_TO_FIX[SEVERITY.LOW.name]
        + TIME_TO_FIX[SEVERITY.MODERATE.name]
        + TIME_TO_FIX[SEVERITY.HIGH.name]
        + TIME_TO_FIX[SEVERITY.CRITICAL.name],
    },
    SEVERITY.MODERATE.name: {
        EFFECTIVE_SEVERITY.HIGH.name: TIME_TO_FIX[SEVERITY.MODERATE.name],
        EFFECTIVE_SEVERITY.CRITICAL.name: TIME_TO_FIX[SEVERITY.MODERATE.name]
        + TIME_TO_FIX[SEVERITY.HIGH.name],
        EFFECTIVE_SEVERITY.CRITICAL_BREACH.name: TIME_TO_FIX[SEVERITY.MODERATE.name]
        + TIME_TO_FIX[SEVERITY.HIGH.name]
        + TIME_TO_FIX[SEVERITY.CRITICAL.name],
    },
    SEVERITY.HIGH.name: {
        EFFECTIVE_SEVERITY.CRITICAL.name: TIME_TO_FIX[SEVERITY.HIGH.name],
        EFFECTIVE_SEVERITY.CRITICAL_BREACH.name: TIME_TO_FIX[SEVERITY.HIGH.name]
        + TIME_TO_FIX[SEVERITY.CRITICAL.name],
    },
    SEVERITY.CRITICAL.name: {
        EFFECTIVE_SEVERITY.CRITICAL_BREACH.name: TIME_TO_FIX[SEVERITY.CRITICAL.name]
    },
}
