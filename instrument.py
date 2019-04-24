"""
file: instrument.py
author: Louis Jacobowitz (ljacobo@ncsu.edu)
"""

import re

HALF_STEPS_IN_OCTAVE = 12

class Pitch:
    """
    Represents a cSound pitch class, decomposed into octave and note
    """

    def __init__(self, pitch_class):
        """
        Constructs a pitch object from a given pitch string or tuple
        :param pitch_class: A string (e.g. '8.01'), representing octave and number of half-steps,
                            or a tuple (octave, halfsteps), e.g. (8, 1).
        """
        if type(pitch_class) == str:
            if not re.fullmatch(r'\d+.\d+', pitch_class):
                raise ValueError('Pitch class must be a string in the form "octave.note", e.g. "8.01"')
            self.octave, self.note = (int(i) for i in pitch_class.split('.'))
        elif type(pitch_class) == tuple and len(pitch_class) == 2:
            self.octave, self.note = pitch_class
        else:
            raise ValueError("Pitch class must be a string or a 2-tuple")
        self.resolve()

    def resolve(self):
        """
        Changes the octave according to the note, if the note is greater than or equal to 12 or less than 0.
        Then, mods the note to be within that range.
        """
        self.octave += self.note // HALF_STEPS_IN_OCTAVE
        self.note %= HALF_STEPS_IN_OCTAVE

    def __iadd__(self, other):
        """
        If argument is a Pitch, adds octaves together and notes together.
        If argument is an int, adds that many half-steps.
        Throws a ValueError otherwise.
        """
        if type(other) not in (Pitch, int):
            raise ValueError('Cannot add Pitch to non-Pitch/non-Int value')
        if type(other) == Pitch:
            self.octave += other.octave
            self.note += other.note
        else:
            self.note += other
        self.resolve()
        return self

    def __isub__(self, other):
        """
        If argument is a Pitch, subtracts the number of octaves and notes.
        If argument is an int, subtracts that many notes.
        Throws a ValueError otherwise.
        """
        if type(other) not in (Pitch, int):
            raise ValueError('Cannot add Pitch to non-Pitch/non-Int value')
        if type(other) == Pitch:
            self.octave -= other.octave
            self.note -= other.note
        else:
            self.note -= other
        self.resolve()
        return self

    def __add__(self, other):
        """
        If argument is a Pitch, adds octaves together and notes together.
        If argument is an int, adds that many half-steps.
        Throws a ValueError otherwise.
        """
        if type(other) not in (Pitch, int):
            raise ValueError('Cannot add Pitch to non-Pitch/non-Int value')
        if type(other) == Pitch:
            new_oct = self.octave + other.octave
            new_note = self.note + other.note
        else:
            new_oct = self.octave
            new_note = self.note + other
        return Pitch((new_oct, new_note))

    def __sub__(self, other):
        """
            If argument is a Pitch, subtracts the number of octaves and notes.
            If argument is an int, subtracts that many notes.
            Throws a ValueError otherwise.
        """
        if type(other) not in (Pitch, int):
            raise ValueError('Cannot add Pitch to non-Pitch/non-Int value')
        if type(other) == Pitch:
            new_oct = self.octave - other.octave
            new_note = self.note - other.note
        else:
            new_oct = self.octave
            new_note = self.note - other
        return Pitch((new_oct, new_note))

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __str__(self):
        """
        Returns a string representation of the pitch in the format "8.02", with non-padded octave
        and two-character zero-padded note
        """
        return "{:d}.{:02d}".format(self.octave, self.note)


class Instrument:
    def __init__(self, mapping, short="i1", long="i1", default_pitch="8.00", default_amplitude=86, **kwargs):
        """
        Initializes an instrument.
        :param mapping: A dict with keys corresponding to variable names, and values corresponding to p-variables
                        in a cSound score.
        :param short: (str) The instrument in the orchestra to refer to for short notes (1 beat)
        :param long: (str) The instrument in the orchestra to refer to for long notes (>1 beat)
        :param default_pitch: The default pitch class for this instrument, added to/subtracted from
        :param default_amplitude: The default amplitude for this instrument in decibels, to be added to/subtracted from
        :param kwargs: Other named fields that map to p-variables through mapping, and their default values.
        """
        self.mapping = mapping
        self.short_instrument = short
        self.long_instrument = long
        self.default_pitch = Pitch(default_pitch)
        self.default_amplitude = default_amplitude
        self.default_kwargs = kwargs
        self.note_sequence = []
        self.dormant_until = 0

    def add_note(self, start, length=1.0, pitch=None, amplitude=None, ignore_dormant=False, **kwargs):
        """
        Adds a note to the sequence of notes this Instrument will play during the piece.
        Values not given that are nevertheless in `mapping` will be assumed to be default values, or 0 if none exist.
        If the note is told to start while this instrument is currently playing another note, then the instrument
          will ignore the request.
        :param start: The beat on which this note starts
        :param length: The length of this note, in beats
        :param pitch: The pitch adjustment of this note relative to the default for this instrument (as an int)
        :param amplitude: The amplitude adjustment of this note relative to default (as an int, in decibels)
        :param kwargs: Other named fields mapping to p-variables, changed relative to default values.
        """
        if not ignore_dormant and start < self.dormant_until:
            return
        note = {
            "instrument": self.short_instrument if length <= 1 else self.long_instrument,
            "start": start,
            "duration": length,
            "amplitude": (self.default_amplitude + amplitude) if type(amplitude) == int else self.default_amplitude,
            "pitch": (self.default_pitch + pitch) if type(pitch) == int else self.default_pitch,
        }
        for key in self.mapping.keys():
            if key in note:
                # then we already covered it and have no need to do so again
                continue
            if key in kwargs and key in self.default_kwargs:
                note[key] = self.default_kwargs[key] + kwargs[key]
            elif key in kwargs:
                note[key] = kwargs[key]
            elif key in self.default_kwargs:
                note[key] = self.default_kwargs[key]
            else:
                note[key] = 0
        self.note_sequence.append(note)
        self.dormant_until = start + length

    def output_note_sequence(self):
        """
        Returns, as a string, a cSound score table for each note this instrument plays throughout the piece,
        in order, without headings, according to the mapping given upon construction.
        Arguments in each line are tab-separated.
        """
        output = []
        for note in self.note_sequence:
            mapping = sorted(list(self.mapping.items()), key=lambda x: x[1])
            args = [str(note[x[0]]) for x in mapping]
            output.append("\t".join(args))
        return "\n".join(output)
        # return "\n".join("\t".join(str(note[x[0]]) for x in sorted(list(self.mapping.items()), key=lambda i:i[1])) for note in self.note_sequence)

