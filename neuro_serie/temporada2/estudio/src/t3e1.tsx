import React, {useId, useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame} from 'remotion';
import type {TransitionPresentation, TransitionPresentationComponentProps} from '@remotion/transitions';
import {Neuro} from './personagens';
import {Coracao, Legendas, Pilula, Texto, TITULO} from './ui';
import {Abs, useBoca, useT} from './cenas';
import type {Cena} from './cenas';
import type {RivalProps} from './ctx';
import {iris, whip} from './ep45';

// Temporada 3 — planejado com a skill video-plan-editor (preset viral) + regras do HyperFrames.
const LEG_Y = 1222;

// ================================================================ TRANSICOES (todas com causa)
type V = Record<string, never>;
/** zoom atraves do olho/porta: a cena que sai cresce e borra, a nova assenta vindo grande */
const ZoomComp: React.FC<TransitionPresentationComponentProps<V>> = ({children, presentationDirection, presentationProgress: p}) =>
  presentationDirection === 'exiting' ? (
    <AbsoluteFill style={{transform: `scale(${1 + p * p * 5})`, transformOrigin: '50% 34%', filter: `blur(${p * 18}px)`, opacity: 1 - Math.max(0, p - 0.6) * 2.5}}>{children}</AbsoluteFill>
  ) : (
    <AbsoluteFill style={{transform: `scale(${1.35 - 0.35 * p})`, filter: `blur(${(1 - p) * 14}px)`, opacity: Math.min(1, p * 2.2)}}>{children}</AbsoluteFill>
  );
export const zoomAtraves = (): TransitionPresentation<V> => ({component: ZoomComp, props: {}});
/** giro com zoom (classico de edicao de TikTok) */
const GiroComp: React.FC<TransitionPresentationComponentProps<V>> = ({children, presentationDirection, presentationProgress: p}) =>
  presentationDirection === 'exiting' ? (
    <AbsoluteFill style={{transform: `rotate(${p * 30}deg) scale(${1 + p * 0.8})`, filter: `blur(${p * 16}px)`, opacity: 1 - p}}>{children}</AbsoluteFill>
  ) : (
    <AbsoluteFill style={{transform: `rotate(${(1 - p) * -30}deg) scale(${1.6 - 0.6 * p})`, filter: `blur(${(1 - p) * 16}px)`}}>{children}</AbsoluteFill>
  );
export const giro = (): TransitionPresentation<V> => ({component: GiroComp, props: {}});
/** corte com falha (glitch RGB) */
const GlitchComp: React.FC<TransitionPresentationComponentProps<V>> = ({children, presentationDirection, presentationProgress: p}) => {
  const f = useCurrentFrame();
  const forca = Math.sin(Math.PI * p);
  const dx = (random(`gx${f}${presentationDirection}`) - 0.5) * 80 * forca;
  const vis = presentationDirection === 'exiting' ? p < 0.5 : p >= 0.5;
  return (
    <AbsoluteFill style={{opacity: vis ? 1 : 0, transform: `translateX(${dx}px)`, filter: `hue-rotate(${forca * 90}deg) saturate(${1 + forca * 2})`}}>
      {children}
      {vis && forca > 0.2 && <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(255,0,80,0.25) 0 4px, rgba(0,255,255,0.18) 4px 9px, transparent 9px 16px)'}} />}
    </AbsoluteFill>
  );
};
export const glitch = (): TransitionPresentation<V> => ({component: GlitchComp, props: {}});
/** flash branco no meio */
const FlashComp: React.FC<TransitionPresentationComponentProps<V>> = ({children, presentationDirection, presentationProgress: p}) => {
  const vis = presentationDirection === 'exiting' ? p < 0.5 : p >= 0.5;
  return (
    <AbsoluteFill style={{opacity: vis ? 1 : 0}}>
      {children}
      {vis && <AbsoluteFill style={{background: '#fff', opacity: 1 - Math.abs(p - 0.5) * 2}} />}
    </AbsoluteFill>
  );
};
export const flash = (): TransitionPresentation<V> => ({component: FlashComp, props: {}});
// uma por costura, na ordem das cenas (gancho→intro→esfinge→e1→e2→e3→cta→continua)
export const TRANS_T3E1 = [zoomAtraves, whip, giro, whip, giro, glitch, flash, iris];

