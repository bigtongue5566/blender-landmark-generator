import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const $=id=>document.getElementById(id), host=$('viewport');
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const mobile=()=>innerWidth<=700;
if(mobile()){document.body.classList.add('panel-hidden');$('panelToggle').setAttribute('aria-expanded','false');}
let renderer,scene,camera,controls,model,sun,hemi,ground,transition=null,ready=false;
const original=new Map(),vegetation=[],people=[],labels=[],clay=new THREE.MeshStandardMaterial({color:0xe3dfd2,roughness:.8});
const views={
 overview:{position:[245,240,300],target:[-1,0,4],zoom:300,label:'園區鳥瞰'},
 front:{position:[65,70,175],target:[-31,11,-6],zoom:150,label:'館前廣場'},
 lake:{position:[210,110,-90],target:[-10,9,-20],zoom:218,label:'湖畔視角'},
 top:{position:[0,330,.1],target:[0,0,0],zoom:285,label:'俯視平面'}
};
let currentView='overview',frameWidth=300;
const download=(blob,name)=>{const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),3000);};
function toast(s){$('toast').textContent=s;$('toast').classList.add('show');setTimeout(()=>$('toast').classList.remove('show'),2600);}
function rawModel(){return Uint8Array.from(atob($('model-data').textContent.trim()),c=>c.charCodeAt(0));}
function resize(){if(!renderer)return;const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);const aspect=w/h;const scale=mobile()?frameWidth*1.15:frameWidth;camera.left=-scale*aspect/2;camera.right=scale*aspect/2;camera.top=scale/2;camera.bottom=-scale/2;camera.updateProjectionMatrix();}
function setView(name,instant=false){
 currentView=name;const v=views[name];$('viewName').textContent=v.label;
 document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('active',b.dataset.view===name);b.setAttribute('aria-pressed',String(b.dataset.view===name));});
 controls.autoRotate=false;$('orbit').checked=false;
 if(instant||reduced){camera.position.fromArray(v.position);controls.target.fromArray(v.target);frameWidth=v.zoom;resize();controls.update();transition=null;}
 else transition={t:performance.now(),from:camera.position.clone(),targetFrom:controls.target.clone(),widthFrom:frameWidth,to:new THREE.Vector3(...v.position),targetTo:new THREE.Vector3(...v.target),widthTo:v.zoom};
}
function light(){if(!ready)return;const mood=$('mood').value,elev=+$('sun').value*Math.PI/180;
 const moods={day:{sun:0xfff1d7,power:3.2,sky:0xd2dce0,ambient:2.2,water:0x397f7c},golden:{sun:0xffbd72,power:3.7,sky:0xd8cbb9,ambient:1.65,water:0x618c87},blue:{sun:0x94b6ed,power:.9,sky:0x849bb6,ambient:1.5,water:0x315a79}};
 const m=moods[mood];sun.color.set(m.sun);sun.intensity=m.power;sun.position.set(-Math.cos(elev)*180,Math.sin(elev)*240,95);hemi.intensity=m.ambient;scene.background.set(m.sky);ground.material.color.set(m.sky);document.body.style.background='#'+new THREE.Color(m.sky).getHexString();
 renderer.toneMappingExposure=+$('exposure').value/100; $('sunValue').textContent=$('sun').value+'°';$('exposureValue').textContent=$('exposure').value+'%';
}
function showError(e){console.error(e);const loading=$('loading');if(loading)loading.innerHTML='<strong>無法啟動三維畫面</strong><small>請使用支援 WebGL 的瀏覽器，並確認 HTML 檔案完整。</small>'; $('modelState').textContent='載入失敗';}
function init(){
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.toneMapping=THREE.ACESFilmicToneMapping;host.appendChild(renderer.domElement);
 scene=new THREE.Scene();scene.background=new THREE.Color(0xd2dce0);
 camera=new THREE.OrthographicCamera(-200,200,150,-150,.1,1800);
 controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.065;controls.minZoom=.55;controls.maxZoom=6;controls.maxPolarAngle=Math.PI*.49;controls.autoRotateSpeed=.35;controls.screenSpacePanning=true;
 controls.addEventListener('start',()=>{transition=null;controls.autoRotate=false;$('orbit').checked=false;});
 hemi=new THREE.HemisphereLight(0xe7f3ff,0x697a54,2.2);scene.add(hemi);
 sun=new THREE.DirectionalLight(0xfff1d7,3.2);sun.position.set(-120,180,100);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-190;sun.shadow.camera.right=190;sun.shadow.camera.top=190;sun.shadow.camera.bottom=-190;sun.shadow.camera.near=1;sun.shadow.camera.far=650;sun.shadow.normalBias=.35;sun.shadow.bias=-.00008;scene.add(sun);
 ground=new THREE.Mesh(new THREE.PlaneGeometry(3000,3000),new THREE.MeshStandardMaterial({color:0xd2dce0,roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-4.2;ground.receiveShadow=true;scene.add(ground);
 setView('overview',true);resize();window.addEventListener('resize',resize);
 new GLTFLoader().parse(rawModel().buffer,'',g=>{
  model=g.scene;model.traverse(o=>{if(o.isMesh){o.castShadow=!o.name.startsWith('Water');o.receiveShadow=true;original.set(o,o.material);if(o.name.startsWith('Landscape')&&(o.name.includes('Canopy')||o.name.includes('Bark')))vegetation.push(o);if(o.name.startsWith('People'))people.push(o);if(o.material){o.material.side=THREE.DoubleSide;}}});
  scene.add(model);ready=true;light();$('modelState').textContent='Blender 模型';$('loading').style.opacity=0;setTimeout(()=>$('loading').remove(),550);
  for(const [n,title,pos] of [['01','美術館主館',[-32,33,-30]],['02','半圓迴廊',[-66,9,46]],['03','生態湖',[76,2,-18]]]){const e=document.createElement('div');e.className='landmark';e.innerHTML=`<b>${n}</b>${title}`;$('landmarks').appendChild(e);labels.push({e,pos:new THREE.Vector3(...pos)});}
 },showError);
 renderer.setAnimationLoop(now=>{
  if(transition){const p=Math.min((now-transition.t)/1100,1),t=1-Math.pow(1-p,3);camera.position.lerpVectors(transition.from,transition.to,t);controls.target.lerpVectors(transition.targetFrom,transition.targetTo,t);frameWidth=THREE.MathUtils.lerp(transition.widthFrom,transition.widthTo,t);camera.zoom=1;resize();if(p===1)transition=null;}
  controls.update();renderer.render(scene,camera);
  for(const l of labels){const v=l.pos.clone().project(camera);l.e.style.left=(v.x*.5+.5)*host.clientWidth+'px';l.e.style.top=(-v.y*.5+.5)*host.clientHeight-20+'px';l.e.hidden=!$('labels').checked||v.z>1||Math.abs(v.x)>.94||Math.abs(v.y)>.89;}
  $('compassNeedle').style.transform=`rotate(${-controls.getAzimuthalAngle()*180/Math.PI}deg)`;
 });
}
try{init();}catch(e){showError(e);}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{if(ready)setView(b.dataset.view);if(mobile()){document.body.classList.add('panel-hidden');$('panelToggle').setAttribute('aria-expanded','false');}}));
for(const id of ['sun','exposure'])$(id).addEventListener('input',light);
$('mood').addEventListener('change',()=>{$('sun').value={day:48,golden:20,blue:12}[$('mood').value];light();});
$('vegetation').addEventListener('change',()=>vegetation.forEach(o=>o.visible=$('vegetation').checked));
$('people').addEventListener('change',()=>people.forEach(o=>o.visible=$('people').checked));
$('material').addEventListener('change',()=>{if(!model)return;model.traverse(o=>{if(o.isMesh)o.material=$('material').value==='clay'?clay:original.get(o);});});
$('orbit').addEventListener('change',()=>{if(controls){transition=null;controls.autoRotate=$('orbit').checked;}if(reduced&&$('orbit').checked)toast('已依你的操作開啟環繞');});
$('reset').addEventListener('click',()=>{if(!ready)return;$('mood').value='day';$('sun').value=48;$('exposure').value=100;$('material').value='original';for(const id of ['vegetation','people','labels'])$(id).checked=true;vegetation.concat(people).forEach(o=>o.visible=true);model.traverse(o=>{if(o.isMesh)o.material=original.get(o);});setView('overview');light();toast('已回到初始場景');});
$('panelToggle').addEventListener('click',()=>{const hidden=document.body.classList.toggle('panel-hidden');$('panelToggle').setAttribute('aria-expanded',String(!hidden));});
$('aboutBtn').addEventListener('click',()=>$('about').showModal());$('closeAbout').addEventListener('click',()=>$('about').close());$('about').addEventListener('click',e=>{if(e.target===$('about')){const r=$('about').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)$('about').close();}});
$('download').addEventListener('click',()=>{if(!ready)return;download(new Blob([rawModel()],{type:'model/gltf-binary'}),'KMFA.blender-model.glb');toast('正在下載 3D 模型');});
$('capture').addEventListener('click',()=>{if(!ready)return;renderer.render(scene,camera);renderer.domElement.toBlob(b=>{if(b){download(b,'KMFA-'+currentView+'.png');toast('已儲存目前視角');}},'image/png');});
host.addEventListener('keydown',e=>{if(!ready)return;if(e.key==='Home'){setView('overview');e.preventDefault();}if(e.key==='+'||e.key==='='){camera.zoom=Math.min(camera.zoom*1.12,6);camera.updateProjectionMatrix();}if(e.key==='-'){camera.zoom=Math.max(camera.zoom/1.12,.55);camera.updateProjectionMatrix();}});
