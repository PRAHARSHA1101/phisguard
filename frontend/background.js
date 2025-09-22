const API_URL="http://localhost:8000/predict";

chrome.webNavigation.onBeforeNavigate.addListener(async (d)=>{
  if(d.frameId!==0) return;
  if(!d.url.startsWith("http")) return;
  try{
    const r=await fetch(API_URL,{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({url:d.url})
    });
    const j=await r.json();
    if(j.label==="phishing"){
      chrome.tabs.update(d.tabId,{url:chrome.runtime.getURL("warning.html")+"?u="+encodeURIComponent(d.url)+"&s="+j.score});
    }
  }catch(e){console.error("API fail",e);}
},{url:[{schemes:["http","https"]}]});
