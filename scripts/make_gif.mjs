// Regenerates experiments/laser-experiment/laser-experiment.gif — a neutral,
// schematic 8-second loop: the water settles from choppy to still, the laser
// powers on and its level beam shimmers east over the water, a drone flies out
// logging its height, and the reading-ticks tick in behind it. Both predictions
// drawn equally — flat holds, curved falls away. Not to scale, no title band
// (the page/README supply the heading). Rendered at 2x and lanczos-downscaled
// with no dither for crisp text.
//
// Requires: Node 18+, ffmpeg on PATH, and `npm i @napi-rs/canvas` (prebuilt,
// no system deps). Run from the repo root:  node scripts/make_gif.mjs
import { createCanvas } from '@napi-rs/canvas'
import { writeFileSync, mkdirSync, rmSync } from 'fs'
import { tmpdir } from 'os'
import { join } from 'path'
import { execSync } from 'child_process'
const FR = join(tmpdir(), 'rb_gif_frames')

const W = 760, H = 400, FPS = 20
const SETTLE = 30, FLY = 104, HOLD = 26     // 1.5s settle + 5.2s flyout + 1.3s hold = 8.0s
const N = SETTLE + FLY + HOLD

const C = {
  cream:'#faf7f0', sky:'#eef3fb', sea:'#d3e4f1', seaTop:'#c4dbed', ink:'#2e2a24', mute:'#6b6457',
  gold:'#a06e14', goldHi:'#e7c071', flat:'#2f6690', curved:'#6a5b96', bluff:'#c3bcac', bluffE:'#969692',
}
const yTitle = 30, yCap = 368
const x0 = 132, xR = 730
const yBeam = 150, yW = 286, A = 70
const dS = x0 + 52, dE = xR - 28
const curveY = x => yW + A * Math.pow(Math.max(0,(x - x0)/(xR - x0)), 2)
const mono = px => `${px}px Menlo`
const clamp = (v,a,b) => Math.max(a, Math.min(b, v))
const easeOut = t => 1 - Math.pow(1 - t, 3)
const tracked = (ctx,s,x,y) => { let cx=x; for (const ch of s){ ctx.fillText(ch,cx,y); cx += ctx.measureText(ch).width + 1.5 } }

function drone(ctx,x,y){
  ctx.strokeStyle=C.ink; ctx.lineWidth=1.6
  ctx.beginPath(); ctx.moveTo(x-12,y-6); ctx.lineTo(x+12,y-6); ctx.stroke()
  for (const dx of [-12,12]){
    ctx.beginPath(); ctx.moveTo(x+dx,y-9); ctx.lineTo(x+dx,y-3); ctx.stroke()
    ctx.beginPath(); ctx.arc(x+dx,y-6,3.4,0,7); ctx.stroke()
  }
  ctx.fillStyle=C.ink; ctx.fillRect(x-6,y-5,12,7)
  ctx.fillStyle='#a03228'; ctx.fillRect(x-9,y-3,4,4)
}

function laser(ctx){
  ctx.fillStyle=C.bluff; ctx.strokeStyle=C.bluffE; ctx.lineWidth=1
  ctx.beginPath(); ctx.moveTo(20,yW); ctx.lineTo(20,yW-60); ctx.lineTo(70,yW-56)
  ctx.lineTo(x0-22,yW-118); ctx.lineTo(x0+26,yW); ctx.closePath(); ctx.fill(); ctx.stroke()
  const bx=x0-14, by=yBeam+8
  ctx.strokeStyle=C.ink; ctx.lineWidth=1.5
  for (const dx of [-12,0,12]){ ctx.beginPath(); ctx.moveTo(bx+dx,by+30); ctx.lineTo(bx,by-2); ctx.stroke() }
  ctx.fillStyle='#dcd9cf'; ctx.strokeStyle=C.ink
  ctx.fillRect(bx-15,by-12,30,9); ctx.strokeRect(bx-15,by-12,30,9)
  ctx.fillStyle='#646460'; ctx.fillRect(bx-9,yBeam-5,34,8)
  ctx.strokeStyle=C.ink; ctx.lineWidth=1.4
  for (const ox of [x0-44,x0-30]){
    const oy=yW-2
    ctx.beginPath(); ctx.arc(ox,oy-34,5,0,7); ctx.stroke()
    ctx.beginPath(); ctx.moveTo(ox,oy-29); ctx.lineTo(ox,oy-12)
    ctx.moveTo(ox,oy-24); ctx.lineTo(ox-7,oy-18); ctx.moveTo(ox,oy-24); ctx.lineTo(ox+7,oy-18)
    ctx.moveTo(ox,oy-12); ctx.lineTo(ox-6,oy); ctx.moveTo(ox,oy-12); ctx.lineTo(ox+6,oy); ctx.stroke()
  }
}

