import React from 'react';
import {Composition, continueRender, delayRender} from 'remotion';
import '@fontsource/lilita-one';
import '@fontsource/nunito/800.css';
import '@fontsource/nunito/900.css';
import {ComZonas, Episodio, Episodio2, Episodio3} from './Episodio';
import d2 from './data/s2e2.json';
import d3 from './data/s2e3.json';
import dados from './data/s2e1.json';

if (typeof document !== 'undefined') {
  const h = delayRender('carregando fontes');
  Promise.all([document.fonts.load('80px "Lilita One"'), document.fonts.load('900 80px Nunito'), document.fonts.load('800 80px Nunito')])
    .then(() => continueRender(h))
    .catch(() => continueRender(h));
}

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="S2E1" component={Episodio} durationInFrames={dados.total} fps={30} width={1080} height={1920} />
    <Composition id="S2E2" component={Episodio2} durationInFrames={d2.total} fps={30} width={1080} height={1920} />
    <Composition id="S2E3" component={Episodio3} durationInFrames={d3.total} fps={30} width={1080} height={1920} />
    <Composition id="S2E1-zonas" component={ComZonas} durationInFrames={dados.total} fps={30} width={1080} height={1920} />
  </>
);
