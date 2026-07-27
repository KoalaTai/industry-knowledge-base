/**
 * POWDER PUP 64 — a dog snowboarding game in modern-N64 style.
 * Three.js, flat-shaded low-poly, chunky HUD. Endless downhill:
 * steer, jump, spin for style, grab bones, dodge trees/rocks/fences.
 */
import * as THREE from 'three';

// ---------------- deterministic rng ----------------
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------------- renderer (N64: low internal res, pixelated upscale) ----------------
const stage = document.getElementById('stage')!;
const renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance' });
renderer.outputColorSpace = THREE.SRGBColorSpace;
const RES_SCALE = 0.5; // N64 chunk factor
stage.appendChild(renderer.domElement);
renderer.domElement.style.width = '100%';
renderer.domElement.style.height = '100%';
renderer.domElement.style.imageRendering = 'pixelated';

const scene = new THREE.Scene();
const SKY = 0x7ec8f0;
scene.fog = new THREE.Fog(0xbfe4f7, 60, 210);

const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 400);

function resize(): void {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(Math.max(2, Math.floor(w * RES_SCALE)), Math.max(2, Math.floor(h * RES_SCALE)), false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);

// ---------------- sky dome + sun + mountain ring ----------------
{
  const skyGeo = new THREE.SphereGeometry(300, 16, 8);
  const cols: number[] = [];
  const pos = skyGeo.attributes.position;
  const top = new THREE.Color(0x4f9fe0), bot = new THREE.Color(0xcfeafc);
  for (let i = 0; i < pos.count; i += 1) {
    const t = THREE.MathUtils.clamp((pos.getY(i) / 300) * 0.5 + 0.5, 0, 1);
    const c = bot.clone().lerp(top, t);
    cols.push(c.r, c.g, c.b);
  }
  skyGeo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  const sky = new THREE.Mesh(skyGeo, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false }));
  scene.add(sky);

  const sun = new THREE.Mesh(new THREE.CircleGeometry(14, 16), new THREE.MeshBasicMaterial({ color: 0xfff2b8, fog: false }));
  sun.position.set(-90, 120, -240);
  sun.lookAt(0, 0, 0);
  scene.add(sun);

  const rng = mulberry32(7);
  const mtnMat = new THREE.MeshLambertMaterial({ color: 0xdfe9f7, flatShading: true });
  for (let i = 0; i < 14; i += 1) {
    const ang = (i / 14) * Math.PI * 2;
    if (Math.abs(Math.sin(ang)) < 0.25 && Math.cos(ang) < 0) continue; // gap ahead
    const m = new THREE.Mesh(new THREE.ConeGeometry(24 + rng() * 22, 40 + rng() * 45, 5), mtnMat);
    m.position.set(Math.sin(ang) * 235, 8, Math.cos(ang) * 235 - 40);
    m.rotation.y = rng() * Math.PI;
    scene.add(m);
  }
}

scene.add(new THREE.HemisphereLight(0xcfe8ff, 0x8fa3c8, 0.9));
const sunLight = new THREE.DirectionalLight(0xfff4d8, 1.6);
sunLight.position.set(-40, 80, -30);
scene.add(sunLight);

