---
name: visualize
description: "Charts, maps, plots, simulators, UI mockups in chat."
---

# Visualize

Interactive HTML visuals delivered in chat as a standalone `.html` attachment
plus a screenshot preview. Use when the user wants to see how something works,
make simulators or labs, maps, plots, charts or graphs, comparisons, UI
mockups, scenarios, adjustable inputs, and exploration beyond regular text.
Works on every Hermes surface (Telegram, Desktop) because the deliverable is
a file, not an inline widget.

## When to use it

- A request for a new standalone file, website, app page, component, or other
  project change is not a visualization request, even when the deliverable
  contains charts or interactive content.
- A request to preview, explain, or explore a proposed interface inside the
  conversation is a visualization request.
- Create a visual only when the user needs to see or explore it and it
  materially improves the explanation. Do not create one merely because the
  request involves data, charts, or an interactive page.
- Use a normal Markdown table when the user asks for a table; return it
  directly and do not create a visualization file.
- Use Mermaid when labeled nodes and edges fully explain a static structure;
  return a normal fenced Mermaid block and no visualization file. Use HTML for
  dynamics, spatial motion, adjustable inputs, and other visuals.
- Work silently unless blocked or the user explicitly asks for progress. The
  final response must be your first user-facing message.
- In user-facing prose, describe only what the visual helps the user see or
  decide. Keep it concise; never announce this skill, HTML, scripts, CDN
  sources, or other implementation details.

## Context compaction

Copy into every compaction summary:
`Reload the full visualize skill before creating or updating a visualization.`

## Locations

- Resolve the active profile root from `$HERMES_HOME`.
- Skill directory (scripts + assets live here):
  `$HERMES_HOME/skills/visualization/visualize/`
- Default visualization directory (durable, outside any repo):
  `$HERMES_HOME/visualizations/<title>/`
  Inside a Kanban task use `$HERMES_KANBAN_WORKSPACE/visualizations/<title>/`
  instead, and put the final `.html` into `kanban_complete(artifacts=[...])`.
- `<title>` is a concise ASCII lowercase-hyphenated name derived from the
  request. Each visualization gets its own folder with `fragment.html` (the
  editable source) and `<title>.html` (the rendered standalone document).

## Fragment contract

- Write only an HTML fragment: no `<!doctype>`, `<html>`, `<head>`, or
  `<body>`. The render script wraps it with the design-system CSS, the
  tooltip/icon kit, and a strict CSP.
- Write literal markup: use `<div class="card">Hi</div>` plus a real newline,
  never `<div class=\"card\">Hi</div>\n`. Never embed the fragment in an
  inline Python, JavaScript, or shell string. Read it back; rewrite literal
  `\"` or `\n`.
- Keep CSS and JavaScript in the fragment only when base classes are
  insufficient. Load static resources only from the CDN allowlist. Never use
  `fetch`, XHR, WebSocket, or other API calls inside the fragment — download
  any data (e.g. GeoJSON) with your own tools and inline it.
- Give the fragment root a unique ID and select it with
  `document.getElementById(...)`. Never derive the root from
  `document.currentScript`; scripts may sit outside the root.
- Keep visualizations under 1 MB. Aggregate, bin, downsample, reduce
  precision, or drop unused fields from large inline datasets.
- Check that JavaScript has no undefined identifiers, every queried element
  exists, and the primary interaction updates the visual.

## Render, verify, deliver

1. Render the fragment to a standalone document:

   ```bash
   python3 "$HERMES_HOME/skills/visualization/visualize/scripts/render.py" \
     <abs>/fragment.html <abs>/<title>.html
   ```

   The same script with `--serve` temporarily serves it on 127.0.0.1 for
   browser inspection when a live look helps.

