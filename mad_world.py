from numpy import random
from pandas import read_csv
import lib
b = 480
c = 240

def l1():
    key = ["s", "a3- c4", "f3", "a3- c4",
            "b3-", "d4 f4", "b3-", "d4 f4",
            "f3", "a3- c4", "f3", "a3- c4",
            "b3-", "d4 f4", "b3-", "d4 f4"]
    dur = 16*[b]
    vol = lib.set_vol((50, len(key),0), 10)
    lgh = 3*[0.90] + [0.5]
    for i in range(3):
        lgh += 3*[0.90] + [0.5]
    part = lib.gen_part(key, dur, vol, lgh)
    return part


def l2():
    key = ["f3", "a3- c4", "f3", "a3- c4",
            "a3-", "c4 e4-", "a3-", "c4 e4-",
            "e3-", "g3 b3-", "e3-", "g3 b3-",
            "b3-", "d4 f4", "b3-", "d4 f4"]
    dur = 16*[b]
    vol = lib.set_vol((50, len(key),0), 10)
    lgh = 3*[0.90] + [0.5]
    for i in range(3):
        lgh += 3*[0.90] + [0.5]
    part = lib.gen_part(key, dur, vol, lgh)
    return part


def left(seeds):
    random.seed(seed=int(seeds[1]))
    part = l1()
    for i in range(4):
        part += l2()
    return [part]


def r1():
    key = ["a4-", "c5", "g4", "a4-", "f4", "g4", "e4-", "d4",
           "s", "a4-",
           "c5", "g4", "a4-", "f4", "g4", "a4-",
           "b4-"]
    dur = 8*[c] + [2*b+b+c] + [2*c] + 6*[c] + [c + 4*b]
    vol = lib.set_vol((64, len(key), 0), 5)
    lgh = lib.set_lgh((0.95, len(key), 0), 0.05)
    part = lib.gen_part(key, dur, vol, lgh)
    return part


def r2():
    key = ["s", "f4", "f4", "a4-", "a4-", "f4", "f4"] + 3*["c5"] + ["a4-", "s"]
    key += 3*["b4-"] + ["g4", "s"] + 3*["b4-"] + ["a4-", "g4", "f4"]
    dur = [b] + 6*[c] + 2*[c, b, b, c, b] + [c, b, b, c, c, c]
    vol = lib.set_vol((64, len(key), 0), 5)
    lgh = lib.set_lgh((0.95, len(key), 0), 0.05)
    part = lib.gen_part(key, dur, vol, lgh)
    return part


def right(seeds):
    random.seed(seed=int(seeds[0]))
    part = r1()
    for i in range(4):
        part += r2()
    return  [part]


def mad_world(seeds=[1,2,3]):
    parts = left(seeds)
    parts += right(seeds)
    return parts, 480, "mad_world", seeds

md = lib.interpret(mad_world, [(700000, 16, 0)], 50000)
lib.play('mad_world.mid')
