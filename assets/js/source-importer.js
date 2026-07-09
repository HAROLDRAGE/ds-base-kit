/* Source importer: produces a reviewable DTCG proposal without changing approved tokens. */
(function () {
  'use strict';

  var maxPerCategory = 48;
  var proposalText = '';
  var proposalCss = '';

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
    var fontMatches = Array.from(source.matchAll(/font-family\s*:\s*([^;}\n<]+)/gi));
    var fontFamilies = fontMatches.map(function (match) { return match[1].trim().replace(/["']\s*$/, ''); });
    return { colors: colors, dimensions: dimensions, durations: durations, fontFamilies: fontFamilies };
  }

  function alias(path) {
    return '{' + path + '}';
  }

  function baseKeys(groups, groupName) {
    return groups[groupName] ? Object.keys(groups[groupName].base) : [];
  }

  function addSemanticGroups(groups) {
    var colors = baseKeys(groups, 'color');
    var dimensions = baseKeys(groups, 'dimension');
    var fontFamilies = baseKeys(groups, 'fontFamily');
    if (colors.length) {
      var colorAt = function (index) { return colors[Math.min(index, colors.length - 1)]; };
      groups.color.semantic = {
        bg: { '$type': 'color', '$value': alias('color.base.' + colorAt(0)), '$description': 'Alias normalizado: color.bg. Requiere revisión.' },
        surface: { '$type': 'color', '$value': alias('color.base.' + colorAt(1)), '$description': 'Alias normalizado: color.surface. Requiere revisión.' },
        text: { '$type': 'color', '$value': alias('color.base.' + colorAt(2)), '$description': 'Alias normalizado: color.text. Requiere revisión.' },
        action: { '$type': 'color', '$value': alias('color.base.' + colorAt(3)), '$description': 'Alias normalizado: color.action. Requiere revisión.' },
        border: { '$type': 'color', '$value': alias('color.base.' + colorAt(4)), '$description': 'Alias normalizado: color.border. Requiere revisión.' },
      };
    }
    if (dimensions.length) {
      groups.dimension.semantic = {
        space: { '$type': 'dimension', '$value': alias('dimension.base.' + dimensions[0]), '$description': 'Alias normalizado: space.4. Requiere revisión.' },
      };
    }
    if (fontFamilies.length) {
      groups.fontFamily.semantic = {
        base: { '$type': 'fontFamily', '$value': alias('fontFamily.base.' + fontFamilies[0]), '$description': 'Alias normalizado: typography.font-family-base. Requiere revisión.' },
      };
    }
  }

  function buildProposal(values, sourceKind, sourceUrl) {
    var groups = {};
    if (values.colors.length) groups.color = { base: category(values.colors, 'color', 'Valor base extraído de ' + sourceKind) };
    if (values.dimensions.length) groups.dimension = { base: category(values.dimensions, 'dimension', 'Valor base extraído de ' + sourceKind) };
    if (values.durations.length) groups.duration = { base: category(values.durations, 'duration', 'Valor base extraído de ' + sourceKind) };
    if (values.fontFamilies.length) groups.fontFamily = { base: category(values.fontFamilies, 'fontFamily', 'Valor base extraído de ' + sourceKind) };
    addSemanticGroups(groups);
    return {
      '$description': 'Tokens base extraídos y aliases normalizados. Requiere revisión semántica, WCAG y white label antes de aprobarse.',
      '$extensions': {
        sourceImport: {
          kind: sourceKind,
          url: sourceUrl || 'contenido pegado',
          reviewRequired: true,
          normalizedTargets: ['color.bg', 'color.surface', 'color.text', 'color.action', 'color.border', 'space.4', 'typography.font-family-base'],
        },
      },
      ...groups,
    };
  }

  function cssVariable(group, name) {
    return '--base-' + group.toLowerCase() + '-' + name;
  }

  function generateCss(proposal) {
    var lines = [
      '/* Valores base importados y aliases compatibles con los tokens normalizados del sistema. */',
      ':root {',
    ];
    ['color', 'dimension', 'duration', 'fontFamily'].forEach(function (group) {
      var base = proposal[group] && proposal[group].base;
      if (!base) return;
      Object.keys(base).forEach(function (name) {
        lines.push('  ' + cssVariable(group, name) + ': ' + base[name].$value + ';');
      });
    });
    var semanticColor = proposal.color && proposal.color.semantic;
    if (semanticColor) Object.keys(semanticColor).forEach(function (name) {
      var baseName = semanticColor[name].$value.match(/^\{color\.base\.([^}]+)\}$/)[1];
      lines.push('  --color-' + name + ': var(' + cssVariable('color', baseName) + ');');
    });
    var semanticDimension = proposal.dimension && proposal.dimension.semantic;
    if (semanticDimension) {
      var spaceName = semanticDimension.space.$value.match(/^\{dimension\.base\.([^}]+)\}$/)[1];
      lines.push('  --space-4: var(' + cssVariable('dimension', spaceName) + ');');
    }
    var semanticFont = proposal.fontFamily && proposal.fontFamily.semantic;
    if (semanticFont) {
      var fontName = semanticFont.base.$value.match(/^\{fontFamily\.base\.([^}]+)\}$/)[1];
      lines.push('  --typography-font-family-base: var(' + cssVariable('fontFamily', fontName) + ');');
    }
    lines.push('}');
    return lines.join('\n') + '\n';
  }

  function applyPreview(preview, proposal) {
    var style = preview.style;
    var baseColors = proposal.color && proposal.color.base;
    var baseDimensions = proposal.dimension && proposal.dimension.base;
    var baseFonts = proposal.fontFamily && proposal.fontFamily.base;
    var semanticColors = proposal.color && proposal.color.semantic;
    var semanticColorValue = function (name) {
      if (!semanticColors || !baseColors || !semanticColors[name]) return '';
      var baseName = semanticColors[name].$value.match(/^\{color\.base\.([^}]+)\}$/)[1];
      return baseColors[baseName].$value;
    };
    style.setProperty('--color-bg', semanticColorValue('bg'));
    style.setProperty('--color-surface', semanticColorValue('surface'));
    style.setProperty('--color-text', semanticColorValue('text'));
    style.setProperty('--color-action', semanticColorValue('action'));
    style.setProperty('--color-border', semanticColorValue('border'));
    if (baseDimensions && proposal.dimension.semantic) {
      var spaceName = proposal.dimension.semantic.space.$value.match(/^\{dimension\.base\.([^}]+)\}$/)[1];
      style.setProperty('--space-4', baseDimensions[spaceName].$value);
    }
    if (baseFonts && proposal.fontFamily.semantic) {
      var fontName = proposal.fontFamily.semantic.base.$value.match(/^\{fontFamily\.base\.([^}]+)\}$/)[1];
      style.setProperty('--typography-font-family-base', baseFonts[fontName].$value);
    }
  }

  function figmaFileKey(url) {
    var match = String(url).match(/figma\.com\/(?:file|design)\/([^/?#]+)/i);
    return match ? match[1] : null;
  }

  async function websiteSource(url) {
    var response = await fetch(url, { mode: 'cors' });
    if (!response.ok) throw new Error('El sitio no devolvió contenido (' + response.status + ').');
    var html = await response.text();
    var document = new DOMParser().parseFromString(html, 'text/html');
    var inlineStyles = Array.from(document.querySelectorAll('style')).map(function (style) { return style.textContent; });
    var elementStyles = Array.from(document.querySelectorAll('[style]')).map(function (element) { return element.getAttribute('style'); });
    var visualAttributes = Array.from(document.querySelectorAll('[fill], [stroke], [color]')).map(function (element) {
      return ['fill', 'stroke', 'color'].map(function (attribute) {
        return element.hasAttribute(attribute) ? attribute + ': ' + element.getAttribute(attribute) + ';' : '';
      }).join(' ');
    });
    var styleUrls = Array.from(document.querySelectorAll('link[rel~="stylesheet"][href]')).map(function (link) {
      return new URL(link.getAttribute('href'), url).href;
    });
    var stylesheetResults = await Promise.allSettled(styleUrls.map(function (stylesheetUrl) {
      return fetch(stylesheetUrl, { mode: 'cors' }).then(function (stylesheet) {
        return stylesheet.ok ? stylesheet.text() : '';
      });
    }));
    var stylesheets = stylesheetResults
      .filter(function (result) { return result.status === 'fulfilled'; })
      .map(function (result) { return result.value; });
    return inlineStyles.concat(elementStyles, visualAttributes, stylesheets).join('\n');
  }

  async function sourceText(kind, url, payload, figmaToken, file) {
    if (file) {
      if (file.size > 10 * 1024 * 1024) throw new Error('El archivo supera el límite de 10 MB.');
      if (kind !== 'figma') throw new Error('Los documentos JSON cargados se procesan como fuente Figma. Selecciona Documento Figma.');
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
    return websiteSource(url);
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

  function downloadCssProposal() {
    var blob = new Blob([proposalCss], { type: 'text/css' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'design-system-starter.css';
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
    var downloadCss = document.getElementById('source-download-css');
    var preview = document.getElementById('source-preview');

    kind.addEventListener('change', function () {
      var isFigma = kind.value === 'figma';
      tokenField.hidden = !isFigma;
      token.value = '';
      url.placeholder = isFigma ? 'https://www.figma.com/design/…' : 'https://…';
    });

    file.addEventListener('change', function () {
      var selected = file.files[0];
      fileName.textContent = selected ? 'Archivo seleccionado: ' + selected.name : 'Ningún archivo seleccionado.';
      if (selected) {
        kind.value = 'figma';
        kind.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });

    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      copy.disabled = true;
      download.disabled = true;
      downloadCss.disabled = true;
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
        var proposal = buildProposal(values, kind.value === 'figma' ? 'Figma' : 'sitio web', url.value || (selectedFile && selectedFile.name));
        proposalText = JSON.stringify(proposal, null, 2) + '\n';
        proposalCss = generateCss(proposal);
        output.textContent = proposalText;
        result.hidden = false;
        preview.hidden = false;
        applyPreview(preview, proposal);
        copy.disabled = false;
        download.disabled = false;
        downloadCss.disabled = false;
        setStatus(status, 'Propuesta generada con ' + total + ' valores base detectados y aliases normalizados. Revísala antes de incorporarla.', false);
      } catch (error) {
        result.hidden = true;
        preview.hidden = true;
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
    downloadCss.addEventListener('click', downloadCssProposal);
  });
}());
