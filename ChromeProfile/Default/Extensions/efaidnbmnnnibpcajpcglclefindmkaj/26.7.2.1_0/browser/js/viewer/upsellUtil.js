/*************************************************************************
* ADOBE CONFIDENTIAL
* ___________________
*
*  Copyright 2015 Adobe Systems Incorporated
*  All Rights Reserved.
*
* NOTICE:  All information contained herein is, and remains
* the property of Adobe Systems Incorporated and its suppliers,
* if any.  The intellectual and technical concepts contained
* herein are proprietary to Adobe Systems Incorporated and its
* suppliers and are protected by all applicable intellectual property laws,
* including trade secret and or copyright laws.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Adobe Systems Incorporated.
**************************************************************************/
import{dcLocalStorage as e}from"../../../common/local-storage.js";import{getFloodgateFlag as t}from"../../../common/util.js";import{loggingApi as n}from"../../../common/loggingApi.js";import{CACHE_PURGE_SCHEME as o}from"../../../sw_modules/constant.js";const r="dc-cv-upsell-popup-metadata",i=85,a=95;export async function getUpsellPopupDimensions(){const e={widthPercent:i,heightPercent:a};try{if(!await t(r,o.NO_CALL))return e;const n=await chrome.runtime.sendMessage({main_op:"getFloodgateMeta",flag:r});if(!n)return e;const i=JSON.parse(n);return{widthPercent:i.widthPercent??e.widthPercent,heightPercent:i.heightPercent??e.heightPercent}}catch(t){return e}}export async function openUpsellPopupWindow(t,o,r,i){const{widthPercent:a,heightPercent:s}=await getUpsellPopupDimensions(),w=Math.round(window.outerWidth*(a/100)),c=Math.round(window.innerHeight*(s/100)),p=window.outerHeight-window.innerHeight,d=Math.round(window.screenX+(window.outerWidth-w)/2),l=Math.round(window.screenY+p+(window.innerHeight-c)/2);try{const a=await chrome.windows.create({url:t,type:"popup",width:w,height:c,left:d,top:l});if("number"!=typeof a?.id)return void n.error({message:"[Paywall] Popup window creation failed — chrome.windows.create returned no id",redirectionStartTime:i});const s=e.getItem("upsellSessions")||{};s[o]={...s[o],popupWindow:a,openedAt:Date.now(),...i&&{redirectionStartTime:i}},e.setItem("upsellSessions",s),r&&r(a)}catch(e){n.error({message:"[Paywall] Popup window creation failed — chrome.windows.create returned no id",redirectionStartTime:i,error:e?.message||String(e)})}}export function logPaywallOpening(e,t,o){const r=Date.now();n.info({message:"[Paywall] Perf: opening paywall",redirectionStartTime:e,openingAt:r,durationMs:r-e,paywallType:t}),o("DCBrowserExt:Viewer:Paywall:Opening")}