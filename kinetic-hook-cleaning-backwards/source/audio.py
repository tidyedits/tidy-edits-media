"""Minimal house, 150 BPM, chromatic descending bass (A -> G# -> G -> F#). Cut times copied from index.html."""
from audio_lib import Mix, note as n, chord
DUR, BPM = 20, 150
B = 60/BPM
CUTS = [0, 1.6, 3.2, 4.0, 7.2, 10.4, 13.6, 15.2, 17.2]
m = Mix(duration=DUR, bpm=BPM)
prog = [('Am9', -24), ('G#m7', -25), ('Gmaj7', -26), ('F#m7', -27)]  # chromatic bass walk
for i, t0 in enumerate([1.6 + k*3.2 for k in range(5)]):
    name, root = prog[i % 4]
    t1 = min(t0 + 3.2, 15.2)
    if t0 >= 15.2: break
    m.pad(chord(name), t0, t1, amp=0.035)
    m.beat(t0, t1, n(root), kick=0.2, bass=0.09, hat=0.018, snare=0.0, sixteenths=True, pattern='four', clap=True)
# hook: hard boom + whoosh, silence-ish pad so the slam reads
m.boom(0.0, 0.45); m.whoosh(0.05, 0.6, 0.12)
m.pluck(0.45, n(7), 0.1); m.pluck(0.6, n(7), 0.1)        # scribble X strokes
m.riser(1.6, 0.5, 0.1)
m.riser(13.6, 0.8, 0.14)
for t in (13.6, 14.0, 14.4, 14.8):                         # climax strobe
    m.boom(t, 0.3 if t == 13.6 else 0.16); m.chord_hit(t, chord('Am9', 4), voice='piano', amp=0.06, dur=0.5)
    m.kick(t, 0.24); m.clap(t, 0.06)
# outro: warm and calm under logo + poster
m.pad(chord('Fmaj9'), 15.2, 20, amp=0.05)
m.chord_hit(15.2, chord('Fmaj9', 4), voice='piano', amp=0.08, dur=2.5)
m.chord_hit(17.2, chord('Cmaj9', 4), voice='piano', amp=0.08, dur=3.0)
for k, t in enumerate([15.6, 16.0, 16.4, 17.6, 18.0, 18.4, 18.8]):
    m.bell(t, n([12, 16, 19, 12, 16, 21, 19][k]), 0.05, 1.2)
for t in CUTS[1:]:
    m.tick(t, 0.04)
for t in (5.4, 8.4, 11.65):                                # DOWN / WET / strike-through accents
    m.boom(t, 0.14)
for t in (15.2, 17.2):
    m.boom(t, 0.28); m.kick(t, 0.24); m.whoosh(t - 0.05, 0.5, 0.08)
m.bell(16.55, n(24), 0.06, 1.5)
m.render('audio.wav')
