/* ===== Tema ===== */
function toggleTheme(btn){
  var dark = document.documentElement.dataset.theme === 'dark';
  document.documentElement.dataset.theme = dark ? 'light' : 'dark';
  btn.setAttribute('aria-pressed', String(!dark));
  btn.textContent = dark ? '🌙 Tema oscuro' : '☀️ Tema claro';
  renderTokens();
}

/* Inicializar botón de tema */
document.addEventListener('DOMContentLoaded', function(){
  var themeBtn = document.getElementById('themeBtn');
  if(themeBtn) {
    themeBtn.addEventListener('click', function(){ toggleTheme(this); });
  }
});

function closeSidebar(){
  // No-op para desktop, pero útil para mobile en futuro
}

/* ===== Tabla de tokens autogenerada ===== */
var TOKEN_META = [
  // === COLORES SEMÁNTICOS ===
  ['--color-bg','Fondo base de página'],
  ['--color-surface','Tarjetas, paneles, inputs'],
  ['--color-text','Texto principal'],
  ['--color-muted','Texto secundario'],
  ['--color-action','Acciones principales, enlaces, foco'],
  ['--color-on-action','Texto/icono sobre color-action'],
  ['--color-focus','Anillo de foco visible'],
  ['--color-danger','Errores: siempre con icono + palabra'],
  ['--color-success','Confirmaciones: siempre con icono + palabra'],
  ['--color-warning','Advertencias'],
  ['--color-border','Bordes y divisores'],
  // === COLORES EXTENDIDOS ===
  ['--color-bg-secondary','Fondo secundario'],
  ['--color-surface-subtle','Superficie sutil'],
  ['--color-action-hover','Hover de acciones'],
  ['--color-action-soft','Fondos suaves de acción'],
  ['--color-text-secondary','Texto secundario'],
  // === TIPOGRAFÍA ===
  ['--typography-font-family-base','Font-family base (sans)'],
  ['--typography-font-family-mono','Font-family monoespaciada'],
  ['--typography-font-weight-light','Weight 300 — Textos finos'],
  ['--typography-font-weight-regular','Weight 400 — Estándar'],
  ['--typography-font-weight-medium','Weight 500 — Énfasis moderado'],
  ['--typography-font-weight-semibold','Weight 600 — Énfasis fuerte'],
  ['--typography-font-weight-bold','Weight 700 — Muy enfatizado'],
  ['--typography-font-weight-extrabold','Weight 800 — Máximo énfasis'],
  ['--typography-size-xs','0.75rem (12px) — Ayudas'],
  ['--typography-size-sm','0.875rem (14px) — Labels'],
  ['--typography-size-base','1rem (16px) — Base'],
  ['--typography-size-lg','1.125rem (18px) — Subtítulos'],
  ['--typography-size-xl','1.25rem (20px) — Heading grande'],
  ['--typography-size-2xl','1.5rem (24px) — H4'],
  ['--typography-size-3xl','1.875rem (30px) — H3'],
  ['--typography-size-4xl','2.25rem (36px) — H2'],
  ['--typography-size-5xl','3rem (48px) — H1'],
  ['--typography-line-height-tight','1.2 — Headings compactos'],
  ['--typography-line-height-normal','1.5 — Cuerpo estándar'],
  ['--typography-line-height-relaxed','1.75 — Párrafos largos'],
  ['--typography-line-height-loose','2 — Accesibilidad aumentada'],
  ['--typography-letter-spacing-tight','-0.02em — Display'],
  ['--typography-letter-spacing-normal','0 — Estándar'],
  ['--typography-letter-spacing-wide','0.05em — Labels'],
  ['--typography-letter-spacing-wider','0.1em — Mayúsculas'],
  // === ESPACIADO ===
  ['--space-0','0px — Sin espaciado'],
  ['--space-1','4px — Mínimo'],
  ['--space-2','8px — Compacto'],
  ['--space-3','12px — Interno controles'],
  ['--space-4','16px — Estándar'],
  ['--space-5','20px — Medio'],
  ['--space-6','24px — Entre bloques'],
  ['--space-8','32px — Entre secciones'],
  ['--space-10','40px — Separación grande'],
  ['--space-12','48px — Separación muy grande'],
  ['--space-16','64px — Entre secciones principales'],
  // === BORDES ===
  ['--radius-none','0 — Sin redondeo'],
  ['--radius-sm','4px — Badges, inputs pequeños'],
  ['--radius-md','8px — Botones, inputs'],
  ['--radius-lg','12px — Tarjetas, modales'],
  ['--radius-xl','16px — Paneles grandes'],
  ['--radius-2xl','20px — Componentes prominentes'],
  ['--radius-pill','999px — Pills, avatares'],
  ['--border-width-hairline','0.5px — Línea muy fina'],
  ['--border-width-thin','1px — Línea estándar'],
  ['--border-width-base','2px — Línea media'],
  ['--border-width-thick','4px — Línea gruesa'],
  // === SOMBRAS ===
  ['--shadow-sm','Sombra pequeña — sm elevation'],
  ['--shadow-md','Sombra media — md elevation'],
  ['--shadow-lg','Sombra grande — lg elevation'],
  ['--shadow-xl','Sombra muy grande — xl elevation'],
  ['--shadow-2xl','Sombra máxima — 2xl elevation'],
  // === MOTION ===
  ['--motion-fast','120ms — Interacción rápida'],
  ['--motion-base','240ms — Transición estándar'],
  ['--motion-slow','400ms — Animación lenta'],
  ['--motion-easing-linear','linear — Movimiento constante'],
  ['--motion-easing-in','cubic-bezier(0.4,0,1,1) — Entrada'],
  ['--motion-easing-out','cubic-bezier(0,0,0.2,1) — Salida'],
  ['--motion-easing-in-out','cubic-bezier(0.4,0,0.2,1) — Ambas'],
  // === LAYOUT ===
  ['--layout-breakpoint-xs','320px — Móvil pequeño'],
  ['--layout-breakpoint-sm','480px — Móvil estándar'],
  ['--layout-breakpoint-md','768px — Tablet'],
  ['--layout-breakpoint-lg','1024px — Desktop pequeño'],
  ['--layout-breakpoint-xl','1280px — Desktop full'],
  ['--layout-breakpoint-2xl','1536px — Desktop ultra-wide'],
  ['--layout-grid-cols-mobile','1 — Columnas móvil'],
  ['--layout-grid-cols-tablet','2 — Columnas tablet'],
  ['--layout-grid-cols-desktop','3 — Columnas desktop'],
  ['--layout-touch-target-min','44px — Touch target mínimo'],
  ['--layout-container-max-width','1280px — Ancho máximo contenedor'],
  ['--layout-container-padding','16px — Padding contenedor'],
  // === MEDIA ===
  ['--media-aspect-square','1/1 — Square'],
  ['--media-aspect-video','16/9 — Video'],
  ['--media-aspect-3-2','3/2 — Fotografía'],
  // === HEADINGS PRESETS ===
  ['--heading-h1-size','3rem — H1 tamaño'],
  ['--heading-h2-size','2.25rem — H2 tamaño'],
  ['--heading-h3-size','1.875rem — H3 tamaño'],
  ['--heading-h4-size','1.5rem — H4 tamaño'],
  ['--heading-h5-size','1.25rem — H5 tamaño'],
  ['--heading-h6-size','1.125rem — H6 tamaño'],
  // === BODY TEXT PRESETS ===
  ['--body-lg-size','1.125rem — Body Large'],
  ['--body-base-size','1rem — Body Base'],
  ['--body-sm-size','0.875rem — Body Small'],
  ['--body-xs-size','0.75rem — Body XS']
];

