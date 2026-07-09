/* Source importer: produces a reviewable DTCG proposal without changing approved tokens. */
(function () {
  'use strict';

  var maxPerCategory = 48;
  var proposalText = '';

  function unique(values) {
    return Array.from(new Set(values)).slice(0, maxPerCategory);
  }

  function tokenName(value, index) {
    var slug = String(value)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 28);
    return (slug || 'value') + '-' + String(index + 1).padStart(2, '0');
  }

  function category(values, type, description) {
    return Object.fromEntries(unique(values).map(function (value, index) {
      return [tokenName(value, index), {
        '$type': type,
        '$value': value,
        '$description': description,
      }];
    }));
  }

  function normaliseFigmaColor(color, opacity) {
    if (!color || typeof color.r !== 'number' || typeof color.g !== 'number' || typeof color.b !== 'number') return null;
    var channel = function (value) { return Math.round(Math.max(0, Math.min(1, value)) * 255).toString(16).padStart(2, '0'); };
    var hex = '#' + channel(color.r) + channel(color.g) + channel(color.b);
    return typeof opacity === 'number' && opacity < 1 ? hex + channel(opacity) : hex;
  }

  function addDimension(values, value) {
    if (typeof value === 'number' && Number.isFinite(value) && value >= 0) values.push(String(value) + 'px');
  }

  function extractFromFigma(document) {
    var values = { colors: [], dimensions: [], durations: [], fontFamilies: [] };
    var dimensions = new Set(['fontSize', 'lineHeightPx', 'letterSpacing', 'cornerRadius', 'itemSpacing', 'strokeWeight', 'paddingLeft', 'paddingRight', 'paddingTop', 'paddingBottom', 'width', 'height', 'radius', 'blur', 'spread']);

    function visit(value, key) {
      if (Array.isArray(value)) {
        value.forEach(function (item) { visit(item, key); });
        return;
      }
      if (!value || typeof value !== 'object') {
        if (dimensions.has(key)) addDimension(values.dimensions, value);
        if (key === 'fontFamily' && typeof value === 'string') values.fontFamilies.push(value);
        return;
      }

      var color = normaliseFigmaColor(value.color, value.opacity);
      if (color) values.colors.push(color);
      if (key === 'backgroundColor') {
        var background = normaliseFigmaColor(value, value.a);
        if (background) values.colors.push(background);
      }
      Object.keys(value).forEach(function (childKey) { visit(value[childKey], childKey); });
    }

    visit(document, 'root');
    return values;
  }

  function extractFromWebsite(source) {
    var colors = source.match(/#[0-9a-f]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)/gi) || [];
    var dimensions = source.match(/(?<![\w.-])-?\d*\.?\d+(?:px|rem|em|vw|vh|%)/gi) || [];
    var durations = source.match(/\b\d*\.?\d+(?:ms|s)\b/gi) || [];
    var fontMatches = Array.from(source.matchAll(/font-family\s*:\s*([^;}]+)/gi));
    var fontFamilies = fontMatches.map(function (match) { return match[1].trim(); });
    return { colors: colors, dimensions: dimensions, durations: durations, fontFamilies: fontFamilies };
  }

  function buildProposal(values, sourceKind, sourceUrl) {
    var groups = {};
    if (values.colors.length) groups.color = { raw: category(values.colors, 'color', 'Valor bruto extraído de ' + sourceKind) };
    if (values.dimensions.length) groups.dimension = { raw: category(values.dimensions, 'dimension', 'Valor bruto extraído de ' + sourceKind) };
    if (values.durations.length) groups.duration = { raw: category(values.durations, 'duration', 'Valor bruto extraído de ' + sourceKind) };
    if (values.fontFamilies.length) groups.fontFamily = { raw: category(values.fontFamilies, 'fontFamily', 'Valor bruto extraído de ' + sourceKind) };
    return {
      '$description': 'Propuesta de valores brutos. Requiere revisión semántica, WCAG y white label antes de aprobarse.',
      '$extensions': {
        sourceImport: {
          kind: sourceKind,
          url: sourceUrl || 'contenido pegado',
          reviewRequired: true,
        },
      },
      ...groups,
    };
  }

  function figmaFileKey(url) {
    var match = String(url).match(/figma\.com\/(?:file|design)\/([^/?#]+)/i);
    return match ? match[1] : null;
  }

  async function sourceText(kind, url, payload, figmaToken, file) {
    if (file) {
      if (file.size > 10 * 1024 * 1024) throw new Error('El archivo supera el límite de 10 MB.');
      return file.text();
    }
    if (payload.trim()) return payload.trim();
    if (!url.trim()) throw new Error('Indica una URL o pega el contenido que deseas analizar.');
    if (kind === 'figma') {
      var key = figmaFileKey(url);
      if (!key) throw new Error('La URL de Figma debe incluir /file/ o /design/ seguido de la clave del documento.');
      if (!figmaToken) throw new Error('Pega el JSON de Figma o introduce un token de acceso para consultar el documento.');
      var figmaResponse = await fetch('https://api.figma.com/v1/files/' + encodeURIComponent(key), {
        headers: { 'X-Figma-Token': figmaToken },
      });
      if (!figmaResponse.ok) throw new Error('Figma no devolvió el documento (' + figmaResponse.status + '). Comprueba permisos y token.');
      return figmaResponse.text();
    }
    var response = await fetch(url, { mode: 'cors' });
    if (!response.ok) throw new Error('El sitio no devolvió contenido (' + response.status + ').');
    return response.text();
  }

  function setStatus(node, message, isError) {
    node.textContent = (isError ? '⚠ Error: ' : '✓ ') + message;
    node.classList.toggle('source-status-ok', !isError);
  }

  function downloadProposal() {
    var blob = new Blob([proposalText], { type: 'application/json' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'token-proposal.dtcg.json';
    link.click();
    URL.revokeObjectURL(link.href);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('source-import-form');
    if (!form) return;
    var kind = document.getElementById('source-kind');
    var url = document.getElementById('source-url');
    var payload = document.getElementById('source-content');
    var file = document.getElementById('source-file');
    var fileName = document.getElementById('source-file-name');
    var token = document.getElementById('figma-token');
    var tokenField = document.getElementById('figma-token-field');
    var status = document.getElementById('source-import-status');
    var output = document.getElementById('source-output');
    var result = document.querySelector('.source-result');
    var copy = document.getElementById('source-copy');
    var download = document.getElementById('source-download');

    kind.addEventListener('change', function () {
      var isFigma = kind.value === 'figma';
      tokenField.hidden = !isFigma;
      token.value = '';
      url.placeholder = isFigma ? 'https://www.figma.com/design/…' : 'https://…';
    });

    file.addEventListener('change', function () {
      var selected = file.files[0];
      fileName.textContent = selected ? 'Archivo seleccionado: ' + selected.name : 'Ningún archivo seleccionado.';
    });

    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      copy.disabled = true;
      download.disabled = true;
      setStatus(status, 'Analizando la fuente…', false);
      try {
        var selectedFile = file.files[0];
        var text = await sourceText(kind.value, url.value, payload.value, token.value, selectedFile);
        var values;
        if (kind.value === 'figma') {
          var figmaJson = JSON.parse(text);
          values = extractFromFigma(figmaJson);
        } else {
          values = extractFromWebsite(text);
        }
        var total = values.colors.length + values.dimensions.length + values.durations.length + values.fontFamilies.length;
        if (!total) throw new Error('No se encontraron valores compatibles. Pega CSS/HTML o JSON de Figma con estilos.');
        proposalText = JSON.stringify(buildProposal(values, kind.value === 'figma' ? 'Figma' : 'sitio web', url.value || (selectedFile && selectedFile.name)), null, 2) + '\n';
        output.textContent = proposalText;
        result.hidden = false;
        copy.disabled = false;
        download.disabled = false;
        setStatus(status, 'Propuesta generada con ' + total + ' valores brutos detectados. Revísala antes de incorporarla.', false);
      } catch (error) {
        result.hidden = true;
        setStatus(status, error.message + ' Si la URL bloquea CORS, pega el contenido directamente.', true);
      } finally {
        token.value = '';
      }
    });

    copy.addEventListener('click', async function () {
      await navigator.clipboard.writeText(proposalText);
      setStatus(status, 'Propuesta copiada al portapapeles.', false);
    });
    download.addEventListener('click', downloadProposal);
  });
}());
