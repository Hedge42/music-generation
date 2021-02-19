import mido
import os
import random
from src import Scale, Instruments, Words
from mido import MidiFile, MidiTrack, Message, MetaMessage


class Composition:
    def __init__(self):
        self.midi_file = MidiFile()
        self.name = 'example'
        self.tracks = 0

    def add_track(self, instrument=-1):
        self.midi_file.tracks.append(MidiTrack())
        return self.midi_file.tracks.count() - 1

    def save_file(name='generated'):
        file_name = name + '.mid' if name.__contains__('.mid') else name
        # https://www.w3schools.com/python/python_file_remove.asp
        # to overwrite - because saving raises errors if the file already exists
        if os.path.exists(file_name):
            os.remove(file_name)
        m.save(file_name)


def set_bpm(bpm=-1):
    # tempo is the only requirement
    if bpm <= 60:
        bpm = random.randint(70, 160)
        print('BPM set to ' + str(bpm))
    tempo = mido.bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    # track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    # track.append(MetaMessage('key_signature', key=Scale.get_note_name(0)))


def set_instrument(instrument=-1):
    # https://i.gyazo.com/38682c2adf56d01422a7266f62c4794f.png
    # if 0 > instrument >= 127:
    if instrument < 0 or instrument > 127:
        instrument = random.randint(0, 127)
        print('Instrument: ' + Instruments.instruments[instrument])
    msg_program = Message(type='program_change', channel=0, program=instrument, time=0)
    track.append(msg_program)


def calculate_instrument(words, debug=False):
    max = 0
    ins = 0
    for i, name in enumerate(Instruments.instruments):
        score = Words.compare(words, name, debug=False)
        if score > max:
            max = score
            ins = i
    if debug:
        print('Instrument: ' + Instruments.instruments[ins] + ' (%.2f' % round(max, 2) + ')')
    return i


def calculate_bpm(words, debug=False):
    slow_score = Words.compare(words, 'slowness')
    fast_score = Words.compare(words, 'fastness')

    if debug:
        print('BPM: [%.2f' % round(slow_score, 2) + ', %.2f' % round(fast_score, 2) + ']')


def calculate_brightness(words, debug=False):
    bright_score = Words.compare(words, 'brightness')
    dark_score = Words.compare(words, 'darkness')

    if debug:
        print('Brightness: [%.2f' % round(dark_score, 2) + ', %.2f' % round(bright_score, 2) + ']')


def generate_chords(rhythm, progression, key, mode):
    if len(rhythm) != len(progression):
        print('Incompatible rhythm and progression')
        return
    messages = []
    current = []
    octave = 5
    offset = octave * 12
    for i in range(len(progression) + 1):
        # turn off current chord
        for k, n in enumerate(current):
            # only add delay for 2nd chord and beyond...
            messages.append(msg_note_off.copy(note=n, time=rhythm[i - 1] if k == 0 else 0))

        # turn on new chord, only if it's not the end of the progression
        if i < len(progression):
            chord = Scale.chord(key=key, mode=mode, root=progression[i], voices=3)
            current.clear()
            for note in chord:
                messages.append(msg_note_on.copy(note=note + offset))
                current.append(note + offset)
            # print(string_values(current))
    return messages


def generate_rhythm(length, options, min=-1, max=-1, max_length=-1, min_length=-1, debug=False):
    rhythm = []
    # while controlling for [min or max] and it is not satisfied
    while 0 <= min > len(rhythm) or 0 <= max < len(rhythm):
        rhythm = []
        while sum(rhythm) < length:
            beat = random.choice(options)
            if random.random() < 0.5:
                beat += random.choice(options)

            # Rules
            # length must equal rhythm
            # ensure length of measure is not exceeded
            while sum(rhythm) + beat > length:
                beat = random.choice(options)
                if random.random() < 0.5:
                    beat += random.choice(options)
            rhythm.append(beat)

    if debug:
        print_rhythm(rhythm)
    return rhythm


def generate_beat(options, min_length=-1, max_length=-1):
    beat = random.choice(options)
    # tie randomly
    if random.random() < 0.5:
        beat += random.choice(options)

    # while max_length < 0 or beat > max_length or beat < min_length

    return beat


def generate_melody():
    return 0


