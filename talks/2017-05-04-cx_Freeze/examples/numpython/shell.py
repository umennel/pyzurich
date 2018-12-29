import numpy as np
import matplotlib.pyplot as plt
import rlcompleter, readline
import code

def demo():
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C = np.cos(X)
    plt.plot(X,C)
    plt.show()
    
readline.parse_and_bind('tab: complete')
vars = globals().copy()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()