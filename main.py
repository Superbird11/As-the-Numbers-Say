"""
file: main.py
author: Louis Jacobowitz (ljacobo@ncsu.edu)
"""
import ctcsound
from instrument import Instrument, Pitch
import heuristics
import sys


def init_score():
    """
    Returns the header of the cSound score, to be added to by actual instruments, as a string.
    """
    return """
; Frequency generators
f1	0	4096	10	1	                                       ; Sine wave
f2  0   4096    10  1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth wave
f3  0   4096    10  1 0   0.3 0    0.2 0     0.14 0     .111   ; Square wave
f4  0   4096    10  1 1   1   1    0.7 0.5   0.3  0.1          ; Pulse wave
f5  0   4096    9   1 1   0                                    ; for ACCCI Drumbell
f12 0    256     1  "samples/marmstk1.wav" 0 0 0               ; for Marimba


; Envelopes
f51 0   513     5   256   512  1

t   0   217                                         ; tempo: 217 BPM

"""


def init_instruments():
    """
    Creates a dict of Instrument objects (hardcoded), and returns them.
    :return: a dict of Instrument objects, where key is name/role of instrument
    """
    return {
        "bass": Instrument(mapping={"instrument": 1,
                                    "start": 2,
                                    "duration": 3,
                                    "amplitude": 4,
                                    "pitch": 5,
                                    "comment": 999,
                                    },
                           short="i4", long="i4",
                           default_pitch="5.07",
                           default_amplitude=86,
                           comment="",
                           ),
        "arpeggio": Instrument(mapping={"instrument": 1,
                                        "start": 2,
                                        "duration": 3,
                                        "amplitude": 4,
                                        "pitch": 5,
                                        "attack": 6,
                                        "reverb": 7,
                                        "comment": 999,
                                        },
                               short="i1", long="i1",
                               default_pitch="8.06",
                               default_amplitude=74,
                               attack=.02,
                               release=.01,
                               reverb=1.5,
                               comment="",
                               ),
        "high": Instrument(mapping={"instrument": 1,
                                    "start": 2,
                                    "duration": 3,
                                    "amplitude": 4,
                                    "pitch": 5,
                                    "attack": 6,
                                    "modulator": 7,
                                    "comment": 999,
                                    },
                           short="i5", long="i5",
                           default_pitch="7.08",
                           default_amplitude=70,
                           attack=.1,
                           modulator=1,
                           comment="",
                           ),
        "quick": Instrument(mapping={"instrument": 1,
                                     "start": 2,
                                     "duration": 3,
                                     "amplitude": 4,
                                     "pitch": 5,
                                     "attack": 6,
                                     "release": 7,
                                     "comment": 999,
                                     },
                            short="i3", long="i3",
                            default_pitch="8.00",
                            default_amplitude=81,
                            attack=.03,
                            release=.3,
                            comment="",
                            ),
        "long": Instrument(mapping={"instrument": 1,
                                    "start": 2,
                                    "duration": 3,
                                    "amplitude": 4,
                                    "pitch": 5,
                                    "attack": 6,
                                    "modulator": 7,
                                    "index_of_modulation": 8,
                                    "comment": 999,
                                    },
                           short="i2", long="i2",
                           default_pitch="7.00",
                           default_amplitude=71,
                           attack=1,
                           modulator=1,
                           index_of_modulation=8,
                           comment="",
                           ),
        "ascent": Instrument(mapping={"instrument": 1,
                                      "start": 2,
                                      "duration": 3,
                                      "amplitude": 4,
                                      "pitch": 5,
                                      "attack": 6,
                                      "release": 7,
                                      "comment": 999,
                                      },
                             short="i6", long="i6",
                             default_pitch="7.01",
                             default_amplitude=80,
                             attack=0.05,
                             release=0.4,
                             comment="",
                             ),
        "erratic": Instrument(mapping={"instrument": 1,
                                       "start": 2,
                                       "duration": 3,
                                       "amplitude": 4,
                                       "pitch": 5,
                                       "comment": 999,
                                       },
                              short="i7", long="i7",
                              default_pitch="7.08",
                              default_amplitude=82,
                              comment="",
                              ),
        "buzzy": Instrument(mapping={"instrument": 1,
                                     "start": 2,
                                     "duration": 3,
                                     "amplitude": 4,
                                     "pitch": 5,
                                     "attack": 6,
                                     "release": 7,
                                     "comment": 999,
                                     },
                            short="i8", long="i8",
                            default_pitch="8.06",
                            default_amplitude=77,
                            attack=0.1,
                            release=0.1,
                            comment="",
                            ),
        "churchbell": Instrument(mapping={"instrument": 1,
                                          "start": 2,
                                          "duration": 3,
                                          "amplitude": 4,
                                          "pitch": 5,
                                          "hardness": 6,
                                          "position": 7,
                                          "vibf": 8,
                                          "vibamp": 9,
                                          "comment": 999,
                                          },
                                 short="i9", long="i9",
                                 default_pitch="6.04",
                                 default_amplitude=77,
                                 hardness=0.5,
                                 position=0.9,
                                 vibf=441,
                                 vibamp=12,
                                 comment=""
                                 ),
        "happy": Instrument(mapping={"instrument": 1,
                                     "start": 2,
                                     "duration": 3,
                                     "amplitude": 4,
                                     "pitch": 5,
                                     "attack": 6,
                                     "release": 7,
                                     "comment": 999,
                                     },
                            short="i10", long="i11",
                            default_pitch="6.09",
                            default_amplitude=86,
                            attack=0.1,
                            release=0.1,
                            comment=""
                            ),
    }


