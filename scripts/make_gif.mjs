// Regenerates experiments/laser-experiment/laser-experiment.gif — a neutral,
// schematic side-view loop of the experiment (laser levelled on a bluff, gold
// beam east over water, drone flying out logging its height; both predictions
// drawn — flat holds, curved falls away). Not to scale.
//
// Requires: Node 18+, ffmpeg on PATH, and `npm i @napi-rs/canvas` (prebuilt,
// no system deps). Run from the repo root:  node scripts/make_gif.mjs
import { createCanvas } from '@napi-rs/canvas'
import { writeFileSync, mkdirSync, rmSync } from 'fs'
import { tmpdir } from 'os'
import { join } from 'path'
import { execSync } from 'child_process'
const FR = join(tmpdir(), 'rb_gif_frames')

const W = 760, H = 400
const START = 8, FLY = 64, HOLD = 26   // start beat + flyout + hold-at-end
const N = START + FLY + HOLD

// theme
const C = {
  cream:'#faf7f0', sky:'#eef3fb', sea:'#dbe8f3', ink:'#2e2a24', mute:'#6b6457',
  gold:'#a06e14', flat:'#2f6690', curved:'#6a5b96', bluff:'#c3bcac', bluffE:'#969692',
}

// scene geometry
const yTitle = 30, yCap = 368
const x0 = 132, xR = 730          // shore origin / beam end
const yBeam = 150, yW = 286       // beam height / flat waterline
const A = 70                      // curved-surface sag at far end (exaggerated)
const dS = x0 + 52, dE = xR - 28  // drone start / end x
const curveY = x => yW + A * Math.pow(Math.max(0,(x - x0)/(xR - x0)), 2)

const mono = px => `${px}px Menlo`
const tracked = (ctx,s,x,y) => {           // crude letter-spacing for caps labels
  let cx = x
  for (const ch of s){ ctx.fillText(ch,cx,y); cx += ctx.measureText(ch).width + 1.5 }
}

function drone(ctx,x,y){
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6
  ctx.beginPath(); ctx.moveTo(x-12,y-6); ctx.lineTo(x+12,y-6); ctx.stroke()   // arm bar
  for (const dx of [-12,12]){                                                 // rotors
    ctx.beginPath(); ctx.moveTo(x+dx,y-9); ctx.lineTo(x+dx,y-3); ctx.stroke()
    ctx.beginPath(); ctx.arc(x+dx,y-6,3.4,0,7); ctx.stroke()
  }
  ctx.fillStyle = C.ink; ctx.fillRect(x-6,y-5,12,7)                            // body
  ctx.fillStyle = '#a03228'; ctx.fillRect(x-9,y-3,4,4)                         // sensor face
}

function laser(ctx){
  // bluff
  ctx.fillStyle = C.bluff; ctx.strokeStyle = C.bluffE; ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(20,yW); ctx.lineTo(20,yW-60); ctx.lineTo(70,yW-56)
  ctx.lineTo(x0-22,yW-118); ctx.lineTo(x0+26,yW); ctx.closePath()
  ctx.fill(); ctx.stroke()
  const bx = x0-14, by = yBeam+8
  // tripod
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5
  for (const dx of [-12,0,12]){ ctx.beginPath(); ctx.moveTo(bx+dx,by+30); ctx.lineTo(bx,by-2); ctx.stroke() }
  ctx.fillStyle = '#dcd9cf'; ctx.strokeStyle = C.ink
  ctx.fillRect(bx-15,by-12,30,9); ctx.strokeRect(bx-15,by-12,30,9)            // head
  ctx.fillStyle = '#646460'; ctx.fillRect(bx-9,yBeam-5,34,8)                  // laser barrel
  // two operators
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.4
  for (const ox of [x0-44,x0-30]){
    const oy = yW-2
    ctx.beginPath(); ctx.arc(ox,oy-34,5,0,7); ctx.stroke()
    ctx.beginPath(); ctx.moveTo(ox,oy-29); ctx.lineTo(ox,oy-12)
    ctx.moveTo(ox,oy-24); ctx.lineTo(ox-7,oy-18); ctx.moveTo(ox,oy-24); ctx.lineTo(ox+7,oy-18)
    ctx.moveTo(ox,oy-12); ctx.lineTo(ox-6,oy); ctx.moveTo(ox,oy-12); ctx.lineTo(ox+6,oy); ctx.stroke()
  }
}

