(()=>{"use strict";
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const lang=(document.documentElement.lang||"en").slice(0,2);
const detailsOpen=new URLSearchParams(location.search).get("view")==="details"; if(detailsOpen)document.body.classList.add("myv2-details-open");
$("[data-myv2-details], a[href=\"#tour-details\"]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();document.body.classList.add("myv2-details-open");history.replaceState(null,"",location.pathname+"?view=details#tour-details");scrollTo({top:0,behavior:"smooth"});}));
const copy={en:"Book Now",ru:"Забронировать",de:"Jetzt buchen",tr:"Rezervasyon",uk:"Забронювати",sr:"Rezerviši"};
const label=copy[lang]||copy.en;
const book=$("#book-now"), form=book&&$(".book-form",book);
if(!book||!form)return;
const marker=document.createComment("myv2-book-form-home");
form.parentNode.insertBefore(marker,form);
const modal=document.createElement("div"); modal.className="myv2-modal"; modal.setAttribute("role","dialog"); modal.setAttribute("aria-modal","true"); modal.setAttribute("aria-label",label);
modal.innerHTML='<div class="myv2-modal-card"><button class="myv2-modal-close" type="button" aria-label="Close">×</button><div class="myv2-modal-slot"></div></div>';
document.body.appendChild(modal);
const sticky=document.createElement("button"); sticky.type="button"; sticky.className="myv2-sticky-book"; sticky.textContent=label; document.body.appendChild(sticky);
let lastFocus=null;
function track(name,params={}){try{if(typeof window.gtag==="function")window.gtag("event",name,params)}catch(e){}}
function open(source){lastFocus=document.activeElement;$(".myv2-modal-slot",modal).appendChild(form);modal.classList.add("open");document.body.classList.add("myv2-modal-open");$(".myv2-modal-close",modal).focus();track("booking_open",{source:source||"unknown",page_path:location.pathname});}
function close(){if(marker.parentNode)marker.parentNode.insertBefore(form,marker.nextSibling);modal.classList.remove("open");document.body.classList.remove("myv2-modal-open");if(lastFocus&&lastFocus.focus)lastFocus.focus();}
sticky.addEventListener("click",()=>{track("book_now_click",{source:"sticky",page_path:location.pathname});open("sticky")});
$$('a[href="#book-now"]').forEach(a=>a.addEventListener("click",e=>{e.preventDefault();track("book_now_click",{source:"inline",page_path:location.pathname});open("inline")}));
$(".myv2-modal-close",modal).addEventListener("click",close);modal.addEventListener("click",e=>{if(e.target===modal)close()});document.addEventListener("keydown",e=>{if(e.key==="Escape"&&modal.classList.contains("open"))close()});
const submit=$(".btn-book",form);if(submit)submit.addEventListener("click",()=>track("booking_submit",{page_path:location.pathname,tour:document.body.dataset.tourId||""}));
const hdr=$(".site-header");if(hdr){const sync=()=>hdr.classList.toggle("scrolled",scrollY>18);sync();addEventListener("scroll",sync,{passive:true});}
})();