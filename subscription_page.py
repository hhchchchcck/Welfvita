"""Production subscription profile page for RVG Gateway.

The page intentionally contains no external JavaScript framework so a copied
subscription URL remains fast, portable and usable on small mobile browsers.
Subscription clients continue to receive the normal base64 feed from main.py.
"""

from __future__ import annotations

import json


def get_public_page_html(
    uuid_key: str,
    subscription_type: str = "group",
    page_data: dict | None = None,
) -> str:
    """Return a 3x-ui-compatible browser profile for a group or single subscription.

    `page_data` follows the public `window.__SUB_PAGE_DATA__` contract used by
    3x-ui's SubPage.  This lets RVG render the same view model server-side while
    retaining a framework-free page suitable for its FastAPI architecture.
    """
    if subscription_type not in {"group", "single"}:
        raise ValueError("subscription_type must be 'group' or 'single'")
    page = r'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#17191f">
  <title>Subscription info · RVG Gateway</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
  <style>
    :root{
      color-scheme:dark;
      --page:#17191f;--surface:#202228;--surface-2:#25272e;--surface-3:#2d3038;
      --text:#f4f5f8;--text-2:#c5c8d0;--muted:#9297a4;--faint:#666b76;
      --border:#393d47;--border-soft:#2c2f37;--brand:#2375e8;--brand-hover:#3987ef;
      --brand-soft:rgba(35,117,232,.16);--green:#55c783;--green-soft:rgba(64,185,113,.15);
      --amber:#f0bb52;--amber-soft:rgba(240,187,82,.14);--red:#f07379;--red-soft:rgba(240,115,121,.14);
      --purple:#b99aff;--purple-soft:rgba(185,154,255,.14);--shadow:0 18px 46px rgba(0,0,0,.28);
      --radius:19px;--font:'Inter','Vazirmatn',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    }
    [data-theme="light"]{
      color-scheme:light;
      --page:#f1f3f7;--surface:#ffffff;--surface-2:#f8f9fc;--surface-3:#edf0f6;
      --text:#1b1f29;--text-2:#4f5665;--muted:#717989;--faint:#98a0ae;
      --border:#dce1ea;--border-soft:#e9ecf2;--brand:#1769d7;--brand-hover:#095cce;
      --brand-soft:rgba(23,105,215,.1);--green:#198754;--green-soft:rgba(25,135,84,.1);
      --amber:#ac7100;--amber-soft:rgba(172,113,0,.1);--red:#c9424d;--red-soft:rgba(201,66,77,.1);
      --purple:#7954cf;--purple-soft:rgba(121,84,207,.1);--shadow:0 18px 42px rgba(27,36,55,.1);
    }
    *{box-sizing:border-box} html{min-height:100%;background:var(--page)}
    body{margin:0;min-width:320px;min-height:100vh;background:radial-gradient(900px 480px at 50% -180px,rgba(53,92,168,.2),transparent 70%),var(--page);color:var(--text);font-family:var(--font);font-size:14px;transition:background .25s,color .25s}
    [dir="rtl"] body{font-family:'Vazirmatn','Inter',system-ui,sans-serif}
    button,a{font:inherit}button{border:0}a{color:inherit;text-decoration:none}.hidden{display:none!important}
    .page{width:min(100%,760px);margin:0 auto;padding:86px 18px 48px;position:relative}.brand-bar{position:absolute;z-index:4;top:86px;inset-inline:42px;display:flex;align-items:center;gap:16px;pointer-events:none}.brand{display:none}.brand-mark{display:grid;place-items:center;width:34px;height:34px;border:1px solid var(--border);border-radius:10px;background:linear-gradient(145deg,var(--surface-3),var(--surface));color:var(--brand);font-size:18px;box-shadow:inset 0 1px rgba(255,255,255,.06)}.brand-copy{min-width:0}.brand-name{font-size:12px;line-height:1.2;font-weight:800;color:var(--text);letter-spacing:.01em}.brand-sub{color:var(--muted);font-size:10px;line-height:1.4;margin-top:2px}.top-actions{display:flex;gap:8px;align-items:center;margin-inline-start:auto;pointer-events:auto}.icon-button{position:relative;display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:var(--surface);border:1px solid var(--border);color:var(--text-2);cursor:pointer;transition:.18s ease;box-shadow:0 4px 12px rgba(0,0,0,.06)}.icon-button:hover{border-color:var(--brand);background:var(--brand-soft);color:var(--brand-hover);transform:translateY(-1px)}.icon-button:focus-visible,.copy-button:focus-visible,.app-button:focus-visible{outline:3px solid rgba(35,117,232,.35);outline-offset:2px}
    .subscription-card{overflow:hidden;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}.card-head{min-height:92px;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:22px 126px 22px 24px;border-bottom:1px solid var(--border-soft)}.title-line{display:flex;align-items:center;flex-wrap:wrap;gap:10px;min-width:0}.title-line h1{margin:0;font-size:26px;line-height:1.2;font-weight:750;letter-spacing:-.035em}.identity-pill{max-width:270px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;border:1px solid var(--border);background:var(--surface-3);border-radius:8px;padding:6px 10px;color:var(--text-2);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:14px;font-weight:700}.card-body{padding:24px}
    .announcement{display:flex;align-items:flex-start;gap:9px;padding:11px 13px;margin-bottom:18px;border:1px solid var(--brand);border-radius:12px;background:var(--brand-soft);color:var(--text-2);font-size:12px;line-height:1.7}.announcement i{font-size:16px;color:var(--brand);margin-top:1px}.info-table{border:1px solid var(--border);border-radius:15px;overflow:hidden}.info-row{display:grid;grid-template-columns:minmax(155px,.9fr) minmax(0,1.15fr);min-height:54px;background:var(--surface)}.info-row+.info-row{border-top:1px solid var(--border)}.info-label,.info-value{display:flex;align-items:center;padding:11px 16px;min-width:0}.info-label{background:rgba(127,135,152,.06);color:var(--text-2);font-weight:500;border-inline-end:1px solid var(--border)}.info-value{font-size:14px;color:var(--text);font-weight:500;overflow-wrap:anywhere}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}.status{display:inline-flex;align-items:center;gap:6px;border-radius:6px;padding:4px 8px;font-size:12px;font-weight:700}.status.active{background:var(--green-soft);color:var(--green)}.status.inactive{background:var(--red-soft);color:var(--red)}.status.unlimited{background:var(--purple-soft);color:var(--purple)}.status .dot{width:7px;height:7px;border-radius:50%;background:currentColor;box-shadow:0 0 0 3px color-mix(in srgb,currentColor 16%,transparent)}
    .usage-summary{padding:16px;margin-top:16px;border:1px solid var(--border);border-radius:16px;background:var(--surface-2)}.usage-head,.usage-foot{display:flex;align-items:center;justify-content:space-between;gap:12px}.usage-figures{display:flex;align-items:baseline;gap:7px;min-width:0}.usage-used{font-size:25px;line-height:1;font-weight:800;letter-spacing:-.04em}.usage-separator{font-size:21px;color:var(--faint);font-weight:400}.usage-total{font-size:16px;color:var(--text-2);font-weight:600}.expiry-chip{display:inline-flex;align-items:center;gap:5px;border-radius:6px;padding:5px 8px;background:var(--brand-soft);color:#5b9fff;font-size:12px;font-weight:700;white-space:nowrap}.usage-bar{position:relative;overflow:hidden;width:100%;height:10px;margin:15px 0 8px;border-radius:999px;background:var(--surface-3)}.usage-fill{position:relative;height:100%;border-radius:inherit;min-width:0;transition:width .45s ease,background .3s}.usage-fill::after{position:absolute;content:'';inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.24),transparent);animation:shine 2.2s linear infinite}.usage-foot{font-size:12px;color:var(--muted)}.usage-pct{font-weight:800;color:var(--text-2)}
    .divider{display:flex;align-items:center;gap:14px;margin:27px 0 18px;color:var(--text);font-size:16px;font-weight:750;letter-spacing:-.01em}.divider::before,.divider::after{content:'';height:1px;flex:1;background:var(--border)}.links-list{display:grid;gap:11px}.link-row{display:flex;align-items:center;min-height:66px;gap:10px;padding:11px 12px 11px 14px;background:var(--surface-2);border:1px solid var(--border);border-radius:13px;transition:border-color .18s,background .18s}.link-row:hover{border-color:#5a6271}.link-row.is-inactive{opacity:.68}.link-main{display:flex;align-items:center;gap:10px;min-width:0;flex:1}.tag-stack{display:flex;align-items:center;flex-wrap:wrap;gap:5px;flex-shrink:0}.tag{display:inline-flex;align-items:center;justify-content:center;min-height:25px;border-radius:6px;padding:3px 7px;font-size:10px;font-weight:800;letter-spacing:.015em;white-space:nowrap}.tag.sub{background:var(--green-soft);color:var(--green)}.tag.vless{background:rgba(91,116,255,.16);color:#8498ff}.tag.trojan{background:var(--purple-soft);color:var(--purple)}.tag.xhttp{background:var(--amber-soft);color:var(--amber)}.tag.tls{background:var(--green-soft);color:var(--green)}.tag.ws{background:var(--brand-soft);color:#64a1ff}.tag.other{background:var(--surface-3);color:var(--text-2)}.link-title{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--text-2);font-size:13px;font-weight:600}.link-subtitle{color:var(--muted);font-size:10.5px;line-height:1.45;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.link-actions{display:flex;gap:7px;margin-inline-start:auto}.copy-button{display:grid;place-items:center;width:34px;height:34px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--text-2);cursor:pointer;transition:.16s}.copy-button:hover{color:var(--brand-hover);background:var(--brand-soft);border-color:var(--brand)}
    .app-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:22px}.app-menu-wrap{position:relative}.app-button{width:100%;display:flex;align-items:center;justify-content:center;gap:8px;padding:13px 15px;border-radius:10px;background:var(--brand);color:#fff;font-size:15px;font-weight:700;cursor:pointer;box-shadow:0 6px 16px rgba(35,117,232,.28);transition:.16s}.app-button:hover{background:var(--brand-hover);transform:translateY(-1px)}.app-button i:first-child{font-size:20px}.app-menu{position:absolute;z-index:20;display:none;top:calc(100% + 7px);inset-inline:0;padding:5px;background:var(--surface);border:1px solid var(--border);border-radius:12px;box-shadow:var(--shadow)}.app-menu.open{display:block}.app-menu button{display:flex;align-items:center;width:100%;padding:9px 10px;border-radius:8px;background:transparent;color:var(--text-2);font-size:12px;text-align:start;cursor:pointer}.app-menu button:hover{background:var(--brand-soft);color:var(--brand-hover)}
    .error-state,.loading-state{display:grid;place-items:center;min-height:360px;padding:30px;text-align:center;color:var(--muted)}.state-icon{display:grid;place-items:center;width:54px;height:54px;margin:auto auto 14px;border-radius:17px;background:var(--red-soft);color:var(--red);font-size:26px}.loading-state i{font-size:28px;color:var(--brand);animation:spin 1s linear infinite}.empty-links{padding:22px;border:1px dashed var(--border);border-radius:13px;text-align:center;color:var(--muted);font-size:12px}.toast{position:fixed;z-index:80;inset-inline-start:50%;bottom:max(24px,env(safe-area-inset-bottom));transform:translate(-50%,18px);opacity:0;display:flex;align-items:center;gap:8px;max-width:calc(100vw - 32px);padding:11px 15px;border:1px solid var(--border);border-radius:11px;background:var(--surface);box-shadow:var(--shadow);color:var(--text);font-size:12px;font-weight:700;pointer-events:none;transition:.22s}.toast.show{opacity:1;transform:translate(-50%,0)}.toast i{color:var(--green);font-size:16px}.modal{position:fixed;z-index:70;inset:0;display:none;place-items:center;padding:20px;background:rgba(0,0,0,.66);backdrop-filter:blur(6px)}.modal.open{display:grid}.modal-card{width:min(100%,330px);padding:22px;border:1px solid var(--border);border-radius:19px;background:var(--surface);box-shadow:var(--shadow);text-align:center}.modal-title{font-size:14px;font-weight:800;margin-bottom:14px}.modal-card img{width:100%;max-width:245px;background:#fff;border-radius:12px;padding:9px}.modal-close{width:100%;margin-top:14px;padding:10px;border:1px solid var(--border);border-radius:9px;background:var(--surface-2);color:var(--text-2);cursor:pointer}.language-menu{position:absolute;z-index:30;display:none;top:calc(100% + 7px);inset-inline-end:0;width:150px;padding:5px;background:var(--surface);border:1px solid var(--border);border-radius:12px;box-shadow:var(--shadow)}.language-menu.open{display:block}.language-menu button{display:block;width:100%;padding:9px 10px;background:transparent;border:0;border-radius:8px;color:var(--text-2);text-align:start;cursor:pointer;font-size:12px}.language-menu button:hover{background:var(--brand-soft);color:var(--brand-hover)}.language-wrap{position:relative}
    @keyframes spin{to{transform:rotate(360deg)}}@keyframes shine{from{transform:translateX(-130%)}to{transform:translateX(250%)}}@media(max-width:580px){.page{padding:76px 12px 36px}.brand-bar{top:76px;inset-inline:28px}.brand-name{font-size:11px}.card-head{padding:18px 112px 18px 16px;min-height:76px}.title-line h1{font-size:21px}.identity-pill{max-width:178px;font-size:11px}.card-body{padding:16px}.info-row{grid-template-columns:42% 58%;min-height:51px}.info-label,.info-value{padding:10px 11px;font-size:12px}.usage-used{font-size:23px}.usage-total{font-size:14px}.expiry-chip{font-size:11px}.link-row{padding:10px;min-height:62px}.tag-stack{gap:4px}.tag{font-size:9px;padding:3px 5px}.link-title{font-size:12px}.copy-button{width:33px;height:33px}.app-grid{gap:10px}.app-button{font-size:14px;padding:12px 8px}.divider{font-size:15px;margin:23px 0 15px}.announcement{font-size:11px}}
    @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;scroll-behavior:auto!important;transition-duration:.001ms!important}}
  </style>
</head>
<body>
  <main class="page">
    <header class="brand-bar" aria-label="RVG Gateway">
      <div class="brand"><div class="brand-mark"><i class="ti ti-shield-check"></i></div><div class="brand-copy"><div class="brand-name">RVG GATEWAY</div><div class="brand-sub">Secure subscription profile</div></div></div>
      <div class="top-actions">
        <button class="icon-button" id="theme-button" type="button" aria-label="Toggle theme" title="Toggle theme"><i class="ti ti-moon" id="theme-icon"></i></button>
        <div class="language-wrap"><button class="icon-button" id="language-button" type="button" aria-label="Change language" title="Change language"><i class="ti ti-language"></i></button><div class="language-menu" id="language-menu"><button type="button" data-lang="en">English</button><button type="button" data-lang="fa">فارسی</button></div></div>
      </div>
    </header>
    <section class="subscription-card" id="subscription-card" aria-live="polite">
      <div class="loading-state"><div><i class="ti ti-loader-2"></i><p id="loading-copy">Loading subscription information…</p></div></div>
    </section>
  </main>
  <div class="toast" id="toast" role="status"><i class="ti ti-circle-check"></i><span></span></div>
  <div class="modal" id="qr-modal" aria-hidden="true"><div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="qr-title"><div class="modal-title" id="qr-title">QR Code</div><img id="qr-image" alt="Subscription QR code"><button type="button" class="modal-close" id="qr-close">Close</button></div></div>
<script>
(() => {
  'use strict';
  // همان قرارداد bootstrap که SubPage در 3x-ui استفاده می‌کند.
  window.__SUB_PAGE_DATA__ = __BOOTSTRAP_JSON__;
  const subData = window.__SUB_PAGE_DATA__ || {};
  const BOOTSTRAP_SUB_PAGE_DATA = subData;
  const SUB_KEY = __SUBSCRIPTION_KEY__;
  const SUBSCRIPTION_TYPE = __SUBSCRIPTION_TYPE__;
  const state = { data: null, password: '', lang: localStorage.getItem('rvg-sub-language') || 'en', theme: localStorage.getItem('rvg-sub-theme') || 'dark' };
  const text = {
    en: { title:'Subscription info', subId:'Subscription ID', account:'Account', status:'Status', active:'Active', inactive:'Inactive', unlimited:'Unlimited', downloaded:'Downloaded', uploaded:'Uploaded', usage:'Usage', quota:'Total quota', remaining:'Remaining', lastOnline:'Last Online', expiry:'Expiry', noExpiry:'No expiry', never:'—', info:'Subscription info', copyUrl:'Copy URL', copyAll:'Copy All Configs', copyAllSub:'Copy all active configuration links', copied:'Copied to clipboard', qr:'QR Code', android:'Android', ios:'iOS', loading:'Loading subscription information…', unavailable:'Subscription unavailable', retry:'Please confirm that this link is valid and try again.', config:'Config', expiresIn:'remaining', noConfigs:'No configurations are available for this subscription.', lockedTitle:'Protected subscription', lockedSub:'Enter the subscription password to view your access details.', password:'Password', unlock:'Unlock', wrongPassword:'Incorrect password. Please try again.', refresh:'Updated just now', days:'d', hours:'h', copy:'Copy', close:'Close' },
    fa: { title:'اطلاعات اشتراک', subId:'شناسه اشتراک', account:'حساب', status:'وضعیت', active:'فعال', inactive:'غیرفعال', unlimited:'نامحدود', downloaded:'دریافت‌شده', uploaded:'ارسال‌شده', usage:'مصرف', quota:'سقف کل', remaining:'باقی‌مانده', lastOnline:'آخرین فعالیت', expiry:'انقضا', noExpiry:'بدون انقضا', never:'—', info:'اطلاعات سابسکریپشن', copyUrl:'کپی لینک', copyAll:'کپی همه کانفیگ‌ها', copyAllSub:'تمام لینک‌های فعال را یک‌جا کپی کنید', copied:'در کلیپ‌بورد کپی شد', qr:'کد QR', android:'اندروید', ios:'iOS', loading:'در حال بارگذاری اطلاعات اشتراک…', unavailable:'اشتراک در دسترس نیست', retry:'از معتبر بودن لینک مطمئن شوید و دوباره تلاش کنید.', config:'کانفیگ', expiresIn:'باقی‌مانده', noConfigs:'کانفیگی برای این اشتراک موجود نیست.', lockedTitle:'اشتراک محافظت‌شده', lockedSub:'رمز اشتراک را برای مشاهدهٔ اطلاعات دسترسی وارد کنید.', password:'رمز عبور', unlock:'باز کردن', wrongPassword:'رمز واردشده صحیح نیست.', refresh:'همین حالا به‌روزرسانی شد', days:'روز', hours:'ساعت', copy:'کپی', close:'بستن' }
  };
  const $ = (selector, parent=document) => parent.querySelector(selector);
  const escapeHtml = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const t = key => (text[state.lang] || text.en)[key] || text.en[key] || key;
  const formatBytes = bytes => {
    const value = Number(bytes) || 0;
    if (value < 1024) return value + ' B';
    const units = ['KB','MB','GB','TB']; let n = value / 1024; let index = 0;
    while (n >= 1024 && index < units.length - 1) { n /= 1024; index += 1; }
    return n.toFixed(n >= 100 ? 0 : n >= 10 ? 1 : 2) + units[index];
  };
  const formatDate = iso => {
    if (!iso) return t('noExpiry');
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return t('never');
    return new Intl.DateTimeFormat(state.lang === 'fa' ? 'fa-IR' : 'en-US', {year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}).format(d);
  };
  const statusFor = summary => summary.unlimited ? 'unlimited' : summary.active ? 'active' : 'inactive';
  const formatRemaining = summary => summary.limit > 0 ? formatBytes(Math.max(summary.limit - summary.used, 0)) : t('unlimited');
  const expiryChip = iso => {
    if (!iso) return '';
    const diff = new Date(iso).getTime() - Date.now();
    if (!Number.isFinite(diff) || diff <= 0) return '<span class="expiry-chip"><i class="ti ti-clock-off"></i> '+escapeHtml(t('inactive'))+'</span>';
    const hours = Math.max(1, Math.ceil(diff / 3600000));
    const label = hours >= 24 ? Math.ceil(hours / 24) + t('days') : hours + t('hours');
    return '<span class="expiry-chip"><i class="ti ti-clock"></i> '+label+'</span>';
  };
  function protocolFromLink(link) {
    const value = String(link || '').toLowerCase();
    if (value.startsWith('vless://')) return value.includes('type=xhttp') || value.includes('&xhttp') ? 'vless-xhttp' : value.includes('type=ws') ? 'vless-ws' : 'vless';
    if (value.startsWith('trojan://')) return value.includes('type=xhttp') ? 'trojan-xhttp' : 'trojan';
    if (value.startsWith('ss://')) return 'shadowsocks';
    if (value.startsWith('wireguard://') || value.startsWith('wg://')) return 'wireguard';
    if (value.startsWith('tg://') || value.startsWith('https://t.me/proxy')) return 'mtproto';
    return 'vless';
  }
  function normalize3xPageData(raw) {
    if (!raw || !raw.sId) return raw;
    const expiry = Number(raw.expire || 0) > 0 ? new Date(Number(raw.expire) * 1000).toISOString() : null;
    const sourceLinks = Array.isArray(raw.links) ? raw.links : Array.isArray(raw.result) ? raw.result : [];
    const sourceEmails = Array.isArray(raw.emails) ? raw.emails : [];
    const used = Number(raw.usedByte || 0) || (Number(raw.downloadByte || 0) + Number(raw.uploadByte || 0));
    const limit = Number(raw.totalByte || 0);
    return {
      locked: !!raw.locked,
      subscription_id: raw.sId,
      name: raw.subTitle || sourceEmails.filter(Boolean).filter((item, index, list) => list.indexOf(item) === index).join(', ') || 'Subscription',
      desc: raw.announce || '',
      sub_url: raw.subUrl || '',
      total_used: used,
      total_limit: limit,
      expiry_date: expiry,
      uploaded_bytes: Number(raw.uploadByte || 0),
      last_online: Number(raw.lastOnline || 0) > 0 ? new Date(Number(raw.lastOnline)).toISOString() : null,
      active_connections: raw.isOnline ? 1 : 0,
      links: sourceLinks.map((link, index) => ({
        uuid: String(index), label: sourceEmails[index] || raw.subTitle || t('config')+' '+(index + 1),
        active: !!raw.enabled, protocol: protocolFromLink(link), used_bytes: used,
        limit_bytes: limit, expiry_date: expiry, vless_link: link
      }))
    };
  }
  const getSummary = d => {
    const links = Array.isArray(d.links) ? d.links : [];
    const used = Number.isFinite(Number(d.total_used)) ? Number(d.total_used) : links.reduce((sum, link) => sum + (Number(link.used_bytes) || 0), 0);
    const limited = links.filter(link => Number(link.limit_bytes) > 0);
    const limit = Number.isFinite(Number(d.total_limit)) && Number(d.total_limit) > 0 ? Number(d.total_limit) : limited.reduce((sum, link) => sum + Number(link.limit_bytes || 0), 0);
    const expiries = links.map(link => link.expiry_date).filter(Boolean).map(value => new Date(value)).filter(d => !Number.isNaN(d.getTime()));
    const expiry = d.expiry_date || (expiries.length ? new Date(Math.min(...expiries.map(d => d.getTime()))).toISOString() : null);
    const unlimited = limit <= 0;
    const allAllowed = links.length > 0 && links.some(link => link.active);
    const active = allAllowed && (unlimited || used < limit) && (!expiry || new Date(expiry).getTime() > Date.now());
    return { links, used, limit, expiry, unlimited, active, remaining: limit > 0 ? Math.max(limit - used, 0) : 0 };
  };
  const protocolTags = raw => {
    const protocol = String(raw || 'vless-ws').toLowerCase();
    const tags = [];
    if (protocol.includes('vless')) tags.push(['vless','VLESS']); else if (protocol.includes('trojan')) tags.push(['trojan','Trojan']); else if (protocol.includes('shadow')) tags.push(['purple','Shadowsocks']); else if (protocol.includes('mtproto')) tags.push(['other','MTProto']); else tags.push(['other',protocol.toUpperCase()]);
    if (protocol.includes('xhttp')) tags.push(['xhttp','XHTTP']); else if (protocol.includes('ws')) tags.push(['ws','WS']);
    tags.push(['tls','TLS']);
    return tags.map(([kind,label]) => '<span class="tag '+kind+'">'+label+'</span>').join('');
  };
  async function copy(value) {
    if (!value) return;
    try { await navigator.clipboard.writeText(value); showToast(t('copied')); }
    catch (err) { const area=document.createElement('textarea'); area.value=value; area.style.cssText='position:fixed;opacity:0'; document.body.append(area); area.select(); document.execCommand('copy'); area.remove(); showToast(t('copied')); }
  }
  function showToast(message) { const toast=$('#toast'); $('span', toast).textContent=message; toast.classList.add('show'); clearTimeout(showToast.timer); showToast.timer=setTimeout(()=>toast.classList.remove('show'),2400); }
  function showQr(label, value) { $('#qr-title').textContent=label || t('qr'); $('#qr-image').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(value); $('#qr-modal').classList.add('open'); $('#qr-modal').setAttribute('aria-hidden','false'); }
  function renderLock(name, error='') {
    const card=$('#subscription-card');
    card.innerHTML='<div class="card-head"><div class="title-line"><h1>'+escapeHtml(t('lockedTitle'))+'</h1></div></div><div class="card-body"><div class="announcement"><i class="ti ti-lock"></i><span>'+escapeHtml(t('lockedSub'))+'</span></div><form id="unlock-form"><label class="hidden" for="subscription-password">'+escapeHtml(t('password'))+'</label><input id="subscription-password" type="password" autocomplete="current-password" placeholder="'+escapeHtml(t('password'))+'" style="width:100%;padding:13px 14px;border:1px solid var(--border);border-radius:11px;background:var(--surface-2);color:var(--text);outline:none;margin-bottom:10px">'+(error?'<div style="color:var(--red);font-size:12px;margin-bottom:10px">'+escapeHtml(error)+'</div>':'')+'<button class="app-button" type="submit"><i class="ti ti-lock-open"></i>'+escapeHtml(t('unlock'))+'</button></form></div>';
    $('#unlock-form').addEventListener('submit', async event => { event.preventDefault(); state.password=$('#subscription-password').value; await load(); });
    $('#subscription-password').focus();
  }
  function renderContent(d) {
    state.data=d;
    const summary=getSummary(d); const displayId=d.subscription_id || SUB_KEY; const subUrl=d.sub_url || (location.origin + '/sub-group/' + SUB_KEY + (state.password ? '?pw='+encodeURIComponent(state.password) : ''));
    const pct=summary.limit > 0 ? Math.min(100, summary.used / summary.limit * 100) : 0;
    const tone=pct >= 90 ? 'var(--red)' : pct >= 75 ? 'var(--amber)' : 'var(--green)';
    const status=statusFor(summary); const statusLabel=status==='active'?t('active'):status==='unlimited'?t('unlimited'):t('inactive');
    const rows=[
      [t('subId'), '<span class="mono">'+escapeHtml(displayId)+'</span>'],
      [t('account'), escapeHtml(d.name || t('never'))],
      [t('status'), '<span class="status '+status+'"><span class="dot"></span>'+escapeHtml(statusLabel)+'</span>'],
      [t('downloaded'), formatBytes(summary.used)],
      [t('uploaded'), formatBytes(d.uploaded_bytes || 0)],
      [t('usage'), formatBytes(summary.used)],
      [t('quota'), summary.unlimited ? '∞' : formatBytes(summary.limit)],
      [t('remaining'), formatRemaining(summary)],
      [t('lastOnline'), d.last_online ? formatDate(d.last_online) : t('never')],
      [t('expiry'), formatDate(summary.expiry)]
    ];
    const detailRows=rows.map(([label,value])=>'<div class="info-row"><div class="info-label">'+escapeHtml(label)+'</div><div class="info-value">'+value+'</div></div>').join('');
    const usage='<div class="usage-summary"><div class="usage-head"><div class="usage-figures"><span class="usage-used">'+formatBytes(summary.used)+'</span><span class="usage-separator">/</span><span class="usage-total">'+(summary.unlimited?'∞':formatBytes(summary.limit))+'</span></div>'+expiryChip(summary.expiry)+'</div>'+(!summary.unlimited?'<div class="usage-bar"><div class="usage-fill" style="width:'+pct.toFixed(1)+'%;background:'+tone+'"></div></div>':'<div class="usage-bar"><div class="usage-fill" style="width:100%;background:var(--purple)"></div></div>')+'<div class="usage-foot"><span>'+(summary.unlimited?t('unlimited'):formatRemaining(summary))+'</span><span class="usage-pct">'+(summary.unlimited?'∞':pct.toFixed(1)+'%')+'</span></div></div>';
    const configRows=summary.links.length ? summary.links.map((link,index)=>{
      const configTitle=link.label || t('config')+' '+(index+1); const detail=link.limit_bytes ? formatBytes(link.used_bytes || 0)+' / '+formatBytes(link.limit_bytes) : formatBytes(link.used_bytes || 0)+' · '+t('unlimited');
      const configUrl=link.vless_link || '';
      return '<div class="link-row '+(link.active?'':'is-inactive')+'"><div class="link-main"><div class="tag-stack">'+protocolTags(link.protocol)+'</div><div style="min-width:0"><div class="link-title" title="'+escapeHtml(configTitle)+'">'+escapeHtml(configTitle)+'</div><div class="link-subtitle">'+escapeHtml(detail)+(link.expiry_date?' · '+escapeHtml(formatDate(link.expiry_date)):'')+'</div></div></div><div class="link-actions"><button class="copy-button" data-copy="'+index+'" type="button" aria-label="'+escapeHtml(t('copy'))+'" title="'+escapeHtml(t('copy'))+'"><i class="ti ti-copy"></i></button><button class="copy-button" data-qr="'+index+'" type="button" aria-label="'+escapeHtml(t('qr'))+'" title="'+escapeHtml(t('qr'))+'" '+(!configUrl?'disabled':'')+'><i class="ti ti-qrcode"></i></button></div></div>';
    }).join(''):'<div class="empty-links">'+escapeHtml(t('noConfigs'))+'</div>';
    const announce=d.desc ? '<div class="announcement"><i class="ti ti-info-circle"></i><span>'+escapeHtml(d.desc)+'</span></div>':'';
    $('#subscription-card').innerHTML='<div class="card-head"><div class="title-line"><h1>'+escapeHtml(t('title'))+'</h1><span class="identity-pill" title="'+escapeHtml(displayId)+'">'+escapeHtml(displayId)+'</span></div></div><div class="card-body">'+announce+'<div class="info-table">'+detailRows+'</div>'+usage+'<div class="divider"><span>'+escapeHtml(t('info'))+'</span></div><div class="links-list"><div class="link-row"><div class="link-main"><span class="tag sub">SUB</span><div style="min-width:0"><div class="link-title" title="'+escapeHtml(subUrl)+'">'+escapeHtml(displayId)+'</div><div class="link-subtitle">'+escapeHtml(subUrl)+'</div></div></div><div class="link-actions"><button class="copy-button" data-copy-sub type="button" aria-label="'+escapeHtml(t('copyUrl'))+'" title="'+escapeHtml(t('copyUrl'))+'"><i class="ti ti-copy"></i></button><button class="copy-button" data-qr-sub type="button" aria-label="'+escapeHtml(t('qr'))+'" title="'+escapeHtml(t('qr'))+'"><i class="ti ti-qrcode"></i></button></div></div><div class="link-row"><div class="link-main"><div style="min-width:0"><div class="link-title">'+escapeHtml(t('copyAll'))+'</div><div class="link-subtitle">'+escapeHtml(t('copyAllSub'))+'</div></div></div><div class="link-actions"><button class="copy-button" data-copy-all type="button" aria-label="'+escapeHtml(t('copyAll'))+'" title="'+escapeHtml(t('copyAll'))+'"><i class="ti ti-copy"></i></button></div></div>'+configRows+'</div><div class="app-grid"><div class="app-menu-wrap"><button type="button" class="app-button" data-app-toggle="android"><i class="ti ti-brand-android"></i>'+escapeHtml(t('android'))+'<i class="ti ti-chevron-down"></i></button><div class="app-menu" id="android-menu"></div></div><div class="app-menu-wrap"><button type="button" class="app-button" data-app-toggle="ios"><i class="ti ti-brand-apple"></i>'+escapeHtml(t('ios'))+'<i class="ti ti-chevron-down"></i></button><div class="app-menu" id="ios-menu"></div></div></div></div>';
    $('[data-copy-sub]').addEventListener('click',()=>copy(subUrl)); $('[data-qr-sub]').addEventListener('click',()=>showQr(displayId,subUrl));
    $('[data-copy-all]').addEventListener('click',()=>copy(summary.links.filter(link=>link.active&&link.vless_link).map(link=>link.vless_link).join('\n')));
    document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',()=>copy(summary.links[Number(button.dataset.copy)].vless_link)));
    document.querySelectorAll('[data-qr]').forEach(button=>button.addEventListener('click',()=>{const link=summary.links[Number(button.dataset.qr)];showQr(link.label || t('config'),link.vless_link);}));
    mountDeviceMenus(subUrl,displayId);
  }
  function mountDeviceMenus(subUrl, name) {
    const entries={android:[['V2RayNG','v2rayng://install-config?url='+encodeURIComponent(subUrl)],['V2Box','v2box://install-sub?url='+encodeURIComponent(subUrl)+'&name='+encodeURIComponent(name)],['Sing-box',null],['Happ','happ://add/'+subUrl]],ios:[['Shadowrocket','shadowrocket://add/sub://'+btoa(subUrl)+'?remark='+encodeURIComponent(name)],['Streisand','streisand://import/'+encodeURIComponent(subUrl)],['V2Box','v2box://install-sub?url='+encodeURIComponent(subUrl)+'&name='+encodeURIComponent(name)],['V2RayTun',null]]};
    Object.entries(entries).forEach(([platform, apps])=>{
      const menu=$('#'+platform+'-menu'); menu.innerHTML=apps.map(([label,url])=>'<button type="button" data-url="'+escapeHtml(url||'')+'">'+escapeHtml(label)+(url?'':' · '+escapeHtml(t('copy')))+'</button>').join('');
      $('[data-app-toggle="'+platform+'"]').addEventListener('click',event=>{event.stopPropagation();document.querySelectorAll('.app-menu').forEach(item=>item!==menu&&item.classList.remove('open'));menu.classList.toggle('open');});
      menu.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{menu.classList.remove('open');button.dataset.url?location.href=button.dataset.url:copy(subUrl);}));
    });
  }
  function renderError() { $('#subscription-card').innerHTML='<div class="error-state"><div><div class="state-icon"><i class="ti ti-alert-triangle"></i></div><strong style="color:var(--text);font-size:16px">'+escapeHtml(t('unavailable'))+'</strong><p style="max-width:300px;line-height:1.7">'+escapeHtml(t('retry'))+'</p></div></div>'; }
  async function load() {
    const card=$('#subscription-card'); card.innerHTML='<div class="loading-state"><div><i class="ti ti-loader-2"></i><p>'+escapeHtml(t('loading'))+'</p></div></div>';
    try { const endpoint=SUBSCRIPTION_TYPE==='single' ? '/api/public/single/' : '/api/public/sub/'; const url=endpoint+encodeURIComponent(SUB_KEY)+(state.password?'?pw='+encodeURIComponent(state.password):''); const response=await fetch(url,{headers:{Accept:'application/json'}}); if(!response.ok) throw new Error('load'); const responseData=await response.json(); if(responseData.locked){renderLock(responseData.name,state.password?t('wrongPassword'):'');return;} const data=normalize3xPageData(responseData.subPageData || responseData); renderContent(data); } catch (error) { renderError(); }
  }
  function applyPreference() { document.documentElement.dataset.theme=state.theme; document.documentElement.lang=state.lang; document.documentElement.dir=state.lang==='fa'?'rtl':'ltr'; $('#theme-icon').className='ti '+(state.theme==='dark'?'ti-sun':'ti-moon'); $('#loading-copy').textContent=t('loading'); }
  $('#theme-button').addEventListener('click',()=>{state.theme=state.theme==='dark'?'light':'dark';localStorage.setItem('rvg-sub-theme',state.theme);applyPreference();if(state.data)renderContent(state.data);});
  $('#language-button').addEventListener('click',event=>{event.stopPropagation();$('#language-menu').classList.toggle('open');});
  $('#language-menu').addEventListener('click',event=>{const button=event.target.closest('button[data-lang]');if(!button)return;state.lang=button.dataset.lang;localStorage.setItem('rvg-sub-language',state.lang);$('#language-menu').classList.remove('open');applyPreference();if(state.data)renderContent(state.data);else load();});
  document.addEventListener('click',()=>{document.querySelectorAll('.app-menu,.language-menu').forEach(item=>item.classList.remove('open'));});
  $('#qr-close').addEventListener('click',()=>$('#qr-modal').classList.remove('open')); $('#qr-modal').addEventListener('click',event=>{if(event.target===$('#qr-modal'))$('#qr-modal').classList.remove('open');});
  applyPreference();
  const initialPageData = normalize3xPageData(BOOTSTRAP_SUB_PAGE_DATA);
  if (initialPageData && initialPageData.locked) renderLock(initialPageData.name);
  else if (initialPageData && initialPageData.subscription_id) renderContent(initialPageData);
  else load();
  setInterval(()=>{if(state.data)load();},60000);
})();
</script>
</body>
</html>'''
    return (page
            .replace("__SUBSCRIPTION_KEY__", json.dumps(uuid_key))
            .replace("__SUBSCRIPTION_TYPE__", json.dumps(subscription_type))
            .replace("__BOOTSTRAP_JSON__", json.dumps(page_data or {}, ensure_ascii=False)))
