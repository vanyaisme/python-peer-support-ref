# Production Plan — `python-guide_final.html`

> **Audit date:** 2026-03-04  
> **File audited:** `python-guide_final.html` (9,408 lines)  
> **Purpose:** Interactive Python learning guide for SICT Year 2 students  
> **Stack:** Single-file HTML — inline CSS (~1,046 lines) + HTML content (~7,700 lines) + inline JS (~632 lines) + Pyodide v0.26.4 (CDN)

---

## Priority Legend

| Level | Meaning |
|-------|---------|
| **P0 — Blocker** | Must fix before any public deployment. Page is broken or embarrassing without it. |
| **P1 — Important** | Should fix before launch. Affects SEO, accessibility, or user experience meaningfully. |
| **P2 — Nice-to-Have** | Post-launch improvements. Good for production quality but not launch-blocking. |

---

## P0 — Pre-Launch Blockers

### P0-1 · Fix canonical URL placeholder

**File:** `python-guide_final.html`, lines 7–8

```html
<!-- TODO: update canonical URL before publishing -->
<link rel="canonical" href="https://your-domain.com/python-guide">
```

**Problem:** The canonical URL contains a literal `your-domain.com` placeholder. Search engines will index the wrong URL. This is a hard blocker.

**Fix:** Replace with the actual deployment URL before publishing:

```html
<link rel="canonical" href="https://your-actual-domain.com/python-guide">
```

---

### P0-2 · Remove or update the TODO comment on the canonical tag

**File:** Lines 7–8 (same location as P0-1)

Once the canonical URL is corrected, remove the `<!-- TODO: update canonical URL before publishing -->` comment. Leaving TODO comments in production HTML is unprofessional and reveals intent to search engine scrapers.

---

## P1 — Important Pre-Launch Improvements

### P1-1 · Add missing Open Graph meta tags

**File:** `<head>` section (lines 1–23)

Currently present: `og:title`, `og:description`, `og:type`  
Currently missing: `og:url`, `og:image`

Social shares on Facebook, LinkedIn, Slack, etc. will render without a preview image and may use the wrong URL.

**Fix:** Add before `</head>`:

```html
<meta property="og:url" content="https://your-actual-domain.com/python-guide">
<meta property="og:image" content="https://your-actual-domain.com/assets/og-preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

Create a 1200×630px preview image (`og-preview.png`) for this purpose.

---

### P1-2 · Add Twitter/X card meta tags

**File:** `<head>` section

No `twitter:` meta tags are present. Twitter/X will not generate rich link previews.

**Fix:** Add:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Python Guide — SICT Year 2">
<meta name="twitter:description" content="Interactive Python learning guide for SICT Year 2 students.">
<meta name="twitter:image" content="https://your-actual-domain.com/assets/og-preview.png">
```

---

### P1-3 · Add `<meta name="robots">` tag

**File:** `<head>` section

Without an explicit robots directive, search engine indexing behaviour is undefined. If this page is intended to be publicly indexed:

```html
<meta name="robots" content="index, follow">
```

If it is an internal/school resource only:

```html
<meta name="robots" content="noindex, nofollow">
```

Choose based on intended audience.

---

### P1-4 · Add `<meta name="author">` tag

**File:** `<head>` section

Standard for academic/educational pages. Add:

```html
<meta name="author" content="[Your Name / Institution Name]">
```

---

### P1-5 · Add `<meta name="theme-color">` for mobile

**File:** `<head>` section

Without this tag, mobile browsers show a default chrome colour (typically white or grey) that clashes with the dark theme.

**Fix:** Add two variants to support both themes:

```html
<meta name="theme-color" content="#0f172a" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
```

---

### P1-6 · Fix semantic landmark elements

**File:** HTML content, `<div class="container" role="main">`

Using `<div role="main">` instead of `<main>` is a redundant workaround. Screen readers and assistive technologies prefer native HTML5 landmark elements.

**Fix:** Replace:
```html
<div class="container" role="main">
```
with:
```html
<main class="container">
```
And update the closing tag accordingly.

