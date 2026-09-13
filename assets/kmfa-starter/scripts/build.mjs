import {build} from 'esbuild';
import {readFile,writeFile,mkdir,copyFile} from 'node:fs/promises';
await mkdir('dist',{recursive:true});
const bundled=await build({entryPoints:['src/app.js'],bundle:true,minify:true,format:'iife',target:'es2022',write:false,legalComments:'inline'});
const html=(await readFile('src/index.html','utf8')).replace('/*__STYLE__*/',await readFile('src/style.css','utf8')).replace('/*__MODEL__*/',(await readFile('dist/assets/kmfa.glb')).toString('base64')).replace('/*__APP__*/',()=>bundled.outputFiles[0].text.replaceAll('</script','<\\/script'));
await writeFile('dist/index.html',html);
await copyFile('dist/index.html','高美館建築漫遊.html');
console.log('Built standalone HTML:',Math.round(Buffer.byteLength(html)/1024),'KiB');