// ================================================================ TEXTURA: grao de filme
export const Grao: React.FC<{forca?: number}> = ({forca = 0.1}) => {
  const f = useCurrentFrame();
  const id = useId().replace(/:/g, '');
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity: forca, mixBlendMode: 'overlay'}}>
      <svg width={1080} height={1920}>
        <filter id={`g${id}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={Math.floor(f / 2) % 50} />
        </filter>
        <rect width={1080} height={1920} filter={`url(#g${id})`} />
      </svg>
    </AbsoluteFill>
  );
};

// ================================================================ CENARIO DO EGITO (camadas + camera)
export const Egito: React.FC<{camera?: number; noite?: number}> = ({camera = 0, noite = 0}) => {
  const f = useCurrentFrame();
  const estrelas = useMemo(() => Array.from({length: 60}).map((_, i) => ({x: random(`ex${i}`) * 1080, y: random(`ey${i}`) * 900, r: 1 + random(`er${i}`) * 3})), []);
  const p = (f / 30) * 0.02 + camera; // push-in lento
  const camada = (k: number) => ({transform: `scale(${1 + p * k}) translateY(${-p * k * 40}px)`, transformOrigin: '50% 60%'});
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: `linear-gradient(180deg, #120a3a 0%, #3b1d6e 45%, #d9783a 78%, #f2b75c 100%)`}}>
      <AbsoluteFill style={camada(0.3)}>
        {estrelas.map((e, i) => (
          <div key={i} style={{position: 'absolute', left: e.x, top: e.y, width: e.r * 2, height: e.r * 2, borderRadius: '50%', background: '#fff', opacity: 0.5 + 0.5 * Math.sin(f / 9 + i)}} />
        ))}
        <div style={{position: 'absolute', left: 760, top: 260, width: 150, height: 150, borderRadius: '50%', background: '#fff3c4', boxShadow: '0 0 90px 30px rgba(255,236,170,0.45)'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{...camada(0.6), filter: 'blur(3px)'}}>
        <svg width={1080} height={1920}>
          <polygon points="80,1150 330,820 580,1150" fill="#7a3d2a" />
          <polygon points="330,820 580,1150 450,1150" fill="#5a2a1c" />
          <polygon points="620,1150 820,900 1020,1150" fill="#8a4630" />
          <polygon points="820,900 1020,1150 910,1150" fill="#62301f" />
        </svg>
      </AbsoluteFill>
      <AbsoluteFill style={camada(1)}>
        <svg width={1080} height={1920}>
          <path d="M 0 1180 Q 270 1080 540 1170 Q 810 1260 1080 1140 L 1080 1920 L 0 1920 Z" fill="#c9783c" />
          <path d="M 0 1330 Q 360 1220 720 1330 Q 900 1380 1080 1300 L 1080 1920 L 0 1920 Z" fill="#a85a2a" />
        </svg>
      </AbsoluteFill>
      <AbsoluteFill style={{background: `rgba(10,4,30,${noite})`}} />
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 42%, transparent 50%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

// ================================================================ A ESFINGE
export const Esfinge: React.FC<RivalProps & {brilho?: number}> = ({tamanho, boca = 0, modo = 'normal', silhueta = false, brilho = 0}) => {
  const f = useCurrentFrame();
  const id = useId().replace(/:/g, '');
  const pedra = modo === 'erro';
  const S = (c: string) => (silhueta ? '#0c0718' : pedra ? '#8d8a86' : c);
  const olho = pedra ? '#555' : modo === 'convencido' || brilho > 0 ? '#7dfcff' : '#ffd23f';
  const tremor = pedra ? Math.sin(f * 2.4) * 4 : 0;
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id={`ouro${id}`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#ffe08a" />
          <stop offset="100%" stopColor="#c98a1a" />
        </linearGradient>
        <filter id={`luz${id}`} x="-60%" y="-60%" width="220%" height="220%">
          <feGaussianBlur stdDeviation={6 + brilho * 10} result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <g transform={`translate(${tremor} 0)`}>
        {/* nemes (toucado listrado) */}
        <path d="M -175 -60 Q -150 -215 0 -228 Q 150 -215 175 -60 L 215 175 L 95 120 L 70 -10 L -70 -10 L -95 120 L -215 175 Z" fill={S('#2d5bd6')} stroke={S('#14286b')} strokeWidth={7} />
        {!silhueta &&
          !pedra &&
          [-150, -110, -70, 70, 110, 150].map((x, i) => <path key={i} d={`M ${x} -120 L ${x * 1.25} 160`} stroke="#ffd23f" strokeWidth={14} opacity={0.9} />)}
        {/* rosto */}
        <path d="M -95 -150 Q 0 -190 95 -150 L 100 40 Q 0 140 -100 40 Z" fill={silhueta ? '#0c0718' : pedra ? '#a29e98' : `url(#ouro${id})`} stroke={S('#7a4e0e')} strokeWidth={6} />
        <path d="M -95 -150 Q 0 -190 95 -150 L 95 -118 Q 0 -150 -95 -118 Z" fill={S('#ffd23f')} />
        {/* olhos com delineado */}
        {[-45, 45].map((x) => (
          <g key={x}>
            {!silhueta && <path d={`M ${x - 34} -45 Q ${x} -72 ${x + 34} -45 Q ${x} -30 ${x - 34} -45 L ${x + (x < 0 ? -50 : 50)} -40`} fill={pedra ? '#888' : '#fff'} stroke="#1b1033" strokeWidth={6} />}
            <ellipse cx={x} cy={-48} rx={13} ry={12 - (f % 110 < 4 && !pedra ? 10 : 0)} fill={olho} filter={`url(#luz${id})`} />
          </g>
        ))}
        {/* nariz e boca */}
        {!silhueta && <path d="M 0 -40 L -14 15 L 14 15 Z" fill="rgba(0,0,0,0.15)" />}
        <ellipse cx={0} cy={58} rx={30} ry={5 + boca * 22} fill={silhueta ? '#7dfcff' : pedra ? '#555' : '#5a1020'} stroke={S('#3a0a14')} strokeWidth={5} />
        {/* barba farao */}
        <rect x={-14} y={100} width={28} height={60} rx={8} fill={S('#2d5bd6')} stroke={S('#14286b')} strokeWidth={5} />
        {/* rachaduras quando vira pedra */}
        {pedra && (
          <g stroke="#3a3530" strokeWidth={6} fill="none" strokeLinecap="round">
            <path d="M -60 -170 L -30 -100 L -55 -40 L -20 30" />
            <path d="M 70 -160 L 40 -80 L 75 -20" />
            <path d="M 0 120 L 25 60 L -10 20" />
          </g>
        )}
      </g>
    </svg>
  );
};

// ================================================================ ICONES DO ENIGMA 3
const Camelo: React.FC<{s?: number}> = ({s = 1}) => (
  <svg width={110 * s} height={90 * s} viewBox="-60 -50 120 100">
    <ellipse cx={0} cy={0} rx={42} ry={22} fill="#d9a05b" stroke="#fff" strokeWidth={4} />
    <circle cx={-14} cy={-18} r={15} fill="#d9a05b" />
    <circle cx={14} cy={-16} r={13} fill="#d9a05b" />
    <path d="M 38 -6 Q 52 -30 46 -44" stroke="#d9a05b" strokeWidth={12} fill="none" strokeLinecap="round" />
    <ellipse cx={50} cy={-44} rx={12} ry={8} fill="#d9a05b" />
    {[-28, -12, 12, 28].map((x) => <rect key={x} x={x - 4} y={14} width={8} height={30} rx={3} fill="#c48a48" />)}
  </svg>
);
const Piramide: React.FC<{s?: number}> = ({s = 1}) => (
  <svg width={100 * s} height={90 * s} viewBox="-50 -45 100 90">
    <polygon points="0,-40 46,38 -46,38" fill="#e2b04a" stroke="#fff" strokeWidth={4} />
    <polygon points="0,-40 46,38 12,38" fill="#b9832a" />
  </svg>
);
const Sol: React.FC<{s?: number}> = ({s = 1}) => (
  <svg width={100 * s} height={100 * s} viewBox="-50 -50 100 100">
    {Array.from({length: 8}).map((_, i) => (
      <line key={i} x1={0} y1={-30} x2={0} y2={-44} stroke="#ffb300" strokeWidth={7} strokeLinecap="round" transform={`rotate(${i * 45})`} />
    ))}
    <circle r={24} fill="#ffd23f" stroke="#fff" strokeWidth={4} />
  </svg>
);
const ICON: Record<string, React.FC<{s?: number}>> = {c: Camelo, p: Piramide, s: Sol};
const LINHAS: [string[], string][] = [
  [['c', '+', 'c', '+', 'c'], '15'],
  [['p', '+', 'p', '+', 'c'], '11'],
  [['s', '+', 's', '+', 'p'], '7'],
  [['s', '+', 'c', '×', 'p'], '?'],
];

// ================================================================ VISUAIS DAS RODADAS
const Boneco: React.FC<{tipo: 'bebe' | 'adulto' | 'idoso'}> = ({tipo}) => (
  <svg width={150} height={170} viewBox="-75 -85 150 170">
    <g stroke="#fff" strokeWidth={9} strokeLinecap="round" fill="none">
      {tipo === 'bebe' ? (
        <>
          <circle cx={-38} cy={-8} r={16} fill="#fff" />
          <path d="M -22 0 L 30 0" />
          <path d="M -15 0 L -22 40 M 0 0 L 6 40 M 22 0 L 16 40 M 30 0 L 40 40" />
        </>
      ) : (
        <>
          <circle cx={0} cy={-62} r={16} fill="#fff" />
          <path d={tipo === 'idoso' ? 'M 0 -44 Q 10 -10 6 22' : 'M 0 -44 L 0 22'} />
          <path d="M 0 -26 L -26 0 M 0 -26 L 26 0" />
          <path d="M 4 22 L -18 70 M 4 22 L 26 70" />
          {tipo === 'idoso' && <path d="M 26 0 L 40 72" stroke="#ffd23f" />}
        </>
      )}
    </g>
  </svg>
);

const VPernas: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const r = cena.eventos.revelaEm;
  const rev = t >= r;
  const etapas: [string, string, 'bebe' | 'adulto' | 'idoso', string][] = [
    ['MANHÃ', '4', 'bebe', '#ffb36b'],
    ['TARDE', '2', 'adulto', '#ffd23f'],
    ['NOITE', '3', 'idoso', '#9b8cff'],
  ];
  return (
    <>
      {etapas.map(([nome, n, tipo, cor], i) => {
        const e = spring({frame: f - 14 - i * 5, fps: 30, config: {damping: 12}});
        const er = spring({frame: f - Math.round((r + 0.3 + i * 0.35) * 30), fps: 30, config: {damping: 10}});
        return (
          <Abs key={i} x={255 + i * 222} y={668} escala={e}>
            <div style={{width: 200, height: 225, borderRadius: 28, background: 'rgba(20,8,40,0.82)', border: `5px solid ${cor}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'space-between', padding: '10px 0', fontFamily: TITULO}}>
              <div style={{fontSize: 34, color: cor}}>{nome}</div>
              {rev ? (
                <div style={{transform: `scale(${er})`}}>
                  <Boneco tipo={tipo} />
                </div>
              ) : (
                <div style={{fontSize: 110, color: '#fff', lineHeight: 1}}>{n}</div>
              )}
              <div style={{fontSize: 28, color: '#fff'}}>{rev ? '' : 'PERNAS'}</div>
            </div>
          </Abs>
        );
      })}
    </>
  );
};

const VEscuro: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const r = cena.eventos.revelaEm;
  const k = interpolate(t, [r + 0.2, r + 1.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Abs x={540} y={680}>
        <svg width={420} height={300} viewBox="-210 -150 420 300">
          <circle cx={0} cy={0} r={90 - k * 40} fill="#ffd23f" opacity={1 - k * 0.8} />
          <path d="M -60 70 L 60 70 L 0 -40 Z" fill="#7a3d2a" opacity={1 - k} />
          <ellipse cx={0} cy={110} rx={150 + k * 60} ry={20 + k * 10} fill="#000" opacity={0.4 + k * 0.6} />
        </svg>
      </Abs>
      {k > 0 && <AbsoluteFill style={{background: `radial-gradient(circle at 50% 36%, transparent ${Math.max(0, 40 - k * 40)}%, rgba(0,0,0,${0.85 * k}) ${Math.max(10, 70 - k * 50)}%)`}} />}
    </>
  );
};

const VIcones: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const ev = cena.eventos;
  const r = ev.revelaEm;
  const rev = t >= r;
  const valores: Record<string, string> = {c: '5', p: '3', s: '2'};
  return (
    <div style={{position: 'absolute', left: 80, top: 452, width: 700}}>
      {LINHAS.map(([itens, res], li) => {
        const ini = (ev.linhas ?? 0.6) + li * 0.4;
        const e = spring({frame: f - Math.round(ini * 30), fps: 30, config: {damping: 11, stiffness: 160}});
        if (t < ini) return null;
        const ultima = li === 3;
        return (
          <div key={li} style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, height: 80, marginBottom: 4, transform: `scale(${e})`, background: ultima ? 'rgba(255,210,63,0.16)' : 'rgba(20,8,40,0.6)', borderRadius: 22, border: ultima ? '4px solid #ffd23f' : '3px solid rgba(255,255,255,0.3)'}}>
            {itens.map((x, i) => {
              const I = ICON[x];
              return I ? (
                <div key={i} style={{position: 'relative'}}>
                  <I s={0.72} />
                  {rev && (
                    <div style={{position: 'absolute', right: -6, top: -6, background: '#1fb85c', color: '#fff', fontFamily: TITULO, fontSize: 26, borderRadius: 14, padding: '0 8px', transform: `scale(${spring({frame: f - Math.round((r + 0.2) * 30), fps: 30, config: {damping: 9}})})`}}>{valores[x]}</div>
                  )}
                </div>
              ) : (
                <span key={i} style={{fontFamily: TITULO, fontSize: 56, color: x === '×' && rev ? '#ff4d6d' : '#fff'}}>
                  {x}
                </span>
              );
            })}
            <span style={{fontFamily: TITULO, fontSize: 56, color: ultima ? '#ffd23f' : '#fff', marginLeft: 8}}>= {ultima && rev ? '17' : res}</span>
          </div>
        );
      })}
    </div>
  );
};
export const VISUAIS_T3 = {pernas: VPernas, escuro: VEscuro, icones: VIcones};

// ================================================================ CENAS
export const GanchoEsfinge: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = useT();
  const bE = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const punch = spring({frame: f, fps: 30, from: 1.6, to: 1.15, config: {damping: 13}});
  const brilho = interpolate(f, [0, 8], [1, 0.3], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill>
      <Egito noite={0.35} />
      <Abs x={540} y={820} escala={punch}>
        <Esfinge tamanho={900} boca={bE} brilho={brilho} />
      </Abs>
      <Texto y={290} tamanho={104} cor="#fff" escala={1}>
        RESPONDA…
      </Texto>
      <Texto y={410} tamanho={124} cor="#7dfcff" rot={-3}>
        OU VIRE PEDRA
      </Texto>
      {t >= fl[1] && (
        <>
          <Abs x={170} y={1080} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 9}})}>
            <Neuro tamanho={270} boca={bN} humor="surpreso" />
          </Abs>
          <Pilula y={1110} x={640} cor="#ff2d6f" tamanho={40} escala={spring({frame: f - Math.round(fl[1] * 30) - 3, fps: 30, config: {damping: 9}})}>
            QUASE NINGUÉM PASSA DO 3º
          </Pilula>
        </>
      )}
      {f >= 2 && f < 6 && <AbsoluteFill style={{background: 'rgba(125,252,255,0.3)'}} />}
      <Grao />
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const IntroMundo: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = useT();
  const b = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const zoom = interpolate(t, [fl[1], fl[1] + 0.9], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (x) => x * x * (3 - 2 * x)});
  return (
    <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 35%, #2a3f9e, #070b22 75%)'}}>
      <Pilula y={235} cor="#ff3d8b" tamanho={46} escala={spring({frame: f - 2, fps: 30, config: {damping: 12}})}>
        DESAFIOS DO NEURO
      </Pilula>
      <Pilula y={312} cor="#e08600" tamanho={32} escala={spring({frame: f - 6, fps: 30, config: {damping: 12}})}>
        TEMPORADA 3 • TORNEIO MUNDIAL
      </Pilula>
      {/* globo: gira e da zoom ate o Egito */}
      <Abs x={540} y={640} escala={1 + zoom * 1.6}>
        <svg width={420} height={420} viewBox="-210 -210 420 420" style={{overflow: 'visible'}}>
          <circle r={200} fill="#1f6fd6" stroke="#fff" strokeWidth={6} />
          {[0, 1, 2].map((i) => {
            const x = ((f * 2.2 + i * 160) % 480) - 240;
            return <path key={i} d={`M ${x - 60} -80 q 40 -50 90 -10 q 30 40 -10 80 q -60 30 -80 -70`} fill="#3fbf6a" opacity={Math.abs(x) < 190 ? 1 : 0} />;
          })}
          <path d="M 10 -40 q 50 -20 70 30 q -10 60 -60 50 q -30 -40 -10 -80" fill="#e2b04a" opacity={zoom} />
          {zoom > 0.5 && (
            <g transform="translate(45 5)">
              <circle r={14} fill="#ff2d6f" stroke="#fff" strokeWidth={4} />
            </g>
          )}
        </svg>
      </Abs>
      {t >= fl[1] && (
        <Pilula y={900} cor="#c98a1a" tamanho={50} escala={spring({frame: f - Math.round((fl[1] + 0.5) * 30), fps: 30, config: {damping: 9}})}>
          FASE 1: EGITO
        </Pilula>
      )}
      <Abs x={200} y={1040}>
        <Neuro tamanho={330} boca={b} humor={t < fl[1] ? 'rindo' : 'feliz'} aceno />
      </Abs>
      {t >= fl[2] &&
        [0, 1, 2].map((i) => (
          <Abs key={i} x={560 + i * 120} y={1060} escala={spring({frame: f - Math.round((fl[2] + 0.1 + i * 0.1) * 30), fps: 30, config: {damping: 8}})}>
            <Coracao tamanho={96} />
          </Abs>
        ))}
      <Grao forca={0.08} />
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const ApresentaEsfinge: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = useT();
  const b = useBoca('robo', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const sobe = spring({frame: f, fps: 30, config: {damping: 14, stiffness: 70}});
  return (
    <AbsoluteFill>
      <Egito camera={0.02} />
      <Abs x={540} y={720 + (1 - sobe) * 700} escala={1 + (1 - sobe) * 0.2}>
        <Esfinge tamanho={760} boca={b} modo={t >= fl[1] ? 'convencido' : 'normal'} />
      </Abs>
      <Pilula y={1110} cor="#2d5bd6" tamanho={60} escala={spring({frame: f - 10, fps: 30, config: {damping: 10}})}>
        A ESFINGE
      </Pilula>
      {t >= fl[1] && (
        <Texto y={300} tamanho={96} cor="#d8d4cc" rot={-4} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 8}})}>
          ERROU = PEDRA
        </Texto>
      )}
      <Grao />
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const CtaPedra: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const poeira = useMemo(() => Array.from({length: 40}).map((_, i) => ({a: random(`pa${i}`) * 6.28, v: 6 + random(`pv${i}`) * 14, r: 10 + random(`pr${i}`) * 30})), []);
  const tremor = f < 16 ? Math.sin(f * 3) * 14 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${tremor}px)`}}>
      <Egito noite={0.2} />
      <Abs x={540} y={560}>
        <Esfinge tamanho={560} modo="erro" />
      </Abs>
      {poeira.map((p, i) => (
        <div key={i} style={{position: 'absolute', left: 540 + Math.cos(p.a) * f * p.v - p.r, top: 600 + Math.sin(p.a) * f * p.v * 0.6 - p.r, width: p.r * 2, height: p.r * 2, borderRadius: '50%', background: '#b8aa98', opacity: Math.max(0, 0.8 - f / 40)}} />
      ))}
      <Texto y={260} tamanho={110} cor="#5dff9b" escala={spring({frame: f - 3, fps: 30, config: {damping: 9}})}>
        3 DE 3!
      </Texto>
      <Abs x={260} y={1020}>
        <Neuro tamanho={380} boca={b} humor="rindo" aceno />
      </Abs>
      <div style={{position: 'absolute', left: 470, top: 960, width: 470, transform: `scale(${spring({frame: f - 10, fps: 30, config: {damping: 10}})})`, transformOrigin: 'left center', background: 'rgba(10,6,30,0.9)', border: '5px solid #ffd23f', borderRadius: 28, padding: '14px 20px', fontFamily: TITULO, fontSize: 46, color: '#fff', lineHeight: 1.1}}>
        QUANTOS VOCÊ ACERTOU?
        <div style={{color: '#ffd23f', fontSize: 40}}>COMENTA AÍ!</div>
      </div>
      <Grao />
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const PortaLabirinto: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const t = useT();
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const abre = interpolate(t, [0.2, 1.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (x) => 1 - Math.pow(1 - x, 3)});
  const push = interpolate(t, [1.2, 5], [1, 1.5], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const ult = cena.clipes[cena.clipes.length - 1];
  const fim = ult.ini + ult.dur;
  const cont = spring({frame: f - Math.round((fim + 0.1) * 30), fps: 30, config: {damping: 9}});
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{transform: `scale(${push})`, transformOrigin: '50% 45%'}}>
        <Egito noite={0.45} />
        <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
          <polygon points="140,1150 540,420 940,1150" fill="#b98a3a" stroke="#6b4a1a" strokeWidth={8} />
          <rect x={430} y={820} width={220} height={330} fill="#08050f" />
          {/* labirinto brilhando la dentro */}
          <g stroke="#7dfcff" strokeWidth={6} fill="none" opacity={0.3 + abre * 0.7} style={{filter: 'drop-shadow(0 0 10px #7dfcff)'}}>
            <path d="M 450 1130 L 450 860 L 630 860 L 630 1100 L 480 1100 L 480 890 L 600 890 L 600 1070 L 510 1070 L 510 920 L 570 920 L 570 1040" />
          </g>
          <rect x={430 - abre * 110} y={820} width={110} height={330} fill="#d9a85a" stroke="#6b4a1a" strokeWidth={6} />
          <rect x={540 + abre * 110} y={820} width={110} height={330} fill="#d9a85a" stroke="#6b4a1a" strokeWidth={6} />
        </svg>
      </AbsoluteFill>
      {t >= fl[1] && (
        <Abs x={830} y={1080} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 9}})}>
          <Neuro tamanho={300} boca={bN} humor="surpreso" />
        </Abs>
      )}
      {t >= fl[0] && t < fim + 0.1 && (
        <Texto y={300} tamanho={86} cor="#7dfcff" escala={spring({frame: f - Math.round(fl[0] * 30), fps: 30, config: {damping: 10}})}>
          BEM-VINDO AO LABIRINTO…
        </Texto>
      )}
      {t >= fim + 0.1 && (
        <AbsoluteFill style={{background: `rgba(0,0,0,${0.62 * cont})`}}>
          <Texto y={780} tamanho={140} cor="#fff" escala={cont}>
            CONTINUA...
          </Texto>
          <Pilula y={930} cor="#e08600" tamanho={44} escala={cont}>
            FASE 2: GRÉCIA
          </Pilula>
          <Pilula y={1040} cor="#ff2d6f" tamanho={46} escala={cont}>
            SEGUE O NEURO PRA VER!
          </Pilula>
        </AbsoluteFill>
      )}
      <Grao />
      <Legendas clipes={cena.clipes} y={LEG_Y} />
    </AbsoluteFill>
  );
};

export const EXTRA_T3E1 = {
  ganchoEsfinge: GanchoEsfinge,
  introMundo: IntroMundo,
  apresentaEsfinge: ApresentaEsfinge,
  ctaPedra: CtaPedra,
  portaLabirinto: PortaLabirinto,
};
