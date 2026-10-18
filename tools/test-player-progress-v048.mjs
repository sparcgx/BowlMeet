import fs from 'node:fs';import assert from 'node:assert/strict';
const h=fs.readFileSync('index.html','utf8'),checks=[];
const core=h.split('\n').find(l=>l.startsWith('function normalizeScore('));
const calc=new Function(core+h.split('// PLAYER_PROGRESS_BEGIN')[1].split('// PLAYER_PROGRESS_END')[0]+';return playerProgress')();
function test(name,fn){try{fn();checks.push({name,status:'PASS'})}catch(e){checks.push({name,status:'FAIL',detail:e.message})}}
const games=(n,score)=>Array.from({length:n},(_,i)=>({date:'2026-10-18',createdAt:i,score:typeof score==='function'?score(i):score}));
test('Empty data',()=>{const r=calc([]);assert.equal(r.average,null);assert.equal(r.delta,null)});
test('Zero counts',()=>assert.equal(calc(games(20,0)).delta,0));
test('Insufficient prior period cannot imply progress',()=>assert.equal(calc(games(19,100)).delta,null));
test('Equal non-overlapping 10 game windows',()=>assert.equal(calc(games(20,i=>i<10?100:150)).delta,50));
test('20 game window uses forty games',()=>assert.equal(calc(games(40,i=>i<20?150:100),20).delta,-50));
test('Unsorted input sorted chronologically',()=>assert.equal(calc(games(20,i=>i<10?100:200).reverse()).delta,100));
test('Invalid scores excluded',()=>assert.equal(calc([{score:null},{score:301},{score:-1},{score:2.5},{score:0}]).count,1));
test('Partial current window sample count',()=>assert.equal(calc(games(3,100)).count,3));
test('Older results outside windows excluded',()=>assert.equal(calc(games(30,i=>i<10?300:100)).delta,0));
test('No mutation',()=>{const g=games(20,100).reverse(),s=JSON.stringify(g);calc(g);assert.equal(JSON.stringify(g),s)});
console.log(JSON.stringify({suite:'Player progress',checks,passed:checks.filter(x=>x.status==='PASS').length,failed:checks.filter(x=>x.status==='FAIL').length},null,2));process.exitCode=checks.some(x=>x.status==='FAIL')?1:0;
