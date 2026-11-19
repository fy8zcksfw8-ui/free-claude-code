import React from 'react';
import {AbsoluteFill, staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import type {TransitionPresentation} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {fade} from '@remotion/transitions/fade';
import {clockWipe} from '@remotion/transitions/clock-wipe';
import d1 from './data/s2e1.json';
import {EpProvider} from './ctx';
import type {Ep} from './ctx';
import {Calculino} from './personagens';
import {CenaHook, CenaIntro, CenaOutro, CenaRegras, CenaRobo, CenaRodada, CenaTema, CenaVitoria} from './cenas';
import type {Cena} from './cenas';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const transicoes: (() => TransitionPresentation<any>)[] = [
  () => slide({direction: 'from-right'}),
  () => wipe({direction: 'from-left'}),
  () => slide({direction: 'from-bottom'}),
  () => clockWipe({width: 1080, height: 1920}),
  () => fade(),
];

export const EP1: Ep = {dados: d1, rivalNome: 'ROBÔ', rivalCor: '#3ff3ff', Rival: Calculino, rodadas: 4};

/** Monta qualquer episodio: cenas padrao + cenas especiais do episodio (extra) */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const MontaEpisodio: React.FC<{ep: Ep; audio: string; extra?: Record<string, React.FC<{cena: Cena}>>; trans?: (() => TransitionPresentation<any>)[]}> = ({ep, audio, extra = {}, trans = transicoes}) => {
  const dados = ep.dados;
  const T = dados.transicao;
  const cenas = dados.cenas as Cena[];
  let placar: [number, number] = [0, 0];
  const itens: React.ReactNode[] = [];
  cenas.forEach((c, i) => {
    let el: React.ReactNode;
    const Especial = extra[c.tipo];
    if (Especial) {
      el = <Especial cena={c} />;
      if (c.tipo === 'rodadaEspecial') {
        placar = c.ponto === 'neuro' ? [placar[0] + 1, placar[1]] : [placar[0], placar[1] + 1];
      }
    } else if (c.tipo === 'rodada') {
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
        <TransitionSeries.Transition key={`t${i}`} presentation={trans[i % trans.length]()} timing={linearTiming({durationInFrames: T})} />,
      );
    }
  });
  return (
    <EpProvider ep={ep}>
      <AbsoluteFill style={{background: '#000'}}>
        <TransitionSeries>{itens}</TransitionSeries>
        <Audio src={staticFile(audio)} />
      </AbsoluteFill>
    </EpProvider>
  );
};

export const Episodio: React.FC = () => <MontaEpisodio ep={EP1} audio="s2e1/mix.wav" />;

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

// ------------------------------------------------------------------ Episodios 2 e 3
import d2 from './data/s2e2.json';
import d3 from './data/s2e3.json';
import {EXTRA, Miragem, Turbo, VISUAIS} from './ep23';

export const EP2: Ep = {dados: d2, rivalNome: 'MIRAGEM', rivalCor: '#ff4fd8', Rival: Miragem, rodadas: 4, visuais: VISUAIS};
export const EP3: Ep = {dados: d3, rivalNome: 'TURBO', rivalCor: '#ffd000', Rival: Turbo, rodadas: 6, visuais: VISUAIS};
export const Episodio2: React.FC = () => <MontaEpisodio ep={EP2} audio="s2e2/mix.wav" extra={EXTRA} />;
export const Episodio3: React.FC = () => <MontaEpisodio ep={EP3} audio="s2e3/mix.wav" extra={EXTRA} />;

// ------------------------------------------------------------------ Episodios 4 e 5 (regras do HyperFrames)
import d4 from './data/s2e4.json';
import d5 from './data/s2e5.json';
import {Doutor, EXTRA45, TRANS45} from './ep45';
import {VISUAIS as VIS23} from './ep23';

export const EP4: Ep = {dados: d4, rivalNome: 'DOUTOR', rivalCor: '#c45cff', Rival: Doutor, rodadas: 4, visuais: VIS23};
export const EP5: Ep = {dados: d5, rivalNome: 'DOUTOR', rivalCor: '#c45cff', Rival: Doutor, rodadas: 4, visuais: VIS23};
export const Episodio4: React.FC = () => <MontaEpisodio ep={EP4} audio="s2e4/mix.wav" extra={EXTRA45} trans={TRANS45} />;
export const Episodio5: React.FC = () => <MontaEpisodio ep={EP5} audio="s2e5/mix.wav" extra={EXTRA45} trans={TRANS45} />;

// ------------------------------------------------------------------ Temporada 3, episodio 1
import d31 from './data/s3e1.json';
import {EXTRA_T3E1, Egito, Esfinge, Grao, TRANS_T3E1, VISUAIS_T3} from './t3e1';

const FundoEgito: React.FC<{n: number}> = ({n}) => (
  <>
    <Egito noite={0.35 + n * 0.1} />
    <Grao />
  </>
);
export const EP_T3E1: Ep = {
  dados: d31, rivalNome: 'ESFINGE', rivalCor: '#7dfcff', Rival: Esfinge, rodadas: 3, semPlacar: true,
  rotuloRival: 'ARMADILHA', rotuloErro: 'VIROU PEDRA!', visuais: VISUAIS_T3, FundoRodada: FundoEgito,
};
export const EpisodioT3E1: React.FC = () => <MontaEpisodio ep={EP_T3E1} audio="s3e1/mix.wav" extra={{...EXTRA45, ...EXTRA_T3E1}} trans={TRANS_T3E1} />;
