# Sith Lab — img2threejs recreation

Procedural Three.js recreation of a Comic-Con photo (yellow Labrador in a black
Sith robe, red lightsaber in mouth), built with the
[img2threejs](https://github.com/img2threejs/img2threejs) staged pipeline:
intake → pre-spec assessment → sculpt spec (strict-validated) → hand-authored
`THREE.Group` factory → screenshot review loop.

## Contents

- `src/createJediLabrador.ts` — the model factory: 38 meshes / 11 materials,
  deterministic seeded noise, canvas-generated fur/cloth textures, emissive
  blade with additive glow shells, jaw-grip socket, tail-wag pivot.
- `src/viewer.ts` — interactive viewer (OrbitControls, tail wag, saber hum flicker).
- `src/main.ts` + `src/shot.js` — headless render harness (esbuild + Playwright/Chromium).
- `spec/spec.json` — full object-sculpt-spec with referencePbr evidence and
  8-pass review history (all passes `continue`, self-scored 0.70 stylized fidelity).
- `renders/` — reference-view and orbit renders plus the side-by-side comparison sheet.
- `index.html` — self-contained interactive page (bundle inlined).

## Build

```
npm i three@0.170.0 esbuild playwright-core
npx esbuild src/viewer.ts --bundle --outfile=viewer.js --format=iife --minify
```

## Honest limitations

Single-photo reconstruction: right side and underside inferred symmetric;
head is a stylized cartoon likeness, not a photoreal scan; the robe reads
smoother than the reference's crumpled cotton; deterministic silhouette IoU
(~0.50) is ceiling-limited by the photo's crowded convention background.
