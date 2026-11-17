import React from 'react';
import {AbsoluteFill, staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import type {TransitionPresentation} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {fade} from '@remotion/transitions/fade';
import {clockWipe} from '@remotion/transitions/clock-wipe';
import dados from './data/s2e1.json';
import {CenaHook, CenaIntro, CenaOutro, CenaRegras, CenaRobo, CenaRodada, CenaTema, CenaVitoria} from './cenas';
import type {Cena} from './cenas';

const T = dados.transicao;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const transicoes: (() => TransitionPresentation<any>)[] = [
  () => slide({direction: 'from-right'}),
  () => wipe({direction: 'from-left'}),
  () => slide({direction: 'from-bottom'}),
  () => clockWipe({width: 1080, height: 1920}),
  () => fade(),
];

export const Episodio: React.FC = () => {
  const cenas = dados.cenas as Cena[];
  let placar: [number, number] = [0, 0];
  const itens: React.ReactNode[] = [];
  cenas.forEach((c, i) => {
    let el: React.ReactNode;
    if (c.tipo === 'rodada') {
      const antes: [number, number] = [...placar] as [number, number];
      placar = c.ponto === 'neuro' ? [placar[0] + 1, placar[1]] : [placar[0], placar[1] + 1];
      el = <CenaRodada cena={c} placarAntes={antes} placarDepois={placar} />;
    } else if (c.tipo === 'hook') el = <CenaHook cena={c} />;
    else if (c.tipo === 'intro') el = <CenaIntro cena={c} />;
    else if (c.tipo === 'tema') el = <CenaTema cena={c} />;
    else if (c.tipo === 'robo') el = <CenaRobo cena={c} />;
    else if (c.tipo === 'regras') el = <CenaRegras cena={c} />;
    else if (c.tipo === 'vitoria') el = <CenaVitoria cena={c} />;
    else el = <CenaOutro cena={c} />;
    itens.push(
      <TransitionSeries.Sequence key={c.id} durationInFrames={c.duracao} premountFor={30}>
        {el}
      </TransitionSeries.Sequence>,
    );
    if (i < cenas.length - 1) {
      itens.push(
        <TransitionSeries.Transition key={`t${i}`} presentation={transicoes[i % transicoes.length]()} timing={linearTiming({durationInFrames: T})} />,
      );
    }
  });
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <TransitionSeries>{itens}</TransitionSeries>
      <Audio src={staticFile('s2e1/mix.wav')} />
    </AbsoluteFill>
  );
};

/** Moldura de conferencia das zonas seguras (nao vai para o video final) */
export const ComZonas: React.FC = () => (
  <AbsoluteFill>
    <Episodio />
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 192, background: 'rgba(255,0,0,0.25)'}} />
      <div style={{position: 'absolute', left: 0, top: 1536, width: 1080, height: 384, background: 'rgba(255,0,0,0.25)'}} />
      <div style={{position: 'absolute', left: 960, top: 900, width: 120, height: 636, background: 'rgba(255,140,0,0.25)'}} />
    </AbsoluteFill>
  </AbsoluteFill>
);
