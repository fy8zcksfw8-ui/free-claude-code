import React, {useId, useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {TransitionPresentation, TransitionPresentationComponentProps} from '@remotion/transitions';
import {Calculino, Neuro, Trofeu} from './personagens';
import type {Humor, ModoRobo} from './personagens';
import {Contagem, Coracao, Fundo, Hud, Legendas, Opcoes, Pilula, Texto, TITULO, useMola} from './ui';
import {Abs, useBoca, useT} from './cenas';
import type {Cena} from './cenas';
import {Miragem, Turbo} from './ep23';
import {Brilhos} from './brilhos';
import {useEp} from './ctx';
import type {RivalProps} from './ctx';

// Regras do HyperFrames para video vertical: todo texto entre 168 e 1330 px; legenda no fim dessa faixa.
const LEG_Y = 1222;

// ================================================================ TRANSICOES COM CAUSA
type Vazio = Record<string, never>;
const WhipComp: React.FC<TransitionPresentationComponentProps<Vazio>> = ({children, presentationDirection, presentationProgress}) => {
  const p = presentationProgress;
  const entrando = presentationDirection === 'entering';
  const x = entrando ? (1 - p) * 1080 : -p * 1080;
  const blur = Math.sin(Math.PI * p) * 22;
  return <AbsoluteFill style={{transform: `translateX(${x}px)`, filter: `blur(${blur}px)`}}>{children}</AbsoluteFill>;
};
export const whip = (): TransitionPresentation<Vazio> => ({component: WhipComp, props: {}});
const IrisComp: React.FC<TransitionPresentationComponentProps<Vazio>> = ({children, presentationDirection, presentationProgress}) => {
  if (presentationDirection === 'exiting') return <AbsoluteFill>{children}</AbsoluteFill>;
  const r = presentationProgress * 120;
  return <AbsoluteFill style={{clipPath: `circle(${r}% at 50% 42%)`}}>{children}</AbsoluteFill>;
};
export const iris = (): TransitionPresentation<Vazio> => ({component: IrisComp, props: {}});
const DipComp: React.FC<TransitionPresentationComponentProps<Vazio>> = ({children, presentationDirection, presentationProgress}) => {
  const p = presentationProgress;
  if (presentationDirection === 'exiting') return <AbsoluteFill style={{filter: `brightness(${1 - p * 0.6})`, opacity: p > 0.5 ? 0 : 1}}>{children}</AbsoluteFill>;
  return <AbsoluteFill style={{opacity: p > 0.5 ? 1 : 0}}>{children}</AbsoluteFill>;
};
export const dip = (): TransitionPresentation<Vazio> => ({component: DipComp, props: {}});
export const TRANS45 = [whip, iris, whip, dip];

// ================================================================ DOUTOR (colorido)
export const Doutor: React.FC<RivalProps> = ({tamanho, boca = 0, modo = 'normal', silhueta = false}) => {
  const f = useCurrentFrame();
  const id = useId().replace(/:/g, '');
  const erro = modo === 'erro';
  const tremor = erro ? Math.sin(f * 2.1) * 7 : 0;
  const pele = silhueta ? '#08050f' : `url(#pele${id})`;
  const S = (c: string) => (silhueta ? '#08050f' : c);
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      <defs>
        <radialGradient id={`pele${id}`} cx="40%" cy="30%" r="75%">
          <stop offset="0%" stopColor="#e2f5dc" />
          <stop offset="100%" stopColor="#9fcc95" />
        </radialGradient>
      </defs>
      <ellipse cx={0} cy={232} rx={150} ry={18} fill="rgba(0,0,0,0.3)" />
      <g transform={`translate(${tremor} ${Math.sin(f / 9) * 4})`}>
        <path d="M -175 240 L -130 95 L 130 95 L 175 240 Z" fill={S('#f4f4fa')} stroke={S('#9a9ab0')} strokeWidth={6} />
        {!silhueta && <path d="M -45 95 L 0 185 L 45 95" fill="#6b1fa8" />}
        {Array.from({length: 11}).map((_, i) => {
          const a = Math.PI * (0.92 + i * 0.12), r1 = 100, r2 = 170 + (i % 2) * 28;
          return <polygon key={i} points={`${r1 * Math.cos(a - 0.2)},${-30 + r1 * Math.sin(a - 0.2)} ${r2 * Math.cos(a)},${-30 + r2 * Math.sin(a)} ${r1 * Math.cos(a + 0.2)},${-30 + r1 * Math.sin(a + 0.2)}`} fill={S('#eef0ff')} stroke={S('#b9bbd6')} strokeWidth={3} />;
        })}
        <ellipse cx={0} cy={-10} rx={110} ry={125} fill={pele} stroke={S('#4f7a47')} strokeWidth={6} />
        {[-46, 46].map((x) => (
          <g key={x} style={{filter: silhueta ? 'drop-shadow(0 0 16px #c45cff)' : undefined}}>
            <circle cx={x} cy={-35} r={38} fill={silhueta ? '#2a0a40' : '#fff'} stroke={silhueta ? '#c45cff' : '#2b2b38'} strokeWidth={8} />
            {[0, 1, 2].map((j) => {
              const rr = 30 - j * 9, a0 = ((f * (erro ? 30 : 12) + j * 120) * Math.PI) / 180;
              return <path key={j} d={`M ${x + rr * Math.cos(a0)} ${-35 + rr * Math.sin(a0)} A ${rr} ${rr} 0 1 1 ${x + rr * Math.cos(a0 + 3.5)} ${-35 + rr * Math.sin(a0 + 3.5)}`} fill="none" stroke={silhueta ? '#e7a8ff' : '#9b3df0'} strokeWidth={6} />;
            })}
            {!silhueta && <path d={`M ${x - 38} -88 L ${x + 34} ${x < 0 ? -72 : -100}`} stroke="#2b2b38" strokeWidth={11} strokeLinecap="round" transform={x > 0 ? `scale(-1 1) translate(${-2 * x} 0)` : undefined} />}
          </g>
        ))}
        <line x1={-8} y1={-35} x2={8} y2={-35} stroke={S('#2b2b38')} strokeWidth={8} />
        {(() => {
          const mh = 16 + boca * 46;
          return (
            <g>
              <path d={`M -56 40 Q 0 ${40 + mh * 1.6} 56 40 Z`} fill={silhueta ? '#c45cff' : '#4a0a2a'} stroke={S('#2b0a1a')} strokeWidth={5} style={{filter: silhueta ? 'drop-shadow(0 0 12px #c45cff)' : undefined}} />
              {!silhueta && <path d={`M -48 42 L 48 42 L 40 ${48 + mh * 0.3} L -40 ${48 + mh * 0.3} Z`} fill="#fff" />}
            </g>
          );
        })()}
        {erro && [0, 1, 2].map((i) => {
          const k = (f + i * 10) % 30;
          return <circle key={i} cx={-70 + i * 70 + k} cy={-190 - k * 4} r={16 + k} fill="#7a7a88" opacity={1 - k / 30} />;
        })}
      </g>
    </svg>
  );
};

