#!/usr/bin/env python3
"""The labelling page for a map: where the editor marks place names on it.

    python pipeline/maps/label_page.py lukom1766

Writes review/maps/<key>/index.html (review/ is not in the repository) and
copies the vendored OpenSeadragon to review/maps/vendor/openseadragon.min.js.
The page is one self-contained HTML file; its data (the map, the gazetteer's
"to find" list for this map, every place, and any labels already made) is
embedded as JSON. It is served locally, because the tiles come over HTTP:

    python -m http.server 8765 --directory review/maps
    http://localhost:8765/<key>/

The work is kept in the browser's localStorage as the editor goes
("maplabels:<key>"); "Save" downloads labels_<key>_<date>.json, the file
pipeline/maps/import_labels.py brings in. Like pipeline/intake/fold_page.py,
this is the one page for the job: do not build another.

Saved format (fixed; import_labels.py reads it):
  {"map", "width", "height", "saved",
   "labels": [{"id", "place", "new_place", "form", "point", "trace",
               "height", "shows", "note", ["breaks"]}]}
all coordinates integers in the image's own pixels. "trace" runs along the
BASELINE of the lettering (the line the letters stand on); "height" is the
letters' height above that baseline in image pixels ("up" is the left-hand
perpendicular of each line's reading direction, (dy, -dx) in y-down pixels);
descenders are allowed 0.35 * height below it. "breaks" (only when
non-empty) lists the indices into "trace" where a new line of a name written
on several lines starts; without it the lines are found by the rule in
import_labels.split_lines (which the page's splitLines mirrors).
"""
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "pipeline" / "maps" / "vendor" / "openseadragon" / "openseadragon.min.js"


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_data(key):
    maps = load_yaml(ROOT / "reference" / "maps.yml")["maps"]
    if key not in maps:
        sys.exit("No map %r in reference/maps.yml" % key)
    m = maps[key]
    for need in ("width", "height", "tiles"):
        if not m.get(need):
            sys.exit("Map %r has no %s in reference/maps.yml" % (key, need))
    mapinfo = {
        "key": key,
        "title": m.get("title_en") or m.get("title") or key,
        "cited_as": m.get("cited_as") or key,
        "width": m["width"],
        "height": m["height"],
        "view_rotation": m.get("view_rotation") or 0,
        "tiles": m["tiles"],
    }
    find, places = [], []
    for p in sorted((ROOT / "reference" / "gazetteer").glob("*.yml")):
        g = load_yaml(p) or {}
        slug = g.get("slug") or p.stem
        heading = g.get("heading") or slug
        forms = []
        for n in g.get("names") or []:
            f = (n or {}).get("form")
            if f and f not in forms:
                forms.append(f)
        for a in g.get("aliases") or []:
            if a and a not in forms:
                forms.append(a)
        places.append({"slug": slug, "heading": heading, "forms": forms})
        for it in g.get("maps") or []:
            # absent: true records that the entry says the place is NOT on
            # this map (Myszakówek on Łukom 1766): nothing to find.
            if (it or {}).get("map") == key and not it.get("absent"):
                find.append({"place": slug, "heading": heading,
                             "form": it.get("form"), "note": it.get("note")})
    labels = []
    lp = ROOT / "maps" / key / "labels.yml"
    if lp.exists():
        d = load_yaml(lp)
        if isinstance(d, dict):
            d = d.get("labels")
        labels = d or []
    return {"map": mapinfo, "find": find, "places": places, "labels": labels}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    key = sys.argv[1]
    data = build_data(key)
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("/*DATA*/null", blob).replace("%%TITLE%%", data["map"]["cited_as"])
    out = ROOT / "review" / "maps" / key
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "index.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    vend = ROOT / "review" / "maps" / "vendor"
    vend.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(VENDOR, vend / "openseadragon.min.js")
    print("Wrote", out / "index.html", "(%d to find, %d places, %d labels)" % (
        len(data["find"]), len(data["places"]), len(data["labels"])))
    print("To open it:")
    print("  python -m http.server 8765 --directory review/maps")
    print("  http://localhost:8765/%s/" % key)


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Label the map: %%TITLE%%</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font:14px/1.4 system-ui,Segoe UI,Arial,sans-serif;color:#222;background:#fff}
#panel{position:absolute;left:0;top:0;bottom:0;width:320px;overflow-y:auto;padding:10px;background:#f6f4ef;border-right:1px solid #bbb}
#viewer{position:absolute;left:320px;right:0;top:0;bottom:0;background:#333}
#overlay{position:absolute;left:320px;top:0;pointer-events:none;z-index:5}
h1{font-size:16px;margin:0 0 2px}
h2{font-size:13px;margin:12px 0 4px;text-transform:uppercase;letter-spacing:.04em;color:#555}
.sub{color:#666;font-size:12px;margin-bottom:6px}
button{font:inherit;padding:3px 8px;margin:2px 2px 2px 0;border:1px solid #999;background:#fff;border-radius:3px;cursor:pointer}
button:hover{background:#eee}
button.on{background:#c0392b;color:#fff;border-color:#c0392b}
button.danger{color:#a00}
input,select{font:inherit;width:100%;padding:3px 5px;border:1px solid #999;border-radius:3px;margin:1px 0 4px}
label.f{display:block;font-size:12px;color:#555}
#status{margin:8px 0;padding:6px 8px;background:#fff8d8;border:1px solid #d9c96a;border-radius:3px;min-height:34px}
#counter{font-weight:600}
ul.items{list-style:none;margin:0;padding:0}
ul.items li{padding:3px 6px;border-radius:3px;cursor:pointer;border:1px solid transparent}
ul.items li:hover{background:#ebe7dc}
ul.items li.done{color:#888}
ul.items li.done .t:before{content:"\2713  "}
ul.items li.sel{background:#fff;border-color:#c0392b}
ul.items .h{font-size:12px;color:#777}
details{margin:6px 0;font-size:13px}
details summary{cursor:pointer;font-weight:600}
details p{margin:4px 0}
kbd{background:#fff;border:1px solid #bbb;border-radius:3px;padding:0 4px;font-size:12px}
#work{margin-top:10px;padding:8px;background:#fff;border:1px solid #bbb;border-radius:4px}
#work .step{font-weight:600;margin-bottom:4px}
.shows button{display:inline-block}
.small{font-size:12px;color:#666}
</style></head><body>
<div id="panel">
  <h1>Label the map: <span id="mtitle"></span></h1>
  <div class="sub" id="msub"></div>
  <div><button id="b-turn">Turn 180&deg;</button><button id="b-save">Save</button><button id="b-load">Load</button><button id="b-reset" class="danger">Start from the saved file</button></div>
  <input type="file" id="fileinput" accept=".json,application/json" style="display:none">
  <details id="help"><summary>How to use this page</summary>
    <p><b>1.</b> Click the place's symbol on the map (a quick click; dragging still moves the map). <kbd>N</kbd> means the map has no symbol there.</p>
    <p><b>2.</b> Trace along the baseline of the letters (the line they stand on), in reading order: click its start, each bend, and double-click its end (or press <kbd>Enter</kbd>). The band covers the letters above it and a little below for descenders; <kbd>[</kbd> and <kbd>]</kbd> make it taller or shorter. <kbd>Backspace</kbd> removes the last point; <kbd>S</kbd> skips the trace. The picture of the name is cut along the band, so make it reach the tops of the letters, flourishes included. A finished label's band is changed the same way: select it and press <kbd>[</kbd> or <kbd>]</kbd>.</p>
    <p>Trace each name in the order you read it, even when it is upside down; that is what makes its picture come out upright.</p>
    <p>A name on two lines: trace the first line, then click the start of the second and go on; or press <kbd>L</kbd> before clicking the second line's start.</p>
    <p><b>3.</b> Say what the map shows here: <kbd>1</kbd> village, <kbd>2</kbd> Olęder settlement, <kbd>3</kbd> folwark or manor, <kbd>4</kbd> tavern, <kbd>5</kbd> water mill, <kbd>6</kbd> windmill, <kbd>7</kbd> forest, <kbd>8</kbd> field or meadow, <kbd>9</kbd> water, <kbd>0</kbd> road or crossing, <kbd>-</kbd> church, <kbd>=</kbd> other, <kbd>U</kbd> unsure. Choosing saves the label and moves to the next place.</p>
    <p><kbd>Esc</kbd> cancels the step in progress. <kbd>,</kbd> and <kbd>.</kbd> turn the map by 90&deg;. Click a ticked item, or a mark on the map, to look at a label again.</p>
    <p>Your work is kept in this browser as you go. Press <b>Save</b> to download a file to bring into the edition.</p>
  </details>
  <div id="status"></div>
  <div id="counter"></div>
  <h2>To find</h2><ul class="items" id="find"></ul>
  <h2>Other labels</h2><ul class="items" id="other"></ul>
  <button id="b-new">+ New label</button>
  <div id="work" style="display:none"></div>
  <datalist id="placelist"></datalist>
</div>
<div id="viewer"></div>
<canvas id="overlay"></canvas>
<script src="../vendor/openseadragon.min.js"></script>
<script>
"use strict";
var DATA = /*DATA*/null;
var M = DATA.map, KEY = M.key;
var SHOWS = [["1","village","Village"],["2","oleder-settlement","Olęder settlement"],["3","folwark","Folwark or manor"],
  ["4","tavern","Tavern"],["5","water-mill","Water mill"],["6","windmill","Windmill"],["7","forest","Forest"],
  ["8","field","Field or meadow"],["9","water","Water"],["0","road","Road or crossing"],["-","church","Church"],
  ["=","other","Other"],["u","unsure","Unsure"]];
var LSKEY = "maplabels:" + KEY;

var labels = [];      // saved labels
var cur = null;       // the label being worked on (a draft, or an existing label)
var isDraft = false;
var step = null;      // 'point' | 'trace' | 'shows' | null
var tmp = [];         // trace being drawn
var tmpPx = [];       // screen positions of those clicks
var tmpBreaks = [];   // indices into tmp where a new line starts (key L)
var pendingBreak = false; // L pressed: the next click starts a new line
var placeMap = {};    // datalist string -> slug
var headingOf = {};

function $(id){return document.getElementById(id);}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
function rnd(v){return Math.round(v);}
function resetTmp(){ tmp=[]; tmpPx=[]; tmpBreaks=[]; pendingBreak=false; }

// Mirrors split_lines in pipeline/maps/import_labels.py exactly.
function splitLines(trace,breaks){
  var n=trace?trace.length:0, starts=[], i;
  if(!n) return [];
  if(breaks&&breaks.length){
    var seen={};
    breaks.forEach(function(b){ b=Math.round(b); if(b>0&&b<n&&!seen[b]){seen[b]=1;starts.push(b);} });
    starts.sort(function(a,b){return a-b;});
  } else if(n>2){
    var sx=trace[1][0]-trace[0][0], sy=trace[1][1]-trace[0][1];
    for(var k=1;k<n-1;k++){
      var dx=trace[k+1][0]-trace[k][0], dy=trace[k+1][1]-trace[k][1];
      if(dx*sx+dy*sy<0) starts.push(k+1);
    }
  }
  var lines=[], prev=0;
  starts.concat([n]).forEach(function(s){ lines.push(trace.slice(prev,s)); prev=s; });
  return lines;
}

// ---------- storage ----------
function normLabel(l){
  var o={id:l.id, place:l.place||null, new_place:l.new_place||null, form:l.form||"",
    point:l.point?[rnd(l.point[0]),rnd(l.point[1])]:null,
    trace:(l.trace&&l.trace.length)?l.trace.map(function(p){return [rnd(p[0]),rnd(p[1])];}):null};
  if(o.trace&&l.breaks&&l.breaks.length) o.breaks=l.breaks.map(rnd);
  o.height=rnd(l.height||80); o.shows=l.shows||"unsure"; o.note=l.note||null;
  return o;
}
function payload(){
  return {map:KEY,width:M.width,height:M.height,saved:new Date().toISOString(),labels:labels.map(normLabel)};
}
function persist(){
  try{localStorage.setItem(LSKEY,JSON.stringify(payload()));}catch(e){}
}
function loadInitial(){
  var got=null;
  try{var s=localStorage.getItem(LSKEY); if(s){got=JSON.parse(s).labels;}}catch(e){}
  if(!got) got=DATA.labels||[];
  labels=got.map(normLabel);
}

// ---------- assignments: which label satisfies which to-find item ----------
function assign(){
  var byPlace={}, used={};
  labels.forEach(function(l){ if(l.place){(byPlace[l.place]=byPlace[l.place]||[]).push(l);} });
  var seen={}, items=[];
  DATA.find.forEach(function(it,i){
    var n=seen[it.place]||0; seen[it.place]=n+1;
    var l=(byPlace[it.place]||[])[n]||null;
    if(l) used[l.id]=true;
    items.push({item:it,index:i,label:l});
  });
  var other=labels.filter(function(l){return !used[l.id];});
  return {items:items,other:other};
}
function nextFree(){
  var mx=0;
  labels.concat(cur&&isDraft?[cur]:[]).forEach(function(l){
    var m=/-(\d+)$/.exec(l.id||""); if(m) mx=Math.max(mx,parseInt(m[1],10));
  });
  var n=String(mx+1); while(n.length<3) n="0"+n;
  return KEY+"-"+n;
}

// ---------- viewer ----------
var viewer=OpenSeadragon({
  id:"viewer", prefixUrl:"", showNavigationControl:false, tileSources:M.tiles,
  gestureSettingsMouse:{clickToZoom:false,dblClickToZoom:false},
  crossOriginPolicy:"Anonymous", maxZoomPixelRatio:4, visibilityRatio:0.5, animationTime:0.6
});
var canvas=$("overlay"), ctx=canvas.getContext("2d");
viewer.addHandler("open",function(){
  viewer.viewport.setRotation(M.view_rotation||0,true);
  draw();
});
viewer.addHandler("open-failed",function(e){
  setStatus("The map tiles did not load ("+esc(e.message||"")+"). Is the tile server published and this page opened through http://localhost:8765/ ?",true);
});
["animation","update-viewport","resize","rotate","open"].forEach(function(ev){viewer.addHandler(ev,draw);});
window.addEventListener("resize",function(){sizeCanvas();draw();});

function sizeCanvas(){
  var r=$("viewer").getBoundingClientRect(), dpr=window.devicePixelRatio||1;
  canvas.style.width=r.width+"px"; canvas.style.height=r.height+"px";
  canvas.style.left=r.left+"px"; canvas.style.top=r.top+"px";
  canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
function i2s(p){
  var q=viewer.viewport.imageToViewerElementCoordinates(new OpenSeadragon.Point(p[0],p[1]));
  return [q.x,q.y];
}
function s2i(pos){
  var q=viewer.viewport.viewerElementToImageCoordinates(pos);
  return [rnd(q.x),rnd(q.y)];
}
var DESC=0.35; // descenders: the band reaches DESC*height below the baseline
// "up" of a line of the trace, in image pixels (y down): for the unit reading
// direction d=(dx,dy) from the line's first to its last point, up=(dy,-dx).
function upOf(ln){
  if(!ln||ln.length<2) return [0,-1];
  var dx=ln[ln.length-1][0]-ln[0][0], dy=ln[ln.length-1][1]-ln[0][1], L=Math.hypot(dx,dy);
  return L?[dy/L,-dx/L]:[0,-1];
}
function traceOf(l){ return (l===cur && step==="trace") ? tmp : l.trace; }
function linesOf(l){ return (l===cur && step==="trace") ? splitLines(tmp,tmpBreaks) : splitLines(l.trace,l.breaks); }

function drawLabel(l,selected){
  var tr=traceOf(l);
  var col=selected?"192,57,43":"220,60,50";
  if(tr&&tr.length){
    ctx.lineJoin="round"; ctx.lineCap="round";
    var lines=linesOf(l), prevEnd=null;
    lines.forEach(function(ln){
      var pts=ln.map(i2s);
      if(prevEnd){ // the jump to the next line: a thin dotted grey line only
        ctx.save(); ctx.setLineDash([3,5]); ctx.strokeStyle="rgba(120,120,120,.9)"; ctx.lineWidth=1;
        ctx.beginPath(); ctx.moveTo(prevEnd[0],prevEnd[1]); ctx.lineTo(pts[0][0],pts[0][1]); ctx.stroke(); ctx.restore();
      }
      var H=l.height||80, up=upOf(ln);
      if(ln.length>=2){ // the band: H above the baseline, DESC*H below, SIDE*H beyond each end; offset in image pixels
        var rd=[-up[1],up[0]]; // reading direction, from the first point towards the last
        var SIDE=0.4*H, bp=ln.map(function(p){return [p[0],p[1]];});
        bp[0]=[bp[0][0]-SIDE*rd[0],bp[0][1]-SIDE*rd[1]];
        var lp=ln[ln.length-1]; bp[bp.length-1]=[lp[0]+SIDE*rd[0],lp[1]+SIDE*rd[1]];
        var top=bp.map(function(p){return i2s([p[0]+H*up[0],p[1]+H*up[1]]);});
        var bot=bp.map(function(p){return i2s([p[0]-DESC*H*up[0],p[1]-DESC*H*up[1]]);});
        ctx.beginPath(); top.forEach(function(p,i){i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]);});
        for(var j=bot.length-1;j>=0;j--) ctx.lineTo(bot[j][0],bot[j][1]);
        ctx.closePath(); ctx.fillStyle="rgba("+col+","+(selected?0.30:0.16)+")"; ctx.fill();
      }
      ctx.beginPath(); pts.forEach(function(p,i){i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]);});
      ctx.strokeStyle=selected?"rgb(255,40,20)":"rgb(220,50,40)"; ctx.lineWidth=2; ctx.stroke();
      if(selected){ ctx.fillStyle="#fff"; pts.forEach(function(p){ctx.beginPath();ctx.arc(p[0],p[1],3,0,7);ctx.fill();ctx.strokeStyle="#c0392b";ctx.lineWidth=1;ctx.stroke();}); }
      prevEnd=pts[pts.length-1];
    });
  }
  var anchor=null;
  if(l.point){
    var s=i2s(l.point); anchor=s;
    ctx.beginPath(); ctx.arc(s[0],s[1],6,0,7);
    ctx.fillStyle=selected?"#ff2a14":"#d63b2f"; ctx.fill();
    ctx.strokeStyle="#fff"; ctx.lineWidth=selected?2:1; ctx.stroke();
  } else if(tr&&tr.length){ anchor=i2s(tr[0]); }
  if(!selected && l.form && anchor){
    ctx.font="12px system-ui,Arial"; ctx.lineWidth=3; ctx.strokeStyle="rgba(255,255,255,.9)";
    ctx.strokeText(l.form,anchor[0]+9,anchor[1]-8); ctx.fillStyle="#a01a10"; ctx.fillText(l.form,anchor[0]+9,anchor[1]-8);
  }
}
function draw(){
  if(!canvas.width) sizeCanvas();
  var r=canvas.getBoundingClientRect();
  ctx.clearRect(0,0,r.width,r.height);
  if(!viewer.world||!viewer.world.getItemCount()) return;
  labels.forEach(function(l){ if(l!==cur) drawLabel(l,false); });
  if(cur) drawLabel(cur,true);
}

// ---------- status ----------
function setStatus(t,bad){ var s=$("status"); s.innerHTML=t; s.style.background=bad?"#fde0dc":"#fff8d8"; }
function stepText(){
  var who=cur?("<b>"+esc(cur.form||curHeading()||"new label")+"</b>: "):"";
  if(!cur) return "Choose a place from the list, or press + New label.";
  if(step==="point") return who+"Step 1 of 3. Click the place's symbol (<kbd>N</kbd> if there is none).";
  if(step==="trace") return who+"Step 2 of 3. Trace along the baseline of the letters (the line they stand on), in reading order: click its start, each bend, double-click its end (or Enter). The band covers the letters above it and a little below for descenders; <kbd>[</kbd> <kbd>]</kbd> make it taller or shorter ("+(cur.height||80)+"). <kbd>L</kbd> starts the next line of a two-line name; <kbd>S</kbd> skips.";
  if(step==="shows") return who+"Step 3 of 3. What does the map show here? Press a key or a button.";
  return who+"Saved. Use the buttons below to change it.";
}
function traceInfo(){
  var n=splitLines(tmp,tmpBreaks).length+(pendingBreak?1:0);
  return " ("+tmp.length+" points, line "+Math.max(1,n)+(pendingBreak?": click its start":"")+")";
}
function curHeading(){ return cur&&cur.place?headingOf[cur.place]:null; }

// ---------- panel ----------
function render(){
  var a=assign(), found=a.items.filter(function(x){return x.label;}).length;
  $("counter").textContent=found+" of "+a.items.length+" found"+(labels.length?" ("+labels.length+" labels in all)":"");
  var f=$("find"); f.innerHTML="";
  a.items.forEach(function(x){
    var li=document.createElement("li");
    var isSel=cur&&((x.label&&x.label===cur)||(!x.label&&isDraft&&cur.fromItem===x.index));
    li.className=(x.label?"done ":"")+(isSel?"sel":"");
    li.innerHTML='<div class="t">'+esc(x.item.form||x.item.heading)+'</div><div class="h">'+esc(x.item.heading)+(x.item.note?" - "+esc(x.item.note):"")+'</div>';
    li.onclick=function(){ x.label?selectLabel(x.label):startItem(x.index); };
    f.appendChild(li);
  });
  var o=$("other"); o.innerHTML="";
  if(!a.other.length){o.innerHTML='<li class="h" style="cursor:default">none yet</li>';}
  a.other.forEach(function(l){
    var li=document.createElement("li"); li.className="done"+(cur===l?" sel":"");
    li.innerHTML='<div class="t">'+esc(l.form||"(no form)")+'</div><div class="h">'+esc(l.place?headingOf[l.place]:(l.new_place?"new place: "+l.new_place:"no place"))+'</div>';
    li.onclick=function(){selectLabel(l);};
    o.appendChild(li);
  });
  setStatus(stepText());
  renderWork();
  draw();
}
function renderWork(){
  var w=$("work");
  if(!cur){w.style.display="none";return;}
  w.style.display="block";
  var h='';
  if(isDraft && !cur.fromItem && cur.fromItem!==0){
    h+='<label class="f">Place (type to search the gazetteer)</label><input id="f-place" list="placelist" value="'+esc(cur._placeText||"")+'" autocomplete="off">';
    h+='<div class="small" id="f-placeinfo">'+(cur.place?"Place chosen: <b>"+esc(headingOf[cur.place])+"</b>":"No gazetteer place chosen.")+'</div>';
    h+='<label class="f">New place (only if no place above fits)</label><input id="f-newplace" value="'+esc(cur.new_place||"")+'">';
  } else {
    h+='<div class="small">Place: <b>'+esc(cur.place?headingOf[cur.place]:(cur.new_place||"none"))+'</b></div>';
  }
  h+='<label class="f">Form as written on the map</label><input id="f-form" value="'+esc(cur.form)+'">';
  if(step==="shows"){
    h+='<div class="step">What does the map show here?</div><div class="shows">';
    SHOWS.forEach(function(s){ h+='<button data-shows="'+s[1]+'" class="'+(cur.shows===s[1]&&!isDraft?"on":"")+'">'+s[0].toUpperCase()+' '+esc(s[2])+'</button>'; });
    h+='</div>';
  }
  h+='<label class="f">Note (optional)</label><input id="f-note" value="'+esc(cur.note||"")+'">';
  if(!isDraft && step===null){
    h+='<div class="small">Shows: <b>'+esc(cur.shows)+'</b>; height '+cur.height+'</div>';
    h+='<div><button data-act="goto">Go to</button><button data-act="redopoint">Redo point</button><button data-act="redotrace">Redo trace</button><button data-act="redoshows">Change what it shows</button><button data-act="delete" class="danger">Delete label</button></div>';
  } else if(isDraft){
    h+='<div><button data-act="cancel">Cancel this label</button></div>';
  } else {
    h+='<div><button data-act="cancel">Cancel</button></div>';
  }
  w.innerHTML=h;
  var fp=$("f-place");
  if(fp){
    fp.oninput=function(){
      cur._placeText=fp.value;
      var slug=placeMap[fp.value]||null; cur.place=slug;
      $("f-placeinfo").innerHTML=slug?"Place chosen: <b>"+esc(headingOf[slug])+"</b>":"No gazetteer place chosen.";
      if(slug){ var ff=$("f-form"); var m=/^(.*) → /.exec(fp.value); var v=m?m[1]:headingOf[slug]; if(!ff.value||ff.dataset.auto){ff.value=v;ff.dataset.auto="1";cur.form=v;} }
    };
  }
  var nn=$("f-newplace"); if(nn) nn.oninput=function(){cur.new_place=nn.value||null;};
  var fm=$("f-form"); if(fm) fm.oninput=function(){cur.form=fm.value;fm.dataset.auto="";if(!isDraft)persist();};
  var nt=$("f-note"); if(nt) nt.oninput=function(){cur.note=nt.value||null;if(!isDraft)persist();};
  Array.prototype.forEach.call(w.querySelectorAll("button"),function(b){
    b.onclick=function(){
      b.blur();
      if(b.dataset.shows) chooseShows(b.dataset.shows);
      else act(b.dataset.act);
    };
  });
}

// ---------- the work ----------
function newDraft(base){
  cur=Object.assign({id:nextFree(),place:null,new_place:null,form:"",point:null,trace:null,height:80,shows:"unsure",note:null},base||{});
  isDraft=true; step="point"; resetTmp();
}
function startItem(i){
  var it=DATA.find[i];
  newDraft({place:it.place,form:it.form||it.heading,fromItem:i});
  render();
}
function startNew(){
  newDraft({}); cur.fromItem=null; render();
}
function selectLabel(l){
  cur=l; isDraft=false; step=null; resetTmp(); render();
}
function nextUndone(){
  var a=assign();
  for(var i=0;i<a.items.length;i++) if(!a.items[i].label) return i;
  return -1;
}
function finishDraft(){
  cur.id=nextFree();
  if(!cur.form) cur.form=cur.place?headingOf[cur.place]:(cur.new_place||"");
  delete cur.fromItem; delete cur._placeText;
  var l=normLabel(cur); labels.push(l); persist();
  cur=null; isDraft=false; step=null;
  var n=nextUndone();
  if(n>=0) startItem(n); else { render(); setStatus("Every place on the list has a label. Press Save to download the file.");}
}
function chooseShows(code){
  if(!cur||step!=="shows") return;
  cur.shows=code;
  if(isDraft){ finishDraft(); }
  else { step=null; persist(); render(); }
}
function setPoint(p){
  cur.point=p;
  if(isDraft){ step="trace"; resetTmp(); } else { step=null; persist(); }
  render();
}
function endTrace(){
  if(tmp.length<2){ setStatus("A trace needs at least two points (start and end). Click more points, or press S to skip.",true); return; }
  cur.trace=tmp.map(function(p){return [p[0],p[1]];});
  var br=tmpBreaks.filter(function(i){return i>0&&i<tmp.length;});
  if(br.length) cur.breaks=br; else delete cur.breaks;
  resetTmp();
  if(isDraft){ step="shows"; } else { step=null; persist(); }
  render();
}
function skipTrace(){
  cur.trace=null; delete cur.breaks; resetTmp();
  if(isDraft){ step="shows"; } else { step=null; persist(); }
  render();
}
function cancelStep(){
  if(!cur) return;
  if(step==="trace" && tmp.length){ resetTmp(); render(); return; }
  if(isDraft){ cur=null; isDraft=false; step=null; resetTmp(); render(); return; }
  step=null; resetTmp(); render();
}
function act(a){
  if(a==="cancel") cancelStep();
  else if(a==="goto") goTo(cur);
  else if(a==="redopoint"){step="point";render();}
  else if(a==="redotrace"){step="trace";resetTmp();render();}
  else if(a==="redoshows"){step="shows";render();}
  else if(a==="delete"){
    if(confirm("Delete the label \""+cur.form+"\"?")){
      labels=labels.filter(function(l){return l!==cur;}); cur=null; step=null; persist(); render();
    }
  }
}
function goTo(l){
  var pts=[]; if(l.point) pts.push(l.point); if(l.trace) pts=pts.concat(l.trace);
  if(!pts.length){setStatus("This label has no point or trace to go to.",true);return;}
  var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  pts.forEach(function(p){x0=Math.min(x0,p[0]);y0=Math.min(y0,p[1]);x1=Math.max(x1,p[0]);y1=Math.max(y1,p[1]);});
  var pad=Math.max(150,(l.height||80)*3);
  x0-=pad;y0-=pad;x1+=pad;y1+=pad;
  viewer.viewport.fitBounds(viewer.viewport.imageToViewportRectangle(x0,y0,x1-x0,y1-y0));
}

// ---------- map events ----------
function hit(pos){
  var best=null,bd=14;
  labels.forEach(function(l){
    var d=1e9;
    if(l.point){var s=i2s(l.point);d=Math.min(d,Math.hypot(s[0]-pos.x,s[1]-pos.y));}
    if(l.trace&&l.trace.length){
      var P=l.trace.map(i2s);
      for(var i=0;i<P.length;i++){
        d=Math.min(d,Math.hypot(P[i][0]-pos.x,P[i][1]-pos.y));
        if(i){d=Math.min(d,segDist(pos,P[i-1],P[i]));}
      }
    }
    if(d<bd){bd=d;best=l;}
  });
  return best;
}
function segDist(p,a,b){
  var dx=b[0]-a[0],dy=b[1]-a[1],L=dx*dx+dy*dy;
  var t=L?Math.max(0,Math.min(1,((p.x-a[0])*dx+(p.y-a[1])*dy)/L)):0;
  return Math.hypot(p.x-(a[0]+t*dx),p.y-(a[1]+t*dy));
}
viewer.addHandler("canvas-click",function(e){
  if(!e.quick) return;
  e.preventDefaultAction=true;
  if(cur&&step==="point"){ setPoint(s2i(e.position)); }
  else if(cur&&step==="trace"){
    if(pendingBreak){ if(tmp.length) tmpBreaks.push(tmp.length); pendingBreak=false; }
    tmp.push(s2i(e.position)); tmpPx.push([e.position.x,e.position.y]); draw(); setStatus(stepText()+traceInfo());
  } else if(!cur||step===null){
    var l=hit(e.position); if(l) selectLabel(l);
  }
});
viewer.addHandler("canvas-double-click",function(e){
  e.preventDefaultAction=true;
  if(cur&&step==="trace"){
    // the two clicks of the double-click each added a point at the same place: keep one
    if(tmpPx.length){
      var q=tmpPx[tmpPx.length-1];
      if(Math.hypot(q[0]-e.position.x,q[1]-e.position.y)<10 && tmp.length>=1){ tmp.pop(); tmpPx.pop(); }
    }
    if(pendingBreak){ if(tmp.length) tmpBreaks.push(tmp.length); pendingBreak=false; }
    tmp.push(s2i(e.position)); tmpPx.push([e.position.x,e.position.y]);
    // a repeated point from the second click: drop exact duplicates at the end
    while(tmp.length>1 && tmp[tmp.length-1][0]===tmp[tmp.length-2][0] && tmp[tmp.length-1][1]===tmp[tmp.length-2][1]){tmp.pop();tmpPx.pop();}
    endTrace();
  }
});

document.addEventListener("keydown",function(e){
  var t=e.target, tag=t&&t.tagName;
  if(tag==="INPUT"||tag==="TEXTAREA"||tag==="SELECT") return;
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  var k=e.key, lk=k.length===1?k.toLowerCase():k;
  if(k===","){rotateBy(-90);return;}
  if(k==="."){rotateBy(90);return;}
  if(k==="Escape"){cancelStep();return;}
  if(!cur) return;
  if(k==="["||k==="]"){
    cur.height=Math.max(10,(cur.height||80)+(k==="]"?20:-20));
    if(!isDraft)persist(); setStatus(stepText()); draw(); return;
  }
  if(step==="point"&&lk==="n"){setPoint(null);return;}
  if(step==="trace"){
    if(k==="Enter"){e.preventDefault();endTrace();return;}
    if(k==="Backspace"){
      e.preventDefault();
      if(pendingBreak){pendingBreak=false;}
      else if(tmp.length){
        tmp.pop(); tmpPx.pop();
        tmpBreaks=tmpBreaks.filter(function(i){return i!==tmp.length;});
      }
      draw(); setStatus(stepText()+traceInfo()); return;
    }
    if(lk==="l"){
      if(tmp.length){ pendingBreak=true; setStatus(stepText()+traceInfo()); }
      return;
    }
    if(lk==="s"){skipTrace();return;}
  }
  if(step==="shows"){
    for(var i=0;i<SHOWS.length;i++) if(SHOWS[i][0]===lk){chooseShows(SHOWS[i][1]);return;}
  }
});
function rotateBy(d){ viewer.viewport.setRotation(viewer.viewport.getRotation()+d); }

// ---------- buttons ----------
document.addEventListener("click",function(e){ if(e.target.tagName==="BUTTON") e.target.blur(); });
$("b-turn").onclick=function(){rotateBy(180);};
$("b-new").onclick=startNew;
function stamp(){
  var d=new Date(),p=function(n){return (n<10?"0":"")+n;};
  return d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+"-"+p(d.getHours())+p(d.getMinutes());
}
$("b-save").onclick=function(){
  var blob=new Blob([JSON.stringify(payload(),null,1)],{type:"application/json"});
  var a=document.createElement("a"); a.href=URL.createObjectURL(blob);
  a.download="labels_"+KEY+"_"+stamp()+".json"; document.body.appendChild(a); a.click();
  setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);
  setStatus("Downloaded "+esc(a.download)+" (to your Downloads folder).");
};
$("b-load").onclick=function(){$("fileinput").click();};
$("fileinput").onchange=function(){
  var f=this.files[0]; if(!f) return; var inp=this;
  var r=new FileReader();
  r.onload=function(){
    try{
      var d=JSON.parse(r.result); var L=Array.isArray(d)?d:d.labels;
      if(!L) throw new Error("no labels");
      if(d.map&&d.map!==KEY&&!confirm("This file is for the map "+d.map+", not "+KEY+". Load it anyway?")) return;
      if(labels.length&&!confirm("Replace the "+labels.length+" labels now on the page with the "+L.length+" in the file?")) return;
      labels=L.map(normLabel); cur=null; step=null; persist(); afterLoad();
    }catch(err){ setStatus("That file could not be read: "+esc(err.message),true); }
    inp.value="";
  };
  r.readAsText(f);
};
$("b-reset").onclick=function(){
  if(!confirm("Discard what this browser has kept and start again from the file the page was made with?")) return;
  try{localStorage.removeItem(LSKEY);}catch(e){}
  labels=(DATA.labels||[]).map(normLabel); cur=null; step=null; afterLoad();
};
function afterLoad(){
  var n=nextUndone(); if(n>=0) startItem(n); else render();
}

// ---------- start ----------
(function init(){
  $("mtitle").textContent=M.cited_as;
  $("msub").textContent=M.title+" ("+M.width+" × "+M.height+" px)";
  var dl=$("placelist");
  DATA.places.forEach(function(p){
    headingOf[p.slug]=p.heading;
    var add=function(s){ if(!(s in placeMap)){placeMap[s]=p.slug; var o=document.createElement("option"); o.value=s; dl.appendChild(o);} };
    add(p.heading);
    p.forms.forEach(function(f){ if(f!==p.heading) add(f+" → "+p.heading); });
  });
  loadInitial();
  sizeCanvas();
  afterLoad();
})();
</script></body></html>
"""

if __name__ == "__main__":
    main()