Similarly, the sidebar navigation wrapper should be a `<nav>` element:
```html
<nav class="sidebar" aria-label="Section navigation">
```

---

### P1-7 · Add `aria-expanded` to collapsible scenario cards

**File:** JS section (IIFE, ~line 8773+) and HTML scenario card markup

Collapsible `.scenario` cards toggle open/closed with a click, but they have no `aria-expanded` attribute. Screen readers cannot communicate the expanded/collapsed state to users.

**Fix:**
- Add `aria-expanded="false"` to each scenario toggle button by default in HTML
- In the click handler JS, toggle `aria-expanded` between `"true"` and `"false"` on click

---

### P1-8 · Fix theme toggle button ARIA

**File:** HTML theme toggle button (inside header)

The theme toggle has an `aria-label` ✅ but is missing `role="switch"` and `aria-pressed` (or `aria-checked`), which are the correct ARIA pattern for a binary toggle.

**Fix:**
```html
<button id="theme-toggle" role="switch" aria-checked="false" aria-label="Toggle dark mode">
```
Update `aria-checked` in JS when theme changes:
```js
toggleBtn.setAttribute('aria-checked', isDark ? 'true' : 'false');
```

---

### P1-9 · Fix `<h1>` gradient text accessibility

**File:** `.header h1` CSS rule (around line ~100 in the CSS block)

The header uses `-webkit-text-fill-color: transparent` with a gradient clip. Some screen readers (particularly older ones) may not announce transparent fill text correctly.

**Fix:** Ensure the `<h1>` has visible fallback text colour in the CSS, and consider adding a visually-hidden `<span>` as fallback if testing shows announcement issues:

```css
h1 {
  color: #e2e8f0; /* fallback for screen readers */
  background: linear-gradient(...);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

### P1-10 · Remove duplicate CSS rule blocks

**File:** Inline `<style>` block (lines 24–1069)

The following rule blocks are defined twice and the second definition silently overrides the first. This is dead code and a maintenance hazard:

| Selector | First occurrence | Second occurrence |
|---|---|---|
| `.scenario-title` | ~line 307 | ~line 609 |
| `.scenario-body` | ~line 365 | ~line 627 |
| `.section` (scroll-margin) | defined inline | defined separately |

**Fix:** Remove the duplicate definitions, keeping the later (overriding) version unless the first contains rules the second does not.

---

### P1-11 · Move inline `style=""` attributes to CSS classes

**File:** Roadmap section HTML content

The roadmap section table rows use inline `style="background: rgba(...)"` attributes scattered directly in HTML. This mixes presentation into structure and makes theme changes painful.

**Fix:** Create named CSS classes:
```css
.roadmap-row-highlight { background: rgba(99, 102, 241, 0.1); }
.roadmap-row-muted { background: rgba(0, 0, 0, 0.15); }
```
Replace the inline `style=` attributes with these classes.

---

### P1-12 · Add `<noscript>` content improvement

**File:** Existing `<noscript>` banner in HTML

The page already has a `<noscript>` banner ✅. Verify it clearly explains:
1. JavaScript is required
2. Specifically, the Python runner will not work
3. What the user can still access (read-only content)

Improve the message if it only says "Enable JavaScript."

---

### P1-13 · Verify Pyodide SRI integrity hash

**File:** `<head>` line 21

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"
        integrity="sha384-i3R37..."
        crossorigin="anonymous"></script>
```

The SRI hash `sha384-i3R37...` must match the actual Pyodide v0.26.4 release hash exactly.