def generate_progression(rhythm, debug=False):
    # ensure that (one of) the longest beat(s) is the tonic
    longest = max(rhythm)
    longest_idx = rhythm.index(longest)

    for i in range(longest_idx):
        b = rhythm.pop()
        rhythm.append(b)


    # reorder the rhythm so that this longest beat is at the beginning

    # https://thispointer.com/python-how-to-find-all-indexes-of-an-item-in-a-list/
    longest_indices = [i for i, r in enumerate(rhythm) if r == longest]
    # for i,r in enumerate(rhythm):
    # if r == longest:
    # longest_indices.append(i)

    # randomly set one of these to the tonic
    tonic_index = random.choice(longest_indices)
    tonic_index = longest_indices[0]

    # set all to invalid
    p = [-1] * len(rhythm)
    p[tonic_index] = 0

    for i in range(0, len(p)):
        # dont set if it has already been set
        if p[i] >= 0:
            continue
        while True:
            p[i] = random.randint(0, 6)
            # doesn't match previous, and doesn't match next (if next exists)
            if p[i] != p[i - 1] and (i == len(p) - 1 or p[i] != p[i + 1]):
                break

    cadence = False
    if cadence:
        # end with 4th, 5th, or 6th
        while True:
            p[len(p) - 1] = random.randint(4, 6)
            if p[-1] != p[-2]:
                break
    if debug:
        print_progression(p)
    return p


def existing_tonic_length(intervals):
    min_tonic_ratio = 1 / 4
    min_tonic_length = 1 / 4 * w

    # get existing tonic length
    existing_tonic_length = 0
    for existing_beat in rhythm:
        if existing_beat == intervals[0]:
            existing_tonic_length += existing_beat


def mode_by_score(score):
    # brightest first
    ranked_modes = [3, 0, 4, 1, 5, 2, 6]
    if score < 0 or score > 1:
        print('Expected score in range [0,1]')
        return -1

    # get int nearest score
    return round(score)


def bpm_by_score(score):
    if score < 0 or score > 1:
        print('Excpected value in range [0,1]')
        return -1

    bpm_min, bpm_max = 40, 180
    bpm_range = bpm_max - bpm_min
    return bpm_min + round(bpm_range * score)


def random_score():
    return random.random()


def string_values(p):
    # https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    return '[' + ', '.join(map(str, p)) + ']'


def print_rhythm(rhythm):
    print('Rhythm: [' + ', '.join('%.2f' % round(r / w, 2) for r in rhythm) + ']')


def print_progression(progression):
    print('Progression: [' + ', '.join(str(p + 1) for p in progression) + ']')


def save_file(folder_path, title='generated'):
    # title = title + '.mid' if not title.__contains__('.mid') else title
    title = validate_filename(folder_path, title)

    file_path = folder_path + title + '.mid'
    m.save(file_path)
    print('Generated: ' + file_path)

def validate_filename(folder_path, title):
    temp_name = title
    ext = '.mid'
    count = 2
    while os.path.exists(folder_path + temp_name + ext):
        temp_name = title + '(' + str(count) + ')'
        count += 1
    return temp_name


phrase = 'Its a sunny day on this old hill while I walk to work begrudgingly'
calculate_instrument(phrase, debug=True)
calculate_bpm(phrase, debug=True)
calculate_brightness(phrase, debug=True)


# type cannot be overridden
msg_note_on = Message(type='note_on', channel=0, note=60, velocity=100, time=0)
msg_note_off = Message(type='note_off', channel=0, note=60, velocity=100, time=0)

# generation settings
num_generations = 10
num_measures = 4
output_folder = 'E:/Audio Samples/Generated/'

# use None or negative for random
key=4
mode=1

# export file
for n in range(num_generations):
    # create midi file, add a track
    m = MidiFile()

    # create single channel track
    m.tracks.append(MidiTrack())
    track = m.tracks[0]

    # set song information
    bpm = random.randint(70, 160)
    tempo = mido.bpm2tempo(bpm)
    set_bpm(bpm)

    # create create timings
    q = m.ticks_per_beat
    w = q * 4
    h = q * 2
    e = q // 2
    s = q // 4

    set_instrument()

    scale = Scale.Scale(key=key, mode=mode)

    title = Scale.get_mode_name(scale.mode) + '_' + Scale.get_note_name(scale.key)

    options = [w, h]

    rhythm = generate_rhythm(length=num_measures * w, options=options, min=2, debug=True)
    progression = generate_progression(rhythm, debug=True)

    progression_text = ''
    for i in range(len(progression)):
        progression_text += '_' + str(progression[i] + 1)

    title += progression_text

    # write messages, repeat
    repeats = 1
    for i in range(0, repeats):
        for msg in generate_chords(rhythm=rhythm, progression=progression, key=scale.key, mode=scale.mode):
            track.append(msg)

    save_file(folder_path=output_folder, title=title)

