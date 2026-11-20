// news-image-20261120: one image summing up the world news of Friday 20 November 2026.
// The image ships beside this program; the program copies it to the grader's output
// directory. No network is used, and every run writes the same bytes.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));

// The copy is byte for byte, so a second run writes identical bytes.
// Guard against a silent empty write: the image must actually be there.
const written = statSync(join(outDir, "entry.png"));
if (written.size === 0) throw new Error("entry.png was copied empty");
