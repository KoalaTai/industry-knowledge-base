# Powder Pup 64

A dog snowboarding game in modern-N64 style, built with Three.js. Endless
downhill: carve with arrows/WASD, ollie with Space, hold a direction while
jumping for a 360 (combo multiplier), grab bones, ride boost pads, dodge
trees/rocks/fences. Three hearts, ramping difficulty, persistent best score,
touch controls on mobile.

N64 treatment: flat-shaded low-poly kit (Lambert materials, vertex-color
slope shading), half-resolution render upscaled with `image-rendering:
pixelated`, fog + gradient sky dome + mountain ring, chunky outlined HUD,
WebAudio square-wave bleeps.

- `index.html` — self-contained playable build (bundle inlined)
- `src/game.ts` — full game source (one file: renderer, slope chunk recycler,
  pup rig, physics, collisions, state machine, HUD, audio)
- `src/shell.html` — page shell + HUD styles
- `src/test.js` — Playwright smoke test: title → play → trick → pause →
  wipeout → restart, error-free, ~56 fps under SwiftShader
- `shots/` — title, gameplay, trick, and game-over captures

Build: `npm i three esbuild && npx esbuild src/game.ts --bundle --minify --format=iife`, inline into `src/shell.html`.
