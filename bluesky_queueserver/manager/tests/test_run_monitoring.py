import pytest
import uuid

from bluesky_queueserver.manager.run_monitoring import RunList, CallbackRegisterRun


def test_RunList_1():
    """
    Basic tests from RunList class.
    """
    uids = [uuid.uuid4() for _ in range(3)]
    is_open = [True] * 3
    exit_code = [None] * 3
    expected_run_list = [{"uid": _[0], "is_open": _[1], "exit_status": _[2]}
                         for _ in zip(uids, is_open, exit_code)]

    # Create run list
    run_list = RunList()
    assert run_list.is_changed() is False

    # Add one object
    run_list.add_run(uid=uids[0])
    assert run_list.is_changed() is True
    assert run_list.get_run_list() == expected_run_list[0:1]
    assert run_list.is_changed() is True
    assert run_list.get_run_list(clear_state=True) == expected_run_list[0:1]
    assert run_list.is_changed() is False

    # Add two more objects
    run_list.add_run(uid=uids[1])
    run_list.add_run(uid=uids[2])
    assert run_list.is_changed() is True
    assert run_list.get_run_list(clear_state=True) == expected_run_list
    assert run_list.is_changed() is False

    # Set the second object as completed
    expected_run_list[1]["is_open"] = False
    expected_run_list[1]["exit_status"] = "success"
    run_list.set_run_closed(uid=uids[1], exit_status="success")
    assert run_list.is_changed() is True
    assert run_list.get_run_list(clear_state=True) == expected_run_list
    assert run_list.is_changed() is False

    # Fail case: non-existing UID
    with pytest.raises(Exception, match="Run with UID .* was not found in the list"):
        run_list.set_run_closed(uid="non-existing-uid", exit_status="success")
    assert run_list.is_changed() is False
