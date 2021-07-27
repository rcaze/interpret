from mido import MidiFile
from numpy import random
import lib


key = ['c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4', 'c5']
dur = [480 for i in range(len(key))]
vol = lib.set_vol((64, 8, 2))
lgh = lib.set_lgh((0.9, 8, 0))

def music(seed=3):
    mid = MidiFile()
    mid.ticks_per_beat = 480
    random.seed(seed=seed)

    part = lib.gen_part(key, dur, vol, lgh)
    trk = lib.part2trk(part)

    mid.tracks.append(trk)

    mid, ibis = lib.set_ibis(mid, (500000, 8, 0), scale=100000)

    return mid


seed = input('Set the seed:')
name = 'music.mid'
mid = music(int(seed))
mid.save(name)
play(name)
