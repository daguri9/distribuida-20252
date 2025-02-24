import simpy
import random

env = simpy.Environment()


def megafono(msg, times):
    i = 1
    while i < times:
        print(msg.upper(), f"{i}/{times}")
        yield
        i += 1


if __name__ == "__main__":
    fn = megafono("here we go!", 1)
    until = 16
    env.process(megafono("blsls", until))
    env.run(until=16)