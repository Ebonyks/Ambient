"""Third test file (a cross-check, not a strict held-out test): A minor / C region, piano-like decaying chord
tones + sustained pad, melody INSIDE the chord register, common tape wobble on everything,
chorus-detuned doubles, softer saturation, long reverb, vinyl crackle and hiss."""
import numpy as np, soundfile as sf, pickle
from scipy.signal import fftconvolve, lfilter

sr = 44100
rng = np.random.default_rng(42)
TUNE = +0.22
chords = [  # (bass, upper voices), 4 s each
    [33, 45, 52, 60, 64, 71],   # Am(add9)
    [29, 41, 48, 57, 64, 67],   # Fmaj7
    [36, 48, 55, 59, 64, 69],   # Cmaj7/6
    [31, 43, 50, 59, 62, 69],   # G6/9
    [38, 50, 57, 60, 65, 69],   # Dm7
    [28, 40, 47, 55, 59, 64],   # Em
]
truth = []
t0 = 0.0
for ch in chords:
    for m in ch:
        truth.append((t0, t0 + 4.0, m, "chord"))
    t0 += 4.0
dur = t0 + 3
# melody in the MIDDLE register, A minor pentatonic, 0.4-1.2 s
pent = [57, 60, 62, 64, 67, 69, 72]
t = 0.8
while t < t0 - 1.2:
    d = float(rng.choice([0.4, 0.6, 0.8, 1.2]))
    truth.append((t, t + d, int(rng.choice(pent)), "melody"))
    t += d + float(rng.choice([0.1, 0.3, 0.6]))

tt = np.arange(int(dur * sr)) / sr
wobble = 0.08 * np.sin(2 * np.pi * 0.45 * tt) + 0.03 * np.sin(2 * np.pi * 1.7 * tt)  # semitones, common
y = np.zeros_like(tt)
for s, e, m, kind in truth:
    i0, i1 = int(s * sr), int(e * sr)
    x = tt[i0:i1] - s
    for det in ((0.0, 1.0), (0.09, 0.6)) if kind == "chord" else ((0.0, 1.0),):
        f = 440 * 2 ** ((m + det[0] + TUNE + wobble[i0:i1] - 69) / 12)
        ph = 2 * np.pi * np.cumsum(f) / sr
        if kind == "chord":
            env = (0.55 * np.exp(-x / 1.2) + 0.45 * np.minimum(1, x / 1.0)) * np.minimum(1, (e - s - x) / 0.5)
            H, alpha = 9, 1.2
        else:
            env = np.exp(-x / 0.7) * np.minimum(1, x / 0.01) * np.minimum(1, (e - s - x) / 0.08) * 1.3
            H, alpha = 6, 0.9
        sig = sum(h ** -alpha * np.sin(h * ph + 0.7 * h) for h in range(1, H + 1) if 440 * 2 ** ((m - 69) / 12) * h < 8000)
        y[i0:i1] += det[1] * env * sig * (0.8 if kind == "chord" else 1.0)
y /= np.max(np.abs(y))
y = np.tanh(2.0 * y)
ir_t = np.arange(int(2.5 * sr)) / sr
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.6)
ir[0] = 12
y = fftconvolve(y, ir)[: len(tt)]
y /= np.max(np.abs(y))
hiss = lfilter([1, -0.3], [1], rng.standard_normal(len(y)))
y += 0.05 * hiss / np.max(np.abs(hiss))
crack = np.zeros(len(y))
pos = rng.integers(0, len(y), 400)
crack[pos] = rng.uniform(-1, 1, 400)
y += 0.5 * lfilter([1], [1, -0.6], crack)
y /= np.max(np.abs(y)) * 1.05
sf.write("test_holdout.wav", y.astype(np.float32), sr)
pickle.dump(([(s, e, m, 0, k) for s, e, m, k in truth], TUNE), open("truth_holdout.pkl", "wb"))
print(sum(1 for x in truth if x[3] == "melody"), "melody notes;", sum(1 for x in truth if x[3] == "chord"), "chord tones")
