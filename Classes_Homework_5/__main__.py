import sqlite3 as sql

from pyinputplus import inputMenu

from exec_utils.configloader import Config
from counts import Counts
from modules.input import Proceed
from modules.run import Execute
from modules.exceptions import Duplicate
from fromfile import WriteFromFile
from fromjson import FromJson
from fromxml import FromXML

cnf = Config()
p = Proceed(cnf.get_values("INPUTS", "proceed_msg"), cnf.get_values("MESSAGES", "goodbye"))
e = Execute()
wff = WriteFromFile(cnf.get_values("PATHS", "source_file"), cnf.get_values("PATHS", "target_file"))
fj = FromJson(cnf.get_values("PATHS", "json_source"), cnf.get_values("PATHS", "target_file"))
fx = FromXML(cnf.get_values("PATHS", "xml_source"), cnf.get_values("PATHS", "target_file"))
cnt = Counts(cnf.get_values("PATHS", "target_file"), cnf.get_values("PATHS", "csv_words"), cnf.get_values("PATHS", "csv_letters"))


def manual_input():
    """Run end-to-end manual input flow (ask for input, write to file),
    ask if user wants to proceed - if yes, run again, if no - print goodbye message.
    Both messages are configurable, see in configs.ini"""
    decision = "yes"
    while decision == "yes":
        try:
            e.manual_flow()
        except sql.DatabaseError as err:
            print(err)
        except Duplicate as err:
            print(err)
        decision = p.next_steps()
    else:
        p.goodbye()


def select_source():
    decision = inputMenu(prompt=cnf.get_values("INPUTS", "choose_source")+"\n",
                         choices=[cnf.get_values("LABELS", "def_file"), cnf.get_values("LABELS", "my_file")],
                         numbered=True)
    return decision


def select_flow():
    """Ask user if he wants to input section manually or write from file"""
    choice1, choice2, choice3, choice4 = cnf.get_values("LABELS", "manual"), \
                                cnf.get_values("LABELS", "from_file"), \
                                cnf.get_values("LABELS", "from_json"), \
                                cnf.get_values("LABELS", "from_xml")
    flow = inputMenu(prompt=cnf.get_values("INPUTS", "input_format")+"\n"
                     , choices=[choice1, choice2, choice3, choice4]
                     , numbered=True)
    if flow == choice1:
        manual_input()
    elif flow == choice2:
        if select_source() == cnf.get_values("LABELS", "def_file"):
            wff.file_full_flow(wff.def_source)
        else:
            wff.file_full_flow(input(cnf.get_values("INPUTS", "filepath")+"\n"))
    elif flow == choice3:
        if select_source() == cnf.get_values("LABELS", "def_file"):
            fj.file_full_flow(fj.def_source)
        else:
            fj.file_full_flow(input(cnf.get_values("INPUTS", "filepath")+"\n"))
    elif flow == choice4:
        if select_source() == cnf.get_values("LABELS", "def_file"):
            fx.file_full_flow(fx.def_source)
        else:
            fx.file_full_flow(input(cnf.get_values("INPUTS", "filepath")+"\n"))


def main():
    """End-to-end flow: from input selection to writing new section to news file + writing counts to csvs."""
    select_flow()
    cnt.write_csv()


if __name__ == '__main__':
    main()
