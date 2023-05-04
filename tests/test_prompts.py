import pytest

from os.path import join as path_join
from reddit_to_video.prompts import prompt_list, prompt_bool, prompt_int, prompt_str, prompt_write_file


def test_prompt_list_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert prompt_list([("test", 1)]) == 1


def test_prompt_list_invalid(monkeypatch):
    cur_index = 0
    inputs = ["0", "2", "1"]

    def mock_input(prompt):
        assert prompt == ": "
        nonlocal cur_index
        cur_index += 1
        return str(inputs[cur_index - 1])

    monkeypatch.setattr("builtins.input", mock_input)

    assert prompt_list([("test", 1)], ":") == 1


def test_prompt_bool_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert prompt_bool("test") == True


def test_prompt_bool_invalid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert prompt_bool("test") == False


def test_prompt_bool_incorrect_inputs(monkeypatch):
    cur_index = 0
    inputs = ["c", "okfpaosef", "q", "y"]

    def mock_input(prompt):
        assert prompt == ": "
        nonlocal cur_index
        cur_index += 1
        return str(inputs[cur_index - 1])

    monkeypatch.setattr("builtins.input", mock_input)

    assert prompt_bool(": ") == True


def test_prompt_int_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert prompt_int("test") == 1


def test_prompt_int_invalid(monkeypatch):
    inputs = ["a", "1.2", "1"]

    def mock_input(prompt):
        assert prompt == ": "
        return inputs.pop(0)

    monkeypatch.setattr("builtins.input", mock_input)

    assert prompt_int(": ") == 1


string_inputs = [
    "test",
    "123908",
    "I love_cats@",
    "0xFFFF"
]


@pytest.mark.parametrize("mocked_input", string_inputs)
def test_prompt_str_valid(mocked_input, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: mocked_input)
    assert prompt_str("test") == mocked_input


def test_prompt_write_file_valid(monkeypatch, tmp_path):
    file_folder = tmp_path / "test"
    file_folder.mkdir()
    expected_path = str(file_folder / "test.txt")
    monkeypatch.setattr("builtins.input", lambda _: expected_path)
    assert prompt_write_file("test", True) == expected_path


def test_prompt_write_file_invalid(monkeypatch, tmp_path):
    file_folder = tmp_path / "test"
    file_folder.mkdir()
    expected_path = str(file_folder / "test.txt")

    inputs = ["\0/dfasefasdf/sdfasefa/sdsaftest", expected_path]

    def mock_input(prompt):
        assert prompt == ": "
        return inputs.pop(0)

    monkeypatch.setattr("builtins.input", mock_input)
    assert prompt_write_file(": ", True) == expected_path


def test_prompt_file_valid(monkeypatch, tmp_path):
    file_folder = tmp_path / "test"
    file_folder.mkdir()
    expected_path = str(file_folder / "test.txt")
    monkeypatch.setattr("builtins.input", lambda _: expected_path)
    assert prompt_write_file("test", True) == expected_path


def test_prompt_file_invalid(monkeypatch, tmp_path):
    file_folder = tmp_path / "test"
    file_folder.mkdir()
    expected_path = str(file_folder / "test.txt")

    inputs = ["test", expected_path]

    def mock_input(prompt):
        assert prompt == ": "
        return inputs.pop(0)

    monkeypatch.setattr("builtins.input",  mock_input)
    assert prompt_write_file(": ", True) == expected_path
