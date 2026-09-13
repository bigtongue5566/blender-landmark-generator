import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const model=await readFile('dist/assets/kmfa.glb');
assert.equal(model.readUInt32LE(0),0x46546c67);assert.equal(model.readUInt32LE(4),2);assert.equal(model.readUInt32LE(8),model.length);
const gltf=JSON.parse(model.subarray(20,20+model.readUInt32LE(12)).toString());
assert(gltf.meshes.length>10);assert.equal(gltf.scenes.length,1);assert(!gltf.nodes.some(n=>n.name==='Cube'));assert(gltf.nodes.some(n=>n.name.startsWith('Architecture')));assert(gltf.nodes.some(n=>n.name.startsWith('Water')));assert(gltf.nodes.some(n=>n.name.startsWith('Landscape')));
for(const a of gltf.accessors){if(a.min)assert(a.min.every(Number.isFinite));if(a.max)assert(a.max.every(Number.isFinite));}
const html=await readFile('dist/index.html','utf8');assert(!html.includes('/*__MODEL__*/'));assert(!html.includes('/*__APP__*/'));assert(!html.includes('/*__STYLE__*/'));
const encoded=html.match(/<script id="model-data" type="application\/octet-stream">([^<]+)<\/script>/)[1];assert(Buffer.from(encoded,'base64').equals(model));assert(!/<script[^>]+src=/.test(html));assert(!/<link[^>]+rel="stylesheet"/.test(html));
for(const id of ['viewport','sun','exposure','mood','vegetation','people','material','orbit','labels','capture','download','reset'])assert(html.includes(`id="${id}"`));
console.log(JSON.stringify({valid:true,meshCount:gltf.meshes.length,materials:gltf.materials.length,modelBytes:model.length,standaloneHtmlBytes:Buffer.byteLength(html),externalRuntimeDependencies:0},null,2));
