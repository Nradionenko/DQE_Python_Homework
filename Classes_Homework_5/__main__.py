from pyinputplus import inputMenu
from exec_utils.configloader import Config
from modules.input import Proceed
from modules.run import Execute
from fromfile import WriteFromFile

cnf = Config()
p = Proceed(cnf.get_values("INPUTS", "proceed_msg"), cnf.get_values("MESSAGES", "goodbye"))
e = Execute()
wff = WriteFromFile(cnf.get_values("PATHS", "source_file"), cnf.get_values("PATHS", "target_file"))


def manual_input():
    """Run end-to-end flow (ask for input, write to file),
    ask if user wants to proceed - if yes, run again, if no - print goodbye message.
    Both messages are configurable, see in configs.ini"""
    decision = "yes"
    while decision == "yes":
        e.end_to_end()
        decision = p.next_steps()
    else:
        p.goodbye()


def main():
    choice1, choice2 = cnf.get_values("LABELS", "manual"), cnf.get_values("LABELS", "from_file")
    flow = inputMenu(prompt=cnf.get_values("INPUTS", "input_format")+"\n", choices=[choice1, choice2], numbered=True)
    if flow == choice1:
        manual_input()
    else:
        wff.write_and_remove()


if __name__ == '__main__':
    main()
