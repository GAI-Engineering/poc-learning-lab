#!/usr/bin/env python3
"""POC 01 - An Agent That Sees: layered scene parser (deterministic stub).
Synthetic scenes only. Each scene is a grid of regions with ground-truth
objects; the stub parser emits region-grounded claims with confidences.
Claims below 0.60 confidence are flagged as guesses - the confidence map.
"""
import json

SCENES = [
    {"scene": "pavement-01", "regions": [
        {"region": "top-left", "object": "pavement slab", "confidence": 0.97},
        {"region": "centre", "object": "crack, 18mm at widest", "confidence": 0.91},
        {"region": "centre-right", "object": "raised edge, trip hazard", "confidence": 0.84},
        {"region": "bottom", "object": "drain cover", "confidence": 0.95},
        {"region": "top-right (occluded)", "object": "possible bollard base", "confidence": 0.42},
    ]},
    {"scene": "entrance-02", "regions": [
        {"region": "centre", "object": "step, no ramp", "confidence": 0.93},
        {"region": "left", "object": "handrail, one side only", "confidence": 0.88},
        {"region": "right", "object": "door, manual, heavy", "confidence": 0.71},
        {"region": "top (small print)", "object": "sign text unreadable", "confidence": 0.35},
    ]},
    {"scene": "crossing-03", "regions": [
        {"region": "centre", "object": "dropped kerb present", "confidence": 0.96},
        {"region": "left", "object": "tactile paving", "confidence": 0.90},
        {"region": "right", "object": "parked bicycle obstructing kerb", "confidence": 0.78},
        {"region": "far side (occluded)", "object": "possible second obstruction", "confidence": 0.48},
    ]},
]
# Human verification on the synthetic ground truth (recorded for this run):
VERIFIED = {  # SCRIPTED demonstration outcomes, fixed for the worked example —
# not measured. (scene, region) -> True if claim survives human check
    ("pavement-01", "top-left"): True, ("pavement-01", "centre"): True,
    ("pavement-01", "centre-right"): True, ("pavement-01", "bottom"): True,
    ("pavement-01", "top-right (occluded)"): False,
    ("entrance-02", "centre"): True, ("entrance-02", "left"): True,
    ("entrance-02", "right"): True, ("entrance-02", "top (small print)"): False,
    ("crossing-03", "centre"): True, ("crossing-03", "left"): True,
    ("crossing-03", "right"): True, ("crossing-03", "far side (occluded)"): False,
}

def main():
    rows = []
    for scene in SCENES:
        for r in scene["regions"]:
            rows.append({"scene": scene["scene"], "region": r["region"],
                         "claim": r["object"], "confidence": r["confidence"],
                         "flag": "GUESS" if r["confidence"] < 0.60 else "GROUNDED",
                         "verified": VERIFIED[(scene["scene"], r["region"])]})
    survived = sum(1 for r in rows if r["verified"])
    print(json.dumps({"claims": rows, "total": len(rows), "survived": survived,
                      "survival_rate": round(survived / len(rows), 3)}, indent=2))

if __name__ == "__main__":
    main()
