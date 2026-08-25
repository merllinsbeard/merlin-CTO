# Direct image-generation provenance

Use this workflow when an infographic must come directly from `image_generate`, or when replacing a programmatically rendered visual that violated the requested production method.

## Production boundary

The image returned by `image_generate` is the source artifact. Copy or move it byte-for-byte to the delivery path. Do not resize, crop, recompress, annotate, overlay, or reconstruct it with SVG, HTML, Mermaid, Graphviz, Canvas, Pillow, ImageMagick, or browser rendering.

Prompts, factual notes, and receipts may accompany the image. They are evidence, not alternate render inputs.

## Produce

1. Generate one candidate with `image_generate`.
2. Inspect that exact returned image at full resolution and expected chat size.
3. Correct defects only through another generation or an image-model edit.
4. Copy the accepted result byte-for-byte to its delivery path.
5. Verify source and delivered bytes before returning media.

Done: the delivered image matches the accepted model output byte-for-byte.

## Replace a nonconforming artifact

When SVG, HTML, browser rendering, or programmatic composition produced an invalid infographic:

1. Mark the artifact invalid immediately.
2. Generate a replacement without using the invalid visual as a reference.
3. Verify the generated replacement.
4. Remove the invalid source and every derived preview, resize, and export.
5. Update reports, gates, links, receipts, and validation scripts that still describe the retired method.
6. Re-run final checks before returning media.

Deleting only the SVG is insufficient when a PNG derived from it remains. A validator that still accepts the retired workflow is also a live regression path.

## Provenance receipt

Record enough metadata to prove provenance without storing credentials:

```json
{
  "method": "image_generate",
  "provider": "<provider>",
  "model": "<model>",
  "generated_at_utc": "<timestamp>",
  "source_path": "<tool-returned path or result identifier>",
  "artifact_path": "<delivery path>",
  "pixel_size": [0, 0],
  "sha256": "<same hash for source and artifact>",
  "post_processing": "byte-for-byte copy only",
  "source_matches_artifact": true,
  "qa": {"status": "PASS"}
}
```

Never store API keys, signed URLs, tokens, credentials, or connection strings in the receipt.

## Verification gate

Check the actual final file, not the prompt or render status:

1. Source and delivered files exist.
2. Their bytes and SHA-256 hashes match.
3. File signature and dimensions match the receipt.
4. Superseded SVG, HTML, and derived previews are absent from the delivery directory.
5. Pixel QA reads every visible label and checks required numbers, statuses, component count, arrow direction, clipping, overlap, Cyrillic integrity, and invented components.
6. Live, configured, unqualified, unknown, and STOP states remain visually distinct.

If the image cannot pass after shorter labels, splitting the view, or bounded image-model edits, report the generation blocker. Do not switch production methods.