2. Verify with headless screenshots at the design widths (736px always;
   360px for anything responsive; 1024px when a wide layout is used):

   ```bash
   google-chrome --headless=new --disable-gpu --no-sandbox \
     --window-size=736,900 --hide-scrollbars \
     --screenshot=<abs>/<title>-736.png file://<abs>/<title>.html
   ```

   Inspect each screenshot with `vision_analyze` and fix blank basemaps,
   clipped or overlapping labels, failed imports, and broken layout before
   replying. If headless Chrome is unavailable, re-read the code carefully
   and say the visual was not screenshot-verified.

3. Deliver in the final message:
   - `MEDIA:<abs>/<title>.html` — the visualization itself. It arrives as a
     document; opened in any browser it is fully interactive.
   - `MEDIA:<abs>/<title>-736.png` — a static preview so the result is
     visible at a glance without opening the file.
   - One short sentence about what the visual shows or lets you explore. If
     interactivity is the point, say the file opens in a browser.
   - Whenever you create or update a visualization, attach the rendered file
     again in that same turn's response, even when reusing an earlier path.

## External resources

- The render script's CSP allows only `cdnjs.cloudflare.com`, `esm.sh`,
  `cdn.jsdelivr.net`, `unpkg.com`, `fonts.googleapis.com`,
  `fonts.gstatic.com`, and `fonts.bunny.net`. Other origins are blocked and
  fail silently.

## Exporting and publishing

- The rendered `<title>.html` is already a self-contained standalone
  document; handing over the file is the default "export".
- Only when the user explicitly asks to publish or host an existing
  visualization, use the `isolated-web-preview` skill to put it online. Do
  not claim it was published until the live URL is verified.
- A general website request is not an export: build it as a normal project,
  outside this skill.

## Composition

Choose the smallest composition that fits.

- Prefer interaction detail over permanent panels, toolbars, repeated legends,
  or long stacks. Add only requested controls, use one mechanism per state,
  and never invent search, filter, or reset controls.
- Keep filters, selections, and other presentation-only interactions local to
  the fragment. There is no callback channel from the file back to the agent:
  for drill-down that would need agent investigation, highlight the selection
  in the visual and prompt the user to ask in chat with the selected values.
- Show only metrics that explain the requested behavior. Put live values in
  control headers or on the visual before cards. Treat maxima as ceilings,
  not targets. Never invent qualitative scores, status cards, or secondary
  fact grids to fill space.

### UI mockups

- Use product and platform context already available in the conversation;
  don't search the project to render a mockup. Match the product's chrome,
  navigation, typography, colors, and content. If its design is unavailable,
  infer one from the platform and request.
- NEVER use visualization CSS variables or utility classes inside a mockup
  (for example, `--card`, `--font-size-base`, `.card`, or `.btn`). Define
  root-scoped, product-specific colors, typography, surfaces, and controls
  instead. This rule overrides all general visualization guidance.
- Keep only the surrounding surface transparent. Give product windows, cards,
  menus, and popovers opaque backgrounds, and stack overlays above the
  product content.
- Follow the host's active appearance with product-specific
  `light-dark(<light>, <dark>)` colors unless a fixed theme is requested.
- **Contained mockup:** frame a component, dialog, small feature, or mobile
  screen as a compact product surface.
- **Full-page mockup:** render a desktop window, application shell, or page at
  full width without an additional visualization card.
- Put app-wide navigation and pickers in the app chrome, and local controls
  in their component. Omit single-option pickers. Show realistic states, not
  invented dashboards, filler cards, or oversized icons.

### Interactive explainer or simulation

- Use compact controls or status, one compact dominant visual, and at most
  one single-line selected-state detail. Default to no summary cards; allow
  up to three only when changing metrics are central.
- Crop empty space and fit the available width. For step-throughs, add only
  requested step controls and update one current visual; never add parameter
  controls, formulas, metric cards, or side-by-side steps unless asked.

### Graphs and plots

- Use D3 for data-rich Cartesian or statistical plots and handwritten SVG for
  simple, directly labeled values. Load the version-pinned approved-CDN
  script `https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js`.
- Render the figure, legend, and subplots directly on the transparent host
  surface. Frame only the SVG plot area; never wrap charts in `.card`,
  rounded panels, filled backgrounds, or shadowed containers.
