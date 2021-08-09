import argparse
from mido import MidiFile
from numpy import random
from pandas import read_csv
import lib

parser = argparse.ArgumentParser(description='Set the tune to interpret and the seed (optional)')
parser.add_argument('tune', nargs='?', type=str, default='002')
parser.add_argument('--seed', nargs='?', type=int, default=3,
                    help='The random seed to use (omit to not use a specific seed)')
parser.add_argument('--var', nargs='?', type=int, default=1000,
                    help='The variation from beat to beat')
args = parser.parse_args()

def music(fname, seed, var):
    """Play a tune encoded in a group of csv file"""
    random.seed(seed=seed)
    mid = lib.MidiFile(fname + ".mid")
    dur = 0
    for msg in mid.tracks[0]:
        if not msg.is_meta:
            dur += msg.time

        if hasattr(msg, 'tempo'):
            tempo = msg.tempo

    #determine the duration in ticks and the number of beats
    nbeats = int(dur / mid.ticks_per_beat)
    mid, ibis = lib.set_ibis(mid, (random.normal(tempo,var), nbeats, 0), scale=var)
    mid.save(fname + '_interpreted.mid')
    return mid

mid = music(args.tune, args.seed, args.var)
lib.play(args.tune + '_interpreted.mid')