// ---------------- materials (flat-shaded N64 kit) ----------------
const M = {
  snow: new THREE.MeshLambertMaterial({ color: 0xf4f7ff, flatShading: true }),
  snowShade: new THREE.MeshLambertMaterial({ color: 0xdde7f8, flatShading: true }),
  pine: new THREE.MeshLambertMaterial({ color: 0x2e7d4f, flatShading: true }),
  pineDark: new THREE.MeshLambertMaterial({ color: 0x22643e, flatShading: true }),
  trunk: new THREE.MeshLambertMaterial({ color: 0x6d4a2f, flatShading: true }),
  rock: new THREE.MeshLambertMaterial({ color: 0x8d93a3, flatShading: true }),
  fence: new THREE.MeshLambertMaterial({ color: 0xc75b39, flatShading: true }),
  bone: new THREE.MeshLambertMaterial({ color: 0xffcf3e, flatShading: true }),
  fur: new THREE.MeshLambertMaterial({ color: 0xe9d5a8, flatShading: true }),
  furLight: new THREE.MeshLambertMaterial({ color: 0xf7ecd2, flatShading: true }),
  dark: new THREE.MeshLambertMaterial({ color: 0x2a2622, flatShading: true }),
  board: new THREE.MeshLambertMaterial({ color: 0x3fb8c9, flatShading: true }),
  boardTop: new THREE.MeshLambertMaterial({ color: 0xff8f4a, flatShading: true }),
  bandana: new THREE.MeshLambertMaterial({ color: 0xe6453f, flatShading: true }),
};

// ---------------- the pup ----------------
function buildPup(): { rig: THREE.Group; pup: THREE.Group; board: THREE.Mesh } {
  const rig = new THREE.Group();   // world position + jump height
  const pup = new THREE.Group();   // lean / spin / crouch
  rig.add(pup);

  const boardGeo = new THREE.BoxGeometry(1.5, 0.12, 4.4, 1, 1, 3);
  {
    const p = boardGeo.attributes.position;
    for (let i = 0; i < p.count; i += 1) {
      const z = p.getZ(i);
      if (Math.abs(z) > 1.9) p.setY(i, p.getY(i) + (Math.abs(z) - 1.9) * 0.5); // kicked tips
    }
    boardGeo.computeVertexNormals();
  }
  const board = new THREE.Mesh(boardGeo, M.board);
  board.position.y = 0.16;
  pup.add(board);
  const deck = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.05, 3.4), M.boardTop);
  deck.position.y = 0.25;
  pup.add(deck);

  const body = new THREE.Group();
  body.position.y = 0.9;
  pup.add(body);

  const torso = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.9, 1.9), M.fur);
  torso.position.set(0, 0.35, 0);
  body.add(torso);
  const chest = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.7, 0.7), M.furLight);
  chest.position.set(0, 0.28, 0.95);
  body.add(chest);

  const head = new THREE.Group();
  head.position.set(0, 0.95, 1.15);
  body.add(head);
  const skull = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.75, 0.85), M.fur);
  head.add(skull);
  const muzzle = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.42, 0.55), M.furLight);
  muzzle.position.set(0, -0.14, 0.6);
  head.add(muzzle);
  const nose = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.18, 0.16), M.dark);
  nose.position.set(0, -0.04, 0.9);
  head.add(nose);
  for (const s of [1, -1]) {
    const eye = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.16, 0.06), M.dark);
    eye.position.set(0.26 * s, 0.14, 0.44);
    head.add(eye);
    const ear = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.55, 0.34), M.fur);
    ear.position.set(0.5 * s, -0.05, -0.1);
    ear.rotation.z = s * 0.25;
    head.add(ear);
  }
  const bandana = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.3, 0.9), M.bandana);
  bandana.position.set(0, 0.62, 1.12);
  bandana.rotation.x = 0.15;
  body.add(bandana);
  const knot = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.5, 0.2), M.bandana);
  knot.position.set(0, 0.35, 1.55);
  knot.rotation.x = 0.5;
  body.add(knot);

  // legs planted on board (snowboard stance: slight angle)
  const legPos: Array<[number, number]> = [[-0.32, 0.75], [0.32, 0.75], [-0.32, -0.65], [0.32, -0.65]];
  for (const [x, z] of legPos) {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.75, 0.26), M.furLight);
    leg.position.set(x, -0.25, z);
    body.add(leg);
  }
  const tail = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.2, 0.9), M.fur);
  tail.position.set(0, 0.75, -1.15);
  tail.rotation.x = -0.6;
  body.add(tail);
  (rig.userData as Record<string, unknown>).tail = tail;

  pup.rotation.y = 0.0;
  return { rig, pup, board };
}
const { rig: pupRig, pup } = buildPup();
scene.add(pupRig);

