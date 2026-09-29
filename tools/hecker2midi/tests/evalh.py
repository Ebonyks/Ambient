"""Evaluation harness: run hecker2midi in-process on all test files with overrides, report
recall and false notes. Usage: python3 evalh.py [--flag value ...]  (flags passed to hecker2midi)"""
import sys, pickle, importlib, numpy as np
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import hecker2midi as H

FILES = {
    "slow": ("test_slow.wav",),
    "fast": ("test_fast.wav",),
    "holdout": ("test_holdout.wav",),
}

def truth_for(name):
    if name == "slow":
        t = np.load("truth_slow.npy")
        return [(s, e, int(m), "chord") for s, e, m, c in t], -0.30
    f = {"fast": "truth_fast.pkl", "holdout": "truth_holdout.pkl"}[name]
    tr, tune = pickle.load(open(f, "rb"))
    return [(s, e, int(m), k) for s, e, m, c, k in tr], tune

def run(path, extra):
    sys.argv = ["x", path] + extra
    a = H.parse_args()
    played, rejected, off, total = H.process(a, log=lambda *x: None)
    return played, off

def score(name, notes, off):
    truth, tune = truth_for(name)
    det = [(n["start"], n["end"], int(round(n["pitch"] - tune))) for n in notes]
    out = {}
    ch = [x for x in truth if x[3] == "chord"]
    cov = [min(1, sum(max(0, min(e, de) - max(s, ds)) for ds, de, dm in det if dm == m) / (e - s)) for s, e, m, k in ch]
    out["chord"] = 100 * np.mean(cov)
    mel = [x for x in truth if x[3] == "melody"]
    if mel:
        hit = sum(1 for s, e, m, k in mel if any(dm == m and abs(ds - s) <= 0.25 or (dm == m and ds <= s and de >= e - 0.1) for ds, de, dm in det))
        out["melody"] = 100 * hit / len(mel)
    fp, octv = 0, 0
    for ds, de, dm in det:
        if not any(dm == m and min(e, de) - max(s, ds) > -0.1 for s, e, m, k in truth):
            fp += 1
            if any(dm % 12 == m % 12 and min(e, de) - max(s, ds) > 0 for s, e, m, k in truth):
                octv += 1
    out["false"] = fp
    out["oct"] = octv
    out["n"] = len(det)
    out["tune_err"] = (off - tune) * 100
    return out

if __name__ == "__main__":
    extra = sys.argv[1:]
    tot_fp = 0
    for name, (path,) in FILES.items():
        notes, off = run(path, extra)
        r = score(name, notes, off)
        tot_fp += r["false"]
        mel = f"melody {r['melody']:3.0f}%" if "melody" in r else "            "
        print(f"{name:8s} chord {r['chord']:3.0f}%  {mel}  false {r['false']:2d} (octave-displaced {r['oct']:2d})  "
              f"of {r['n']:3d}  precision {100 * (r['n'] - r['false']) / max(1, r['n']):3.0f}%  tune err {r['tune_err']:+.1f}c")
    print(f"TOTAL false {tot_fp}   args: {' '.join(extra)}")
