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
  ['--color-action','Acciones principales, enlaces y foco'],
  ['--color-action-hover','Hover de acciones'],
  ['--color-action-soft','Fondos suaves de acción'],
  ['--color-bg','Fondo de página'],
  ['--color-surface','Superficies elevadas'],
  ['--color-text','Texto principal'],
  ['--color-muted','Texto secundario'],
  ['--color-border','Bordes y divisores'],
  ['--color-danger','Errores y acciones destructivas'],
  ['--color-warning','Advertencias'],
  ['--color-success','Confirmaciones'],
  ['--radius-md','Radio estándar de controles'],
  ['--space-4','Padding estándar'],
  ['--motion-fast','Transiciones de interacción']
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