// snow spray
const sprayGeo = new THREE.BufferGeometry();
const SPRAY_N = 40;
const sprayPos = new Float32Array(SPRAY_N * 3);
const sprayLife = new Float32Array(SPRAY_N);
sprayGeo.setAttribute('position', new THREE.BufferAttribute(sprayPos, 3));
const spray = new THREE.Points(sprayGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 0.35, sizeAttenuation: true }));
spray.frustumCulled = false;
scene.add(spray);
let sprayIdx = 0;

// ---------------- slope chunks ----------------
const SLOPE_W = 34;         // playable width
const CHUNK_L = 60;
const CHUNKS = 7;
const chunkRng = mulberry32(1234);

interface Ob { kind: 'tree' | 'rock' | 'fence' | 'bone' | 'boost'; x: number; z: number; r: number; h: number; mesh: THREE.Object3D; taken?: boolean }
interface Chunk { group: THREE.Group; z0: number; obs: Ob[] }
const chunks: Chunk[] = [];

function makeGround(): THREE.Mesh {
  const g = new THREE.PlaneGeometry(SLOPE_W + 44, CHUNK_L, 12, 10);
  g.rotateX(-Math.PI / 2);
  const p = g.attributes.position;
  const cols: number[] = [];
  const cSnow = new THREE.Color(0xf4f7ff), cShade = new THREE.Color(0xc9d8f0);
  for (let i = 0; i < p.count; i += 1) {
    const x = p.getX(i), z = p.getZ(i);
    let y = Math.sin(x * 0.35 + z * 0.2) * 0.25 + Math.cos(x * 0.13 - z * 0.31) * 0.3;
    if (Math.abs(x) > SLOPE_W / 2 + 4) y += (Math.abs(x) - SLOPE_W / 2 - 4) * 0.55; // banked edges
    p.setY(i, y);
    const t = THREE.MathUtils.clamp(y * 0.8 + 0.5, 0, 1);
    const c = cShade.clone().lerp(cSnow, t);
    cols.push(c.r, c.g, c.b);
  }
  g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  g.computeVertexNormals();
  return new THREE.Mesh(g, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true }));
}

function makeTree(scale: number): THREE.Group {
  const t = new THREE.Group();
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 1.2, 5), M.trunk);
  trunk.position.y = 0.6;
  t.add(trunk);
  const tiers = 3;
  for (let i = 0; i < tiers; i += 1) {
    const cone = new THREE.Mesh(new THREE.ConeGeometry(1.6 - i * 0.4, 1.5, 6), i % 2 ? M.pineDark : M.pine);
    cone.position.y = 1.4 + i * 1.0;
    t.add(cone);
  }
  const cap = new THREE.Mesh(new THREE.ConeGeometry(0.5, 0.6, 6), M.snowShade);
  cap.position.y = 1.4 + tiers * 1.0 + 0.1;
  t.add(cap);
  t.scale.setScalar(scale);
  return t;
}
function makeRock(scale: number): THREE.Mesh {
  const r = new THREE.Mesh(new THREE.DodecahedronGeometry(0.9, 0), M.rock);
  r.scale.set(scale * (1 + Math.random() * 0.3), scale * 0.8, scale);
  r.position.y = 0.35 * scale;
  r.rotation.y = Math.random() * Math.PI;
  return r;
}
function makeFence(): THREE.Group {
  const f = new THREE.Group();
  const rail = new THREE.Mesh(new THREE.BoxGeometry(6, 0.25, 0.18), M.fence);
  rail.position.y = 1.0;
  f.add(rail);
  const rail2 = rail.clone();
  rail2.position.y = 0.55;
  f.add(rail2);
  for (const x of [-2.8, 0, 2.8]) {
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.22, 1.3, 0.22), M.fence);
    post.position.set(x, 0.65, 0);
    f.add(post);
  }
  return f;
}
function makeBone(): THREE.Group {
  const b = new THREE.Group();
  const bar = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.16, 0.16), M.bone);
  b.add(bar);
  for (const s of [1, -1]) {
    for (const dy of [0.1, -0.1]) {
      const k = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.2, 0.2), M.bone);
      k.position.set(0.38 * s, dy, 0);
      b.add(k);
    }
  }
  b.position.y = 1.0;
  return b;
}
function makeBoost(): THREE.Mesh {
  const m = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.1, 3.2), new THREE.MeshLambertMaterial({ color: 0x63d6ff, flatShading: true }));
  m.position.y = 0.08;
  return m;
}

