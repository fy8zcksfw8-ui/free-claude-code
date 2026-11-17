import React from 'react';
import {Composition, continueRender, delayRender} from 'remotion';
import '@fontsource/lilita-one';
import '@fontsource/nunito/800.css';
import '@fontsource/nunito/900.css';
import {ComZonas, Episodio} from './Episodio';
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
    <Composition id="S2E1-zonas" component={ComZonas} durationInFrames={dados.total} fps={30} width={1080} height={1920} />
  </>
);
