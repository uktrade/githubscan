# -*- coding: utf-8 -*-
from asyncio.log import logger
from django.http import HttpResponse
from scanner import refresh_scan
from report.report import refresh_processed_data, refresh_database_teams
import time
import logging
import traceback

logger = logging.getLogger(__name__)


def refresh_vulneranility_data(request):
    """
    this method provides a way to refresh report data

    Reason: Since, now reports are in file, it has been observered that
    executing command directly in PaaS as a task results in files to get written in task container
    with view we will attempt to write files on container
    """
    try:
        start_time = time.time()

        refresh_scan()
        refresh_processed_data()
        refresh_database_teams()

        end_time = time.time()

        message = (
            f"Time: {end_time - start_time}s Success: refresh_vulneranility_data()"
        )
        logger.info(message)

    except Exception as e:
        end_time = time.time()
        message = (
            f"Time: {end_time - start_time}s refresh_vulneranility_data() Error: {e}"
        )
        logger.info(message)
        logger.info(f"Error Trace: {traceback.print_exc()}")

    return HttpResponse(message)