function fillChunk(c: Chunk, difficulty: number, isFirst: boolean): void {
  for (const o of c.obs) c.group.remove(o.mesh);
  c.obs = [];
  if (isFirst) return; // clear runway
  const n = 3 + Math.floor(chunkRng() * (3 + difficulty));
  for (let i = 0; i < n; i += 1) {
    const roll = chunkRng();
    const x = (chunkRng() - 0.5) * SLOPE_W;
    const z = -(chunkRng() * (CHUNK_L - 10) + 5);
    let ob: Ob;
    if (roll < 0.34) {
      const s = 0.8 + chunkRng() * 0.7;
      const mesh = makeTree(s);
      ob = { kind: 'tree', x, z, r: 1.1 * s, h: 3.5 * s, mesh };
    } else if (roll < 0.52) {
      const s = 0.8 + chunkRng() * 0.8;
      const mesh = makeRock(s);
      ob = { kind: 'rock', x, z, r: 1.0 * s, h: 0.8 * s, mesh };
    } else if (roll < 0.62) {
      const mesh = makeFence();
      ob = { kind: 'fence', x, z, r: 3.0, h: 1.2, mesh };
    } else if (roll < 0.92) {
      const mesh = makeBone();
      ob = { kind: 'bone', x, z, r: 1.3, h: 2.2, mesh };
    } else {
      const mesh = makeBoost();
      ob = { kind: 'boost', x, z, r: 1.6, h: 0.4, mesh };
    }
    ob.mesh.position.set(x, ob.mesh.position.y, z);
    c.group.add(ob.mesh);
    c.obs.push(ob);
  }
}

for (let i = 0; i < CHUNKS; i += 1) {
  const group = new THREE.Group();
  group.add(makeGround());
  const c: Chunk = { group, z0: -i * CHUNK_L, obs: [] };
  group.position.z = c.z0;
  fillChunk(c, 0, i === 0);
  chunks.push(c);
  scene.add(group);
}

// ---------------- audio (tiny synth, created on first gesture) ----------------
let actx: AudioContext | null = null;
function beep(freq: number, dur: number, type: OscillatorType, vol: number, slide = 0): void {
  try {
    if (!actx) return;
    const o = actx.createOscillator();
    const g = actx.createGain();
    o.type = type;
    o.frequency.value = freq;
    if (slide) o.frequency.linearRampToValueAtTime(freq + slide, actx.currentTime + dur);
    g.gain.setValueAtTime(vol, actx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + dur);
    o.connect(g).connect(actx.destination);
    o.start();
    o.stop(actx.currentTime + dur);
  } catch { /* audio best-effort */ }
}
function initAudio(): void {
  if (actx) return;
  try {
    actx = new (window.AudioContext || (window as any).webkitAudioContext)();
  } catch { actx = null; }
}

