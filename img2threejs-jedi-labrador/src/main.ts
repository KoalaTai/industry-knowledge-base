import * as THREE from 'three';
import { createJediLabradorModel, createJediLabradorLights } from './createJediLabrador';

declare global {
  interface Window {
    __setView: (name: string) => void;
    __renderDone: boolean;
  }
}

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.style.margin = '0';
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x3c3c44);

const model = createJediLabradorModel({ castShadow: true, receiveShadow: true });
scene.add(model);
createJediLabradorLights(scene);

const floor = new THREE.Mesh(
  new THREE.CircleGeometry(5, 48),
  new THREE.MeshStandardMaterial({ color: 0x35353b, roughness: 0.5, metalness: 0.15 }),
);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

const bbox = new THREE.Box3().setFromObject(model);
const center = bbox.getCenter(new THREE.Vector3());
const size = bbox.getSize(new THREE.Vector3());
const radius = Math.max(size.x, size.y, size.z);

const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.01, 100);

function setView(name: string): void {
  const d = radius * 1.05;
  if (name === 'reference') {
    // 3/4 from front-left of frame: dog faces +X which projects image-left
    camera.position.set(center.x - d * 0.04, center.y + d * 0.28, center.z - d * 1.10);
  } else if (name === 'orbit1') {
    camera.position.set(center.x + d * 0.9, center.y + d * 0.45, center.z - d * 0.55);
  } else if (name === 'orbit2') {
    camera.position.set(center.x - d * 0.85, center.y + d * 0.5, center.z + d * 0.6);
  } else if (name === 'front') {
    camera.position.set(center.x + d * 1.1, center.y + d * 0.2, center.z);
  }
  camera.lookAt(center.x + size.x * 0.02, center.y - size.y * 0.02, center.z);
  camera.updateProjectionMatrix();
  renderer.render(scene, camera);
}
window.__setView = setView;
(window as any).__stripMaps = () => {
  const flat = new THREE.MeshStandardMaterial({ color: 0x9a9a9a, roughness: 0.9 });
  model.traverse((o) => {
    const mesh = o as THREE.Mesh;
    if (mesh.isMesh) mesh.material = flat;
  });
  renderer.render(scene, camera);
};

setView('reference');
window.__renderDone = true;
