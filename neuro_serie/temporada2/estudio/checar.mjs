// Renderiza quadros de amostra (com a moldura das zonas seguras) para revisao.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const BROWSER = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const comp = process.argv[2] ?? 'S2E1-zonas';
const frames = process.argv.slice(3).map(Number);
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const c = await selectComposition({serveUrl, id: comp, browserExecutable: BROWSER});
for (const f of frames) {
  await renderStill({composition: c, serveUrl, output: `out/f${String(f).padStart(5, '0')}.png`, frame: f, browserExecutable: BROWSER, scale: 0.25});
  console.log('ok', f);
}