// ---------------- game state ----------------
type State = 'title' | 'playing' | 'paused' | 'over';
let state: State = 'title';
let px = 0, pvx = 0;          // lateral
let py = 0, pvy = 0;          // jump
let grounded = true;
let spin = 0, spinTarget = 0; // trick spin (radians)
let speed = 22, baseSpeed = 22;
let boost = 0;
let dist = 0, score = 0, bones = 0, hearts = 3, combo = 0;
let inv = 0;                  // invulnerability timer
let shake = 0;
let hiscore = 0;
try { hiscore = Number(localStorage.getItem('powderpup64.hi') || 0) || 0; } catch { /* no storage */ }

const hud = {
  score: document.getElementById('score')!,
  bones: document.getElementById('bones')!,
  speed: document.getElementById('speedv')!,
  hearts: document.getElementById('hearts')!,
  trick: document.getElementById('trick')!,
  title: document.getElementById('title')!,
  over: document.getElementById('over')!,
  pause: document.getElementById('pause')!,
  finalScore: document.getElementById('final-score')!,
  finalHi: document.getElementById('final-hi')!,
  hudBar: document.getElementById('hud')!,
};

function setState(s: State): void {
  state = s;
  hud.title.classList.toggle('show', s === 'title');
  hud.over.classList.toggle('show', s === 'over');
  hud.pause.classList.toggle('show', s === 'paused');
  hud.hudBar.classList.toggle('show', s === 'playing' || s === 'paused');
}

function resetRun(): void {
  px = 0; pvx = 0; py = 0; pvy = 0; grounded = true;
  spin = 0; spinTarget = 0;
  speed = baseSpeed; boost = 0;
  dist = 0; score = 0; bones = 0; hearts = 3; combo = 0; inv = 0;
  for (let i = 0; i < CHUNKS; i += 1) {
    chunks[i].z0 = -i * CHUNK_L;
    chunks[i].group.position.z = chunks[i].z0;
    fillChunk(chunks[i], 0, i === 0);
  }
  renderHearts();
}

function renderHearts(): void {
  hud.hearts.textContent = '♥'.repeat(hearts) + '♡'.repeat(Math.max(0, 3 - hearts));
}

function start(): void {
  initAudio();
  resetRun();
  setState('playing');
  beep(523, 0.09, 'square', 0.15); beep(784, 0.12, 'square', 0.15);
}
function gameOver(): void {
  if (score > hiscore) {
    hiscore = score;
    try { localStorage.setItem('powderpup64.hi', String(hiscore)); } catch { /* ok */ }
  }
  hud.finalScore.textContent = String(Math.floor(score));
  hud.finalHi.textContent = String(Math.floor(hiscore));
  setState('over');
  beep(392, 0.2, 'sawtooth', 0.18, -100);
  beep(196, 0.5, 'sawtooth', 0.15, -60);
}

// ---------------- input ----------------
const keys: Record<string, boolean> = {};
function jump(): void {
  if (state !== 'playing') return;
  if (grounded) {
    pvy = 13.5;
    grounded = false;
    beep(440, 0.12, 'square', 0.12, 220);
    // pre-arm a spin if steering hard
    if (keys.ArrowLeft || keys.KeyA) spinTarget = Math.PI * 2;
    else if (keys.ArrowRight || keys.KeyD) spinTarget = -Math.PI * 2;
  }
}
window.addEventListener('keydown', (e) => {
  if (e.repeat) return;
  keys[e.code] = true;
  if (e.code === 'Space' || e.code === 'ArrowUp' || e.code === 'KeyW') { e.preventDefault(); jump(); }
  if (e.code === 'Enter') {
    if (state === 'title' || state === 'over') start();
  }
  if (e.code === 'KeyP' || e.code === 'Escape') {
    if (state === 'playing') setState('paused');
    else if (state === 'paused') setState('playing');
  }
}, { passive: false });
window.addEventListener('keyup', (e) => { keys[e.code] = false; });

