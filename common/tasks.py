# -*- coding: utf-8 -*-
import logging

from celery import shared_task

from report.operators import refresh_database, refresh_processed_data
from scanner.operators import refresh_scan

logger = logging.getLogger(__name__)


@shared_task
def refresh_scan_data():
    """refresh scanner data"""
    logger.info("Starting to run scanner")
    refresh_scan()
    return "Done: Refreshing Scanned Data"


@shared_task
def refresh_report_data():
    """refresh report data"""
    refresh_processed_data()
    refresh_database()
    return "Done: Refreshing Processed Data"