function renderTokens(){
  var cs = getComputedStyle(document.body);
  var tbody = document.querySelector('#tokens-table tbody');
  tbody.innerHTML = '';
  TOKEN_META.forEach(function(t){
    var val = cs.getPropertyValue(t[0]).trim();
    var isColor = t[0].indexOf('color') !== -1;
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>'+t[0]+'</td><td>'+(isColor?'<span class="swatch" style="background:'+val+'"></span>':'')+val+'</td><td>'+t[1]+'</td>';
    tbody.appendChild(tr);
  });
}

/* ===== Botón loading ===== */
function demoLoading(btn){
  btn.disabled = true; var orig = btn.textContent;
  btn.textContent = 'Guardando…';
  setTimeout(function(){ btn.disabled = false; btn.textContent = orig; showToast('✔ Guardado (demo)'); }, 1500);
}

/* ===== Dropdown ===== */
function ddToggle(id){
  var root = document.getElementById(id);
  var btn = root.querySelector('[aria-haspopup]');
  var menu = root.querySelector('.dd-menu');
  var open = btn.getAttribute('aria-expanded') === 'true';
  if(open){ ddClose(root); } else {
    btn.setAttribute('aria-expanded','true'); menu.hidden = false;
    var items = menu.querySelectorAll('[role=menuitem]'); if(items[0]) items[0].focus();
  }
}

function ddClose(root, refocus){
  var btn = root.querySelector('[aria-haspopup]');
  btn.setAttribute('aria-expanded','false');
  root.querySelector('.dd-menu').hidden = true;
  if(refocus !== false) btn.focus();
}

