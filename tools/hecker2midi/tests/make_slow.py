import numpy as np, soundfile as sf
from scipy.signal import fftconvolve, lfilter

sr = 44100
rng = np.random.default_rng(1)
TUNE = -0.30  # whole piece 30 cents flat (tape-speed style)

# (start, end, midi, cents)
truth = [
    (0, 12, 38, 0), (0, 12, 57, 0), (1, 12, 64, 12), (2, 12, 71, -8),
    (12, 24, 46, 0), (12, 24, 53, 0), (12, 24, 58, 0), (13, 24, 59, 0),
    (12, 24, 69, 5), (14, 24, 76, -10),
]
dur = 26
t = np.arange(int(dur * sr)) / sr
y = np.zeros_like(t)
for s, e, m, c in truth:
    f = 440 * 2 ** ((m + c / 100 + TUNE - 69) / 12)
    i0, i1 = int(s * sr), int(e * sr)
    tt = t[i0:i1] - s
    # slow swell, no attack
    env = np.minimum(1, tt / 2.5) * np.minimum(1, (e - s - tt) / 1.5)
    env *= 0.8 + 0.2 * np.sin(2 * np.pi * 0.13 * tt + m)
    drift = 1 + 0.0008 * np.sin(2 * np.pi * 0.07 * tt + m)  # ~1.4 cent wobble
    ph = 2 * np.pi * np.cumsum(f * drift) / sr
    sig = sum((1 / h) * np.sin(h * ph + h) for h in range(1, 11) if h * f < sr / 2)
    y[i0:i1] += env * sig / (1 + 0.02 * (m - 38))
y /= np.max(np.abs(y))
# saturation
y = np.tanh(4 * y)
# sample-rate reduction (zero-order hold at 8810 Hz) and 8-bit crush
step = sr / 8810
idx = (np.floor(np.arange(len(y)) / step) * step).astype(int)
y = y[idx]
y = np.round(y * 127) / 127
# reverb: 3.5 s exponential noise tail
ir_t = np.arange(int(3.5 * sr)) / sr
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.8)
ir[0] = 8
y = fftconvolve(y, ir)[: len(t)]
y /= np.max(np.abs(y))
# pink-ish rain noise
w = rng.standard_normal(len(y))
pink = lfilter([0.049922035, -0.095993537, 0.050612699, -0.004408786], [1, -2.494956002, 2.017265875, -0.522189400], w)
pink /= np.max(np.abs(pink))
y = y + 0.35 * pink
# glitch bursts
for k in range(40):
    i = rng.integers(0, len(y) - 2000)
    y[i : i + rng.integers(50, 1500)] += rng.uniform(-0.8, 0.8)
y /= np.max(np.abs(y)) * 1.05
sf.write("test_slow.wav", y.astype(np.float32), sr)
np.save("truth_slow.npy", np.array(truth, dtype=float))
print("ok")
