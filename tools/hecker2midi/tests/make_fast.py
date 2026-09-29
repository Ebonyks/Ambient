"""Early-era style test: chords every 3 s, a fast pentatonic melody (0.3-0.8 s notes),
glitch stutters, saturation, crush, shorter reverb, rain noise."""
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve, lfilter

sr = 44100
rng = np.random.default_rng(7)
TUNE = -0.18
truth = []
# chords (D major shimmer progression), each 3 s, slow-ish attack
chords = [
    [38, 50, 57, 64, 71],        # Dadd9 / 6
    [35, 47, 54, 57, 64, 71],    # Bm11
    [31, 43, 50, 57, 64, 71],    # G6/9
    [33, 45, 52, 59, 64, 71],    # Aadd9
    [36, 48, 55, 57, 64, 71],    # C
    [29, 41, 57, 64, 71],        # Fmaj7#11
    [31, 43, 46, 50, 57, 64],    # Gm
    [38, 50, 57, 64, 71],        # D
]
t0 = 0.0
for ch in chords:
    for m in ch:
        truth.append((t0, t0 + 3.0, m, 0, "chord"))
    t0 += 3.0
dur = t0 + 2
# melody: D major pentatonic, upper register, 0.3-0.8 s notes with small rests
pent = [74, 76, 78, 81, 83, 86]
t = 0.5
while t < t0 - 1:
    d = rng.choice([0.3, 0.4, 0.5, 0.6, 0.8])
    m = int(rng.choice(pent))
    truth.append((t, t + d, m, 0, "melody"))
    t += d + rng.choice([0.0, 0.05, 0.15, 0.3])

tt_all = np.arange(int(dur * sr)) / sr
y = np.zeros_like(tt_all)
for s, e, m, c, kind in truth:
    f = 440 * 2 ** ((m + c / 100 + TUNE - 69) / 12)
    i0, i1 = int(s * sr), int(e * sr)
    tt = tt_all[i0:i1] - s
    if kind == "chord":
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (e - s - tt) / 0.4) * 0.6
        H = 8
    else:
        env = np.minimum(1, tt / 0.02) * np.exp(-tt / 0.9) * np.minimum(1, (e - s - tt) / 0.05) * 0.9
        H = 5
    ph = 2 * np.pi * f * tt
    sig = sum((1 / h) * np.sin(h * ph + h) for h in range(1, H + 1) if h * f < sr / 2)
    y[i0:i1] += env * sig
y /= np.max(np.abs(y))
# glitch stutter: repeat short buffers at random points
for k in range(25):
    i = rng.integers(sr, len(y) - sr)
    L = int(rng.choice([0.02, 0.04, 0.08]) * sr)
    reps = rng.integers(3, 10)
    seg = y[i:i + L].copy()
    for r in range(reps):
        j = i + r * L
        if j + L < len(y):
            y[j:j + L] = seg
y = np.tanh(3 * y)
step = sr / 11025
idx = (np.floor(np.arange(len(y)) / step) * step).astype(int)
y = np.round(y[idx] * 255) / 255
ir_t = np.arange(int(1.5 * sr)) / sr
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.35)
ir[0] = 10
y = fftconvolve(y, ir)[: len(tt_all)]
y /= np.max(np.abs(y))
w = rng.standard_normal(len(y))
pink = lfilter([0.049922035, -0.095993537, 0.050612699, -0.004408786], [1, -2.494956002, 2.017265875, -0.522189400], w)
y = y + 0.25 * pink / np.max(np.abs(pink))
y /= np.max(np.abs(y)) * 1.05
sf.write("test_fast.wav", y.astype(np.float32), sr)
import pickle
pickle.dump((truth, TUNE), open("truth_fast.pkl", "wb"))
print(len([x for x in truth if x[4] == 'melody']), "melody notes,", len([x for x in truth if x[4] == 'chord']), "chord tones")
