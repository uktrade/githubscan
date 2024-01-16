# -*- coding: utf-8 -*-
from copy import deepcopy

import pytest
from django.conf import settings

from common.functions import singleton
from report.builder.csv_report import BuildCSVReport
from report.builder.email_report import BuildEmailReport
from report.builder.gecko_report import BuildGeckoReport
from report.builder.slack_report import BuildSlackReport
from report.dispatchers import EmailClient, SlackClient
from report.helper.day_manager import DayManager
from report.helper.uk_holidays import UKHolidays
from report.operators import create_processed_data
from report.processor import ReportDataProcessor
from report.reader import ReportReader
from report.tests.mock_test_data import MockTestData, generate_mock_scenarios

settings.GITHUB_TEAMS_ARE_NOT_A_SSO_TARGET = ["team1"]


@singleton
class MockScannerData:
    """
    Class to supply raw mock data to tests
    """

    def __init__(self):
        self.data = {}
        self.data = generate_mock_scenarios()

    @property
    def get(self):
        return self.data


@singleton
class MockProcessedData:
    """
    Class to supply processed data to tests
    """

    def __init__(self):
        self.processed_data = {}
        mock_scanner_data = MockScannerData()

        for scence_index, mock_data in deepcopy(mock_scanner_data.get).items():
            self.processed_data.update(
                {scence_index: create_processed_data(scanner_data=mock_data)}
            )

    @property
    def get(self):
        return self.processed_data


def pytest_generate_tests(metafunc):
    """
    overrride pytest function to generate tests with parameters

    Parameters
    -----------
    metafunc: function to be parameterized, in this case all tests
    """
    mock_raw_scene_data_params = ["scene_index", "scene_data"]
    mock_processed_scene_data_params = ["data_index", "processed_data"]
    """
    This condition checks if test fucntion have any of the fixture listed in it and set them
    if not, just move on
    """
    if set(mock_raw_scene_data_params).issubset(set(metafunc.fixturenames)):
        set_raw_mock_data(mock_raw_scene_data_params, metafunc)

    if set(mock_processed_scene_data_params).issubset(set(metafunc.fixturenames)):
        set_processed_mock_data(mock_processed_scene_data_params, metafunc)


def set_raw_mock_data(parameters, metafunc):
    mock_scanner_data = MockScannerData()
    metafunc.parametrize(parameters, deepcopy(mock_scanner_data.get).items())


def set_processed_mock_data(parameters, metafunc):
    mock_processed_data = MockProcessedData()
    metafunc.parametrize(parameters, deepcopy(mock_processed_data.get).items())


@pytest.fixture(scope="session")
def uk_holidays():
    uk_holidays = UKHolidays(verify_ssl=False)
    yield uk_holidays


@pytest.fixture(scope="session")
def day_manager(uk_holidays):
    uk_holidays.calendar_url = settings.UK_HOLIDAYS_SOURCE_URL
    day_manager = DayManager(uk_holidays=uk_holidays.calendar)

    yield day_manager

    day_manager.clear()


@pytest.fixture(scope="function")
def mock_test_data():
    mock_test_data = MockTestData()
    yield mock_test_data
    mock_test_data.clear()


@pytest.fixture(scope="session")
def processor():
    processor = ReportDataProcessor()
    yield processor
    processor.clear()


@pytest.fixture(scope="session")
def report_reader():
    """
    run report builder tests here with yield
    """
    report_reader = ReportReader()
    yield report_reader
    report_reader.clear()


@pytest.fixture(scope="session")
def build_email_report():
    build_email_report = BuildEmailReport()
    yield build_email_report


@pytest.fixture(scope="session")
def build_slack_report():
    slack_report = BuildSlackReport()
    yield slack_report
    slack_report.clear()


@pytest.fixture(scope="session")
def build_csv_report():
    build_csv_report = BuildCSVReport()
    yield build_csv_report
    build_csv_report.clear()


@pytest.fixture(scope="session")
def build_gecko_report():
    gecko_report = BuildGeckoReport()
    yield gecko_report
    gecko_report.clear()


@pytest.fixture(scope="session")
def fake_test_email_dispatcher():
    report_dispatcher = EmailClient(api_key=settings.GOV_NOTIFY_FAKE_TEST_API_KEY)
    yield report_dispatcher


@pytest.fixture(scope="session")
def real_test_email_dispatcher():
    report_dispatcher = EmailClient(api_key=settings.GOV_NOTIFY_REAL_TEST_API_KEY)
    yield report_dispatcher


@pytest.fixture(scope="session")
def slack_dispatcher():
    slack_dispatcher = SlackClient()
    yield slack_dispatcher
    slack_dispatcher.clear()


@pytest.fixture(scope="session")
def real_fast_test():
    if not (
        settings.DEPLOYMENT_ENVIRONMENT == "real_test"
        or settings.DEPLOYMENT_ENVIRONMENT == "real_fast_test"
    ):
        pytest.skip(
            reason="These tests are against real endpoints and are fast, they needs a valid credentials. if you want to run the, set DEPLOYMENT_ENVIRONMENT to 'real_fast_test' or 'real_test' in evironment"
        )
