import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { createJediLabradorModel, createJediLabradorLights } from './createJediLabrador';

const container = document.getElementById('stage') as HTMLElement;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x232228);
scene.fog = new THREE.Fog(0x232228, 4.5, 9);

const model = createJediLabradorModel({ castShadow: true, receiveShadow: true });
scene.add(model);
createJediLabradorLights(scene);

const floor = new THREE.Mesh(
  new THREE.CircleGeometry(6, 64),
  new THREE.MeshStandardMaterial({ color: 0x2d2d33, roughness: 0.45, metalness: 0.2 }),
);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

const bbox = new THREE.Box3().setFromObject(model);
const center = bbox.getCenter(new THREE.Vector3());
const radius = Math.max(...bbox.getSize(new THREE.Vector3()).toArray());

const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 60);
camera.position.set(center.x - radius * 0.05, center.y + radius * 0.32, center.z - radius * 1.2);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.copy(center);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = radius * 0.5;
controls.maxDistance = radius * 4;
controls.maxPolarAngle = Math.PI * 0.55;

// animation handles
const nodes = (model.userData as Record<string, any>).nodes as Record<string, THREE.Object3D>;
const bladeCoreMat = (model.userData as Record<string, any>).bladeCoreMat as THREE.MeshStandardMaterial;
const bladeLight = (model.userData as Record<string, any>).bladeLight as THREE.PointLight;
const tail = nodes.tail;
const head = nodes.head;
const headBaseY = head.rotation.y;

let wag = true;
let autoOrbit = false;
const wagBtn = document.getElementById('wag') as HTMLButtonElement;
const orbitBtn = document.getElementById('orbit') as HTMLButtonElement;
wagBtn.addEventListener('click', () => {
  wag = !wag;
  wagBtn.textContent = wag ? 'Tail: wagging' : 'Tail: still';
  wagBtn.setAttribute('aria-pressed', String(wag));
});
orbitBtn.addEventListener('click', () => {
  autoOrbit = !autoOrbit;
  controls.autoRotate = autoOrbit;
  controls.autoRotateSpeed = 1.2;
  orbitBtn.textContent = autoOrbit ? 'Orbit: auto' : 'Orbit: drag';
  orbitBtn.setAttribute('aria-pressed', String(autoOrbit));
});

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduceMotion) { wag = false; wagBtn.textContent = 'Tail: still'; }

function resize(): void {
  const w = container.clientWidth;
  const h = container.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);
resize();

const clock = new THREE.Clock();
function tick(): void {
  const t = clock.getElapsedTime();
  if (wag) {
    tail.rotation.x = Math.sin(t * 6.0) * 0.22;
    head.rotation.y = headBaseY + Math.sin(t * 0.7) * 0.06;
  }
  if (!reduceMotion) {
    // saber hum: subtle flicker on core + light
    const flick = 1 + Math.sin(t * 23.0) * 0.05 + Math.sin(t * 7.7) * 0.04;
    bladeCoreMat.emissiveIntensity = 4.0 * flick;
    bladeLight.intensity = 0.9 * flick;
  }
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
tick();
