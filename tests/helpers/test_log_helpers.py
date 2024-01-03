import logging
from datetime import datetime
from unittest.mock import call, mock_open, patch

import pytest

from janitor.helpers.log_helpers import custom_log, load_job_timestamp, make_tmp_folder, save_job_timestamp

logger = logging.getLogger(__name__)

TEST_EVENT_NAME = "test_event"
TEST_MESSAGE = "test_message"


def test_given_invalid_event_type_when_logging_message_then_check_ValueError_raised(mock_info):
    with pytest.raises(ValueError):
        custom_log(logger, "invalid type", TEST_EVENT_NAME, TEST_MESSAGE)


def test_given_info_event_type_when_logging_message_then_check_message_logged_correctly(mock_info):
    custom_log(logger, "info", TEST_EVENT_NAME, TEST_MESSAGE)
    assert mock_info.has_calls([call(f"[{TEST_EVENT_NAME}]"), call(TEST_MESSAGE)])


def test_given_error_event_type_when_logging_message_then_check_message_logged_correctly(mock_error):
    custom_log(logger, "error", TEST_EVENT_NAME, TEST_MESSAGE)
    assert mock_error.has_calls([call(f"[{TEST_EVENT_NAME}]"), call(TEST_MESSAGE)])


@patch("os.mkdir")
def test_given_no_tmp_folder_when_making_tmp_folder_check_folder_created_successfully(mock_mkdir, config):
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        make_tmp_folder(config.JANITOR_TMP_FOLDER_PATH)
        assert mock_mkdir.has_calls(call(config.JANITOR_TMP_FOLDER_PATH))


@patch("os.mkdir")
def test_given_tmp_folder_when_making_tmp_folder_check_no_folder_created(mock_mkdir, config):
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        make_tmp_folder(config.JANITOR_TMP_FOLDER_PATH)
        assert mock_mkdir.call_count == 0


@patch("janitor.helpers.log_helpers.make_tmp_folder")
def test_given_job_name_when_saving_timestamp_then_check_file_has_correct_name_and_timestamp(mock_make_tmp, config):
    test_name = "test_job_name"
    test_timestamp = datetime.now()

    with patch("builtins.open") as mock_open_file:
        save_job_timestamp(config.JANITOR_TMP_FOLDER_PATH, test_name, test_timestamp)

        assert mock_make_tmp.call_count == 1
        assert mock_open_file.has_calls(call(config.JANITOR_TMP_FOLDER_PATH / f"{test_name}_latest_timestamp.txt", "w"))

        mock_write = mock_open_file.return_value.write
        assert mock_write.has_calls(call(str(test_timestamp)))


def test_given_no_timestamp_saved_when_loading_timestamp_then_check_none_returned(config):
    test_name = "test_job_name"

    with patch("builtins.open") as mock_open_file:
        mock_open_file.return_value = Exception
        actual_timestamp = load_job_timestamp(config.JANITOR_TMP_FOLDER_PATH, test_name)

        assert mock_open_file.has_calls(call(f"./janitor/tmp/{test_name}_latest_timestamp.txt", "r"))
        assert actual_timestamp is None


def test_given_timestamp_saved_when_loading_timestamp_then_check_correct_timestamp_returned(
    config,
):
    test_name = "test_job_name"
    test_timestamp = datetime.now()

    with patch("builtins.open", mock_open(read_data=str(test_timestamp))):
        actual_timestamp = load_job_timestamp(config.JANITOR_TMP_FOLDER_PATH, test_name)

        assert str(actual_timestamp) == str(test_timestamp)