function frame(ctx,p){
  // backdrop
  ctx.fillStyle = C.cream; ctx.fillRect(0,0,W,H)
  ctx.fillStyle = C.sky;   ctx.fillRect(0,yTitle+6,W,yW-(yTitle+6))
  ctx.fillStyle = C.sea;   ctx.fillRect(0,yW,W,yCap-yW)

  // title
  ctx.fillStyle = C.ink; ctx.font = `bold ${'15'}px Menlo`; ctx.textBaseline='alphabetic'
  ctx.textAlign='center'; ctx.fillText('LASER  BEAM  FOLLOW  EXPERIMENT', W/2, 21); ctx.textAlign='left'

  laser(ctx)

  // level beam (glow + dashed) east
  ctx.strokeStyle = 'rgba(160,110,20,0.22)'; ctx.lineWidth = 8
  ctx.beginPath(); ctx.moveTo(x0+12,yBeam); ctx.lineTo(xR,yBeam); ctx.stroke()
  ctx.strokeStyle = C.gold; ctx.lineWidth = 1.6; ctx.setLineDash([9,4])
  ctx.beginPath(); ctx.moveTo(x0+12,yBeam); ctx.lineTo(xR,yBeam); ctx.stroke(); ctx.setLineDash([])
  ctx.fillStyle = C.gold; ctx.beginPath(); ctx.moveTo(xR,yBeam); ctx.lineTo(xR-9,yBeam-4); ctx.lineTo(xR-9,yBeam+4); ctx.fill()
  ctx.font = mono(10); ctx.fillStyle = C.gold; ctx.textAlign='center'
  tracked(ctx,'LEVEL BEAM · EAST · LEVELLED & LOCKED', x0+150, yBeam-9); ctx.textAlign='left'

  // both surface predictions from shared shore origin
  ctx.lineWidth = 1.8
  ctx.strokeStyle = C.flat; ctx.setLineDash([7,4])
  ctx.beginPath(); ctx.moveTo(x0,yW); ctx.lineTo(xR,yW); ctx.stroke()
  ctx.strokeStyle = C.curved; ctx.setLineDash([7,4])
  ctx.beginPath(); ctx.moveTo(x0,yW)
  for (let x=x0; x<=xR; x+=4) ctx.lineTo(x,curveY(x))
  ctx.stroke(); ctx.setLineDash([])

  const xd = dS + p*(dE - dS)

  // accumulated readings (ticks along the beam)
  ctx.strokeStyle = 'rgba(45,42,36,0.28)'; ctx.lineWidth = 1
  for (let x=dS; x<=xd; x+=13){ ctx.beginPath(); ctx.moveTo(x,yBeam+2); ctx.lineTo(x,yBeam+9); ctx.stroke() }

  // height-above-water bars to each predicted surface
  ctx.lineWidth = 2
  ctx.strokeStyle = C.flat
  ctx.beginPath(); ctx.moveTo(xd,yBeam); ctx.lineTo(xd,yW); ctx.stroke()
  ctx.fillStyle = C.flat; ctx.beginPath(); ctx.arc(xd,yW,3,0,7); ctx.fill()
  ctx.strokeStyle = C.curved; ctx.setLineDash([3,3])
  ctx.beginPath(); ctx.moveTo(xd,yW); ctx.lineTo(xd,curveY(xd)); ctx.stroke(); ctx.setLineDash([])
  ctx.fillStyle = C.curved; ctx.beginPath(); ctx.arc(xd,curveY(xd),3,0,7); ctx.fill()

  drone(ctx,xd,yBeam)

  // legend (top-right, below title)
  ctx.font = mono(11)
  ctx.fillStyle = C.flat;   ctx.fillRect(W-326,46,16,3); ctx.fillText('IF FLAT — height holds', W-304,51)
  ctx.fillStyle = C.curved; ctx.fillRect(W-326,64,16,3); ctx.fillText('IF CURVED — water falls (≈8 in×mi²)', W-304,69)

  ctx.font = mono(9); ctx.fillStyle = C.mute
  ctx.fillText('OPEN WATER · SURFACE UNDER TEST', 22, yW+32)

  // caption band
  ctx.fillStyle = C.cream; ctx.fillRect(0,yCap,W,H-yCap)
  ctx.font = mono(10); ctx.fillStyle = C.ink; ctx.textAlign='center'
  ctx.fillText('Both predictions are drawn before the run — the drone logs its height the whole way, and the readings land on one.', W/2, yCap+15)
  ctx.font = mono(8.5); ctx.fillStyle = C.mute
  ctx.fillText('illustration — not to scale  ·  replicationbench.github.io/RB', W/2, yCap+27); ctx.textAlign='left'
}

rmSync(FR, {recursive:true, force:true}); mkdirSync(FR, {recursive:true})
for (let i=0;i<N;i++){
  const p = i < START ? 0 : i < START+FLY ? (i-START)/(FLY-1) : 1
  const canvas = createCanvas(W,H)
  frame(canvas.getContext('2d'), p)
  writeFileSync(join(FR, `f${String(i).padStart(4,'0')}.png`), canvas.toBuffer('image/png'))
}
console.log('wrote', N, 'frames', `${W}x${H}`)
const OUT = 'experiments/laser-experiment/laser-experiment.gif'
execSync(`ffmpeg -y -framerate 20 -i ${join(FR,'f%04d.png')} -filter_complex "[0:v] split [a][b];[a] palettegen=stats_mode=diff [p];[b][p] paletteuse=dither=bayer:bayer_scale=3" ${OUT}`, {stdio:'inherit'})
console.log('wrote', OUT)
