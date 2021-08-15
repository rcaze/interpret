import argparse
from numpy import random
from pandas import read_csv
import lib

parser = argparse.ArgumentParser(description='Set the different seeds for the interpretation')
parser.add_argument('lsd', nargs='?', type=int, default=1)
parser.add_argument('rsd', nargs='?', type=int, default=1)
parser.add_argument('tsd', nargs='?', type=int, default=1)
args = parser.parse_args()

b = 480
c = 240
VOL_VAR = 3
TPO_VAR = 20000

def l1():
    key = ["s", "a3- c4", "f3", "a3- c4",
            "b3-", "d4 f4", "b3-", "d4 f4",
            "f3", "a3- c4", "f3", "a3- c4",
            "b3-", "d4 f4", "b3-", "d4 f4"]
    dur = 16*[b]
    vol = lib.set_vol((70, len(key),0), VOL_VAR)
    lgh = 3*[0.90] + [0.5]
    for i in range(3):
        lgh += 3*[0.90] + [0.5]
    part = lib.gen_part(key, dur, vol, lgh)
    return part, vol


def l2(vol_init):
    key = ["f3", "a3- c4", "f3", "a3- c4",
            "a3-", "c4 e4-", "a3-", "c4 e4-",
            "e3-", "g3 b3-", "e3-", "g3 b3-",
            "b3-", "d4 f4", "b3-", "d4 f4"]
    dur = 16*[b]
    vol = lib.set_vol((vol_init, len(key),0), VOL_VAR)
    lgh = 3*[0.90] + [0.5]
    for i in range(3):
        lgh += 3*[0.90] + [0.5]
    part = lib.gen_part(key, dur, vol, lgh)
    return part, vol


def l3(vol_init):
    key = 3*["f3", "a3- c4", "f3", "a3- c4",
             "b3-", "d4 f4", "b3-", "d4 f4"]
    key += ["f3", "a3- c4", "f3", "a3- c4", "d4 f4"]
    key += 2*["f3", "a3- c4", "f3", "a3- c4",
              "b3-", "d4 f4", "b3-", "d4 f4"]
    dur = (3*8+4)*[b] + [4*b] + 2*8*[b]
    vol = lib.set_vol((vol_init, len(key),0), VOL_VAR)
    lgh = 3*[0.90] + [0.5]
    for i in range(6):
        lgh += 3*[0.90] + [0.5]
    lgh += [0.8]
    for i in range(4):
        lgh += 3*[0.90] + [0.5]

    part = lib.gen_part(key, dur, vol, lgh)
    return part, vol


def l4(vol_init):
    key = ["f3", "a3- c4", "f3", "a3- c4",
           "b3-", "d4 f4", "b3-", "d4 f4",
           "f3", "a3- c4", "f3", "a3- c4",
           "b2- b3-"]
    dur = 12*[b] + [4*b+b]
    vol = lib.set_vol((vol_init, len(key),0), VOL_VAR)
    lgh = 3*[0.90] + [0.5]
    for i in range(2):
        lgh += 3*[0.90] + [0.5]
    lgh += [1]
    part = lib.gen_part(key, dur, vol, lgh)
    return part


def left(seeds):
    random.seed(seed=int(seeds[0]))
    part1, vol = l1()
    part = part1
    for i in range(2):
        for j in range(4):
            part2, vol = l2(vol[-1])
            part += part2
        part3, vol = l3(vol[-1])
        part += part3
    part += l4(vol[-1])
    return [part]


def r1():
    key = ["a4-", "c5", "g4", "a4-", "f4", "g4", "e4-", "d4",
           "s", "a4-",
           "c5", "g4", "a4-", "f4", "g4", "a4-",
           "b4-"]
    dur = 8*[c] + [2*b+b+c] + [2*c] + 6*[c] + [c + 4*b]
    vol = lib.set_vol((90, len(key), 0), VOL_VAR)
    lgh = lib.set_lgh((0.95, len(key), 0), 0.05)
    part = lib.gen_part(key, dur, vol, lgh)
    return part, vol


def r2(vol_init):
    key = ["s", "f4", "f4", "a4-", "a4-", "f4", "f4"] + 3*["c5"] + ["a4-", "s"]
    key += 3*["b4-"] + ["g4", "s"] + 3*["b4-"] + ["a4-", "g4", "f4"]
    dur = [b] + 6*[c] + 2*[c, b, b, c, b] + [c, b, b, c, c, c]
    vol = lib.set_vol((vol_init, len(key), 0), VOL_VAR)
    lgh = lib.set_lgh((0.95, len(key), 0), 0.05)
    part = lib.gen_part(key, dur, vol, lgh)
    return part, vol


def r3(vol_init):
    key = ["s", "f4", "f4", "a4-", "a4-", "c5", "c5", "d5", "b4-", "s", "b4-", "d5", "d5", "b4-", "b4-"]
    key += ["f4", "s", "f4", "a4-", "a4-", "c5", "c5", "d5"] + 3*["b4-"] + ["d5", "d5", "b4-", "b4-"]
    key += ["f4", "s", "f4", "a4-", "a4-", "c5", "c5", "d5", "b4-", "s", "b4-", "d5", "d5", "b4-", "b4-"]
    key += ["f4", "s", "f4", "a4-", "a4-", "c5", "c5", "d5"] + 3*["b4-"] + ["d5", "d5", "b4-", "b4-"]
    key += ["a4-", "a4-", "g4", "g4", "f4", "f4", "e4-", "d4", "g4"]
    key += ["a4-", "a4-", "g4", "g4", "f4", "f4", "e4-", "d4 b4-"]
    dur = [b] + 15*[c] + [b] + 14*[c] + [b] + 13*[c] + [b] + 14*[c]
    dur += 7*[c] + [c+3*b] + [c, b] + 6*[c] + [c+4*b]
    vol = lib.set_vol((vol_init, len(key), 0), VOL_VAR)
    lgh = lib.set_lgh((0.95, len(key), 0), 0.05)
    part = lib.gen_part(key, dur, vol, lgh)
    return part, vol


def r4(vol_init):
    key = ["a4-", "a4-", "g4", "g4", "f4", "f4", "e4-", "d4", "g4"]
    key += ["a4-", "a4-", "g4", "g4", "f4", "f4", "e4-", "d4 f4"]
    dur = 7*[c] + [c+3*b] + [c, b] + 6*[c] + [c+4*b+b]
    vol = lib.set_vol((vol_init, len(key), 0), VOL_VAR)
    lgh = lib.set_lgh((0.95, len(key), 0), 0.05)
    lgh[-1] = 1
    part = lib.gen_part(key, dur, vol, lgh)
    return part


def right(seeds):
    random.seed(seed=int(seeds[1]))
    part1, vol = r1()
    part = part1
    for i in range(2):
        for j in range(4):
            part2, vol = r2(vol[-1])
            part += part2
        part3, vol = r3(vol[-1])
        part += part3
    part += r4(vol[-1])
    return  [part]


def mad_world(seeds=[args.lsd, args.rsd, args.tsd]):
    parts = left(seeds)
    parts += right(seeds)
    return parts, 480, "mad_world", seeds


mid = lib.interpret(mad_world, [(700000, 16, 0)], TPO_VAR)
wav = True
if wav:
    aud = lib.mid2aud(mid)
    lib.playwav(aud)
else:
    lib.play('mad_world.mid')
