from mido import MidiFile
from numpy import random
import lib


key = ['c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4', 'c5']
dur = [480 for i in range(len(key))]
cre = 0  # set a crescendo with a positive value and decrescendo otherwise
lev = 64 # set how loud things are played
vol = lib.set_vol((lev, len(key), cre))

def music(seed=3):
    mid = MidiFile()
    mid.ticks_per_beat = 480
    random.seed(seed=seed)

    part = lib.gen_part(key, dur, vol)
    trk = lib.part2trk(part)

    mid.tracks.append(trk)

    mid, ibis = lib.set_ibis(mid, (500000, 8, 0), scale=100000)

    return mid


seed = input('Set the seed:')
name = 'music.mid'
mid = music(int(seed))
mid.save(name)
lib.play(name)