document.addEventListener('keydown', function(e){
  var menu = document.querySelector('.dd-menu:not([hidden])');
  if(!menu) return;
  var items = Array.prototype.slice.call(menu.querySelectorAll('[role=menuitem]'));
  var i = items.indexOf(document.activeElement);
  if(e.key === 'Escape'){ ddClose(menu.closest('.dd')); e.preventDefault(); }
  else if(e.key === 'ArrowDown'){ items[(i+1)%items.length].focus(); e.preventDefault(); }
  else if(e.key === 'ArrowUp'){ items[(i-1+items.length)%items.length].focus(); e.preventDefault(); }
  else if(e.key === 'Tab'){ ddClose(menu.closest('.dd'), false); }
});

document.addEventListener('click', function(e){
  var openMenu = document.querySelector('.dd-menu:not([hidden])');
  if(openMenu && !openMenu.closest('.dd').contains(e.target)) ddClose(openMenu.closest('.dd'), false);
});

/* ===== Formularios: validación al enviar ===== */
function demoValidate(e){
  e.preventDefault();
  var input = document.getElementById('f-email');
  var err = document.getElementById('f-email-err');
  if(!input.value || input.value.indexOf('@') === -1){
    input.setAttribute('aria-invalid','true'); err.hidden = false; input.focus();
  } else {
    input.removeAttribute('aria-invalid'); err.hidden = true;
    showToast('✔ Formulario enviado (demo)');
  }
  return false;
}

/* ===== Modal con focus trap ===== */
var lastFocused = null;

function openModal(){
  lastFocused = document.activeElement;
  var bd = document.getElementById('modal-bd'); bd.hidden = false;
  var focusables = bd.querySelectorAll('button');
  focusables[0].focus();
  bd.addEventListener('keydown', trapFocus);
  document.addEventListener('keydown', escModal);
}

function closeModal(){
  var bd = document.getElementById('modal-bd'); bd.hidden = true;
  bd.removeEventListener('keydown', trapFocus);
  document.removeEventListener('keydown', escModal);
  if(lastFocused) lastFocused.focus();
}

function escModal(e){ if(e.key === 'Escape') closeModal(); }

function trapFocus(e){
  if(e.key !== 'Tab') return;
  var f = document.getElementById('modal-bd').querySelectorAll('button');
  var first = f[0], last = f[f.length-1];
  if(e.shiftKey && document.activeElement === first){ last.focus(); e.preventDefault(); }
  else if(!e.shiftKey && document.activeElement === last){ first.focus(); e.preventDefault(); }
}

/* ===== Tabs con roving tabindex ===== */
(function(){
  var tablist = document.querySelector('[role=tablist]');
  if(!tablist) return;
  var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role=tab]'));
  function activate(tab){
    tabs.forEach(function(t){
      var sel = t === tab;
      t.setAttribute('aria-selected', String(sel));
      t.tabIndex = sel ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !sel;
    });
    tab.focus();
  }
  tabs.forEach(function(t){ t.addEventListener('click', function(){ activate(t); }); });
  tablist.addEventListener('keydown', function(e){
    var i = tabs.indexOf(document.activeElement);
    if(i === -1) return;
    if(e.key === 'ArrowRight'){ activate(tabs[(i+1)%tabs.length]); e.preventDefault(); }
    else if(e.key === 'ArrowLeft'){ activate(tabs[(i-1+tabs.length)%tabs.length]); e.preventDefault(); }
    else if(e.key === 'Home'){ activate(tabs[0]); e.preventDefault(); }
    else if(e.key === 'End'){ activate(tabs[tabs.length-1]); e.preventDefault(); }
  });
})();

/* ===== Toast (aria-live presente antes de inyectar) ===== */
function showToast(msg){
  var region = document.getElementById('toast-region');
  var t = document.createElement('div');
  t.className = 'toast'; t.textContent = msg;
  region.appendChild(t);
  var timer = setTimeout(remove, 4000);
  t.addEventListener('mouseenter', function(){ clearTimeout(timer); });
  t.addEventListener('mouseleave', function(){ timer = setTimeout(remove, 2000); });
  function remove(){ if(t.parentNode) t.parentNode.removeChild(t); }
}

/* ===== Tooltip: Esc lo oculta ===== */
document.addEventListener('keydown', function(e){
  if(e.key === 'Escape'){
    document.querySelectorAll('.tooltip').forEach(function(tt){ tt.style.opacity = '0'; });
    setTimeout(function(){ document.querySelectorAll('.tooltip').forEach(function(tt){ tt.style.opacity = ''; }); }, 600);
  }
});

/* ===== Accordion ===== */
function accToggle(btn){
  var open = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', String(!open));
  document.getElementById(btn.getAttribute('aria-controls')).hidden = open;
}

/* ===== Copiar manifiesto ===== */
function copyManifest(btn){
  var txt = document.getElementById('manifest-pre').textContent;
  navigator.clipboard.writeText(txt).then(function(){
    btn.textContent = '✔ Copiado';
    setTimeout(function(){ btn.textContent = 'Copiar JSON'; }, 2000);
  });
}

/* Inicializar al cargar */
renderTokens();