def compose(instrs, beat_length):
    """
    Runs a "main loop", counting up to beat_length, adding notes for various instruments
    along the way.
    :param instrs: A dict of Instruments, where key is name/role. Hard-coded.
    :param beat_length: How many beats to continue for
    """
    bass_pitch = 1

    high_count = 0

    quick_cooldown = 0

    long_cooldown = 0

    arpeggio = []
    arpeggio_pitch = 0
    arpeggio_cooldown = 0

    ascent_max = 0
    ascent_length = 1

    buzzy_cooldown = 0

    happy_play = -1

    for beat in range(3, beat_length):
        # bassline: plays constantly, ascending until a prime number is reached
        if heuristics.is_prime(beat):
            bass_pitch = 1
            bass_amp = 10
        else:
            bass_pitch += 1
            bass_amp = 0
        instrs['bass'].add_note(
            start=beat,
            pitch=bass_pitch,
            amplitude=bass_amp,
            comment="; bass_pitch = {}".format(bass_pitch),
        )

        # quick: plays doubled staccato notes.
        #   Pitch depends on the digital root of (the beat minus the sum of its divisors).
        #   When it hits a fibonacci number, pauses for up to 9 beats depending
        #   on the number's base-10 digital root.
        if beat in range(21, 797):
            if quick_cooldown > 0:
                quick_cooldown -= 1
            elif heuristics.is_fibonacci_number(heuristics.sum_of_divisors(beat)):
                quick_cooldown = heuristics.digital_root(beat)
            else:
                hsopf = heuristics.sum_of_prime_factors(beat)
                quick_pitch = heuristics.digital_root(beat - hsopf)
                instrs['quick'].add_note(
                    start=beat,
                    length=0.5,
                    pitch=quick_pitch,
                    comment="; root({} - {} = {}) = {}".format(beat, hsopf, beat - hsopf, quick_pitch)
                )
                instrs['quick'].add_note(
                    start=beat + 0.5,
                    length=0.5,
                    pitch=quick_pitch,
                    comment='; "  "  "  "  " '
                )

        # long: plays long tones. The length of each long tone is twice the number of bases 16 or less in which the
        #    beat number is a palindrome, or for which it is not a palindrome, whichever is higher. The pitch
        #    corresponds to the lower of the same.
        #    Then, this instrument pauses for a number of beats corresponding to the number of '2's in
        #    the beat number's base-3 representation.
        if beat in range(45, 720):
            if long_cooldown > 0:
                long_cooldown -= 1
            else:
                palin = len(heuristics.palindromes(beat, range(16, 1, -1)))
                nonpalin = 15 - palin
                long_length, long_pitch = (2 * palin, nonpalin) if palin > nonpalin else (2 * nonpalin, palin)
                long_cooldown = long_length + heuristics._base(beat, 3).count('2')
                instrs['long'].add_note(
                    start=beat,
                    length=long_length,
                    pitch=-4,
                    ignore_dormant=True,
                )
                instrs['long'].add_note(
                    start=beat,
                    length=long_length,
                    pitch=long_pitch,
                    amplitude=-5,
                    ignore_dormant=True,
                    comment="; {} is a palindrome in {} bases: {}".format(
                        beat, palin, heuristics.palindromes(beat, range(16, 1, -1))),
                )

        # high note: plays chords depending on the number of ones in the number's binary representation,
        #   then rests for a number of beats determined by the number's digital sum.
        #   Further into the piece, rests for less time.
        if beat in range(160, 766):
            if high_count > 0:
                high_count -= 1
            else:
                high_pitch = 0
                overtone_add = [4, 3, 5]
                for i in range(heuristics.ones_in_binary_repr(beat)):
                    instrs['high'].add_note(
                        start=beat,
                        duration=3,
                        pitch=high_pitch,
                        ignore_dormant=True,
                        comment="; overtone {}".format(i)
                    )
                    high_pitch += overtone_add[i % 3]
                high_count = heuristics.digital_sum(beat)
                if beat > 400:
                    high_count //= 2

        # arpeggio: Plays beat-by-beat arpeggios according to the prime factors of the given number.
        #   Skips any prime numbers it encounters, and doesn't start another arpeggio until a beat after it
        #   is finished with one.
        if beat in range(222, 737):
            if arpeggio_cooldown > 0:
                arpeggio_cooldown -= 1
            elif len(arpeggio) == 0 and not heuristics.is_prime(beat):
                arpeggio_pitch = 0
                arpeggio = heuristics.prime_factors(beat)
                instrs['arpeggio'].add_note(
                    start=beat,
                    comment="; Start of arpeggio: {} --> {}".format(beat, arpeggio)
                )
            elif arpeggio:
                arpeggio_pitch += (arpeggio.pop(0) % 12) or 12
                instrs['arpeggio'].add_note(
                    start=beat,
                    pitch=arpeggio_pitch,
                    comment="; {}".format(arpeggio)
                )
                if len(arpeggio) == 0:
                    arpeggio_cooldown = 1

        # ascent: Plays a note each time the highest digit of the note (in base 12) increases.
        #   Pitch is relative to the highest digit in base 12; length is relative to how long that remains
        #   the highest digit.
        if beat in range(348, 433) or beat in range(510, 577) or beat in range(600, 721):
            digit_max = heuristics.highest_digit(beat, 12)
            if digit_max == ascent_max:
                ascent_length += 1
            else:
                instrs['ascent'].add_note(
                    start=beat - ascent_length,
                    length=ascent_length,
                    pitch=ascent_max,
                    amplitude=digit_max / 4,
                    comment="; Beat {} --> {}, length={}".format(beat-1, heuristics._base(beat-1, 12), ascent_length)
                )
                ascent_length = 1
                ascent_max = digit_max

        # erratic: Plays continuously. If the beat is divisible by its last nonzero digit, plays the tonic.
        #   If not, and the number of ones is even, plays the fourth. Otherwise, plays the fifth.
        if beat in range(252, 330) or beat in range(413, 510) or beat in range(580, 700):
            amplitude = (500 - beat) if beat in range(500, 510) else (690 - beat) if beat in range(690, 700) else 0,
            if beat % heuristics.last_nonzero_digit(beat) == 0:
                instrs['erratic'].add_note(
                    start=beat,
                    amplitude=amplitude,
                    comment="; Beat {} % {} = 0".format(beat, heuristics.last_nonzero_digit(beat))
                )
            else:
                instrs['erratic'].add_note(
                    start=beat,
                    pitch=5 if heuristics.ones_in_binary_repr(beat) % 2 == 0 else 7,
                    amplitude=amplitude,
                    comment="; Beat {} % {} = {} --> {} has {} ones".format(beat,
                                                                            heuristics.last_nonzero_digit(beat),
                                                                            beat % heuristics.last_nonzero_digit(beat),
                                                                            bin(beat),
                                                                            heuristics.ones_in_binary_repr(beat))
                )

        # buzzy: plays based on the digital root of the number's cube.
        #   When the number is divisible by its digital root (and not divisible by 3 or 9), pauses for a
        #   number of beats dependent on difference between highest and lowest digit in base 10
        if beat in range(116, 330) or beat in range(376, 475) or beat in range(550, 768):
            if buzzy_cooldown > 0:
                buzzy_cooldown -= 1
            else:
                beat_n = beat**3
                base_n = 11
                pitch_n = heuristics.digital_root(beat_n, base_n)
                instrs['buzzy'].add_note(
                    start=beat,
                    pitch=pitch_n,
                    comment="; {}^3 = {}, digital root {}".format(beat, beat_n, pitch_n)
                )
                if beat % heuristics.digital_root(beat) == 0 and beat % 3 != 0:
                    buzzy_cooldown = heuristics.highest_digit(beat) - heuristics.lowest_digit(beat)

        # churchbell: plays inconsistently, randomly, when the number of ones in the number's binary representation
        #   is also one of the number's divisors. Pitch is decided simply by the lowest digit in the number. Length
        #   is determined by the number of divisors, multiplied until it's greater than 8; then that is multiplied by 2
        if beat in range(270, 660):
            if heuristics.ones_in_binary_repr(beat) in heuristics.divisors(beat):
                churchbell_amp = 15 * (beat / 660)
                churchbell_length = len(heuristics.divisors(beat))
                while churchbell_length <= 8:
                    churchbell_length += len(heuristics.divisors(beat))
                # churchbell_length *= 2
                instrs['churchbell'].add_note(
                    start=beat,
                    pitch=heuristics.lowest_digit(beat),
                    amplitude=churchbell_amp,
                    length=churchbell_length,
                    comment="; n1s={}, divisors={}, pitch={}, length={}".format(heuristics.ones_in_binary_repr(beat),
                                                                                heuristics.divisors(beat),
                                                                                heuristics.lowest_digit(beat),
                                                                                churchbell_length)
                )

        # Happy: Plays based on happy numbers. Toggles on/off for each happy number encountered (in base 10). The
        #   pitch depends on how many bases (16 or less) in which the number is happy, when it's toggled off.
        if beat in range(298, 378) or beat in range(435, 560) or beat in range(606, 692):
            is_happy = heuristics.is_happy_number(beat)
            if is_happy:
                if happy_play == -1:
                    happy_play = beat
                else:
                    happy_pitch = sum(heuristics.is_happy_number(beat, b) for b in range(2, 17))  # adding booleans
                    instrs['happy'].add_note(
                        start=happy_play,
                        length=beat - happy_play,
                        pitch=happy_pitch,
                        comment="; {} --> {} is happy in bases {}".format(happy_play, beat, [b for b in range(2, 17)
                                                                          if heuristics.is_happy_number(beat, b)])
                    )
                    happy_play = -1
    #
    return


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'custom':
        with open('custom.orc') as orc_file, open('custom.sco') as sco_file:
            orc = orc_file.read()
            sco = sco_file.read()
            print(orc)
            print(sco)
    else:
        with open('inst.orc') as orc_file:
            orc = orc_file.read()

        sco = init_score()
        instruments = init_instruments()
        beats_total = 810  # at 217 BPM, around 3:41
        #
        compose(instruments, beats_total)
        #
        for instr in instruments.values():
            sco += instr.output_note_sequence() + "\n"
        print(sco)
        #
    cout = ctcsound.Csound()
    cout.setOption("-ocomposition.wav")
    cout.compileOrc(orc)
    cout.readScore(sco)
    cout.start()
    cout.perform()
    cout.reset()

    c = ctcsound.Csound()
    c.setOption("-odac")    # output to the DAC
    c.compileOrc(orc)
    c.readScore(sco)
    c.start()
    c.perform()
    c.reset()



