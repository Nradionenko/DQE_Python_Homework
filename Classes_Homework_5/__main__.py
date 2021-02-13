from exec_utils.configloader import Config
from modules.input import Proceed
from modules.run import Execute

cnf = Config()
p = Proceed(cnf.get_values("INPUTS", "proceed_msg"), cnf.get_values("MESSAGES", "goodbye"))
e = Execute()


def main():
    """Run end-to-end flow (ask for input, write to file),
    ask if user wants to proceed - if yes, run again, if no - print goodbye message.
    Both messages are configurable, see in configs.ini"""
    decision = "yes"
    while decision == "yes":
        e.end_to_end()
        decision = p.next_steps()
    else:
        p.goodbye()


if __name__=='__main__':
    main()