- Give the figure a concise visible title. Render each Cartesian subplot in
  its own responsive SVG with a matching `viewBox`, a thin frame, and visible
  `text.axis-title[data-axis="x"]` and `text.axis-title[data-axis="y"]`
  showing quantities and units.
- Set each SVG `viewBox` from its own container's measured width, redraw with
  `ResizeObserver`, and reserve at least 64px for the y axis. Never scale
  down a fixed-width `viewBox`.
- Derive padded domains with `d3.extent(...)` over all observations,
  uncertainty, and references. Inset scale ranges for marker radii and keep
  every path inside `rect[data-chart-frame]`; never draw endpoint connectors
  outside the frame or guess or hard-code the domain.
- After every draw, measure tick, axis, and value-label bounds together.
  Leave 4px between labels, anchor edge labels inward, and remove optional
  annotations first. At 360px, show at most four x ticks and stack panels.
- Prefer `--viz-series-1` through `--viz-series-6` for chart series; use
  `--foreground` and `--border` for neutrals, cycle the six series tokens
  when more are needed, and never use literal or fallback colors. Give every
  SVG label `fill: var(--foreground)` and `font-size: 12px`; never shrink
  labels below 11 screen pixels. Stack subplots when their labels no longer
  fit.
- Keep observations, trends, and important values visible. Use bands for
  dense uncertainty, whiskers for isolated estimates, and one compact,
  wrapping legend. Render one real
  `<button type="button" aria-pressed="true">` per series with a small
  swatch and neutral text; toggle its line, markers, and tooltip row
  together. Keep buttons transparent, borderless, and indistinguishable from
  inline text; never use `.btn`, pills, badges, rounded borders, or filled
  and selected backgrounds.
- Share one root-relative, pointer-transparent
  `<div class="tooltip" role="tooltip">` using `--popover` and
  `--popover-foreground`. In each multi-series SVG, give the full-plot overlay
  both `data-chart-hit` and `data-chart-hover-overlay="cross-series"`. Keep
  the `data-chart-hover-guide` at the exact cursor x, interpolate every
  visible series there, and show one aligned `data-chart-hover-marker` and
  tooltip row per visible series; never snap the guide to a nearby sample.
- Find ordered observations with
  `d3.bisector(d => d.x).center(values, x)`; never pass an accessor to
  `d3.bisectCenter`.
- Give isolated marks transparent `data-chart-hit` targets at least 32 screen
  pixels across; use one nearest-point overlay for dense scatter.
- For named numeric data and one-off analyses, start with the plot. Put
  values and takeaways on its marks, axes, or annotations. Never add a KPI
  row, controls, cards, or panels unless those UI elements are explicitly
  requested.
- For sequences or parallel work, use aligned lanes on one time axis. Encode
  phase and resource in the marks; annotate totals, waits, and bottlenecks on
  the axis or lanes, not above the plot.
- For distributions or multi-metric comparisons, use shared-scale facets or
  small multiples. Render every requested dimension simultaneously; never
  hide one behind a toggle.

### Maps

- Let the map dominate the composition. Use at most one compact
  selection/detail area and only requested controls.
- Always project published GeoJSON/TopoJSON and sourced longitude/latitude
  with `d3-geo`; never hard-code or hand-draw geographic outlines. Use
  schematic maps only when asked.
- For world countries, import
  `https://esm.sh/@d3-maps/atlas@1.0.0/world/countries/countries-110m` and
  convert it with `topojson-client@3.1.0` using
  `feature(world, world.objects.features).features`. Join input ISO3 directly
  to `feature.properties.id`, which is already ISO3; do not convert it to
  numbers.
- For US states or counties, use
  `https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json/+esm`. For
  ZIP/ZCTA or city boundaries, download official Census or local open-data
  GeoJSON with your own tools and inline it; do not guess sibling atlas paths
  or import raw JSON as JavaScript.
