from mido import MetaMessage, Message, MidiFile, MidiTrack

import numpy.random as rd
import numpy as np
import pygame

import os
from shutil import copyfile
from pathlib import Path

def random_walk(seed, nstp, loc=0, scale=1, rounding=True, bound=(0, 127)):
    """Generate a random walk following a normal law

    Parameters
    ----------
    seed: int or float, initial value of the random walk
    nstp: int, number of elements in the sequence
    loc: float, the mean value of the gaussian noise
    scale: float, the standard deviation

    Output
    ------
    rands: ints list, the entire sequence between low and high of size nstp

    Comments
    --------
    This function is the heart of quantic music
    """
    low, high = bound
    rands = [seed]

    for i in range(nstp-1):
        seed += rd.normal(loc, scale)  # Generate the next value using a normal law

        # The two bounds are sticky seed cannot go beyond them.
        if seed < low:
            rands += [low]
            seed = low
        elif seed > high:
            rands += [high]
            seed = high
        else:
            rands += [seed]  # Add the int to the list

    if rounding:  # Turn the list into ints
        rands = [int(i) for i in rands]

    return rands



def set_vol(v_trpl=(64, 10, 0), scale=1):
    """Generate a drifting volume within a given range"""
    vol = random_walk(v_trpl[0], v_trpl[1], v_trpl[2], scale)

    return vol


def set_lgh(lgh_trpl=(0.9, 4, -0.1), scale=0.1):
    """Generate a drifting lightness"""
    lgh = random_walk(lgh_trpl[0], lgh_trpl[1], lgh_trpl[2], scale,
                      bound=(0.1 , 1), rounding=False)
    return lgh


def split(val, div):
    """Divide a number given a percentage"""
    a_remainer = int(val*div)
    b_remainer = val - a_remainer
    return a_remainer, b_remainer


def char2note(char):
    """Convert a char to a midi note number wih the followung syntax. First
    the note ('a', 'b' , etc..) followed by the keyboard octave number and
    finally its accentuation ('-', '+'). By default the on velocity and off
    velocity are set"""
    if char == 's':  # Return a silence
        return 0, 0, 0
    notes = {'a': 69, 'b': 71, 'c': 60, 'd': 62, 'e': 64, 'f': 65, 'g': 67}
    note_nb = notes[char[0]]
    note_nb += (int(char[1])-4) * 12
    if len(char) == 3:
        if char[2] == '-':
            note_nb -= 1
        if char[2] == '+':
            note_nb += 1
    v_on = 64
    v_off = 100
    return note_nb, v_on, v_off


def gen_part(key, dur, vol, lgh=None):
    """"Merge the different element to add a track to a midi file"""
    if (len(key) != len(dur)) or (len(key) != len(vol)):
        print(len(key), len(dur), len(vol))
        import pdb; pdb.set_trace()  # XXX BREAKPOINT

    if not lgh:
        lgh=[1 for i in range(len(vol))]

    l_size = len(vol)
    out = [[key[i], dur[i], vol[i], lgh[i]] for i in range(l_size)]
    return out


def part2trk(part):
    """Create a track from notes with a particular syntax."""
    remain=0
    trk = MidiTrack()

    for i, note in enumerate(part):
        if note[0] == 's':  # Message for a silence
            trk.append(Message("note_on", note=0, velocity=100, time=0))
            trk.append(Message("note_off", note=0, velocity=100, time=note[1]))
            continue

        nlist = note[0].split(' ')

        for j, c_n in enumerate(nlist):  # Add all notes as on type message
            n_nb, v_pn, v_off = char2note(c_n)
            trk.append(Message("note_on", note=n_nb, velocity=note[2],
                               time=remain))
        end, remain = split(note[1], note[3])

        trk.append(Message("note_off", note=n_nb, velocity=100,
                           time=end))

        for c_n in nlist[:-1]:  # Add the note off message
            n_nb, v_pn, v_off = char2note(c_n)
            trk.append(Message("note_off", note=n_nb, velocity=100,
                               time=0))

    return trk


def set_ibis(mid, ibi=(100000, 1, 0), scale=2000, trk=None):
    """"Set the interbeat intervals (ibs) of a song using rand_v to provide a unique texture to it

    Parameters
    ----------
    mid: MidiFile, the midi file
    ibi: a triple, the initial value of the inter-beat interval (ibi)
    how many ibi and how they evolve
    trk: None or TrackFile, the track containing the tempo
    """
    ibis = random_walk(ibi[0], ibi[1], ibi[2], scale, bound=(100000, 2000000))

    if not trk:  # Create a track to have all the temporal variation
        trk = MidiTrack()
        trk.name = "Tempo variation"

    # Set a metamessage to change the tempo between each beat
    trk.append(MetaMessage("set_tempo",
                           tempo=ibis[0],
                           time=0))

    for i, c_ibi in enumerate(ibis):  # Change the tempo
        trk.append(MetaMessage("set_tempo",
                               time=mid.ticks_per_beat,
                               tempo=c_ibi))

    mid.tracks.append(trk)

    return mid, ibis




def ibs2tpo(ibs):
    """Turn interbeat interval into a tempo or the other ways around"""
    return (1000000/ibs)*60


def play_music(midi_filename):
  '''Stream music_file in a blocking manner'''
  set_pygame()
  clock = pygame.time.Clock()
  pygame.mixer.music.load(midi_filename)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30) # check if playback has finished


def set_pygame():
    # mixer config
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)


def play(midi_filename):
    # listen for interruptions
    try:
        # use the midi file you just saved
        play_music(midi_filename)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit




if __name__ == "__main__":
    mid = MidiFile()
    # Set the keys to play a C scale on two octaves
    Cscale = ["c", "d", "e", "f", "g", "a", "b"]
    key = [i + "4" for i in Cscale] + ["c5"]
    # Set a constant duration of a Whole here
    dur = [480 for s in key]
    # Vary the velocity/volume for each key stroke
    vol = set_vol((64, 8, 3))
    # Set the lightness to have a 4/4 time signature
    lgh = set_lgh((0.9, 4, -0.15))
    lgh += set_lgh((0.9, 4, -0.15))
    deter = False
    if deter:
        lgh = [0.9, 0.8, 0.8, 0.4]
        lgh += [0.9, 0.8, 0.8, 0.4]
    # Merge all and add to the mid
    part = gen_part(key, dur, vol, lgh)
    trk = part2trk(part)
    mid.tracks.append(trk)

    mid, ibs = set_ibis(mid, (500000, 8, 0))
    mid.save("scale.mid")

    # Play the mid file
    play("scale.mid")
