import argparse
import numpy as np
from mido import MidiFile
from numpy import random
from pandas import read_csv
import lib
b = 480
c = 240
parser = argparse.ArgumentParser(description='Set the tune to play and possibly the seed')
parser.add_argument('--seed', nargs='?', type=int, default=3,
                    help='The random seed to use (omit to not use a seed)')
args = parser.parse_args()
def mad_world(seed):
    key = ["a4-", "c5", "g4", "a4-", "f4", "g4", "e4-", "d4",
           "s", "a4-",
           "c5", "g4", "a4-", "f4", "g4", "a4-",
           "b4-"]
    dur = 8*[c] + [2*b+b+c] + [2*c] + 6*[c] + [c + 4*b]
    vol = lib.set_vol((64, len(key), 0), 2)
    lgh = lib.set_lgh((0.9, len(key), 0), 0.01)
    part = lib.gen_part(key, dur, vol, lgh)
    durt = np.sum(dur)
    keyl = ["s", "a3- c4", "f3", "a3- c4",
            "b3-", "d4 f4", "b3-", "d4 f4",
            "f3", "a3- c4", "f3", "a3- c4",
            "b3-", "d4 f4", "b3-", "d4 f4"]
    durl = 16*[b]
    voll = lib.set_vol((54, len(keyl),0))
    lghl = 3*[0.90] + [0.5]
    for i in range(3):
        lghl += 3*[0.90] + [0.5]
    partl = lib.gen_part(keyl, durl, voll, lghl)

    return part, durt, partl


def music(seed, fname="mad_world"):
    """Play a tune encoded in a group of csv file"""
    mid = MidiFile()
    mid.ticks_per_beat = b
    random.seed(seed=seed)

    part, durt, partl = mad_world(seed)
    trk = lib.part2trk(part)
    trkl = lib.part2trk(partl)

    mid.tracks.append(trk)
    mid.tracks.append(trkl)
    nbeats = int(durt / mid.ticks_per_beat)
    mid, ibis = lib.set_ibis(mid, (700000, nbeats, 0), scale=30000)
    mid.save(fname + '.mid')
    return mid


mid = music(args.seed)
lib.play('mad_world.mid')
