import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, Sequence, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {createTikTokStyleCaptions} from '@remotion/captions';
import type {Caption, TikTokPage} from '@remotion/captions';
import {useEp} from './ctx';

export const TITULO = 'Lilita One';
export const CORPO = 'Nunito';

// Zonas seguras (skill short-video-distribution): nada importante nos 10% de cima (0-192px)
// nem nos 20% de baixo (1536px+), e longe da coluna de botoes da direita.
export const ZONA = {topo: 200, base: 1520, direita: 940};

export type Clipe = {quem: string; texto: string; ini: number; dur: number; palavras: [string, number, number][]};

/** spring a partir de um frame de inicio (em segundos locais) */
export const useMola = (inicioSeg: number, cfg: {damping?: number; stiffness?: number; mass?: number} = {damping: 12}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: f - Math.round(inicioSeg * fps), fps, config: cfg});
};

export const Fundo: React.FC<{c1: string; c2: string; c3?: string}> = ({c1, c2, c3 = '#ffffff'}) => {
  const f = useCurrentFrame();
  const bolhas = useMemo(
    () => Array.from({length: 5}).map((_, i) => ({x: random(`bx${i}`) * 1080, y: random(`by${i}`) * 1920, r: 260 + random(`br${i}`) * 260, v: 0.4 + random(`bv${i}`)})),
    [],
  );
  const pontos = useMemo(
    () => Array.from({length: 26}).map((_, i) => ({x: random(`px${i}`) * 1080, y: random(`py${i}`) * 1920, r: 3 + random(`pr${i}`) * 6, v: 0.5 + random(`pv${i}`) * 1.5})),
    [],
  );
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 30%, ${c1} 0%, ${c2} 75%)`, overflow: 'hidden'}}>
      {bolhas.map((b, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: b.x + Math.sin((f / 60) * b.v + i) * 90 - b.r,
            top: b.y + Math.cos((f / 70) * b.v + i) * 110 - b.r,
            width: b.r * 2,
            height: b.r * 2,
            borderRadius: '50%',
            background: c3,
            opacity: 0.09,
            filter: 'blur(70px)',
          }}
        />
      ))}
      {pontos.map((p, i) => (
        <div
          key={`p${i}`}
          style={{
            position: 'absolute',
            left: p.x,
            top: (((p.y - f * p.v * 2) % 1920) + 1920) % 1920,
            width: p.r * 2,
            height: p.r * 2,
            borderRadius: '50%',
            background: '#fff',
            opacity: 0.18,
          }}
        />
      ))}
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
    </AbsoluteFill>
  );
};

export const Texto: React.FC<{
  y: number;
  tamanho: number;
  cor?: string;
  escala?: number;
  children: React.ReactNode;
  fonte?: string;
  contorno?: number;
  largura?: number;
  rot?: number;
}> = ({y, tamanho, cor = '#fff', escala = 1, children, fonte = TITULO, contorno = 12, largura = 900, rot = 0}) => (
  <div
    style={{
      position: 'absolute',
      left: (1080 - largura) / 2,
      width: largura,
      top: y - tamanho * 0.6,
      textAlign: 'center',
      fontFamily: fonte,
      fontWeight: 900,
      fontSize: tamanho,
      lineHeight: 1.05,
      color: cor,
      WebkitTextStroke: `${contorno}px #140a24`,
      paintOrder: 'stroke fill',
      transform: `scale(${escala}) rotate(${rot}deg)`,
      textShadow: '0 8px 0 rgba(0,0,0,0.25)',
    }}
  >
    {children}
  </div>
);

