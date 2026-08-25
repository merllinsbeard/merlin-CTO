# Image-model architecture workflow

Use this reference when the user requires `image_generate` provenance for a software architecture infographic. The output file will often be PNG, but PNG is only the encoding. The final pixels must come from the image model.

## Method gate

Treat these requests as explicit image-model requirements:

- "image", "имейдж", "image_generate";
- "generate the picture" or "генерация картинок";
- a named image model such as GPT Image.

The final infographic must be the direct result of `image_generate`. HTML, SVG, Mermaid, Graphviz, canvas, Pillow, ImageMagick, browser rendering, and deterministic overlays cannot create or repair it. If generation cannot preserve the required facts after prompt simplification, view splitting, and image-model edits, report the blocker.

## Route the view before prompting

Use a different visual form for each question:

- product functions: real screenshot atlas with editorial callouts;
- host placement: spatial or isometric host map;
- open-source wiring: flat C4-like component map;
- end-to-end behavior: sequence/data-flow with separate identity and failure rails.

A successful host-map style is not a template for the other views.

## Build factual references

Ground names, versions, addresses, components, contracts, and status in source and deployment evidence. Put those facts directly in the prompt. Reference images may be real screenshots, user-provided images, or previous `image_generate` results, never a programmatically rendered infographic.

For product work, pass the real screen captures as multi-image references. Require each screen to remain recognizable. Separate employee screens from operator tools.

## Prompt shape

State these blocks in order:

1. the exact visual form and what it must explain;
2. the required components, panels, or stations;
3. exact short labels in the user's language;
4. required connector directions or numbered contracts;
5. deployed, target, STOP, and untouched-production stamps;
6. exclusions such as invented services, cloud, Kubernetes, or fictional UI;
7. the instruction that the final is an original image-model composition.

Short labels survive better than paragraphs. Reduce prose first, not required components or contracts.

## Correction loop

1. Inspect the generated image itself.
2. Read every large label and version.
3. Count panels, components, badges, and steps.
4. Trace arrowheads from source to destination.
5. Use an image edit for one bounded defect at a time. Name the exact missing label or wrong connector and require all other content to remain stable.
6. Re-open the edited image. Check the changed area and adjacent content.
7. If the edit damages unrelated regions, return to the last green generated artifact.

Validated surgical edits include:

- add one missing panel heading while preserving the atlas;
- add one missing numbered contract badge;
- remove an incorrect connector and redraw its local branches;
- preserve the composition while correcting one label.

## Completion

Done means the requested image-model provenance is true, each view uses the form suited to its question, all required content is present, labels are readable, arrowheads are correct, and every correction was rechecked on the final artifact.
