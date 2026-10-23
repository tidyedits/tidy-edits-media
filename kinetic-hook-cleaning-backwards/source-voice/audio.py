"""Minimal house bed (150 BPM, chromatic descending bass) ducked under the Higgsfield ElevenLabs voiceover (vo.wav)."""
import subprocess
from audio_lib import Mix, note as n, chord
DUR = 22
CUTS = [0, .9, 2.15, 3.7, 7.6, 11.85, 14.5, 16.4, 18.8]
m = Mix(duration=DUR, bpm=150)
prog = [('Am9', -24), ('G#m7', -25), ('Gmaj7', -26), ('F#m7', -27)]
secs = [(2.15, 3.7), (3.7, 7.6), (7.6, 11.85), (11.85, 14.5)]
for i, (a, b) in enumerate(secs):
    name, root = prog[i]
    m.pad(chord(name), a, b, amp=0.03)
    m.beat(a, b, n(root), kick=0.18, bass=0.08, hat=0.016, snare=0.0, sixteenths=True, pattern='four', clap=True)
m.boom(0.0, 0.45); m.whoosh(0.05, 0.6, 0.12)
m.pluck(0.45, n(7), 0.1); m.pluck(0.62, n(7), 0.1)
m.riser(2.15, 0.6, 0.1); m.riser(14.5, 0.8, 0.12)
for t in (14.5, 15.0, 15.4, 15.95):
    m.boom(t, 0.3 if t == 14.5 else 0.16); m.chord_hit(t, chord('Am9', 4), voice='piano', amp=0.06, dur=0.5)
    m.kick(t, 0.24); m.clap(t, 0.06)
m.pad(chord('Fmaj9'), 16.4, DUR, amp=0.045)
m.chord_hit(16.4, chord('Fmaj9', 4), voice='piano', amp=0.08, dur=2.5)
m.chord_hit(18.8, chord('Cmaj9', 4), voice='piano', amp=0.08, dur=3.0)
for t in (16.4, 18.8):
    m.boom(t, 0.28); m.kick(t, 0.24); m.whoosh(t - 0.05, 0.5, 0.08)
for t in CUTS[1:]:
    m.tick(t, 0.04)
for t in (4.95, 9.1, 13.85, 17.45):
    m.boom(t, 0.14)
m.render('music.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'music.wav', '-i', 'vo.wav', '-filter_complex',
  '[1:a]aresample=48000,apad,pan=stereo|c0=c0|c1=c0,volume=1.6,asplit=2[v][sc];[0:a]aresample=48000,volume=0.55[m];'
  '[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=250[md];'
  '[md][v]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11',
  '-ar', '48000', '-t', str(DUR), 'audio.wav'], check=True)
print('audio.wav mixed with voiceover')