**Fix:** Verify against the [official Pyodide v0.26.4 release](https://github.com/pyodide/pyodide/releases/tag/0.26.4) or use `openssl dgst -sha384 -binary pyodide.js | openssl base64 -A` on the downloaded file to confirm the hash matches. An incorrect SRI hash will silently block Pyodide from loading.

---

## P1 — Architecture / File Splitting

### P1-14 · Split into separate files (Recommended architecture)

The current monolith is 9,408 lines in a single file. This is unsustainable for maintenance. The recommended split:

```
python-guide/
├── index.html          ← Structure only (~7,700 lines HTML → ~500 after CSS/JS extracted)
├── style.css           ← Extracted from inline <style> (~1,046 lines)
├── runner.js           ← Extracted from inline <script> (~632 lines)
└── assets/
    └── og-preview.png  ← Social preview image (new, 1200×630px)
```

**Steps:**
1. Cut everything between `<style>` and `</style>` → paste into `style.css`
2. Replace with `<link rel="stylesheet" href="style.css">`
3. Cut everything between `<script>` and `</script>` → paste into `runner.js`
4. Replace with `<script src="runner.js" defer></script>`
5. Verify all relative paths still resolve
6. Test all functionality (theme toggle, copy buttons, Pyodide runner, sidebar nav, collapsible cards)

**Benefits:** Individual files become cacheable by the browser. CSS/JS edits no longer require navigating a 9,408-line file. Enables minification pipelines (see P2-1).

---

### P1-15 · Add `'Fira Code'` font import or update fallback chain

**File:** CSS block (font-family declarations for code elements)

`'Fira Code'` is referenced in the CSS `font-family` stack but no `@import` or `<link>` for it is present in `<head>`. The browser silently falls through to `'Cascadia Code'` → `'Consolas'` → `monospace`.

**Fix (Option A — load the font):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
```

**Fix (Option B — remove the dead reference):**
Remove `'Fira Code'` from the font-family stack since it never loads. The fallback chain is perfectly acceptable.

Choose based on whether ligatures and the Fira Code aesthetic are desired.

---

## P2 — Post-Launch / Nice-to-Have

### P2-1 · Minify CSS and JavaScript

After splitting into separate files (P1-14), run minification:

```bash
# CSS
npx cssnano style.css style.min.css

# JS
npx terser runner.js -o runner.min.js --compress --mangle
```

Update `index.html` to reference the `.min.` variants. Minification reduces file size by ~30–60%.

---

### P2-2 · Add `<link rel="preload">` for critical assets

Once files are split, add resource hints:

```html
<link rel="preload" href="style.css" as="style">
<link rel="preload" href="runner.js" as="script">
```

This signals to the browser to fetch these assets earlier in the render pipeline.

---

### P2-3 · Evaluate enabling Pyodide warm-up

**File:** JS IIFE, line ~9401

```js
// window.addEventListener('load', () => setTimeout(() => getPy().catch(()=>{}), 2000));
```

This line pre-warms the Pyodide runtime 2 seconds after page load (silently, ignoring errors). It was intentionally commented out.

**Evaluate:** On a fast connection, enabling this would make the first "Run" button click feel instant. On slow connections, it wastes bandwidth. Consider enabling it behind a `navigator.connection` check:

```js
window.addEventListener('load', () => {
  if (!navigator.connection || navigator.connection.effectiveType === '4g') {
    setTimeout(() => getPy().catch(() => {}), 2000);
  }
});
```

---

### P2-4 · Add Content Security Policy (CSP) meta tag

No CSP is defined. Pyodide and the inline scripts require a permissive policy, but a baseline CSP header reduces XSS exposure for the static content portions.

**Suggested baseline** (adjust for hosting environment):

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
               font-src https://fonts.gstatic.com;
               connect-src https://cdn.jsdelivr.net;
               worker-src blob:;">
```

> ⚠️ Note: Pyodide requires `blob:` worker-src and `unsafe-eval` may be needed for some Pyodide builds. Test thoroughly before enabling.

---

### P2-5 · Add closing section comments for all sections

**File:** HTML content

Only some sections have closing comments (e.g., `<!-- /s11 -->`). Adding them to all 32 sections makes navigation in a raw HTML editor significantly easier:

```html
</div><!-- /s1 -->
</div><!-- /s2 -->
...
```

---

### P2-6 · Simplify `<code class="inline-code">` inside table cells

**File:** HTML content (throughout table-heavy sections)

`<code class="inline-code">` is used repeatedly inside `<td>` elements. The class is redundant if a CSS rule handles `td code` directly:

```css
td code { /* styles currently on .inline-code */ }
```

This allows the HTML to be simplified from:
```html
<td><code class="inline-code">len()</code></td>
```
to:
```html
<td><code>len()</code></td>
```

---

### P2-7 · Add `manifest.json` for PWA installability

For students wanting to install the guide as an offline-capable app:

```json
{
  "name": "Python Guide — SICT Y2",
  "short_name": "PyGuide",
  "start_url": "/python-guide/",
  "display": "standalone",
  "background_color": "#0f172a",
  "theme_color": "#0f172a",
  "icons": [{ "src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png" }]
}
```

Add to `<head>`:
```html
<link rel="manifest" href="manifest.json">
```

---

### P2-8 · Add a Service Worker for offline support

Since Pyodide is loaded from CDN, full offline mode is complex. However, caching `index.html`, `style.css`, and `runner.js` locally would allow the static content to be read offline (Python runner would fail gracefully).

This is a larger effort — implement after P1 file splitting is done.

---

### P2-9 · Fix inconsistent section wrapper indentation

**File:** HTML content (~lines 1216, 1261, 1318 and others)

Some `<div class="section">` blocks have extra leading whitespace compared to others. This is cosmetic but worth cleaning in a single pass with a formatter.

**Fix:** Run the file through [Prettier](https://prettier.io/) HTML formatting after the file split (P1-14) to normalize all indentation in one shot.

---

### P2-10 · Document the `roadmap` section exclusion from sidebar

**File:** JS IIFE — sidebar nav generation

The sidebar generates links for all `[id]` sections but the `id="roadmap"` section is deliberately excluded. This is intentional but undocumented, which will confuse future maintainers.

**Fix:** Add a comment in the JS:
```js
// Note: #roadmap is excluded from sidebar nav intentionally — it appears as a top-level intro card
```

---

## Summary — Prioritized Action Order

### Before deploying (P0 — must do):
1. Fix canonical URL placeholder (P0-1)
2. Remove the TODO comment (P0-2)

### Before deploying (P1 — should do):
3. Add `og:url` and `og:image` meta tags (P1-1)
4. Add Twitter card meta tags (P1-2)
5. Add robots meta tag (P1-3)
6. Add author meta tag (P1-4)
7. Add theme-color meta tag (P1-5)
8. Fix `<div role="main">` → `<main>` (P1-6)
9. Fix sidebar to `<nav>` landmark (P1-6)
10. Add `aria-expanded` to collapsible cards (P1-7)
11. Fix theme toggle ARIA (P1-8)
12. Verify Pyodide SRI hash (P1-13)
13. Remove duplicate CSS rules (P1-10)
14. Move inline `style=` to CSS classes (P1-11)
15. Add/fix Fira Code font (P1-15)
16. Split into separate files: `style.css`, `runner.js` (P1-14)

### After deploying (P2 — nice-to-have):
17. Minify CSS and JS (P2-1)
18. Add `<link rel="preload">` hints (P2-2)
19. Evaluate Pyodide warm-up (P2-3)
20. Add Content Security Policy (P2-4)
21. Add section closing comments (P2-5)
22. Simplify `<code class="inline-code">` in table cells (P2-6)
23. Add `manifest.json` (P2-7)
24. Add Service Worker (P2-8)
25. Run Prettier for indentation (P2-9)
26. Document roadmap sidebar exclusion (P2-10)

---

## Testing Checklist (After Any Changes)

Before re-publishing after fixes:

- [ ] Pyodide runner executes Python in at least 3 different sections
- [ ] Copy buttons work on all code blocks
- [ ] Theme toggle switches dark/light and persists on reload
- [ ] Sidebar navigation scrolls to correct sections
- [ ] All 32 sections + roadmap render correctly
- [ ] Collapsible scenario cards expand/collapse
- [ ] Page loads without console errors
- [ ] `og:url`, `og:image`, canonical URL all point to the live domain
- [ ] SRI hash on Pyodide CDN script verified
- [ ] Run [Lighthouse](https://developer.chrome.com/docs/lighthouse) audit: target 90+ on Performance, Accessibility, Best Practices, SEO
- [ ] Test with a screen reader (VoiceOver on macOS, NVDA on Windows) on at least one section
