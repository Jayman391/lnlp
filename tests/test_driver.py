import json
import os 

from drivers._driver import Driver
from util._session import Session
from menus._menu import Menu


def test_initialize_session():
    driver = Driver()
    session = driver.initialize_session(
        data_path="tests/test_data/usa-vaccine-comments.csv",
        config_path="tests/test_data/config-tm.json",
        optimization_path=None,
    )
    assert session is not None

def test_write_logs():
    driver = Driver()
    
    directory = "output"

    driver.initialize_session(data_path='tests/test_data/brazil-vaccine-comments.csv',save_dir=directory)

    driver.session.log("data", "This is a data message.")
    driver.session.log("errors", "This is an error message.")

    driver._write_logs(directory)

    assert os.path.exists(directory)
    assert os.path.exists(os.path.join(directory, "logs.json"))

    with open(os.path.join(directory, "logs.json"), "r") as f:
        logs = json.load(f)

    assert logs["data"] == ["This is a data message."]
    assert logs["errors"] == ["This is an error message."]

    os.remove(os.path.join(directory, "logs.json"))
    os.rmdir(directory)
    
def test_log():
    driver = Driver()
    driver.initialize_session()
    assert driver.log(type="info", message="This is an info message") == {
        "info": "This is an info message"
    }
    assert "info" in driver.session.logs.keys()
    assert driver.session.logs["info"] == ["This is an info message"]


def test_run_menu_leaf():
    driver = Driver()
    session = Session()
    menu = Menu(session, options=["Option 1", "Option 2"], is_leaf=True, is_root=True)
    # choose option 1
    assert driver._run_menu(menu) == "Option 1"


def test_run_menu_branch():
    driver = Driver()
    session = Session()
    menu = Menu(session, options=["Option 1", "Option 2"], is_leaf=False, is_root=True)
    sub_menu_1 = Menu(
        session, options=["Option 1", "Option 2"], is_leaf=True, is_root=False
    )
    sub_menu_2 = Menu(
        session, options=["Option 1", "Option 2"], is_leaf=True, is_root=False
    )
    menus = [sub_menu_1, sub_menu_2]
    menu.map_options_to_menus(menu.options, menus)
    # choose 1
    assert driver._run_menu(menu) == sub_menu_1

def test_process_response():
    driver = Driver()
    session = Session()
    menu = Menu(session, options=["Option 1", "Option 2"], is_leaf=False, is_root=True)
    sub_menu_1 = Menu(
        session, options=["Option 1", "Option 2"], is_leaf=True, is_root=False
    )
    sub_menu_2 = Menu(
        session, options=["Option 1", "Option 2"], is_leaf=True, is_root=False
    )
    menus = [sub_menu_1, sub_menu_2]
    menu.map_options_to_menus(menu.options, menus)

    # choose 1
    assert driver._process_response(menu.handle_choice(1)) == sub_menu_1
    assert driver._process_response(
        driver._process_response(
            menu.handle_choice(1)
        ).handle_choice(1)
    ) == "Option 1"



    