/**
 * Jedi Labrador with Lightsaber — procedural Three.js reconstruction
 * Built from object-sculpt-spec.json (img2threejs pipeline).
 * Reconstruction-by-code from a single reference photo: stylized likeness,
 * right side / underside inferred symmetric. Deterministic seeds throughout.
 */
import * as THREE from 'three';

export interface JediLabradorOptions {
  castShadow?: boolean;
  receiveShadow?: boolean;
  textureSize?: number;
}

// ---------- deterministic noise ----------
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function noiseCanvasTexture(
  seed: number, size: number, base: string, spots: string[], density: number, blur: number,
): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = base;
  ctx.fillRect(0, 0, size, size);
  const rnd = mulberry32(seed);
  ctx.filter = `blur(${blur}px)`;
  for (let i = 0; i < density; i += 1) {
    ctx.fillStyle = spots[Math.floor(rnd() * spots.length)];
    ctx.globalAlpha = 0.05 + rnd() * 0.1;
    const r = size * (0.01 + rnd() * 0.05);
    ctx.beginPath();
    ctx.arc(rnd() * size, rnd() * size, r, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
  ctx.filter = 'none';
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  return tex;
}

// displace vertices radially (XZ) by per-angle fold ridges + noise — cloth relief
function clothify(geo: THREE.BufferGeometry, seed: number, folds: number, foldAmp: number, noiseAmp: number): void {
  const pos = geo.attributes.position as THREE.BufferAttribute;
  const rnd = mulberry32(seed);
  const phases: number[] = [];
  for (let f = 0; f < folds; f += 1) phases.push(rnd() * Math.PI * 2);
  for (let i = 0; i < pos.count; i += 1) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    const ang = Math.atan2(z, x);
    let d = 0;
    for (let f = 0; f < folds; f += 1) {
      d += Math.max(0, Math.sin(ang * (f % 2 ? folds - 1 : folds) + phases[f])) ** 2;
    }
    d = (d / folds) * foldAmp + (Math.sin(x * 23.7 + seed) * Math.cos(y * 19.3) * 0.5 + 0.5) * noiseAmp;
    const r = Math.sqrt(x * x + z * z) || 1;
    pos.setX(i, x + (x / r) * d);
    pos.setZ(i, z + (z / r) * d);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
}

export function createJediLabradorModel(options: JediLabradorOptions = {}): THREE.Group {
  const castShadow = options.castShadow ?? true;
  const receiveShadow = options.receiveShadow ?? true;
  const texSize = options.textureSize ?? 256;

  const root = new THREE.Group();
  root.name = 'jedi-labrador-root';
  const nodes: Record<string, THREE.Object3D> = {};
  const sockets: Record<string, THREE.Object3D> = {};

  const shadowify = (m: THREE.Mesh) => { m.castShadow = castShadow; m.receiveShadow = receiveShadow; };

  // ---------- materials (from spec referencePbr palettes) ----------
  const furTex = noiseCanvasTexture(101, texSize, '#e9d7b4', ['#d9bd8f', '#c9a97a', '#f4ead2'], 260, 2);
  const furMat = new THREE.MeshStandardMaterial({ map: furTex, roughness: 0.85, metalness: 0 });
  const furDarkMat = new THREE.MeshStandardMaterial({ color: '#c9ad82', roughness: 0.85 });
  const furLightMat = new THREE.MeshStandardMaterial({ color: '#f2e7cd', roughness: 0.85 });
  const clothTex = noiseCanvasTexture(202, texSize, '#1b1a1c', ['#26242a', '#111013', '#3a3740'], 200, 3);
  const clothMat = new THREE.MeshStandardMaterial({
    map: clothTex, roughness: 0.96, metalness: 0, side: THREE.DoubleSide,
  });
  const hiltMat = new THREE.MeshStandardMaterial({ color: '#141414', roughness: 0.55, metalness: 0.1 });
  const tapeMat = new THREE.MeshStandardMaterial({ color: '#b9bcc0', roughness: 0.35, metalness: 0.8 });
  const noseMat = new THREE.MeshPhysicalMaterial({ color: '#17120f', roughness: 0.35, clearcoat: 0.4 });
  const eyeMat = new THREE.MeshPhysicalMaterial({ color: '#241408', roughness: 0.15, clearcoat: 0.9 });
  const bladeCoreMat = new THREE.MeshStandardMaterial({
    color: '#fff6d8', emissive: '#ffdb8f', emissiveIntensity: 4.0, toneMapped: true,
  });
  const bladeGlowMat = new THREE.MeshBasicMaterial({
    color: '#ff2a0d', transparent: true, opacity: 0.30, blending: THREE.AdditiveBlending,
    depthWrite: false, side: THREE.BackSide,
  });
  const mouthMat = new THREE.MeshStandardMaterial({ color: '#5e2f30', roughness: 0.6 });

  // ---------- quadruped core (dog faces +X, up +Y; camera views left flank from +Z) ----------
  // torso barrel: capsule along X
  const torsoGeo = new THREE.CapsuleGeometry(0.155, 0.42, 8, 24);
  const torso = new THREE.Mesh(torsoGeo, furMat);
  torso.rotation.z = Math.PI / 2;
  torso.position.set(-0.02, 0.46, 0);
  torso.scale.set(1, 1, 0.88); // slightly narrow barrel
  shadowify(torso);
  root.add(torso);
  nodes.torso = torso;

  // chest mass
  const chest = new THREE.Mesh(new THREE.SphereGeometry(0.15, 24, 18), furMat);
  chest.position.set(0.26, 0.44, 0);
  chest.scale.set(0.82, 1.0, 0.75);
  shadowify(chest);
  root.add(chest);

  // hindquarters mass
  const rump = new THREE.Mesh(new THREE.SphereGeometry(0.145, 24, 18), furMat);
  rump.position.set(-0.28, 0.47, 0);
  rump.scale.set(1.1, 1.05, 0.9);
  shadowify(rump);
  root.add(rump);

  // neck (angled forward-up)
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.12, 0.24, 20), furMat);
  neck.position.set(0.38, 0.62, 0.0);
  neck.rotation.z = -0.55;
  shadowify(neck);
  root.add(neck);

  // ---------- head group (turned toward camera) ----------
  const head = new THREE.Group();
  head.position.set(0.52, 0.78, -0.03);
  head.rotation.y = 0.55; // turn toward viewer (-Z)
  head.rotation.z = -0.04;
  root.add(head);
  nodes.head = head;

  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.125, 28, 22), furMat);
  skull.scale.set(1.22, 0.86, 1.06);
  shadowify(skull);
  head.add(skull);

  // brow/stop ridge
  const brow = new THREE.Mesh(new THREE.SphereGeometry(0.085, 20, 16), furMat);
  brow.position.set(0.06, -0.01, 0);
  brow.scale.set(0.98, 0.7, 0.95);
  shadowify(brow);
  head.add(brow);

  // muzzle (boxy ellipsoid, slightly down)
  const muzzle = new THREE.Mesh(new THREE.SphereGeometry(0.062, 20, 16), furMat);
  muzzle.position.set(0.108, -0.052, 0);
  muzzle.scale.set(1.25, 1.02, 1.05);
  shadowify(muzzle);
  head.add(muzzle);

  // nose leather
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.030, 16, 12), noseMat);
  nose.position.set(0.185, -0.02, 0);
  nose.scale.set(0.9, 0.75, 1.0);
  shadowify(nose);
  head.add(nose);

  // lower jaw (open, gripping) + inner mouth hint
  const jaw = new THREE.Group();
  jaw.position.set(0.09, -0.075, 0);
  jaw.rotation.z = 0.30; // open ~17deg
  head.add(jaw);
  nodes.jaw = jaw;
  const jawMesh = new THREE.Mesh(new THREE.SphereGeometry(0.048, 18, 14), furLightMat);
  jawMesh.position.set(0.055, -0.012, 0);
  jawMesh.scale.set(1.45, 0.6, 0.8);
  shadowify(jawMesh);
  jaw.add(jawMesh);
  const innerMouth = new THREE.Mesh(new THREE.SphereGeometry(0.030, 12, 10), mouthMat);
  innerMouth.position.set(0.07, 0.008, 0);
  innerMouth.scale.set(1.3, 0.5, 0.7);
  jaw.add(innerMouth);

  // grip socket — the saber hilt passes through here
  const gripSocket = new THREE.Object3D();
  gripSocket.position.set(0.155, -0.075, -0.03);
  head.add(gripSocket);
  sockets['jaw-grip'] = gripSocket;

  // eyes
  for (const side of [1, -1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.021, 14, 12), eyeMat);
    eye.position.set(0.098, 0.03, 0.078 * side);
    head.add(eye);
  }

  // floppy ears — flattened, rotated ellipsoids hanging beside skull
  for (const side of [1, -1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.055, 18, 14), furMat);
    ear.position.set(-0.035, -0.045, 0.098 * side);
    ear.scale.set(0.7, 1.35, 0.24);
    ear.rotation.x = side * 0.10;
    ear.rotation.y = side * -0.25;
    ear.rotation.z = -0.06;
    shadowify(ear);
    head.add(ear);
    nodes[`ear-${side === 1 ? 'l' : 'r'}`] = ear;
  }

  // ---------- legs + paws ----------
  const legDefs: Array<[string, number, number, number]> = [
    ['fl', 0.26, 0.105, 0.02], ['fr', 0.30, -0.105, -0.06],
    ['rl', -0.27, 0.105, 0.03], ['rr', -0.31, -0.105, -0.04],
  ];
  for (const [nm, x, z, xoff] of legDefs) {
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.032, 0.40, 14), furLightMat);
    leg.position.set(x + xoff, 0.21, z);
    shadowify(leg);
    root.add(leg);
    nodes[`leg-${nm}`] = leg;
    const paw = new THREE.Mesh(new THREE.SphereGeometry(0.048, 16, 12), furLightMat);
    paw.position.set(x + xoff + 0.02, 0.032, z);
    paw.scale.set(1.35, 0.65, 1.0);
    shadowify(paw);
    root.add(paw);
  }

  // upper thighs on rear
  for (const side of [1, -1]) {
    const thigh = new THREE.Mesh(new THREE.SphereGeometry(0.095, 18, 14), furMat);
    thigh.position.set(-0.29, 0.42, 0.09 * side);
    thigh.scale.set(1.1, 1.3, 0.6);
    shadowify(thigh);
    root.add(thigh);
  }

  // ---------- tail (raised curve) ----------
  const tailCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-0.40, 0.52, 0),
    new THREE.Vector3(-0.52, 0.62, 0.02),
    new THREE.Vector3(-0.60, 0.74, 0.05),
    new THREE.Vector3(-0.63, 0.86, 0.08),
  ]);
  const tailPivot = new THREE.Group();
  tailPivot.position.set(-0.40, 0.52, 0);
  root.add(tailPivot);
  const tail = new THREE.Mesh(new THREE.TubeGeometry(tailCurve, 20, 0.028, 10), furMat);
  tail.position.set(0.40, -0.52, 0);
  shadowify(tail);
  tailPivot.add(tail);
  nodes.tail = tailPivot;
  const tailTip = new THREE.Mesh(new THREE.SphereGeometry(0.026, 12, 10), furLightMat);
  tailTip.position.copy(tailCurve.getPoint(1)).sub(new THREE.Vector3(0.40, 0.52, 0));
  tailPivot.add(tailTip);

  // ---------- robe ----------
  // torso drape: open hemisphere-ish shell over the back, hanging down the flanks
  const robeGeo = new THREE.SphereGeometry(1, 40, 24, 0, Math.PI * 2, 0, Math.PI * 0.86);
  clothify(robeGeo, 303, 7, 0.05, 0.03);
  const robe = new THREE.Mesh(robeGeo, clothMat);
  robe.position.set(0.0, 0.47, 0);
  robe.scale.set(0.43, 0.215, 0.235);
  shadowify(robe);
  robe.receiveShadow = true;
  root.add(robe);
  nodes['robe-body'] = robe;

  // skirt: open cone over hindquarters with fold ridges
  const skirtGeo = new THREE.CylinderGeometry(0.215, 0.27, 0.30, 40, 6, true);
  clothify(skirtGeo, 404, 9, 0.035, 0.02);
  const skirt = new THREE.Mesh(skirtGeo, clothMat);
  skirt.position.set(-0.25, 0.46, 0);
  skirt.rotation.z = 0.12;
  skirt.scale.set(1.0, 1.0, 0.85);
  shadowify(skirt);
  root.add(skirt);
  nodes['robe-skirt'] = skirt;

  // belly drape panel (hangs below torso between legs, camera side)
  const panelGeo = new THREE.BoxGeometry(0.30, 0.20, 0.015, 12, 8, 1);
  {
    const pos = panelGeo.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i < pos.count; i += 1) {
      const px = pos.getX(i), py = pos.getY(i);
      pos.setZ(i, pos.getZ(i) + Math.sin(px * 18.0) * 0.012 * (0.5 - py));
    }
    panelGeo.computeVertexNormals();
  }
  const panel = new THREE.Mesh(panelGeo, clothMat);
  panel.position.set(0.0, 0.33, -0.125);
  panel.rotation.y = 0.08;
  shadowify(panel);
  root.add(panel);

  // sleeves on forelegs
  for (const side of [1, -1]) {
    const sleeveGeo = new THREE.CylinderGeometry(0.078, 0.105, 0.24, 24, 3, true);
    clothify(sleeveGeo, 505 + side, 5, 0.02, 0.015);
    const sleeve = new THREE.Mesh(sleeveGeo, clothMat);
    sleeve.position.set(side === 1 ? 0.27 : 0.31, 0.27, 0.108 * side + (side === 1 ? 0.01 : -0.01));
    shadowify(sleeve);
    root.add(sleeve);
    nodes[`sleeve-${side === 1 ? 'l' : 'r'}`] = sleeve;
  }

  // collar / hood bunch around neck
  const collarGeo = new THREE.TorusGeometry(0.115, 0.042, 14, 28);
  clothify(collarGeo, 606, 6, 0.02, 0.012);
  const collar = new THREE.Mesh(collarGeo, clothMat);
  collar.position.set(0.41, 0.60, 0.03);
  collar.rotation.x = Math.PI / 2;
  collar.rotation.y = 0.35;
  collar.scale.set(1, 1, 0.62);
  shadowify(collar);
  root.add(collar);

  // ---------- lightsaber (attached at grip socket, world-aligned via group) ----------
  const saber = new THREE.Group();
  saber.name = 'saber';
  nodes.saber = saber;
  // Blade runs along local +Y. Orient: from mouth toward tail (-X), down (-Y), toward viewer (+Z).
  gripSocket.add(saber);
  saber.rotation.set(0, 0, 0);
  // direction in head-local space; head is rotated -0.55 yaw. Compose with quaternion lookalong.
  const bladeDir = new THREE.Vector3(-0.60, -0.42, -0.58).normalize();
  // convert world dir to head-local
  head.updateMatrixWorld(true);
  const headInv = new THREE.Quaternion();
  head.getWorldQuaternion(headInv).invert();
  const localDir = bladeDir.clone().applyQuaternion(headInv);
  saber.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), localDir);

  // hilt: grip section behind mouth (pommel side up-forward), emitter side toward blade
  const hilt = new THREE.Mesh(new THREE.CylinderGeometry(0.021, 0.021, 0.16, 20), hiltMat);
  hilt.position.y = 0.01;
  shadowify(hilt);
  saber.add(hilt);
  // pommel ribs
  for (let i = 0; i < 4; i += 1) {
    const rib = new THREE.Mesh(new THREE.TorusGeometry(0.022, 0.004, 8, 20), hiltMat);
    rib.rotation.x = Math.PI / 2;
    rib.position.y = -(0.055 + i * 0.013);
    saber.add(rib);
  }
  // silver tape band at mouth grip point
  const band = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 0.05, 20), tapeMat);
  band.position.y = -0.01;
  shadowify(band);
  saber.add(band);
  // emitter
  const emitter = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.021, 0.035, 20), hiltMat);
  emitter.position.y = 0.085;
  saber.add(emitter);
  // blade core
  const blade = new THREE.Mesh(new THREE.CapsuleGeometry(0.020, 0.56, 6, 16), bladeCoreMat);
  blade.position.y = 0.42;
  saber.add(blade);
  nodes['blade-core'] = blade;
  // glow shells
  for (const [r, l, o] of [[0.030, 0.58, 0.20], [0.048, 0.60, 0.10]] as Array<[number, number, number]>) {
    const glow = new THREE.Mesh(
      new THREE.CapsuleGeometry(r, l, 6, 16),
      bladeGlowMat.clone(),
    );
    (glow.material as THREE.MeshBasicMaterial).opacity = o;
    glow.position.y = 0.42;
    saber.add(glow);
  }
  // red point light rides the blade midpoint
  const bladeLight = new THREE.PointLight(0xff3a1a, 0.9, 1.2, 2.0);
  bladeLight.position.y = 0.42;
  saber.add(bladeLight);

  // ---------- runtime metadata ----------
  (root.userData as Record<string, unknown>).bladeCoreMat = bladeCoreMat;
  (root.userData as Record<string, unknown>).bladeLight = bladeLight;
  root.userData.sculptRuntime = {
    nodes: Object.keys(nodes),
    sockets: Object.keys(sockets),
    animationAnchors: {
      tailWag: 'tail', headTurn: 'head', jawGrip: 'jaw', saberSwing: 'saber',
    },
  };
  (root.userData as Record<string, unknown>).nodes = nodes;
  (root.userData as Record<string, unknown>).sockets = sockets;

  return root;
}

export function createJediLabradorLights(scene: THREE.Scene): void {
  const ambient = new THREE.AmbientLight(0xffffff, 0.95);
  scene.add(ambient);
  const key = new THREE.DirectionalLight(0xffffff, 2.6);
  key.position.set(1.0, 3.2, -1.5);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.left = -1.5; key.shadow.camera.right = 1.5;
  key.shadow.camera.top = 1.5; key.shadow.camera.bottom = -1.5;
  key.shadow.bias = -0.0005;
  scene.add(key);
  const fill = new THREE.HemisphereLight(0xd6dae8, 0x60544a, 0.9);
  scene.add(fill);
}