// ================================================================ PEÇAS
/** titulo que entra palavra por palavra com desfoque e depois fica parado (HyperFrames: motion.md) */
const TituloV2: React.FC<{y: number; texto: string; tamanho: number; cor?: string; ini?: number}> = ({y, texto, tamanho, cor = '#fff', ini = 0.15}) => {
  const f = useCurrentFrame();
  const palavras = texto.split(' ');
  return (
    <div style={{position: 'absolute', left: 60, width: 960, top: y - tamanho * 0.6, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', columnGap: tamanho * 0.28, fontFamily: TITULO, fontSize: tamanho, lineHeight: 1.05, color: cor, WebkitTextStroke: `${Math.round(tamanho / 7)}px #140a24`, paintOrder: 'stroke fill'}}>
      {palavras.map((p, i) => {
        const k = f - Math.round((ini + i * 0.067) * 30);
        const q = interpolate(k, [0, 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <span key={i} style={{opacity: q, filter: `blur(${(1 - q) * 6}px)`, display: 'inline-block'}}>
            {p}
          </span>
        );
      })}
    </div>
  );
};

/** "take" do personagem: antecipacao, squash, nova cara e acomodacao */
const take = (k: number) => {
  if (k < 0 || k > 22) return {sx: 1, sy: 1};
  const sy = interpolate(k, [0, 4, 10, 22], [1, 0.86, 1.1, 1], {extrapolateRight: 'clamp'});
  return {sx: 2 - sy, sy};
};

export const BarraMemoria: React.FC<{valor: number; y?: number}> = ({valor, y = 238}) => (
  <div style={{position: 'absolute', left: 300, top: y - 30, width: 480}}>
    <div style={{fontFamily: TITULO, fontSize: 28, color: '#fff', textAlign: 'center', WebkitTextStroke: '5px #140a24', paintOrder: 'stroke fill', marginBottom: 4}}>
      MEMÓRIA DO NEURO {Math.round(valor * 100)}%
    </div>
    <div style={{height: 26, borderRadius: 13, background: 'rgba(20,10,40,0.85)', border: '3px solid #fff', overflow: 'hidden'}}>
      <div style={{width: `${valor * 100}%`, height: '100%', background: valor >= 0.99 ? '#36d97a' : 'linear-gradient(90deg,#9b3df0,#ff6fd8)'}} />
    </div>
  </div>
);

const AVATAR: Record<string, React.FC<RivalProps>> = {calculino: Calculino, miragem: Miragem, turbo: Turbo};

// ================================================================ RODADA V2
const TEMAS: [string, string, string][] = [
  ['#2f6fe0', '#06102e', '#7fc8ff'],
  ['#e0532f', '#2a0806', '#ffb36b'],
  ['#1fa86a', '#03200f', '#9dffb0'],
  ['#8a1fd6', '#14021e', '#e7a8ff'],
];
export const RodadaV2: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const ep = useEp();
  const Rival = ep.Rival;
  const ev = cena.eventos;
  const bN = useBoca('neuro', cena.inicio);
  const bR = useBoca('robo', cena.inicio);
  const bD = useBoca(cena.quemDesafia ?? 'x', cena.inicio);
  // placar a partir das rodadas anteriores
  const antes: [number, number] = [0, 0];
  for (const c of ep.dados.cenas as Cena[]) {
    if (c.id === cena.id) break;
    if (c.tipo === 'rodada') c.ponto === 'neuro' ? antes[0]++ : antes[1]++;
  }
  const depois: [number, number] = cena.ponto === 'neuro' ? [antes[0] + 1, antes[1]] : [antes[0], antes[1] + 1];
  const tema = TEMAS[(cena.n - 1) % 4];
  const revelado = t >= ev.revelaEm;
  const roboErrou = cena.robo !== cena.certa;
  const bug = ev.bugEm !== undefined && t >= ev.bugEm;
  const pontuou = t >= ev.pontoEm;
  const kPonto = f - ev.pontoEm * 30;
  const memoria = cena.memAntes !== undefined;
  const memVal: number = memoria ? interpolate(kPonto, [0, 20], [Number(cena.memAntes), Number(cena.memDepois)], {extrapolateLeft: "clamp", extrapolateRight: "clamp"}) : 0;
  const tonto = memoria && memVal < 0.99;
  const humorN: Humor = revelado ? (cena.ponto === 'neuro' ? 'rindo' : 'surpreso') : tonto ? 'tonto' : t >= ev.contaIni ? 'surpreso' : 'feliz';
  const modoR: ModoRobo = bug || (revelado && roboErrou) ? 'erro' : t >= ev.roboEm ? 'convencido' : 'pensando';
  const tk = take(f - Math.round(ev.revelaEm * 30));
  const tkR = take(f - Math.round(ev.roboEm * 30));
  const balao = spring({frame: f - Math.round(ev.roboEm * 30), fps: 30, config: {damping: 10}});
  const jitter = bug ? (random(`j${f}`) - 0.5) * 24 : 0;
  const Desafiante = cena.quemDesafia ? AVATAR[cena.quemDesafia] : null;
  const ExtraVis = ep.visuais?.[cena.visual];
  const nOp = (cena.opcoes as string[]).length;
  return (
    <AbsoluteFill style={{transform: `translate(${jitter}px, ${jitter * 0.5}px)`}}>
      {ep.FundoRodada ? <ep.FundoRodada n={cena.n} /> : <Fundo c1={tema[0]} c2={tema[1]} c3={tema[2]} />}
      {memoria ? (
        <>
          <Hud placar={pontuou ? depois : antes} rodada={cena.n} pulsoPlacar={0} />
          <AbsoluteFill style={{background: 'transparent'}}>
            <div style={{position: 'absolute', left: 290, top: 196, width: 500, height: 90, background: tema[1], borderRadius: 20}} />
            <BarraMemoria valor={memVal} />
          </AbsoluteFill>
        </>
      ) : (
        <Hud placar={pontuou ? depois : antes} rodada={cena.n} pulsoPlacar={pontuou ? Math.max(0, 1 - kPonto / 12) : 0} />
      )}
      <TituloV2 y={378} texto={cena.titulo} tamanho={cena.final ? 82 : 66} cor={cena.final ? '#ff5f7a' : '#fff'} />
      {(cena.texto as string[]).map((l, i) => (
        <TituloV2 key={i} y={452 + i * 56} texto={l} tamanho={48} cor="#ffd23f" ini={0.45 + i * 0.2} />
      ))}
      <Visual45 cena={cena} />
      {ExtraVis && <ExtraVis cena={cena} />}
      {Desafiante && t < ev.roboEm && (
        <Abs x={140} y={600} escala={spring({frame: f - 4, fps: 30, config: {damping: 10}})}>
          <Desafiante tamanho={200} boca={bD} modo="normal" />
        </Abs>
      )}
      <Abs x={118} y={790}>
        <div style={{transform: `scale(${tk.sx}, ${tk.sy})`, transformOrigin: '50% 90%'}}>
          <Neuro tamanho={210} boca={bN} humor={humorN} bracos={false} />
        </div>
      </Abs>
      <Abs x={940} y={780}>
        <div style={{transform: `scale(${tkR.sx}, ${tkR.sy})`, transformOrigin: '50% 90%'}}>
          <Rival tamanho={220} boca={bR} modo={modoR} />
        </div>
      </Abs>
      {t >= ev.roboEm && t < ev.revelaEm && (
        <Abs x={850} y={612} escala={balao}>
          <div style={{background: '#160a26', border: `5px solid ${ep.rivalCor}`, borderRadius: 26, padding: '6px 22px', fontFamily: TITULO, fontSize: 44, color: ep.rivalCor, whiteSpace: 'nowrap'}}>
            {cena.balao ?? `É ${cena.opcoes[cena.robo].toUpperCase()}!`}
          </div>
        </Abs>
      )}
      <Opcoes itens={cena.opcoes} inicio={0.5} certa={cena.certa} robo={cena.robo} roboEm={ev.roboEm} revelaEm={ev.revelaEm} yBase={nOp === 2 ? 935 : 880} passo={112} />
      <Contagem ini={ev.contaIni} fim={ev.contaFim} y={836} x={540} />
      <Brilhos x={500} y={(nOp === 2 ? 935 : 880) + cena.certa * 112 + 52} k={f - Math.round(ev.revelaEm * 30)} />
      {pontuou && kPonto < 22 && (
        <Abs x={interpolate(kPonto, [0, 20], [540, cena.ponto === 'neuro' ? 470 : 610])} y={interpolate(kPonto, [0, 20], [640, 250], {easing: (x) => 1 - Math.pow(1 - x, 3)})} escala={1.2 - kPonto / 30}>
          <div style={{fontFamily: TITULO, fontSize: 90, color: cena.ponto === 'neuro' ? '#ffd23f' : ep.rivalCor, WebkitTextStroke: '10px #140a24', paintOrder: 'stroke fill'}}>{memoria ? '+30%' : '+1'}</div>
        </Abs>
      )}
      {bug && <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(196,92,255,0.16) 0 3px, transparent 3px 7px)', opacity: 0.6 + 0.4 * Math.sin(f)}} />}
      {bug && <TituloV2 y={600} texto={cena.bugTexto ?? 'ERRO!'} tamanho={92} cor="#ff4d6d" ini={ev.bugEm} />}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

// ================================================================ VISUAIS
const Icone: React.FC<{k: string; s?: number}> = ({k, s = 1}) => {
  const c: Record<string, React.ReactNode> = {
    estrela: <path d="M 0 -55 L 16 -17 L 56 -15 L 25 11 L 35 52 L 0 29 L -35 52 L -25 11 L -56 -15 L -16 -17 Z" fill="#ffd23f" stroke="#fff" strokeWidth={6} />,
    coracao: <path d="M 0 48 C -60 8 -55 -42 -22 -42 C -8 -42 0 -30 0 -22 C 0 -30 8 -42 22 -42 C 55 -42 60 8 0 48 Z" fill="#ff3d6e" stroke="#fff" strokeWidth={6} />,
    lua: <path d="M 20 -50 A 52 52 0 1 0 20 50 A 40 40 0 1 1 20 -50 Z" fill="#c9d8ff" stroke="#fff" strokeWidth={6} />,
    raio: <path d="M 12 -58 L -32 6 L -2 6 L -16 58 L 34 -12 L 4 -12 L 22 -58 Z" fill="#ffb300" stroke="#fff" strokeWidth={6} strokeLinejoin="round" />,
    gota: <path d="M 0 -55 C 30 -15 42 5 42 22 A 42 42 0 0 1 -42 22 C -42 5 -30 -15 0 -55 Z" fill="#4fb4ff" stroke="#fff" strokeWidth={6} />,
    nota: (
      <g fill="#7dff9b" stroke="#fff" strokeWidth={5}>
        <ellipse cx={-14} cy={32} rx={22} ry={16} />
        <path d="M 6 32 L 6 -48 L 36 -36 L 36 -20 L 10 -30" />
      </g>
    ),
  };
  return (
    <svg width={130 * s} height={130 * s} viewBox="-65 -65 130 130" style={{overflow: 'visible'}}>
      {c[k]}
    </svg>
  );
};
const OBJ = ['estrela', 'coracao', 'lua', 'raio', 'gota', 'nota'];

const SETAS = [0, -90, 180, 90, 0]; // graus: direita, cima, esquerda, baixo, direita
const Seta: React.FC<{ang: number; s?: number; cor?: string}> = ({ang, s = 1, cor = '#ffd23f'}) => (
  <svg width={150 * s} height={150 * s} viewBox="-75 -75 150 150">
    <g transform={`rotate(${ang})`}>
      <path d="M -50 -16 L 10 -16 L 10 -42 L 58 0 L 10 42 L 10 16 L -50 16 Z" fill={cor} stroke="#fff" strokeWidth={7} strokeLinejoin="round" />
    </g>
  </svg>
);

const Vaca: React.FC = () => (
  <svg width={360} height={280} viewBox="-180 -140 360 280">
    <ellipse cx={0} cy={30} rx={120} ry={80} fill="#fff" stroke="#140a24" strokeWidth={7} />
    <ellipse cx={-40} cy={10} rx={30} ry={22} fill="#140a24" />
    <ellipse cx={50} cy={50} rx={26} ry={18} fill="#140a24" />
    {[-80, -30, 30, 80].map((x) => <rect key={x} x={x - 10} y={95} width={20} height={40} rx={6} fill="#fff" stroke="#140a24" strokeWidth={6} />)}
    <ellipse cx={-120} cy={-50} rx={55} ry={50} fill="#fff" stroke="#140a24" strokeWidth={7} />
    <ellipse cx={-135} cy={-25} rx={38} ry={24} fill="#ffb3c6" stroke="#140a24" strokeWidth={5} />
    <circle cx={-110} cy={-70} r={7} fill="#140a24" />
    <path d="M -95 -100 l 18 -22 M -150 -98 l -14 -22" stroke="#e8c27a" strokeWidth={10} strokeLinecap="round" />
  </svg>
);

const Visual45: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const ev = cena.eventos;
  const r = ev.revelaEm;
  const rev = t >= r;
  const kr = f - Math.round(r * 30);
  const pop = (atraso: number) => spring({frame: f - Math.round(atraso * 30), fps: 30, config: {damping: 11}});
  switch (cena.visual) {
    case 'objetos': {
      const apagou = t >= ev.apaga;
      const ka = f - Math.round(ev.apaga * 30);
      return (
        <>
          {OBJ.map((k, i) => {
            const x = 280 + (i % 3) * 195, y = 585 + Math.floor(i / 3) * 165;
            const sumiu = k === 'lua' && apagou && !rev;
            return (
              <Abs key={k} x={x} y={y} escala={sumiu ? 1 : pop(0.3 + i * 0.08)}>
                <div style={{width: 160, height: 150, borderRadius: 26, background: 'rgba(15,8,40,0.8)', border: `4px solid ${k === 'lua' && rev ? '#5dff9b' : 'rgba(255,255,255,0.7)'}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                  {sumiu ? <span style={{fontFamily: TITULO, fontSize: 90, color: '#ffd23f'}}>?</span> : <Icone k={k} s={0.95} />}
                </div>
              </Abs>
            );
          })}
          {apagou && ka < 10 && <AbsoluteFill style={{background: `rgba(196,92,255,${0.5 * (1 - ka / 10)})`}} />}
          {t >= ev.memo && !apagou && <Pilula y={480} cor="#7a3df0" tamanho={34}>MEMORIZE!</Pilula>}
        </>
      );
    }
    case 'setas': {
      const passo = 0.62;
      if (t < ev.apaga) {
        const j = Math.floor((t - ev.memo) / passo);
        const ativo = t >= ev.memo && j >= 0 && j < 5;
        const kk = f - Math.round((ev.memo + Math.max(0, j) * passo) * 30);
        return (
          <>
            {ativo && (
              <Abs x={540} y={640} escala={spring({frame: kk, fps: 30, config: {damping: 12, stiffness: 220}})}>
                <Seta ang={SETAS[j]} s={2} />
              </Abs>
            )}
            <div style={{position: 'absolute', left: 390, top: 790, display: 'flex', gap: 16}}>
              {[0, 1, 2, 3, 4].map((i) => (
                <div key={i} style={{width: 44, height: 16, borderRadius: 8, background: ativo && i <= j ? '#ffd23f' : 'rgba(255,255,255,0.25)'}} />
              ))}
            </div>
          </>
        );
      }
      return (
        <div style={{position: 'absolute', left: 205, top: 575, display: 'flex', gap: 12}}>
          {SETAS.map((a, i) => (
            <div key={i} style={{width: 118, height: 118, borderRadius: 22, background: rev && i === 2 ? '#1fb85c' : 'rgba(15,8,40,0.8)', border: '4px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${rev && i === 2 ? 1 + 0.15 * spring({frame: kr, fps: 30, config: {damping: 8}}) : 1})`}}>
              {rev ? <Seta ang={a} s={0.8} cor={i === 2 ? '#fff' : '#ffd23f'} /> : <span style={{fontFamily: TITULO, fontSize: 60, color: i === 2 ? '#ffd23f' : '#fff'}}>{i === 2 ? '3ª' : '?'}</span>}
            </div>
          ))}
        </div>
      );
    }
    case 'fas':
      return (
        <>
          {[Calculino, Miragem, Turbo].map((R, i) => (
            <Abs key={i} x={270 + i * 200} y={660} escala={pop(0.6 + i * 0.1)}>
              <div style={{width: 180, height: 210, borderRadius: 26, background: rev && i === 0 ? '#1fb85c' : 'rgba(15,8,40,0.8)', border: `5px solid ${rev && i === 0 ? '#b9ffd2' : '#fff'}`, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: rev && i !== 0 ? 0.45 : 1}}>
                <R tamanho={200} modo={rev && i === 0 ? 'convencido' : 'normal'} />
              </div>
            </Abs>
          ))}
        </>
      );
    case 'enigma':
      return rev ? (
        <Abs x={540} y={650} escala={spring({frame: kr, fps: 30, config: {damping: 9}})}>
          <svg width={340} height={280} viewBox="-170 -140 340 280">
            <rect x={-120} y={-100} width={240} height={200} rx={20} fill="#4fb4ff" stroke="#fff" strokeWidth={8} />
            {[-60, 0, 60].map((y) => <rect key={y} x={-120} y={y - 8} width={240} height={16} fill="#fff" opacity={0.7} />)}
            {[0, 1, 2, 3].map((i) => <path key={i} d={`M ${-90 + i * 60} ${110 + ((f + i * 7) % 20)} c 8 10 8 18 0 22 c -8 -4 -8 -12 0 -22`} fill="#7fd4ff" />)}
          </svg>
        </Abs>
      ) : (
        <>
          <Texto y={650} tamanho={230} cor="#e7a8ff">
            ?
          </Texto>
          {[0, 1, 2, 3, 4].map((i) => <div key={i} style={{position: 'absolute', left: 330 + i * 100, top: 520 + ((f * 6 + i * 50) % 300), width: 22, height: 32, borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%', background: '#7fd4ff', opacity: 0.8}} />)}
        </>
      );
    case 'noves': {
      const nn = Array.from({length: 100}, (_, i) => i + 1);
      const marcados = nn.filter((n) => String(n).includes('9'));
      const quantos = rev ? Math.min(marcados.length, Math.floor(kr / 1.2)) : 0;
      return (
        <>
          <div style={{position: 'absolute', left: 200, top: 548, width: 680, display: 'grid', gridTemplateColumns: 'repeat(10, 68px)', gridAutoRows: 27}}>
            {nn.map((n) => {
              const ix = marcados.indexOf(n);
              const on = ix >= 0 && ix < quantos;
              return (
                <div key={n} style={{fontFamily: TITULO, fontSize: 21, color: on ? (n === 99 ? '#ff4fd8' : '#ffd23f') : 'rgba(255,255,255,0.75)', textAlign: 'center', transform: `scale(${on ? 1.25 : 1})`}}>
                  {n}
                </div>
              );
            })}
          </div>
          {rev && <Pilula y={845 - 40} cor="#1fb85c" tamanho={34} escala={pop(r + 0.5)}>NOVES: {Math.min(20, quantos + (quantos >= 19 ? 1 : 0))}</Pilula>}
        </>
      );
    }
    case 'cafe': {
      const linhas = 8, h = 36, w = 64;
      const desloc = [0, 16, 32, 16, 0, 16, 32, 16];
      return (
        <>
          <div style={{position: 'absolute', left: 170, top: 510, width: 740, height: linhas * (h + 4), overflow: 'hidden', background: '#888', border: '4px solid #fff', borderRadius: 10}}>
            {Array.from({length: linhas}).map((_, l) => (
              <div key={l} style={{position: 'absolute', left: -w + desloc[l], top: l * (h + 4), height: h, width: 900, display: 'flex'}}>
                {Array.from({length: 14}).map((__, i) => <div key={i} style={{width: w, height: h, background: i % 2 ? '#fff' : '#000'}} />)}
              </div>
            ))}
            {rev &&
              Array.from({length: linhas - 1}).map((_, l) => (
                <div key={`g${l}`} style={{position: 'absolute', left: 0, top: (l + 1) * (h + 4) - 3, height: 4, width: 740 * interpolate(kr, [0, 18], [0, 1], {extrapolateRight: 'clamp'}), background: '#ff2d6f'}} />
              ))}
          </div>
          {rev && kr > 20 && <Pilula y={845} cor="#1fb85c" tamanho={34} escala={pop(r + 0.7)}>TODAS RETAS!</Pilula>}
        </>
      );
    }
    case 'vaca':
      return (
        <Abs x={540} y={660} escala={pop(0.3)}>
          <div style={{transform: `rotate(${Math.sin(f / 6) * 3}deg)`}}>
            <Vaca />
          </div>
        </Abs>
      );
    case 'garrafa':
      if (!rev)
        return (
          <Texto y={650} tamanho={230} cor="#e7a8ff">
            ?
          </Texto>
        );
      return (
        <Abs x={540} y={650} escala={spring({frame: kr, fps: 30, config: {damping: 8}})}>
          {rev ? (
            <svg width={200} height={320} viewBox="-100 -160 200 320">
              <path d="M -24 -150 L 24 -150 L 24 -70 Q 70 -40 70 10 L 70 140 Q 70 155 55 155 L -55 155 Q -70 155 -70 140 L -70 10 Q -70 -40 -24 -70 Z" fill="#5dff9b" opacity={0.85} stroke="#fff" strokeWidth={8} />
              <text x={0} y={-100} textAnchor="middle" fontFamily={TITULO} fontSize={26} fill="#140a24" transform="rotate(-90 0 -100)">
                PESCOÇO
              </text>
            </svg>
          ) : (
            <Texto y={0} tamanho={230} cor="#e7a8ff">
              ?
            </Texto>
          )}
        </Abs>
      );
    default:
      return null;
  }
};

// ================================================================ CENAS
const FimContinua: React.FC<{cena: Cena; extra?: string}> = ({cena, extra}) => {
  const t = useT();
  const f = useCurrentFrame();
  const ult = cena.clipes[cena.clipes.length - 1];
  const tFim = ult.ini + ult.dur;
  if (t < tFim + 0.1) return null;
  const c = spring({frame: f - Math.round((tFim + 0.1) * 30), fps: 30, config: {damping: 9}});
  return (
    <AbsoluteFill style={{background: `rgba(0,0,0,${0.62 * c})`}}>
      <Texto y={800} tamanho={140} cor="#fff" escala={c}>
        CONTINUA...
      </Texto>
      {extra && (
        <Pilula y={950} cor="#e08600" tamanho={44} escala={c}>
          {extra}
        </Pilula>
      )}
      <Pilula y={1060} cor="#ff2d6f" tamanho={46} escala={c}>
        SEGUE O NEURO PRA VER!
      </Pilula>
    </AbsoluteFill>
  );
};

export const GanchoDoutor: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = useT();
  const bD = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const s = spring({frame: f, fps: 30, from: 1.25, to: 1, config: {damping: 11}});
  const g = f < 12 ? (random(`g${f}`) - 0.5) * 40 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${g}px)`}}>
      <Fundo c1="#3a0a5a" c2="#05000a" c3="#c45cff" />
      <Abs x={540} y={720} escala={0.9 + 0.1 * s}>
        <Doutor tamanho={760} boca={bD} modo="convencido" />
      </Abs>
      <Texto y={300} tamanho={130} cor="#e7a8ff" escala={s} rot={-3}>
        ELE VOLTOU!
      </Texto>
      {t >= fl[1] && (
        <Abs x={190} y={1080} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 9}})}>
          <Neuro tamanho={330} boca={bN} humor="surpreso" />
        </Abs>
      )}
      {f < 10 && <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(196,92,255,0.25) 0 3px, transparent 3px 7px)'}} />}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const IntroV2: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const logo = useMola(0.05, {damping: 12});
  return (
    <AbsoluteFill>
      <Fundo c1="#7d3df0" c2="#1a0838" c3="#ffd23f" />
      <Pilula y={235} cor="#ff3d8b" tamanho={48} escala={logo}>
        DESAFIOS DO NEURO
      </Pilula>
      <Pilula y={318} cor="#e08600" tamanho={32} escala={logo}>
        TEMPORADA 2
      </Pilula>
      <Abs x={540} y={690}>
        <Neuro tamanho={620} boca={b} humor={t < fl[1] ? 'rindo' : 'feliz'} aceno />
      </Abs>
      {t >= fl[1] &&
        [0, 1, 2].map((i) => (
          <Abs key={i} x={540 + (i - 1) * 140} y={1060} escala={spring({frame: f - Math.round((fl[1] + 0.15 + i * 0.12) * 30), fps: 30, config: {damping: 8}})}>
            <Coracao tamanho={110} />
          </Abs>
        ))}
      {t >= fl[2] && (
        <Pilula y={1150} cor="#7a3df0" tamanho={50} escala={spring({frame: f - Math.round(fl[2] * 30), fps: 30, config: {damping: 9}})}>
          BORA?
        </Pilula>
      )}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const ApresentaV2: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const bR = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const ult = fl[fl.length - 1];
  const entra = useMola(0, {damping: 10, stiffness: 120});
  return (
    <AbsoluteFill>
      <Fundo c1="#5a1a8a" c2="#05000a" c3="#c45cff" />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(231,168,255,0.22), transparent 70%)', clipPath: 'polygon(42% 0, 58% 0, 88% 66%, 12% 66%)'}} />
      <Abs x={540} y={650} escala={0.7 + 0.3 * entra}>
        <Doutor tamanho={680} boca={bR} modo={t >= fl[1] ? 'convencido' : 'normal'} />
      </Abs>
      <Pilula y={990} cor="#6b1fa8" tamanho={60} escala={useMola(0.3, {damping: 10})}>
        DOUTOR ESQUECIDO
      </Pilula>
      {t >= ult && (
        <>
          <Abs x={170} y={1120} escala={spring({frame: f - Math.round(ult * 30), fps: 30, config: {damping: 10}})}>
            <Neuro tamanho={210} boca={bN} humor="bravo" bracos={false} />
          </Abs>
          <div style={{position: 'absolute', left: 290, top: 1080, width: 640, background: 'rgba(10,6,30,0.9)', border: '4px solid #ffd23f', borderRadius: 24, padding: '12px 20px', fontFamily: TITULO, fontSize: 40, color: '#fff', lineHeight: 1.1, transform: `scale(${spring({frame: f - Math.round(ult * 30), fps: 30, config: {damping: 11}})})`, transformOrigin: 'left center'}}>
            ACERTE PRA PROTEGER A MEMÓRIA!
          </div>
        </>
      )}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const VitoriaV2: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const ep = useEp();
  const R = ep.Rival;
  const b = useBoca('neuro', cena.inicio);
  const conf = useMemo(() => Array.from({length: 80}).map((_, i) => ({x: random(`cx${i}`) * 1080, y: -random(`cy${i}`) * 1900, v: 5 + random(`cv${i}`) * 9, c: ['#ff5c8a', '#ffd23f', '#5ac8ff', '#5dff9b', '#c38bff'][i % 5], r: random(`cr${i}`) * 360})), []);
  const pl = useMola(0.1, {damping: 9});
  const time = cena.tipo === 'vitoriaTime';
  return (
    <AbsoluteFill>
      <Fundo c1="#ff9a1f" c2="#3a0a00" c3="#ffe066" />
      {conf.map((c, i) => (
        <div key={i} style={{position: 'absolute', left: c.x + Math.sin(f / 8 + i) * 30, top: (c.y + f * c.v) % 2100, width: 18, height: 30, background: c.c, transform: `rotate(${c.r + f * 8}deg)`, borderRadius: 4}} />
      ))}
      <TituloV2 y={300} texto={time ? 'CAMPEÕES!' : 'VENCEMOS!'} tamanho={124} />
      <Pilula y={440} cor="#140a24" tamanho={52} escala={pl}>
        {cena.placar ?? 'TORNEIO DOS GÊNIOS'}
      </Pilula>
      {time ? (
        <>
          <Abs x={540} y={640} escala={pl}>
            <Trofeu tamanho={330} />
          </Abs>
          <Abs x={540} y={950}>
            <Neuro tamanho={420} boca={b} humor="rindo" aceno />
          </Abs>
          {[Calculino, Miragem, Turbo].map((A, i) => (
            <Abs key={i} x={[180, 900, 900][i]} y={[1000, 900, 1110][i]} escala={spring({frame: f - 8 - i * 5, fps: 30, config: {damping: 9}})}>
              <div style={{transform: `translateY(${-Math.abs(Math.sin(f / 5 + i)) * 24}px)`}}>
                <A tamanho={230} modo="convencido" />
              </div>
            </Abs>
          ))}
        </>
      ) : (
        <>
          <Abs x={400} y={850}>
            <Neuro tamanho={560} boca={b} humor="rindo" aceno />
          </Abs>
          <Abs x={850} y={1030}>
            <R tamanho={300} modo="erro" />
          </Abs>
        </>
      )}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

const zapPath = (x0: number, y0: number, x1: number, y1: number, seed: number) => {
  const pts = [[x0, y0]];
  for (let i = 1; i < 8; i++) pts.push([x0 + ((x1 - x0) * i) / 8 + (random(`z${seed}${i}`) - 0.5) * 60, y0 + ((y1 - y0) * i) / 8 + (random(`w${seed}${i}`) - 0.5) * 60]);
  pts.push([x1, y1]);
  return 'M ' + pts.map((p) => p.join(' ')).join(' L ');
};

export const GanchoAmnesia: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const bD = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const zap = 2.1;
  const atingido = t >= zap;
  const g = atingido && t < zap + 0.6 ? (random(`g${f}`) - 0.5) * 36 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${g}px)`}}>
      <Fundo c1="#2a0a40" c2="#000" c3="#c45cff" />
      <Abs x={820} y={580}>
        <Doutor tamanho={360} boca={bD} modo={atingido ? 'convencido' : 'normal'} />
      </Abs>
      {t >= zap - 0.6 && t < zap + 0.5 && (
        <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
          <path d={zapPath(780, 560, 480, 870, Math.floor(f / 2))} stroke="#c45cff" strokeWidth={26} fill="none" />
          <path d={zapPath(780, 560, 480, 870, Math.floor(f / 2))} stroke="#fff" strokeWidth={8} fill="none" />
        </svg>
      )}
      <Abs x={460} y={900}>
        <Neuro tamanho={520} boca={bN} humor={atingido ? 'tonto' : 'surpreso'} />
      </Abs>
      {t >= fl[2] && (
        <TituloV2 y={290} texto="O NEURO PERDEU A MEMÓRIA!" tamanho={72} cor="#e7a8ff" ini={fl[2]} />
      )}
      {atingido && t < zap + 0.25 && <AbsoluteFill style={{background: 'rgba(231,168,255,0.6)'}} />}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
      <FimContinua cena={cena} />
    </AbsoluteFill>
  );
};

export const GanchoAmnesiaAbre: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const s = spring({frame: f, fps: 30, from: 1.25, to: 1, config: {damping: 11}});
  const g = f < 10 ? (random(`g${f}`) - 0.5) * 36 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${g}px)`}}>
      <Fundo c1="#4a1a7a" c2="#05000a" c3="#c45cff" />
      <TituloV2 y={300} texto="O NEURO PERDEU A MEMÓRIA!" tamanho={86} cor="#e7a8ff" ini={0} />
      <Abs x={540} y={760} escala={s}>
        <Neuro tamanho={680} boca={b} humor="tonto" />
      </Abs>
      {['?', '?', '?'].map((q, i) => (
        <Texto key={i} y={560 + i * 30} tamanho={110} cor="#ffd23f" escala={1}>
          <span style={{position: 'relative', left: [-330, 330, -280][i], top: [0, 60, 330][i], transform: `rotate(${Math.sin(f / 6 + i) * 15}deg)`, display: 'inline-block'}}>{q}</span>
        </Texto>
      ))}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const IntroAmnesia: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const bN = useBoca('neuro', cena.inicio);
  const bC = useBoca('calculino', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const lembra = t >= fl[2];
  const tk = take(f - Math.round(fl[2] * 30));
  return (
    <AbsoluteFill>
      <Fundo c1="#7d3df0" c2="#1a0838" c3="#ffd23f" />
      <Pilula y={235} cor="#ff3d8b" tamanho={48} escala={useMola(0.05, {damping: 12})}>
        DESAFIOS DO NEURO
      </Pilula>
      <Abs x={lembra ? 540 : 470} y={700}>
        <div style={{transform: `scale(${tk.sx}, ${tk.sy})`, transformOrigin: '50% 85%'}}>
          <Neuro tamanho={560} boca={bN} humor={lembra ? 'rindo' : 'tonto'} aceno={lembra} />
        </div>
      </Abs>
      {!lembra && t < fl[1] && <TituloV2 y={340} texto="EU SOU O... O...?" tamanho={70} cor="#ffd23f" ini={fl[0] + 0.6} />}
      {t >= fl[1] && !lembra && (
        <>
          <Abs x={880} y={860} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 9}})}>
            <Calculino tamanho={330} boca={bC} modo="normal" />
          </Abs>
          <Abs x={760} y={640} escala={spring({frame: f - Math.round(fl[1] * 30) - 4, fps: 30, config: {damping: 9}})}>
            <div style={{background: '#0e1a2a', border: '5px solid #3ff3ff', borderRadius: 26, padding: '6px 22px', fontFamily: TITULO, fontSize: 50, color: '#3ff3ff', whiteSpace: 'nowrap'}}>NEURO!</div>
          </Abs>
        </>
      )}
      {lembra && (
        <>
          <TituloV2 y={340} texto="EU SOU O NEURO!" tamanho={86} cor="#ffd23f" ini={fl[2]} />
          {[0, 1, 2].map((i) => (
            <Abs key={i} x={540 + (i - 1) * 140} y={1080} escala={spring({frame: f - Math.round((fl[2] + 1.6 + i * 0.12) * 30), fps: 30, config: {damping: 8}})}>
              <Coracao tamanho={110} />
            </Abs>
          ))}
        </>
      )}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const TimeReune: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const fl: number[] = cena.eventos.falas;
  const bocas = [useBoca('calculino', cena.inicio), useBoca('miragem', cena.inicio), useBoca('turbo', cena.inicio)];
  const bN = useBoca('neuro', cena.inicio);
  return (
    <AbsoluteFill>
      <Fundo c1="#1f7ad6" c2="#050a20" c3="#7fc8ff" />
      <BarraMemoria valor={0.1} y={250} />
      <TituloV2 y={370} texto="O TIME CHEGOU!" tamanho={96} cor="#ffd23f" ini={0.1} />
      {[Calculino, Miragem, Turbo].map((A, i) => {
        const e = spring({frame: f - 6 - i * 6, fps: 30, config: {damping: 9, stiffness: 120}});
        return (
          <Abs key={i} x={220 + i * 320} y={650 + (1 - e) * 600}>
            <A tamanho={300} boca={bocas[i]} modo="normal" />
          </Abs>
        );
      })}
      <Abs x={540} y={950}>
        <Neuro tamanho={300} boca={bN} humor={t >= fl[2] ? 'feliz' : 'tonto'} />
      </Abs>
      {t >= fl[2] && (
        <Pilula y={1130} cor="#1fb85c" tamanho={40} escala={spring({frame: f - Math.round(fl[2] * 30), fps: 30, config: {damping: 10}})}>
          3 DESAFIOS = MEMÓRIA DE VOLTA
        </Pilula>
      )}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const VsBatalha: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const bD = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const sl = spring({frame: f, fps: 30, config: {damping: 12}});
  const vs = spring({frame: f - 10, fps: 30, from: 2, to: 1, config: {damping: 9}});
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{background: 'linear-gradient(160deg,#2a0a40 0 50%,#5a1aa8 50% 100%)'}} />
      <Abs x={540 + (1 - sl) * 700} y={520}>
        <Doutor tamanho={600} boca={bD} modo="convencido" />
      </Abs>
      <Abs x={360 - (1 - sl) * 700} y={1000}>
        <Neuro tamanho={420} boca={bN} humor="bravo" />
      </Abs>
      {[Calculino, Miragem, Turbo].map((A, i) => (
        <Abs key={i} x={700 + i * 120 - (1 - sl) * 700} y={1070}>
          <A tamanho={180} modo="convencido" />
        </Abs>
      ))}
      {f >= 10 && (
        <Texto y={800} tamanho={200} cor="#ffd23f" escala={vs}>
          VS
        </Texto>
      )}
      <TituloV2 y={250} texto="BATALHA FINAL" tamanho={84} cor="#fff" ini={0.1} />
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const SuperAtaque: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const bN = useBoca('neuro', cena.inicio);
  const impacto = 1.6;
  const ko = 2.6;
  const origens: [number, number][] = [[540, 1020], [190, 1040], [890, 960], [890, 1150]];
  const g = t >= impacto && t < ko ? (random(`g${f}`) - 0.5) * 30 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${g}px)`}}>
      <Fundo c1="#3a0a5a" c2="#05000a" c3="#ffd23f" />
      {t < ko ? (
        <Abs x={540} y={420}>
          <Doutor tamanho={420} modo={t >= impacto ? 'erro' : 'convencido'} />
        </Abs>
      ) : (
        Array.from({length: 14}).map((_, i) => {
          const a = i * 0.45, r = (f - ko * 30) * 22;
          return <div key={i} style={{position: 'absolute', left: 540 + r * Math.cos(a) - 14, top: 420 + r * Math.sin(a) - 14, width: 28, height: 28, background: '#ffd23f', transform: `rotate(45deg)`}} />;
        })
      )}
      {t >= 0.4 && t < ko && (
        <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
          {origens.map(([x, y], i) => {
            const p = interpolate(t, [0.4, impacto], [0, 1], {extrapolateRight: 'clamp'});
            const cor = ['#ff6fa8', '#3ff3ff', '#ff4fd8', '#ffd000'][i];
            return (
              <g key={i}>
                <line x1={x} y1={y - 60} x2={x + (540 - x) * p} y2={y - 60 + (420 - (y - 60)) * p} stroke={cor} strokeWidth={34} strokeLinecap="round" />
                <line x1={x} y1={y - 60} x2={x + (540 - x) * p} y2={y - 60 + (420 - (y - 60)) * p} stroke="#fff" strokeWidth={10} strokeLinecap="round" />
              </g>
            );
          })}
        </svg>
      )}
      <Abs x={540} y={1020}>
        <Neuro tamanho={330} boca={bN} humor="bravo" />
      </Abs>
      {[Calculino, Miragem, Turbo].map((A, i) => (
        <Abs key={i} x={origens[i + 1][0]} y={origens[i + 1][1]}>
          <A tamanho={220} modo="convencido" />
        </Abs>
      ))}
      {t >= impacto && t < impacto + 0.25 && <AbsoluteFill style={{background: 'rgba(255,255,255,0.75)'}} />}
      {t >= ko && <Texto y={430} tamanho={200} cor="#ff4d6d" escala={spring({frame: f - Math.round(ko * 30), fps: 30, config: {damping: 8}})}>K.O.!</Texto>}
      {t < ko && <TituloV2 y={700} texto="SUPER ATAQUE DO TIME!" tamanho={70} cor="#ffd23f" ini={0.2} />}
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const Convite: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const voa = spring({frame: f - 6, fps: 30, config: {damping: 12, stiffness: 90}});
  const abre = spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 10}});
  return (
    <AbsoluteFill>
      <Fundo c1="#0d3a6e" c2="#020814" c3="#ffd23f" />
      <Abs x={540 + (1 - voa) * 900} y={740} rot={(1 - voa) * 40}>
        <div style={{width: 640, height: 420, position: 'relative'}}>
          {t >= fl[1] && (
            <div style={{position: 'absolute', left: 40, top: -300 * abre, width: 560, height: 340, background: '#fff8e1', borderRadius: 18, border: '6px solid #e0a800', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: TITULO, color: '#140a24', textAlign: 'center'}}>
              <div style={{fontSize: 40, color: '#b07a00'}}>CONVITE</div>
              <div style={{fontSize: 58, lineHeight: 1.05}}>TORNEIO MUNDIAL DOS GÊNIOS</div>
            </div>
          )}
          <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(160deg,#f6e2a8,#d9b45a)', borderRadius: 20, border: '6px solid #fff'}} />
          <div style={{position: 'absolute', left: 0, top: 0, width: 640, height: 420, clipPath: 'polygon(0 0, 100% 0, 50% 55%)', background: '#e8c66e'}} />
          <div style={{position: 'absolute', left: 280, top: 180, width: 80, height: 80, borderRadius: 40, background: '#c62828', border: '5px solid #ffd23f'}} />
        </div>
      </Abs>
      <Abs x={540} y={1120}>
        <Neuro tamanho={280} boca={b} humor={t >= fl[1] ? 'surpreso' : 'feliz'} />
      </Abs>
      <Legendas clipes={cena.clipes} y={LEG_Y} />
      <FimContinua cena={cena} extra="TEMPORADA 3?" />
    </AbsoluteFill>
  );
};

export const EXTRA45 = {
  rodada: RodadaV2,
  ganchoDoutor: GanchoDoutor,
  introCurta: IntroV2,
  apresentaRival: ApresentaV2,
  vitoriaGen: VitoriaV2,
  vitoriaTime: VitoriaV2,
  ganchoAmnesia: GanchoAmnesia,
  ganchoAmnesiaAbre: GanchoAmnesiaAbre,
  introAmnesia: IntroAmnesia,
  timeReune: TimeReune,
  vsBatalha: VsBatalha,
  superAtaque: SuperAtaque,
  convite: Convite,
};
