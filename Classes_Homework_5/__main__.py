from exec_utils.configloader import Config
from modules.input import Selection
from modules.run import Execute

cnf = Config()
s = Selection()
e = Execute()

msg1, msg2 = cnf.get_values("INPUTS", "proceed_msg"), cnf.get_values("MESSAGES", "goodbye")


def main(msg1, msg2):
    """Run end-to-end flow (ask for input, write to file),
    ask if user wants to proceed - if yes, run again, if no - print goodbye message.
    Both messages are configurable, see in configs.ini"""
    decision = "yes"
    while decision == "yes":
        e.end_to_end()
        decision = s.next_steps(msg1)
    else:
        s.goodbye(msg2)


main(msg1, msg2)