export const Pilula: React.FC<{y: number; cor: string; tamanho?: number; escala?: number; children: React.ReactNode; x?: number}> = ({
  y,
  cor,
  tamanho = 46,
  escala = 1,
  children,
  x = 540,
}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${escala})`}}>
    <div
      style={{
        background: cor,
        color: '#fff',
        fontFamily: TITULO,
        fontSize: tamanho,
        padding: `${tamanho * 0.32}px ${tamanho * 0.8}px`,
        borderRadius: 999,
        whiteSpace: 'nowrap',
        border: '5px solid rgba(255,255,255,0.9)',
        boxShadow: '0 10px 0 rgba(0,0,0,0.25), 0 0 40px rgba(255,255,255,0.15)',
        letterSpacing: 1,
      }}
    >
      {children}
    </div>
  </div>
);

export const Coracao: React.FC<{tamanho: number; cor?: string}> = ({tamanho, cor = '#ff3d6e'}) => (
  <svg width={tamanho} height={tamanho} viewBox="-60 -55 120 110">
    <path d="M 0 45 C -60 5 -55 -45 -22 -45 C -8 -45 0 -33 0 -25 C 0 -33 8 -45 22 -45 C 55 -45 60 5 0 45 Z" fill={cor} stroke="#fff" strokeWidth={7} />
    <ellipse cx={-22} cy={-22} rx={9} ry={14} fill="#fff" opacity={0.5} transform="rotate(30 -22 -22)" />
  </svg>
);

/** HUD: vidas (esquerda), placar (centro) e rodadas (direita) dentro da zona segura */
export const Hud: React.FC<{placar: [number, number]; rodada: number; pulsoPlacar?: number}> = ({placar, rodada, pulsoPlacar = 0}) => {
  const f = useCurrentFrame();
  const ep = useEp();
  return (
    <>
      <div style={{position: 'absolute', left: 50, top: 222, display: 'flex', gap: 4}}>
        {[0, 1, 2].map((i) => (
          <div key={i} style={{transform: `scale(${1 + 0.06 * Math.sin(f / 6 + i)})`}}>
            <Coracao tamanho={56} />
          </div>
        ))}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 540,
          top: 250,
          transform: `translate(-50%,-50%) scale(${1 + pulsoPlacar * 0.25})`,
          display: 'flex',
          alignItems: 'center',
          gap: 18,
          background: 'rgba(10,6,30,0.75)',
          border: '4px solid rgba(255,255,255,0.85)',
          borderRadius: 26,
          padding: '8px 22px',
          fontFamily: TITULO,
          color: '#fff',
          fontSize: 44,
        }}
      >
        <span style={{color: '#ff8db6'}}>TIME</span>
        <span style={{color: '#ffd23f', fontSize: 58}}>{placar[0]}</span>
        <span style={{opacity: 0.7}}>×</span>
        <span style={{color: ep.rivalCor, fontSize: 58}}>{placar[1]}</span>
        <span style={{color: ep.rivalCor}}>{ep.rivalNome}</span>
      </div>
      <div style={{position: 'absolute', left: 540, top: 318, transform: 'translate(-50%,-50%)', display: 'flex', gap: 10}}>
        {Array.from({length: ep.rodadas}, (_, k) => k + 1).map((i) => (
          <div
            key={i}
            style={{
              width: i === rodada ? 64 : 22,
              height: 22,
              borderRadius: 11,
              background: i < rodada ? '#36c46e' : i === rodada ? '#ffd23f' : 'rgba(255,255,255,0.3)',
              border: '3px solid #fff',
            }}
          />
        ))}
      </div>
    </>
  );
};

const CORES_FALA: Record<string, string> = {neuro: '#ffd23f', robo: '#3ff3ff'};

/** Legendas estilo TikTok (skill display-captions), uma fala por vez, na zona segura */
export const Legendas: React.FC<{clipes: Clipe[]; y?: number}> = ({clipes, y = 1430}) => {
  const {fps} = useVideoConfig();
  const ep = useEp();
  return (
    <AbsoluteFill>
      {clipes.map((c, ci) => {
        const caps: Caption[] = c.palavras.map(([w, s, e], j) => ({
          text: (j === 0 ? '' : ' ') + w.toUpperCase(),
          startMs: (c.ini + s) * 1000,
          endMs: (c.ini + e) * 1000,
          timestampMs: null,
          confidence: null,
        }));
        const {pages} = createTikTokStyleCaptions({captions: caps, combineTokensWithinMilliseconds: 700});
        return pages.map((p, pi) => {
          const prox = pages[pi + 1];
          const ini = (p.startMs / 1000) * fps;
          const fimFala = (c.ini + c.dur) * fps + 6;
          const fim = prox ? (prox.startMs / 1000) * fps : fimFala;
          if (fim - ini <= 0) return null;
          return (
            <Sequence key={`${ci}-${pi}`} from={Math.round(ini)} durationInFrames={Math.max(1, Math.round(fim - ini))} layout="none">
              <PaginaLegenda page={p} y={y} cor={c.quem === 'robo' ? ep.rivalCor : CORES_FALA[c.quem] ?? '#ffd23f'} />
            </Sequence>
          );
        });
      })}
    </AbsoluteFill>
  );
};

const PaginaLegenda: React.FC<{page: TikTokPage; y: number; cor: string}> = ({page, y, cor}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const agora = page.startMs + (f / fps) * 1000;
  const entrada = spring({frame: f, fps, config: {damping: 14, stiffness: 220}});
  return (
    <div
      style={{
        position: 'absolute',
        left: 90,
        width: 820,
        top: y,
        textAlign: 'center',
        fontFamily: CORPO,
        fontWeight: 900,
        fontSize: 74,
        lineHeight: 1.1,
        color: '#fff',
        WebkitTextStroke: '12px #140a24',
        paintOrder: 'stroke fill',
        transform: `scale(${0.85 + 0.15 * entrada})`,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        columnGap: 34,
      }}
    >
      {page.tokens.map((t) => {
        const ativo = t.fromMs <= agora && t.toMs + 120 > agora;
        return (
          <span key={t.fromMs} style={{color: ativo ? cor : '#fff', display: 'inline-block', transform: `scale(${ativo ? 1.06 : 1})`}}>
            {t.text.trim()}
          </span>
        );
      })}
    </div>
  );
};

/** Cartoes de alternativas */
export const Opcoes: React.FC<{
  itens: string[];
  inicio: number; // s
  certa: number;
  robo: number;
  roboEm: number;
  revelaEm: number;
}> = ({itens, inicio, certa, robo, roboEm, revelaEm}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const revelado = t >= revelaEm;
  const kRev = f - revelaEm * fps;
  return (
    <>
      {itens.map((txt, i) => {
        const e = spring({frame: f - Math.round((inicio + i * 0.12) * fps), fps, config: {damping: 13, stiffness: 160}});
        const y = 1080 + i * 128;
        const ehCerta = i === certa;
        const tremer = revelado && !ehCerta && i === robo ? Math.sin(kRev * 1.5) * Math.max(0, 12 - kRev) : 0;
        const bg = revelado ? (ehCerta ? 'linear-gradient(90deg,#1fb85c,#36d97a)' : 'rgba(60,20,40,0.85)') : 'linear-gradient(90deg,rgba(35,25,80,0.92),rgba(60,35,120,0.92))';
        const brilho = revelado && ehCerta ? 10 + 6 * Math.sin(kRev / 3) : 0;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 90 + tremer,
              top: y,
              width: 820,
              height: 104,
              transform: `translateX(${(1 - e) * -700}px) scale(${revelado && ehCerta ? 1 + 0.04 * spring({frame: kRev, fps, config: {damping: 8}}) : 1})`,
              opacity: revelado && !ehCerta ? 0.55 : 1,
              background: bg,
              borderRadius: 30,
              border: `5px solid ${revelado && ehCerta ? '#b9ffd2' : 'rgba(255,255,255,0.85)'}`,
              boxShadow: `0 8px 0 rgba(0,0,0,0.3), 0 0 ${brilho * 4}px rgba(80,255,150,${brilho ? 0.7 : 0})`,
              display: 'flex',
              alignItems: 'center',
              gap: 26,
              paddingLeft: 18,
              fontFamily: TITULO,
              color: '#fff',
              fontSize: 54,
            }}
          >
            <div
              style={{
                width: 72,
                height: 72,
                borderRadius: 36,
                background: revelado && !ehCerta ? '#6d4a5a' : '#ffd23f',
                color: '#140a24',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 44,
              }}
            >
              {'ABC'[i]}
            </div>
            <span>{txt}</span>
            {revelado && ehCerta && <Visto k={kRev} />}
            {t >= roboEm && i === robo && <EtiquetaRobo errou={revelado && !ehCerta} desde={f - roboEm * fps} />}
          </div>
        );
      })}
    </>
  );
};

const Visto: React.FC<{k: number}> = ({k}) => {
  const p = interpolate(k, [4, 16], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width={80} height={80} viewBox="0 0 80 80" style={{position: 'absolute', right: 26}}>
      <path d="M 12 42 L 32 62 L 68 18" fill="none" stroke="#fff" strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={100} strokeDashoffset={100 * (1 - p)} />
    </svg>
  );
};

const EtiquetaRobo: React.FC<{errou: boolean; desde: number}> = ({errou, desde}) => {
  const {fps} = useVideoConfig();
  const ep = useEp();
  const Rival = ep.Rival;
  const e = spring({frame: desde, fps, config: {damping: 10}});
  return (
    <div
      style={{
        position: 'absolute',
        right: errou ? 26 : 18,
        top: -34,
        transform: `scale(${e})`,
        display: 'flex',
        alignItems: 'center',
        gap: 6,
        background: errou ? '#ff3b4f' : '#0e1a2a',
        border: `4px solid ${ep.rivalCor}`,
        borderRadius: 999,
        padding: '2px 16px 2px 6px',
        fontSize: 28,
        color: '#fff',
      }}
    >
      <div style={{width: 46, height: 46, overflow: 'visible', marginTop: -4}}>
        <Rival tamanho={46} modo={errou ? 'erro' : 'normal'} />
      </div>
      {errou ? `${ep.rivalNome} ERROU!` : ep.rivalNome}
    </div>
  );
};

/** Contagem regressiva em anel */
export const Contagem: React.FC<{ini: number; fim: number; y?: number}> = ({ini, fim, y = 990}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  if (t < ini || t > fim) return null;
  const resto = fim - t;
  const n = Math.ceil(resto);
  const kSeg = f - Math.round((fim - n) * fps);
  const pulso = spring({frame: (f - Math.round(ini * fps)) % fps, fps, config: {damping: 9, stiffness: 200}});
  const c = 2 * Math.PI * 52;
  return (
    <div style={{position: 'absolute', left: 540, top: y, transform: `translate(-50%,-50%) scale(${0.9 + 0.1 * pulso})`}}>
      <svg width={150} height={150} viewBox="-75 -75 150 150">
        <circle r={60} fill="rgba(10,6,30,0.85)" stroke="#fff" strokeWidth={5} />
        <circle r={52} fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth={10} />
        <circle r={52} fill="none" stroke={n <= 1 ? '#ff3b4f' : '#ffd23f'} strokeWidth={10} strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - resto / (fim - ini))} transform="rotate(-90)" />
        <text y={22} textAnchor="middle" fontFamily={TITULO} fontSize={64} fill="#fff">
          {n}
        </text>
      </svg>
      {kSeg < 0 ? null : null}
    </div>
  );
};

/** Engrenagem com dentes */
export const Engrenagem: React.FC<{r: number; dentes: number; cor: string; ang: number; rotulo: string; destaque?: boolean}> = ({r, dentes, cor, ang, rotulo, destaque}) => {
  const pts: string[] = [];
  for (let i = 0; i < dentes * 2; i++) {
    const a0 = (i / (dentes * 2)) * Math.PI * 2;
    const a1 = ((i + 1) / (dentes * 2)) * Math.PI * 2;
    const rr = i % 2 === 0 ? r : r * 0.82;
    pts.push(`${rr * Math.cos(a0)},${rr * Math.sin(a0)}`, `${rr * Math.cos(a1)},${rr * Math.sin(a1)}`);
  }
  return (
    <g>
      {destaque && <circle r={r + 22} fill="none" stroke="#5dff9b" strokeWidth={10} opacity={0.9} />}
      <g transform={`rotate(${ang})`}>
        <polygon points={pts.join(' ')} fill={cor} stroke="#140a24" strokeWidth={6} strokeLinejoin="round" />
        <circle r={r * 0.45} fill="rgba(0,0,0,0.25)" />
        <line x1={0} y1={-r * 0.62} x2={0} y2={r * 0.62} stroke="rgba(255,255,255,0.5)" strokeWidth={8} strokeLinecap="round" />
      </g>
      <circle r={r * 0.28} fill="#fff" stroke="#140a24" strokeWidth={5} />
      <text y={r * 0.12} textAnchor="middle" fontFamily={TITULO} fontSize={r * 0.34} fill="#140a24">
        {rotulo}
      </text>
    </g>
  );
};