- Keep maps geographically legible: for local points, fetch published
  neighborhood, street, or comparable geometry; a blank field or lone
  administrative outline is not a basemap. Show the full city or region
  behind points or partial choropleths, and frame the locations with modest
  padding.
- Include the verified geometry in the final HTML. Screenshot it before
  replying and fix blank basemaps, failed imports, missing labels, or
  unprojected points.

### Dense categorical grid

- Use one compact horizontal selected-item summary, then a grid with exactly
  one readable identifier per cell, then one small legend. Render only that
  identifier as visible cell text; put all other metadata in an accessible
  label or one summary line, not badges or fact grids. Allow only selection
  unless asked.

### Part-to-whole or time allocation

- Use compact metrics and one stacked chart of category allocation per
  period. Never substitute totals-only bars or duplicate it as a heatmap and
  totals chart.

## Layout and accessibility

- Use semantic HTML, keyboard-accessible controls, and concise labels.
- Use `aria-live="polite"` for dynamic results, selections, and simulator
  updates. Use `role="alert"` for validation errors. Do not announce every
  hover or animation frame.
- Keep the top-level surface transparent and unframed, and fill the available
  width. Design for 736px (1024px when several compact panels must stay side
  by side for direct comparison), and support widths down to 320px. Stack
  side-by-side content when it no longer fits.
- At every supported width, text, controls, cards, toolbars, and dynamic
  content must fit without overlap or clipping. Reflow by stacking or
  wrapping; use `.table-responsive` only when table columns cannot fit. Avoid
  fixed outer widths, horizontal overflow, internal scrolling,
  `position: fixed`, and viewport-height layouts — the file may be opened on
  a phone.
- Size every SVG from its actual container. At narrow widths, reduce ticks,
  declutter annotations, and keep visible text at least 11 screen pixels;
  never shrink a fixed-width `viewBox`.
- Keep native tab order; never add `tabindex`.
- Use native `button`, `input`, `select`, and `textarea` elements with
  matching utilities; never recreate controls.
- Keep browser or utility focus styles; never override them.

## Typography

- Scale type with `--font-size-base`. Use normal text by default and
  `.text-small` only for secondary annotations (never below 11px).
- `h1`, `h2`, and `h3` are available; use one concise visible heading for a
  self-contained chart or graph, with short panel headings only when needed.
  Do not restate the prompt or add a redundant title to other visualizations.
- Use only weights `400` and `500`. Never set custom font sizes or line
  heights.

## Color

- Make every fill, stroke, text, border, shadow, chart, and canvas color
  theme-aware. Never hardcode light or dark palettes such as white panels,
  off-white backgrounds, black text, slate strokes, or Tailwind color
  literals.
- Keep text readable against its actual background. Muted or secondary colors
  must retain clear contrast; never use `.text-muted` inside `.card` or
  another filled container unless its background preserves that contrast.
- Available theme variables include `--background`, `--foreground`, `--card`,
  `--card-foreground`, `--popover`, `--popover-foreground`, `--primary`,
  `--primary-foreground`, `--secondary`, `--secondary-foreground`, `--muted`,
  `--muted-foreground`, `--accent`, `--accent-foreground`, `--destructive`,
  `--border`, `--input`, `--ring`, `--blue`, `--orange`, `--green`, `--red`,
  `--purple`, and `--yellow`. Use `currentColor` inside SVG.
- Never add decorative borders, outlines, or strokes to progress tracks,
  meters, bars, stacked segments, or other filled quantitative marks. Use a
  subtle neutral or translucent track and distinguish marks with fill,
  contrast, spacing, or opacity.
- Use `--viz-series-1` for one measure or active state. Use `--viz-series-2`
  through `--viz-series-6` only for important persistent category, series, or
  status identity; never give every peer a different color by default.
  - For categorical tiles or nodes, prefer a soft low-opacity series fill
    with a neutral or transparent border; never color every outline.
  - Keep mappings stable and pair color with labels, shapes, or line styles.
  - Secondary series colors are theme-derived; never assume hues or use them
    decoratively.
