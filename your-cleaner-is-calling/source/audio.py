"""Soft lo-fi bed (88 BPM, F major 9ths) + phone ring + two Kokoro voices. Times match index.html."""
import numpy as np, wave, subprocess, json, soundfile as sf
from audio_lib import Mix, note as n, chord
DUR, BPM = 37.0, 88
VO = [2.6, 4.1, 8.5, 14.0, 15.8, 20.1, 21.6, 24.2, 25.3, 27.6, 33.6]
CUTS = [2.6, 8.3, 14.0, 15.6, 21.5, 24.1, 27.4, 33.5]
m = Mix(duration=DUR, bpm=BPM)
# phone ring: two-tone trill, twice
for r0 in (0.15, 1.35):
    for k in range(10):
        m.bell(r0 + k * 0.07, n(19 if k % 2 else 15), 0.05, 0.25)
m.boom(0.0, 0.3); m.whoosh(2.45, 0.4, 0.08)
prog = ['Fmaj9', 'Em7', 'Dm9', 'Cmaj9']
bar = 4 * 60 / BPM
t, i = 2.6, 0
while t < 33.5:
    t1 = min(t + bar, 33.5)
    m.pad(chord(prog[i % 4]), t, t1, amp=0.03)
    m.beat(t, t1, n([-31, -32, -34, -36][i % 4]), kick=0.12, bass=0.06, hat=0.012, snare=0.03, sixteenths=False, swing=0.18, pattern='half')
    t, i = t1, i + 1
m.vinyl(2.6, 33.5, 0.008)
for t in CUTS: m.tick(t, 0.035)
for t in (9.0, 10.0, 11.4, 12.5): m.pluck(t, n(12 + [0, 4, 7, 12][[9.0, 10.0, 11.4, 12.5].index(t)]), 0.07)  # checklist ticks
m.pluck(20.1, n(16), 0.09); m.bell(21.6, n(24), 0.06, 1.0)                                                       # button press, calendar ping
m.riser(27.4, 0.7, 0.08)
for k, t in enumerate([27.4, 28.6, 29.5, 30.4, 31.5]): m.chord_hit(t, chord(prog[k % 4], 4), voice='piano', amp=0.05, dur=0.9); m.kick(t, 0.16)
m.boom(33.5, 0.25); m.pad(chord('Fmaj9'), 33.5, DUR, amp=0.045); m.chord_hit(33.5, chord('Fmaj9', 4), voice='piano', amp=0.08, dur=3.0)
m.bell(34.2, n(24), 0.05, 1.5)
m.render('music.wav', rms=.14)
# voice track
sr = 48000; N = int(DUR * sr); vo = np.zeros(N)
for i, t0 in enumerate(VO):
    a, s = sf.read(f'vo/{i:02d}.wav')
    a = np.interp(np.arange(0, len(a), s / sr), np.arange(len(a)), a)
    o = int(t0 * sr); vo[o:o + len(a)] += a[:N - o]
sf.write('vo.wav', vo, sr)
fps = 30; hop = sr // fps
env = [float(np.sqrt(np.mean(vo[k*hop:(k+1)*hop]**2))) for k in range(N // hop)]
mx = max(env); open('env.js', 'w').write('const VOENV=' + json.dumps([round(e / mx, 3) for e in env]) + ';')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'music.wav', '-i', 'vo.wav', '-filter_complex',
  '[1:a]aresample=48000,apad,pan=stereo|c0=c0|c1=c0,volume=1.7,asplit=2[v][sc];[0:a]aresample=48000,volume=0.6[m];'
  '[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300[md];'
  '[md][v]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11',
  '-ar', '48000', '-t', str(DUR), 'audio.wav'], check=True)
print('audio.wav: music + voices')
