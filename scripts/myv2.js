(()=>{"use strict";
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const lang=(document.documentElement.lang||"en").slice(0,2);
const words={
 en:{back:"Back to tour",book:"Book this tour",from:"from / per person"},
 de:{back:"Zurück zur Tour",book:"Diese Tour buchen",from:"ab / pro Person"},
 ru:{back:"Назад к туру",book:"Забронировать тур",from:"от / за человека"},
 tr:{back:"Tura dön",book:"Bu turu rezerve et",from:"başlangıç / kişi başı"},
 uk:{back:"Назад до туру",book:"Забронювати тур",from:"від / за особу"},
 sr:{back:"Nazad na turu",book:"Rezerviši ovaj izlet",from:"od / po osobi"}
};
const w=words[lang]||words.en;
let moved=[];

function track(name,params={}){try{if(typeof window.gtag==="function")window.gtag("event",name,params)}catch(_){}}
function tourData(){
 const id=(document.body.dataset.tourId||"").toLowerCase();
 const all=window.MYV_TOURS?Object.values(window.MYV_TOURS):[];
 return all.find(t=>(t.id||"").toLowerCase()===id)||all.find(t=>id==="green-canyon"&&t.id==="green-canyon")||null;
}
function priceInfo(){
 const t=tourData(); if(!t||!t.packages)return {price:"",note:w.from};
 const adults=Object.values(t.packages).map(p=>Number(p.adult)).filter(Number.isFinite);
 return {price:adults.length?"€"+Math.min(...adults):"",note:w.from};
}
function cleanText(el){return el?(el.textContent||"").replace(/\s+/g," ").trim():"";}
function findDuration(){
 const candidates=$$(".price-features li, .price-card li, #tour-details li");
 const d=candidates.map(cleanText).find(x=>/day|night|tag|nacht|дн|ноч|gün|gece|dan|noć|день|ніч/i.test(x));
 return d||((tourData()&&tourData().duration)||"");
}

function setupBooking(){
 const book=$("#book-now"), form=book&&$(".book-form",book);
 if(!book||!form)return {open:()=>{}};
 const marker=document.createComment("myv2-book-form-home");
 form.parentNode.insertBefore(marker,form);
 const modal=document.createElement("div");
 modal.className="myv2-modal";modal.setAttribute("role","dialog");modal.setAttribute("aria-modal","true");modal.setAttribute("aria-label",w.book);
 modal.innerHTML='<div class="myv2-modal-card"><button class="myv2-modal-close" type="button" aria-label="Close">×</button><div class="myv2-modal-slot"></div></div>';
 document.body.appendChild(modal);
 let lastFocus=null;
 const open=(source)=>{
  lastFocus=document.activeElement;
  $(".myv2-modal-slot",modal).appendChild(form);
  modal.classList.add("open");document.body.classList.add("myv2-modal-open");
  $(".myv2-modal-close",modal).focus();
  track("booking_open",{source:source||"unknown",page_path:location.pathname});
 };
 const close=()=>{
  if(marker.parentNode)marker.parentNode.insertBefore(form,marker.nextSibling);
  modal.classList.remove("open");document.body.classList.remove("myv2-modal-open");
  if(lastFocus&&lastFocus.focus)lastFocus.focus();
 };
 $(".myv2-modal-close",modal).addEventListener("click",close);
 modal.addEventListener("click",e=>{if(e.target===modal)close()});
 document.addEventListener("keydown",e=>{if(e.key==="Escape"&&modal.classList.contains("open"))close()});
 $$('a[href="#book-now"],a[href$="#book-now"],button[data-book-now]').forEach(a=>a.addEventListener("click",e=>{
  e.preventDefault();track("book_now_click",{source:"inline",page_path:location.pathname});open("inline");
 }));
 const submit=$(".btn-book",form);
 if(submit)submit.addEventListener("click",()=>track("booking_submit",{page_path:location.pathname,tour:document.body.dataset.tourId||""}));
 return {open,close};
}

function buildShell(booking){
 const hero=$("#home"), img=$(".hero-bg-img",hero), title=$(".hero-title",hero), badge=$(".hero-badge",hero), sub=$(".hero-sub",hero);
 if(!hero||!img||!title)return null;
 const p=priceInfo();
 const shell=document.createElement("main");shell.className="myv2-detail-shell";shell.id="myv2-detail-view";
 const media=document.createElement("aside");media.className="myv2-detail-media";
 const pic=document.createElement("img");pic.src=img.currentSrc||img.src;pic.alt=img.alt||cleanText(title);pic.decoding="async";
 media.appendChild(pic);
 if(p.price){
  const pb=document.createElement("div");pb.className="myv2-detail-price";
  pb.innerHTML="<strong></strong><span></span>";
  $("strong",pb).textContent=p.price;$("span",pb).textContent=p.note;media.appendChild(pb);
 }
 const panel=document.createElement("div");panel.className="myv2-detail-panel";
 const back=document.createElement("button");back.type="button";back.className="myv2-detail-back";back.innerHTML="← <span></span>";$("span",back).textContent=w.back;
 const tag=document.createElement("p");tag.className="myv2-detail-tag";tag.textContent=cleanText(badge);
 const h=document.createElement("h1");h.className="myv2-detail-title";h.textContent=cleanText(title);
 const dur=document.createElement("p");dur.className="myv2-detail-duration";dur.innerHTML="<b>◷</b><span></span>";$("span",dur).textContent=findDuration();
 const bookBtn=document.createElement("button");bookBtn.type="button";bookBtn.className="myv2-detail-book";bookBtn.textContent=w.book;
 const rule=document.createElement("div");rule.className="myv2-detail-rule";
 const intro=document.createElement("p");intro.className="myv2-detail-intro";intro.textContent=cleanText(sub);
 const content=document.createElement("div");content.className="myv2-detail-content";
 panel.append(back,tag,h,dur,bookBtn,rule,intro,content);
 shell.append(media,panel);
 const bar=document.createElement("div");bar.className="myv2-detail-bar";
 const bt=document.createElement("span");bt.className="myv2-detail-bar-title";bt.textContent=cleanText(title)+(p.price?" — "+p.price:"");
 const bb=document.createElement("button");bb.type="button";bb.textContent=w.book;bar.append(bt,bb);
 document.body.append(shell,bar);
 back.addEventListener("click",()=>closeDetails(shell,bar));
 bookBtn.addEventListener("click",()=>{track("book_now_click",{source:"details",page_path:location.pathname});booking.open("details")});
 bb.addEventListener("click",()=>{track("book_now_click",{source:"details_bar",page_path:location.pathname});booking.open("details_bar")});
 return {shell,bar,content};
}

function moveSections(content){
 moved=[];
 ["#tour-details","#itinerary","#faq"].forEach(sel=>{
  const sec=$(sel);if(!sec)return;
  const ph=document.createComment("myv2-origin-"+sel.slice(1));
  sec.parentNode.insertBefore(ph,sec);moved.push({sec,ph});content.appendChild(sec);
 });
}
function restoreSections(){
 moved.forEach(({sec,ph})=>{if(ph.parentNode){ph.parentNode.insertBefore(sec,ph.nextSibling);ph.remove();}});
 moved=[];
}
function activateDetails(shellObj,replace=false){
 if(!shellObj)return;
 if(!shellObj.content.contains($("#tour-details")))moveSections(shellObj.content);
 document.body.classList.add("myv2-details-open");
 scrollTo(0,0);
 const u=location.pathname+"?view=details#tour-details";
 if(replace)history.replaceState({myv2:"details"},"",u);else history.pushState({myv2:"details"},"",u);
 track("tour_details_open",{page_path:location.pathname,tour:document.body.dataset.tourId||""});
}
function closeDetails(shell,bar){
 document.body.classList.remove("myv2-details-open","myv2-detail-scrolled");
 restoreSections();scrollTo(0,0);
 history.pushState({myv2:"landing"},"",location.pathname);
}
function bindDetails(shellObj){
 $$('a[data-myv2-details],a[href="#tour-details"],a[href*="?view=details"]').forEach(a=>{
  a.addEventListener("click",e=>{e.preventDefault();activateDetails(shellObj,false)});
 });
 addEventListener("popstate",()=>{
  const open=new URLSearchParams(location.search).get("view")==="details";
  if(open&&!document.body.classList.contains("myv2-details-open"))activateDetails(shellObj,true);
  if(!open&&document.body.classList.contains("myv2-details-open")){document.body.classList.remove("myv2-details-open","myv2-detail-scrolled");restoreSections();scrollTo(0,0);}
 });
}
function init(){
 const booking=setupBooking();
 const shellObj=buildShell(booking);
 bindDetails(shellObj);
 const hdr=$(".site-header");
 const sync=()=>{
  if(hdr)hdr.classList.toggle("scrolled",scrollY>18);
  document.body.classList.toggle("myv2-detail-scrolled",document.body.classList.contains("myv2-details-open")&&scrollY>320);
 };
 sync();addEventListener("scroll",sync,{passive:true});
 if(new URLSearchParams(location.search).get("view")==="details")activateDetails(shellObj,true);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>setTimeout(init,0));else setTimeout(init,0);
})();