// touch: left/right halves steer, tap top half jumps, overlays tap to start
let touchDir = 0;
function bindTouch(): void {
  const el = renderer.domElement;
  el.addEventListener('touchstart', (e) => {
    e.preventDefault();
    if (state === 'title' || state === 'over') { start(); return; }
    for (const t of Array.from(e.touches)) {
      const r = el.getBoundingClientRect();
      const nx = (t.clientX - r.left) / r.width;
      const ny = (t.clientY - r.top) / r.height;
      if (ny < 0.4) jump();
      else touchDir = nx < 0.5 ? -1 : 1;
    }
  }, { passive: false });
  const clear = (e: TouchEvent) => { e.preventDefault(); if (e.touches.length === 0) touchDir = 0; };
  el.addEventListener('touchend', clear, { passive: false });
  el.addEventListener('touchcancel', clear, { passive: false });
}
bindTouch();
for (const id of ['title', 'over']) {
  document.getElementById(id)!.addEventListener('click', () => start());
}

// ---------------- collision + update ----------------
const upVec = new THREE.Vector3();
function update(dt: number): void {
  if (state !== 'playing') return;

  // difficulty ramp
  const diff = Math.min(6, dist / 400);
  const targetSpeed = baseSpeed + diff * 4 + boost * 14;
  speed += (targetSpeed - speed) * Math.min(1, dt * 2.5);
  boost = Math.max(0, boost - dt * 0.7);

  // steer
  const steer = (keys.ArrowLeft || keys.KeyA ? -1 : 0) + (keys.ArrowRight || keys.KeyD ? 1 : 0) + touchDir;
  pvx += steer * 68 * dt;
  pvx *= Math.pow(0.0018, dt); // damping
  px = THREE.MathUtils.clamp(px + pvx * dt, -SLOPE_W / 2, SLOPE_W / 2);

  // jump physics
  if (!grounded) {
    pvy -= 32 * dt;
    py += pvy * dt;
    if (spinTarget !== 0) spin += Math.sign(spinTarget) * dt * 9;
    if (py <= 0) {
      py = 0; grounded = true;
      // landing: score the spin if (mostly) completed
      if (spinTarget !== 0 && Math.abs(spin) > Math.PI * 1.5) {
        combo += 1;
        const pts = 150 * combo;
        score += pts;
        hud.trick.textContent = `360 x${combo}  +${pts}`;
        hud.trick.classList.remove('pop');
        void (hud.trick as HTMLElement).offsetWidth;
        hud.trick.classList.add('pop');
        beep(660, 0.1, 'square', 0.14, 200);
      } else if (spinTarget !== 0) {
        combo = 0;
      }
      spin = 0; spinTarget = 0; pvy = 0;
    }
  }

  // move world
  dist += speed * dt;
  score += speed * dt * 1.2;
  for (const c of chunks) {
    c.z0 += speed * dt;
    if (c.z0 > CHUNK_L) {
      c.z0 -= CHUNK_L * CHUNKS;
      fillChunk(c, Math.floor(diff), false);
    }
    c.group.position.z = c.z0;
  }

  // collisions (player at world z=0, x=px)
  inv = Math.max(0, inv - dt);
  for (const c of chunks) {
    for (const o of c.obs) {
      if (o.taken) continue;
      const oz = c.z0 + o.z;
      if (oz < -3 || oz > 3) continue;
      const dx = Math.abs(o.x - px);
      const halfW = o.kind === 'fence' ? o.r : o.r * 0.8;
      if (dx > halfW) continue;
      if (Math.abs(oz) > 1.6) continue;
      if (o.kind === 'bone') {
        o.taken = true;
        o.mesh.visible = false;
        bones += 1;
        score += 100;
        beep(880, 0.09, 'square', 0.13, 240);
      } else if (o.kind === 'boost') {
        o.taken = true;
        boost = 1;
        beep(523, 0.15, 'sawtooth', 0.13, 300);
      } else {
        // solid: only hits if we're low enough
        if (py < o.h && inv <= 0) {
          hearts -= 1;
          renderHearts();
          inv = 1.6;
          shake = 0.6;
          combo = 0;
          speed = Math.max(14, speed * 0.5);
          beep(180, 0.3, 'sawtooth', 0.2, -80);
          if (hearts <= 0) { gameOver(); return; }
        }
      }
    }
  }

  // pup pose
  pupRig.position.set(px, py, 0);
  const lean = THREE.MathUtils.clamp(pvx * 0.05, -0.65, 0.65);
  pup.rotation.z = lean;
  pup.rotation.y = Math.PI + spin - lean * 0.5;
  pup.rotation.x = grounded ? -0.06 : 0.18;
  const tail = (pupRig.userData as Record<string, any>).tail as THREE.Mesh;
  tail.rotation.y = Math.sin(performance.now() * 0.02) * 0.4;
  // blink during invulnerability
  pup.visible = inv <= 0 || Math.floor(inv * 12) % 2 === 0;

  // spray
  if (grounded && Math.abs(pvx) > 2) {
    sprayPos[sprayIdx * 3] = px - Math.sign(pvx) * 0.8;
    sprayPos[sprayIdx * 3 + 1] = 0.25;
    sprayPos[sprayIdx * 3 + 2] = 0.6;
    sprayLife[sprayIdx] = 1;
    sprayIdx = (sprayIdx + 1) % SPRAY_N;
  }
  for (let i = 0; i < SPRAY_N; i += 1) {
    if (sprayLife[i] > 0) {
      sprayLife[i] -= dt * 2.2;
      sprayPos[i * 3 + 1] += dt * 2.2;
      sprayPos[i * 3 + 2] += speed * dt;
      if (sprayLife[i] <= 0) sprayPos[i * 3 + 1] = -5;
    }
  }
  sprayGeo.attributes.position.needsUpdate = true;

  // bone bobbing
  const t = performance.now() * 0.003;
  for (const c of chunks) {
    for (const o of c.obs) {
      if (o.kind === 'bone' && !o.taken) {
        o.mesh.rotation.y = t + o.x;
        o.mesh.position.y = 1.0 + Math.sin(t * 2 + o.z) * 0.15;
      }
    }
  }

  // camera follow + shake
  shake = Math.max(0, shake - dt);
  const sx = (Math.random() - 0.5) * shake * 0.6;
  const sy = (Math.random() - 0.5) * shake * 0.4;
  camera.position.set(px * 0.55 + sx, 4.6 + py * 0.35 + sy, 8.2);
  camera.lookAt(px * 0.8, 1.2 + py * 0.5, -6);
  upVec.set(lean * -0.06, 1, 0).normalize();
  camera.up.copy(upVec);

  // HUD
  hud.score.textContent = String(Math.floor(score)).padStart(6, '0');
  hud.bones.textContent = `x${bones}`;
  hud.speed.textContent = `${Math.floor(speed * 3.6)}`;
}

// ---------------- main loop ----------------
let last = performance.now();
let frames = 0;
function loop(now: number): void {
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;
  update(dt);
  if (state === 'title') {
    // idle attract: slow orbit around pup
    const t = now * 0.0004;
    camera.position.set(Math.sin(t) * 9, 4.0, Math.cos(t) * 9);
    camera.lookAt(0, 1.4, 0);
    camera.up.set(0, 1, 0);
    pup.rotation.set(-0.06, Math.PI + 0.6, 0);
    pupRig.position.set(0, 0, 0);
  }
  renderer.render(scene, camera);
  frames += 1;
  requestAnimationFrame(loop);
}
resize();
setState('title');
requestAnimationFrame(loop);

// test hooks (harmless in production)
(window as any).__game = {
  get state() { return state; },
  get score() { return score; },
  get hearts() { return hearts; },
  get dist() { return dist; },
  get frames() { return frames; },
  start,
  forceCrash: () => { hearts = 1; inv = 0; px = 0; },
};