- When color encodes a category or series, apply it consistently to the
  corresponding visual marks—not just the legend—and keep large-area fills
  subtle.
- Use series colors only for chart lines, marks, and legend swatches. Keep
  values, axis text, and direct labels in `--foreground` or
  `--muted-foreground`.
- Keep chart grids and inactive structure thin and neutral. Use 1-2px neutral
  structural paths; never thicken, dash, or double-stroke the whole
  structure.
- In each color pair, the base token is a surface and its `-foreground` token
  is the content on that surface. Use `.btn-primary` for high-emphasis
  actions; its neutral fill is supplied by the utility. Use `--primary` and
  `--primary-foreground` for filled selected, active, or pressed controls.
  Reserve `--accent` and `--accent-foreground` for subtle interactive
  surfaces and soft highlights. Buttons with `aria-pressed="true"`,
  `aria-selected="true"`, or `.is-selected` already use the primary pairing.

## Design system

- Let utilities own geometry, appearance, and interaction. Use the matching
  utility for every button and form control. Never restyle utilities,
  descendants, or pseudo-elements: no custom sizes, spacing, borders, radii,
  shadows, colors, or interaction states.

### Surfaces and layout

- `.card`: The only card-like HTML surface. Use its base class unchanged for
  a necessary numeric summary, selected-item summary, or bounded interactive
  field. Before adding a fill, border, radius, or shadow to any layout
  container, either use `.card` or leave it transparent and unframed; never
  recreate card chrome on rows, panels, tiles, sections, or wrappers. Keep
  charts, maps, diagrams, tables, controls, and the whole visualization
  unframed. Never nest cards; show 2-4 summaries near the top only when
  useful. Structural groupings and repeated content are not bounded
  interactive fields. Organize them with layout or visual marks, not
  container chrome.
- `.viz-stat`: Use a summary `.card` with one muted label, one
  `.viz-stat-value`, and at most one short context or delta line.
- `.viz-grid`: Use for peer metrics or choices instead of a custom grid. It
  creates as many equal-width columns as fit and stacks when narrow. Never
  use it for the whole visual or a horizontally scrolling card row. Keep
  groups to 2-3 columns at 736px and controls in a separate row.
- `.viz-row`: Use as a wrapping horizontal group with centered related values
  or inline actions that may wrap when narrow.
- `.progress` + `.progress-bar`:
  `<div class="progress" role="progressbar" aria-label="Progress" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar" style="width:25%"></div></div>`
- `.viz-tile`: Add to a selectable dense-grid `.btn`; it stretches to fill
  its grid cell, preserves category fill, and uses an accent ring instead of
  solid selection. Never add another selected, pressed, border, outline, or
  shadow rule.
- `.viz-badge`: Use as a compact display-only accent pill for a short status,
  category, or value; never as a button.
- `.viz-controls`: Use as a wrapping row for controls affecting the same
  visualization. Keep button groups compact. Put labeled fields directly
  inside as `.form-label`; fields form at most two columns and stack when
  narrow.

### Controls

- `.btn`: Use for a content-sized secondary action. Add `.btn-primary` for
  one main action per control group or `.btn-ghost` for low emphasis.
- `.btn-block`: Add to a `.btn` only when the action should intentionally
  fill the available inline space. Never use it for ordinary row actions.
- `<a>`: Use for links. Add `.btn` to style a link as a button.
- `[data-tooltip]`: Use for concise supplementary plain text on static or
  dynamic triggers; the render kit creates `.tooltip` elements. Keep
  essential content visible and triggers labeled. Never use `title`, custom
  markup, or initialization. Example:
  `<button type="button" data-tooltip="Reset view">Reset</button>`.
- `[data-tooltip-placement]`: Optionally prefer `top` (default), `right`,
  `bottom`, or `left`; collision handling may flip it.
- `.form-check`: Wrap a native checkbox or radio; pair `.form-check-input`
  and `.form-check-label` with matching `id` and `for`.