function frame(ctx,i){
  const s = i < SETTLE ? i/(SETTLE-1) : 1                         // settle 0->1
  const p = i < SETTLE ? 0 : i < SETTLE+FLY ? (i-SETTLE)/(FLY-1) : 1
  const es = easeOut(clamp(s,0,1))
  const beamA = clamp(i/9, 0, 1)                                  // beam powers on

  ctx.fillStyle=C.cream; ctx.fillRect(0,0,W,H)
  ctx.fillStyle=C.sky;   ctx.fillRect(0,0,W,yW)

  // --- water: choppy at start, settles to a gentle living ripple ---
  const amp = 7.6*(1-es)                                          // choppy at start, damps to still
  const ph = i*0.34
  const seaY = x => yW + amp*Math.sin(0.05*x + ph) + 0.45*amp*Math.sin(0.11*x - ph*1.25)
  ctx.beginPath(); ctx.moveTo(0, seaY(0))
  for (let x=0; x<=W; x+=4) ctx.lineTo(x, seaY(x))
  ctx.lineTo(W,yCap); ctx.lineTo(0,yCap); ctx.closePath()
  ctx.fillStyle=C.sea; ctx.fill()
  ctx.strokeStyle=C.seaTop; ctx.lineWidth=1.4
  ctx.beginPath(); ctx.moveTo(0,seaY(0)); for (let x=0;x<=W;x+=4) ctx.lineTo(x,seaY(x)); ctx.stroke()

  // --- the two predictions, fading in as the water settles ---
  ctx.globalAlpha = es
  ctx.lineWidth=1.8; ctx.setLineDash([7,4])
  ctx.strokeStyle=C.flat;   ctx.beginPath(); ctx.moveTo(x0,yW); ctx.lineTo(xR,yW); ctx.stroke()
  ctx.strokeStyle=C.curved; ctx.beginPath(); ctx.moveTo(x0,yW)
  for (let x=x0;x<=xR;x+=4) ctx.lineTo(x,curveY(x)); ctx.stroke()
  ctx.setLineDash([]); ctx.globalAlpha=1

  ctx.font=mono(9); ctx.fillStyle=C.mute; ctx.fillText('OPEN WATER · SURFACE UNDER TEST', 22, yW+34)

  laser(ctx)

  // --- level beam: glow, marching dashes, and a travelling shimmer highlight ---
  ctx.globalAlpha=beamA
  ctx.strokeStyle='rgba(160,110,20,0.20)'; ctx.lineWidth=8
  ctx.beginPath(); ctx.moveTo(x0+12,yBeam); ctx.lineTo(xR,yBeam); ctx.stroke()
  ctx.strokeStyle=C.gold; ctx.lineWidth=1.6; ctx.setLineDash([9,4]); ctx.lineDashOffset = -i*1.1
  ctx.beginPath(); ctx.moveTo(x0+12,yBeam); ctx.lineTo(xR,yBeam); ctx.stroke()
  ctx.setLineDash([]); ctx.lineDashOffset=0
  // travelling highlight
  const span = xR-(x0+18)
  const gx = x0+18 + ((i*10) % span)
  const grad = ctx.createRadialGradient(gx,yBeam,0,gx,yBeam,26)
  grad.addColorStop(0,'rgba(231,192,113,0.85)'); grad.addColorStop(1,'rgba(231,192,113,0)')
  ctx.fillStyle=grad; ctx.fillRect(gx-26,yBeam-7,52,14)
  ctx.fillStyle=C.gold; ctx.beginPath(); ctx.moveTo(xR,yBeam); ctx.lineTo(xR-9,yBeam-4); ctx.lineTo(xR-9,yBeam+4); ctx.fill()
  ctx.font=mono(10); ctx.fillStyle=C.gold; ctx.textAlign='center'
  tracked(ctx,'LEVEL BEAM · EAST · LEVELLED & LOCKED', x0+150, yBeam-9); ctx.textAlign='left'
  ctx.globalAlpha=1

  const bob = 1.4*Math.sin(i*0.5)
  const xd = dS + p*(dE - dS)
  const yd = yBeam + (p>0 ? bob : 0)

  if (p > 0){
    // reading ticks "tick in" with a fade as the drone passes
    ctx.strokeStyle=C.ink
    for (let tx=dS; tx<=xd; tx+=13){
      const age = xd - tx
      const a = clamp(age/24, 0, 1)
      ctx.globalAlpha = 0.30*a
      const h = 7 + 5*(1-a)
      ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(tx,yBeam+2); ctx.lineTo(tx,yBeam+2+h); ctx.stroke()
    }
    ctx.globalAlpha=1
    // height bars to each prediction
    ctx.lineWidth=2; ctx.strokeStyle=C.flat
    ctx.beginPath(); ctx.moveTo(xd,yd); ctx.lineTo(xd,yW); ctx.stroke()
    ctx.fillStyle=C.flat; ctx.beginPath(); ctx.arc(xd,yW,3,0,7); ctx.fill()
    ctx.strokeStyle=C.curved; ctx.setLineDash([3,3])
    ctx.beginPath(); ctx.moveTo(xd,yW); ctx.lineTo(xd,curveY(xd)); ctx.stroke(); ctx.setLineDash([])
    ctx.fillStyle=C.curved; ctx.beginPath(); ctx.arc(xd,curveY(xd),3,0,7); ctx.fill()
    // bright sample blip at the drone
    ctx.fillStyle='rgba(231,192,113,0.9)'; ctx.beginPath(); ctx.arc(xd,yBeam+9,2.4,0,7); ctx.fill()
  }
  drone(ctx, xd, yd)

  // legend (top-right)
  ctx.font=mono(11)
  ctx.fillStyle=C.flat;   ctx.fillRect(W-326,22,16,3); ctx.fillText('IF FLAT — height holds', W-304,27)
  ctx.fillStyle=C.curved; ctx.fillRect(W-326,40,16,3); ctx.fillText('IF CURVED — water falls (≈8 in×mi²)', W-304,45)

  // caption
  ctx.fillStyle=C.cream; ctx.fillRect(0,yCap,W,H-yCap)
  ctx.font=mono(10); ctx.fillStyle=C.ink; ctx.textAlign='center'
  ctx.fillText('Both predictions are drawn before the run — the drone logs its height the whole way, and the readings land on one.', W/2, yCap+15)
  ctx.font=mono(8.5); ctx.fillStyle=C.mute
  ctx.fillText('Laser Beam Follow Experiment  ·  illustration, not to scale  ·  replicationbench.github.io/RB', W/2, yCap+27); ctx.textAlign='left'
}

const SCALE = 2   // supersample, then ffmpeg lanczos-downscales to W×H for crisp text
rmSync(FR, {recursive:true, force:true}); mkdirSync(FR, {recursive:true})
for (let i=0;i<N;i++){
  const canvas=createCanvas(W*SCALE,H*SCALE)
  const ctx=canvas.getContext('2d'); ctx.scale(SCALE,SCALE)
  frame(ctx, i)
  writeFileSync(join(FR, `f${String(i).padStart(4,'0')}.png`), canvas.toBuffer('image/png'))
}
console.log('wrote', N, 'frames', `${W*SCALE}x${H*SCALE} → ${W}x${H}`, '=', (N/FPS).toFixed(1)+'s')
const OUT = 'experiments/laser-experiment/laser-experiment.gif'
execSync(`ffmpeg -y -framerate ${FPS} -i ${join(FR,'f%04d.png')} -filter_complex "[0:v] scale=${W}:${H}:flags=lanczos,split [a][b];[a] palettegen=max_colors=96:stats_mode=diff [p];[b][p] paletteuse=dither=none" ${OUT}`, {stdio:'inherit'})
console.log('wrote', OUT)
