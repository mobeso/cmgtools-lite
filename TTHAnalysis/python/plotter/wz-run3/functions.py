""" These are just some stupid functions to print messages with coloring and all that. Useful for debugging. """
def color_msg(msg, color):
    """ Prints a message with ANSI coding so it can be printout with colors """
    codes = {
        "green" : "1;32m",
        "red" : "1;31m",
        "blue" : "1;34m",
    }

    print("\033[%s%s \033[0m"%(codes[color], msg))
    return