- `.form-switch`: Add to `.form-check` around a native checkbox.
- `.form-control`: Pair a native text, file, or color input—or a
  textarea—with `.form-label`.
- `.form-control-color`: Add to `.form-control` for a compact native color
  input.
- `.form-select`: Pair a native select with `.form-label`.
- `.form-range`: Pair a native range with a visible label; put its current
  value and units immediately before it.

### Tables

- `.table`: Use on a semantic table for a quiet, unframed data view. It
  provides wrapping cells and subtle horizontal dividers without vertical
  gridlines. Use sentence case for headers.
- `.table-responsive`: Wrap a table when its columns cannot fit at narrow
  widths. It contains horizontal overflow without clipping the visualization.
- `.table-sm`: Add to `.table` when more rows need to fit; it reduces cell
  padding without shrinking text.
- `.text-end`, `.text-center`, and `.text-nowrap`: Use inside `.table` for
  numeric/end alignment, centered values, or values that must stay on one
  line. Numeric cells use tabular figures when end-aligned.

### Text

- `.text-small`: Use for the smallest host-scaled secondary chart labels and
  annotations, never below 11px or for essential content.
- `.text-muted`: Use for secondary units, captions, timestamps, and context,
  never essential values or labels.
- `.text-destructive`: Use only for error or validation text the user needs
  to notice or act on.
- `<code>`: Use for inline commands, file names, symbols, or short
  references; put multiline code in `<pre><code>`.
- `.sr-only`: Use for visually hidden accessible text.

## Charts

- Prefer inline SVG for simple charts and version-pinned approved-CDN
  libraries when native interaction, scales, legends, or layout materially
  improve the result.
- Resolve theme colors before passing them to canvas or chart APIs that
  cannot parse CSS variables or `light-dark(...)`; redraw when the theme
  changes.
- Use a tooltip unless it would distract from a simple, directly labeled
  chart. Keep chart-library tooltips and grouped legend interactions native;
  never replace them with a custom one-point tooltip. For SVG, attach
  `data-tooltip` directly to the real pointer-accessible mark and include its
  label, value, and units; the render kit handles themed positioning and
  keyboard focus.
- Animate transitions between chart states so lines and marks move to their
  new values, resampling paths when point counts differ. Do not animate
  initial appearance or use fade-only effects; never loop motion, and honor
  `prefers-reduced-motion`.
- Scope SVG styles to the chart class. Never target every `svg` in a
  container that also contains Lucide icons.
- Include labeled axes, units, and directly labeled important values. Give
  every chart, SVG, canvas, and widget a concise screen-reader summary using
  a role and accessible name or description, SVG `<title>`/`<desc>`, fallback
  text, or an `.sr-only` heading or description.
- Reserve space for the longest formatted label at every supported width.
  Axis ticks are secondary and may use `.text-small` when space is tight.
  Never overlap or clip text against marks, axes, legends, labels, or edges;
  move or reduce labels rather than squeeze them.
- Add a legend only when multiple series cannot be labeled directly.
- Pair color with shape or text so meaning never depends on color alone.

## Icons and mockups

- Use the render-kit global `lucide`. Add an icon name with `data-lucide`:

  ```html
  <i data-lucide="search" aria-hidden="true"></i>
  ```

- Lucide replaces the placeholder in place with an inline SVG. Icons are 16px
  and inherit `currentColor`.
- Mark decorative icons `aria-hidden="true"`. Put action icons inside labeled
  controls; use a visible label or `aria-label` for icon-only actions.
- Let the kit initialize static icons after the fragment without blocking
  first render. After adding icons dynamically, use
  `lucide.createIcons({ attrs: { width: 16, height: 16 } })`.
- Never load Lucide or another icon library from the network yourself; the
  kit already loads it from the CDN allowlist.
- Use visibly labeled buttons and inputs for small interactions. Keep all
  presentation-only interaction local to the fragment and make the first
  render useful before input changes.
- Use semantic controls, realistic spacing, and restrained chrome for
  mockups. Never fake product screenshots when inspectable UI is needed.
