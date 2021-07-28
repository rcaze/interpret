import argparse
from mido import MidiFile
from numpy import random
from pandas import read_csv
import lib

parser = argparse.ArgumentParser(description='Set the tune to play and possibly the seed')
parser.add_argument('tune', nargs='?', type=str, default='scale')
parser.add_argument('--seed', nargs='?', type=int, default=3,
                    help='The random seed to use (omit to not use a seed)')
args = parser.parse_args()

def music(fname, seed):
    """Play a tune encoded in a group of csv file"""
    k_d = read_csv(fname + '.csv')
    key = list(k_d['key'])
    dur = list(k_d['dur'])
    cre = 0  # set a crescendo with a positive value and decrescendo otherwise
    lev = 64 # set how loud things are played
    vol = lib.set_vol((lev, len(key), cre))

    mid = MidiFile()
    mid.ticks_per_beat = 480
    random.seed(seed=seed)

    part = lib.gen_part(key, dur, vol)
    trk = lib.part2trk(part)

    mid.tracks.append(trk)

    tks_dur = sum(dur)
    nbeats = int(tks_dur / mid.ticks_per_beat)
    mid, ibis = lib.set_ibis(mid, (500000, nbeats, 0), scale=100000)
    mid.save(fname + '.mid')
    return mid


mid = music(args.tune, args.seed)
lib.play(args.tune + '.mid')
