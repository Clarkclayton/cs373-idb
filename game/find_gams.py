from pprint import pprint
from tabulate import tabulate
import json

fs = [
358,
460,
472,
168,
245,
428,
222,
296,
158,
215,
474,
174,
185,
167,
191,
152,
223,
488,
344,
201,
347,
331,
160,
299,
77,
334,
413,
264,
333,
402,
490,
310,
302,
145,
427,
309,
143,
457,
480,
467,
495,
298,
204,
332,
405,
271,
67,
266,
182,
450,
396,
210,
388,
24,
236,
202,
327,
148,
487,
166,
329,
136,
485,
385,
493,
102,
233,
176,
489,
443,
155,
414,
70]

rows = []

for fn in fs:
    fi = open(str(fn))
    d = json.load(fi)
    for gam in d["games"]:
        if "Pok" in gam["name"] and "mon" in gam["name"]:
            prow = (gam["id"], fn, gam["name"])
            rows.append(prow)
print(tabulate(rows, headers=["Id", "Page", "Name"]))

