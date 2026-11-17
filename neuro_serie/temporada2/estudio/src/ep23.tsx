import React, {useId, useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Neuro} from './personagens';
import type {ModoRobo} from './personagens';
import {Coracao, Fundo, Legendas, Pilula, Texto, TITULO, useMola} from './ui';
import {Abs, useBoca, useT} from './cenas';
import type {Cena} from './cenas';
import {useEp} from './ctx';
import type {RivalProps} from './ctx';

// =============================================================== PERSONAGENS NOVOS
export const Miragem: React.FC<RivalProps> = ({tamanho, boca = 0, modo = 'normal', silhueta = false}) => {
  const f = useCurrentFrame();
  const id = useId().replace(/:/g, '');
  const erro = modo === 'erro';
  const conv = modo === 'convencido';
  const flut = Math.sin(f / 10) * 6;
  const inclina = erro ? -14 + Math.sin(f / 3) * 4 : Math.sin(f / 20) * 3;
  const S = (c: string) => (silhueta ? '#120d22' : c);
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      <defs>
        <radialGradient id={`pele${id}`} cx="40%" cy="35%" r="75%">
          <stop offset="0%" stopColor="#ffe3cf" />
          <stop offset="100%" stopColor="#e9a982" />
        </radialGradient>
        <linearGradient id={`capa${id}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#8a3df0" />
          <stop offset="100%" stopColor="#3a0f7a" />
        </linearGradient>
      </defs>
      <ellipse cx={0} cy={220} rx={150} ry={20} fill="rgba(0,0,0,0.3)" />
      <g transform={`translate(0 ${flut})`}>
        {/* capa */}
        <path d="M -150 210 Q -130 90 -60 70 L 60 70 Q 130 90 150 210 Z" fill={silhueta ? '#120d22' : `url(#capa${id})`} stroke={S('#24074d')} strokeWidth={6} />
        <path d="M -60 70 L 0 140 L 60 70" fill={S('#ffd23f')} />
        {/* cabelo */}
        {[[-95, -10, 55], [95, -10, 55], [-110, 45, 45], [110, 45, 45], [-80, 90, 40], [80, 90, 40]].map(([x, y, r], i) => (
          <circle key={i} cx={x} cy={y} r={r} fill={S('#6b2bd6')} />
        ))}
        {/* rosto */}
        <circle cx={0} cy={0} r={105} fill={silhueta ? '#120d22' : `url(#pele${id})`} stroke={S('#7a4a32')} strokeWidth={5} />
        {/* mascara */}
        {!silhueta && <path d="M -98 -22 Q -50 -60 0 -30 Q 50 -60 98 -22 Q 90 30 40 25 Q 0 20 -40 25 Q -90 30 -98 -22 Z" fill="#4a1594" stroke="#24074d" strokeWidth={5} />}
        {[-46, 46].map((x) =>
          erro ? (
            <g key={x}>
              <circle cx={x} cy={-6} r={20} fill="#fff" />
              <path d={`M ${x} -6 m -12 0 a 12 12 0 1 1 12 12 a 7 7 0 1 1 -7 -7`} fill="none" stroke="#6b2bd6" strokeWidth={4} transform={`rotate(${f * 20} ${x} -6)`} />
            </g>
          ) : (
            <g key={x}>
              <ellipse cx={x} cy={-6} rx={20} ry={conv ? 8 : f % 100 < 4 ? 2 : 17} fill={silhueta ? '#ff4fd8' : '#fff'} />
              {!silhueta && !conv && <circle cx={x + Math.sin(f / 22) * 5} cy={-4} r={9} fill="#4a0f8a" />}
            </g>
          ),
        )}
        {!silhueta &&
          (boca > 0.06 ? (
            <ellipse cx={0} cy={58} rx={22} ry={5 + boca * 20} fill="#9a0f3a" stroke="#5a0a22" strokeWidth={4} />
          ) : (
            <path d={conv ? 'M -30 52 Q 10 78 34 46' : 'M -30 50 Q 0 76 30 50'} stroke="#c2185b" strokeWidth={9} fill="none" strokeLinecap="round" />
          ))}
        {/* cartola */}
        <g transform={`rotate(${inclina} 0 -95)`}>
          <ellipse cx={0} cy={-95} rx={120} ry={22} fill={S('#1a1030')} />
          <rect x={-70} y={-230} width={140} height={140} rx={14} fill={S('#1f1438')} />
          <rect x={-70} y={-130} width={140} height={26} fill={S('#c2185b')} />
          {!silhueta && <path d="M 0 -200 l 9 18 20 3 -15 14 4 20 -18 -10 -18 10 4 -20 -15 -14 20 -3 Z" fill="#ffd23f" />}
        </g>
        {/* varinha */}
        <g transform={`rotate(${-30 + Math.sin(f / 7) * 10} 150 120)`}>
          <line x1={150} y1={120} x2={230} y2={0} stroke={S('#1a1030')} strokeWidth={14} strokeLinecap="round" />
          <circle cx={230} cy={0} r={14 + Math.sin(f / 3) * 4} fill={silhueta ? '#ff4fd8' : '#fff7b0'} opacity={0.95} />
        </g>
        {erro && <path d="M 85 -60 q 12 22 0 30 q -12 -8 0 -30" fill="#7fd4ff" />}
      </g>
    </svg>
  );
};

export const Turbo: React.FC<RivalProps> = ({tamanho, boca = 0, modo = 'normal', silhueta = false}) => {
  const f = useCurrentFrame();
  const id = useId().replace(/:/g, '');
  const erro = modo === 'erro';
  const vib = Math.sin(f * 1.7) * (erro ? 6 : 2.5);
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id={`raio${id}`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#fff6a0" />
          <stop offset="50%" stopColor="#ffd000" />
          <stop offset="100%" stopColor="#ff8a00" />
        </linearGradient>
      </defs>
      {!silhueta && [0, 1, 2].map((i) => <line key={i} x1={-240 - ((f * 18 + i * 60) % 120)} y1={-60 + i * 60} x2={-150 - ((f * 18 + i * 60) % 120)} y2={-60 + i * 60} stroke="#fff" strokeWidth={10} strokeLinecap="round" opacity={0.6} />)}
      <ellipse cx={0} cy={225} rx={110} ry={16} fill="rgba(0,0,0,0.3)" />
      <g transform={`translate(${vib} 0)`}>
        <path d="M 40 -230 L -120 20 L -10 20 L -60 230 L 130 -40 L 20 -40 L 90 -230 Z" fill={silhueta ? '#120d22' : `url(#raio${id})`} stroke={silhueta ? '#ffd000' : '#c25a00'} strokeWidth={9} strokeLinejoin="round" />
        {/* oculos escuros */}
        {erro ? (
          <g>
            {[-30, 50].map((x) => (
              <g key={x}>
                <line x1={x - 18} y1={-110} x2={x + 18} y2={-80} stroke="#140a24" strokeWidth={9} strokeLinecap="round" />
                <line x1={x + 18} y1={-110} x2={x - 18} y2={-80} stroke="#140a24" strokeWidth={9} strokeLinecap="round" />
              </g>
            ))}
            <g transform={`translate(${30 + (f % 20)} ${40 + (f % 20) * 4}) rotate(${f * 6})`}>
              <rect x={-60} y={-14} width={120} height={28} rx={12} fill="#140a24" />
            </g>
          </g>
        ) : (
          <g>
            <rect x={-70} y={-120} width={78} height={44} rx={18} fill={silhueta ? '#ffd000' : '#140a24'} />
            <rect x={14} y={-120} width={78} height={44} rx={18} fill={silhueta ? '#ffd000' : '#140a24'} />
            <rect x={6} y={-108} width={12} height={8} fill="#140a24" />
            {!silhueta && <line x1={-55} y1={-112} x2={-30} y2={-112} stroke="#fff" strokeWidth={6} strokeLinecap="round" opacity={0.7} />}
          </g>
        )}
        {!silhueta &&
          (boca > 0.06 ? (
            <ellipse cx={20} cy={-30} rx={24} ry={5 + boca * 22} fill="#7a1a00" stroke="#4a1000" strokeWidth={4} />
          ) : (
            <path d={modo === 'convencido' ? 'M -10 -40 Q 25 -12 55 -48' : 'M -8 -38 Q 22 -14 50 -38'} stroke="#7a1a00" strokeWidth={9} fill="none" strokeLinecap="round" />
          ))}
      </g>
    </svg>
  );
};

export const DoutorSombra: React.FC<{tamanho: number}> = ({tamanho}) => {
  const f = useCurrentFrame();
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      {Array.from({length: 11}).map((_, i) => {
        const a = Math.PI * (0.92 + i * 0.12), r1 = 110, r2 = 190 + (i % 2) * 30;
        return <polygon key={i} points={`${r1 * Math.cos(a - 0.2)},${-30 + r1 * Math.sin(a - 0.2)} ${r2 * Math.cos(a)},${-30 + r2 * Math.sin(a)} ${r1 * Math.cos(a + 0.2)},${-30 + r1 * Math.sin(a + 0.2)}`} fill="#08050f" />;
      })}
      <ellipse cx={0} cy={-10} rx={125} ry={140} fill="#08050f" />
      <path d="M -200 250 L -140 120 L 140 120 L 200 250 Z" fill="#08050f" />
      {[-52, 52].map((x) => (
        <g key={x} style={{filter: 'drop-shadow(0 0 18px #c45cff)'}}>
          <circle cx={x} cy={-40} r={42} fill="#2a0a40" stroke="#c45cff" strokeWidth={8} />
          {[0, 1, 2].map((j) => {
            const rr = 34 - j * 10, a0 = f * 14 + j * 120;
            return <path key={j} d={`M ${x + rr * Math.cos((a0 * Math.PI) / 180)} ${-40 + rr * Math.sin((a0 * Math.PI) / 180)} A ${rr} ${rr} 0 1 1 ${x + rr * Math.cos(((a0 + 200) * Math.PI) / 180)} ${-40 + rr * Math.sin(((a0 + 200) * Math.PI) / 180)}`} fill="none" stroke="#e7a8ff" strokeWidth={6} />;
          })}
        </g>
      ))}
      <path d="M -70 50 Q 0 110 70 50" stroke="#c45cff" strokeWidth={12} fill="none" strokeLinecap="round" style={{filter: 'drop-shadow(0 0 14px #c45cff)'}} />
    </svg>
  );
};

// =============================================================== VISUAIS DAS RODADAS
const Grade: React.FC<{x: number; y: number; w: number; h: number; cols: number; rows: number; claro?: number}> = ({x, y, w, h, cols, rows, claro = 0}) => {
  const lin = `rgb(${120 + claro * 90},${120 + claro * 90},${120 + claro * 90})`;
  const sx = w / cols, sy = h / rows;
  return (
    <svg width={w} height={h} style={{position: 'absolute', left: x, top: y}}>
      <rect width={w} height={h} fill="#000" />
      {Array.from({length: cols + 1}).map((_, i) => (
        <rect key={`v${i}`} x={i * sx - 7} y={0} width={14} height={h} fill={lin} />
      ))}
      {Array.from({length: rows + 1}).map((_, j) => (
        <rect key={`h${j}`} x={0} y={j * sy - 7} width={w} height={14} fill={lin} />
      ))}
      {Array.from({length: cols + 1}).map((_, i) => Array.from({length: rows + 1}).map((__, j) => <circle key={`${i}-${j}`} cx={i * sx} cy={j * sy} r={9.5} fill="#fff" />))}
    </svg>
  );
};

const VGrade: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const r = cena.eventos.revelaEm;
  const claro = interpolate(t, [r + 0.8, r + 1.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Grade x={160} y={560} w={760} h={330} cols={8} rows={3} claro={claro} />
      {t >= r + 1.2 && (
        <Pilula y={905} cor="#1fb85c" tamanho={42} escala={spring({frame: f - Math.round((r + 1.2) * 30), fps: 30, config: {damping: 10}})}>
          TODAS SÃO BRANCAS!
        </Pilula>
      )}
    </>
  );
};

const VVelocidade: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const r = cena.eventos.revelaEm;
  const some = interpolate(t, [r + 0.8, r + 1.4], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const x = 200 + (Math.sin(f / 22) * 0.5 + 0.5) * 560;
  return (
    <>
      <div style={{position: 'absolute', left: 140, top: 580, width: 800, height: 300, overflow: 'hidden', borderRadius: 20, border: '5px solid #fff', background: '#888'}}>
        <div style={{position: 'absolute', inset: 0, opacity: some, background: 'repeating-linear-gradient(90deg,#000 0 22px,#fff 22px 44px)'}} />
        <div style={{position: 'absolute', left: x - 140, top: 50, width: 90, height: 60, background: '#ffe600'}} />
        <div style={{position: 'absolute', left: x - 140, top: 190, width: 90, height: 60, background: '#0a1a7a'}} />
      </div>
      {t >= r + 1.2 && (
        <Pilula y={905} cor="#1fb85c" tamanho={42} escala={spring({frame: f - Math.round((r + 1.2) * 30), fps: 30, config: {damping: 10}})}>
          MESMA VELOCIDADE!
        </Pilula>
      )}
    </>
  );
};

const VTrilhos: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const r = cena.eventos.revelaEm;
  const p = interpolate(t, [r + 0.6, r + 1.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const W1 = 236, W2 = 262;
  const y1 = 650 + p * 60, y2 = 860 - p * 70;
  const x1 = 540 - W1 / 2 + p * (410 - (540 - W1 / 2)), x2 = 540 - W2 / 2 + p * (410 - (540 - W2 / 2));
  return (
    <>
      <svg width={1080} height={1000} style={{position: 'absolute', left: 0, top: 0, opacity: 1 - p * 0.85}}>
        {Array.from({length: 9}).map((_, i) => {
          const y = 560 + i * 48, k = (y - 560) / 400;
          return <line key={i} x1={510 - k * 230} y1={y} x2={570 + k * 230} y2={y} stroke="#8a5a2b" strokeWidth={10} />;
        })}
        <line x1={505} y1={560} x2={260} y2={960} stroke="#d9d9e8" strokeWidth={14} />
        <line x1={575} y1={560} x2={820} y2={960} stroke="#d9d9e8" strokeWidth={14} />
      </svg>
      <div style={{position: 'absolute', left: x1, top: y1, width: W1, height: 34, background: '#ff3b4f', border: '4px solid #fff', borderRadius: 8}} />
      <div style={{position: 'absolute', left: x2, top: y2, width: W2, height: 34, background: '#ff3b4f', border: '4px solid #fff', borderRadius: 8}} />
      {p >= 1 && <div style={{position: 'absolute', left: 410 + W1, top: 680, height: 160, borderLeft: '6px dashed #ffd23f'}} />}
      {t >= r + 1.4 && (
        <Pilula y={905} cor="#1fb85c" tamanho={42} escala={spring({frame: f - Math.round((r + 1.4) * 30), fps: 30, config: {damping: 10}})}>
          A DE BAIXO É MAIOR!
        </Pilula>
      )}
    </>
  );
};

const Carta: React.FC<{v: string; x: number; y: number; s?: number; op?: number}> = ({v, x, y, s = 1, op = 1}) => {
  const verm = v.includes('♥') || v.includes('♦');
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 120 * s, height: 168 * s, transform: 'translate(-50%,-50%)', opacity: op, background: '#fff', borderRadius: 14 * s, border: `${4 * s}px solid #2a1a4a`, boxShadow: '0 8px 0 rgba(0,0,0,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: `${TITULO}, 'DejaVu Sans'`, fontSize: 62 * s, color: verm ? '#d81b3c' : '#140a24'}}>
      {v}
    </div>
  );
};
const ANTES = ['K♥', 'Q♠', 'J♦', 'K♣', 'Q♥', 'J♠'];
const DEPOIS = ['K♦', 'Q♣', 'J♥', 'K♠', 'Q♦'];
const VCartas: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const ev = cena.eventos;
  if (t < ev.troca) {
    return (
      <>
        {ANTES.map((v, i) => (
          <Carta key={v} v={v} x={330 + (i % 3) * 210} y={655 + Math.floor(i / 3) * 190} s={spring({frame: f - 8 - i * 3, fps: 30, config: {damping: 12}})} />
        ))}
        {t >= ev.memo && <Pilula y={560} cor="#6b2bd6" tamanho={38}>ESCOLHA UMA E MEMORIZE!</Pilula>}
      </>
    );
  }
  const rev = t >= ev.revelaEm;
  const k = f - Math.round(ev.troca * 30);
  return (
    <>
      {rev &&
        ANTES.map((v, i) => <Carta key={v} v={v} x={260 + i * 112} y={600} s={0.62} op={0.55} />)}
      {rev && <Pilula y={520} cor="#4a4a66" tamanho={30}>ANTES</Pilula>}
      {DEPOIS.map((v, i) => (
        <Carta key={v} v={v} x={rev ? 300 + i * 120 : 330 + (i % 3) * 210} y={rev ? 790 : 655 + Math.floor(i / 3) * 190} s={(rev ? 0.75 : 1) * spring({frame: k - i * 3, fps: 30, config: {damping: 11}})} />
      ))}
      {rev && <Pilula y={905} cor="#1fb85c" tamanho={40}>TROCOU TODAS!</Pilula>}
      {k < 12 && <AbsoluteFill style={{background: `rgba(200,120,255,${0.6 * (1 - k / 12)})`}} />}
    </>
  );
};

const VPergunta: React.FC<{cena: Cena}> = () => {
  const f = useCurrentFrame();
  return (
    <>
      {Array.from({length: 8}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: ((f * 40 + i * 170) % 1300) - 200, top: 600 + i * 40, width: 160, height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.35)'}} />
      ))}
      <Texto y={760} tamanho={260} cor="#ffd23f" escala={1 + 0.06 * Math.sin(f / 3)} rot={Math.sin(f / 5) * 4}>
        ?
      </Texto>
    </>
  );
};

export const VISUAIS = {grade: VGrade, velocidade: VVelocidade, trilhos: VTrilhos, cartas: VCartas, pergunta: VPergunta};

// =============================================================== CENAS NOVAS
export const IntroCurta: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const logo = useMola(0.1, {damping: 12});
  const bora = useMola(fl[2], {damping: 9});
  return (
    <AbsoluteFill>
      <Fundo c1="#7d3df0" c2="#1a0838" c3="#ffd23f" />
      <Pilula y={285} cor="#ff3d8b" tamanho={50} escala={logo}>
        DESAFIOS DO NEURO
      </Pilula>
      <Pilula y={375} cor="#e08600" tamanho={34} escala={logo}>
        TEMPORADA 2
      </Pilula>
      <Abs x={540} y={760}>
        <Neuro tamanho={640} boca={b} humor={t < fl[1] ? 'rindo' : 'feliz'} aceno />
      </Abs>
      {t >= fl[1] &&
        [0, 1, 2].map((i) => (
          <Abs key={i} x={540 + (i - 1) * 150} y={1170} escala={spring({frame: f - Math.round((fl[1] + 0.2 + i * 0.15) * 30), fps: 30, config: {damping: 8}})}>
            <Coracao tamanho={120} />
          </Abs>
        ))}
      {t >= fl[2] && (
        <Pilula y={1320} cor="#7a3df0" tamanho={60} escala={bora * (1 + 0.05 * Math.sin(f / 3))}>
          BORA?
        </Pilula>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

const REGRA: Record<string, string> = {MIRAGEM: 'ELA RESPONDE PRIMEIRO... E ADORA ENGANAR!', TURBO: '6 PERGUNTAS • 2 SEGUNDOS CADA'};
const NOME: Record<string, string> = {MIRAGEM: 'MADAME MIRAGEM', TURBO: 'TURBO'};
export const ApresentaRival: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const ep = useEp();
  const R = ep.Rival;
  const bR = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const ultima = fl[fl.length - 1];
  const nome = useMola(0.3, {damping: 10});
  const regra = useMola(ultima, {damping: 11});
  const entra = useMola(0, {damping: 9, stiffness: 120});
  return (
    <AbsoluteFill>
      <Fundo c1={ep.rivalNome === 'TURBO' ? '#d98a00' : '#5a1aa8'} c2="#0a0418" c3={ep.rivalCor} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(255,255,255,0.22), transparent 70%)', clipPath: 'polygon(42% 0, 58% 0, 88% 72%, 12% 72%)'}} />
      <Abs x={540 + (1 - entra) * 700} y={700}>
        <R tamanho={720} boca={bR} modo={t >= ultima ? 'convencido' : 'normal'} />
      </Abs>
      <Pilula y={1090} cor={ep.rivalNome === 'TURBO' ? '#c26a00' : '#6b2bd6'} tamanho={66} escala={nome}>
        {NOME[ep.rivalNome] ?? ep.rivalNome}
      </Pilula>
      {t >= ultima && (
        <>
          <Abs x={170} y={1270} escala={regra}>
            <Neuro tamanho={250} boca={bN} humor="surpreso" bracos={false} />
          </Abs>
          <div style={{position: 'absolute', left: 300, top: 1215, width: 620, transform: `scale(${regra})`, transformOrigin: 'left center', background: 'rgba(10,6,30,0.9)', border: '4px solid #ffd23f', borderRadius: 24, padding: '12px 20px', fontFamily: TITULO, fontSize: 40, color: '#fff', lineHeight: 1.1}}>
            {REGRA[ep.rivalNome]}
          </div>
        </>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

export const GanchoGrade: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const bR = useBoca('robo', cena.inicio);
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const s = spring({frame: f, fps: 30, from: 1.3, to: 1, config: {damping: 10}});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Grade x={-40} y={-40} w={1160} h={2000} cols={9} rows={16} />
      <div style={{position: 'absolute', left: 60, top: 250, width: 960, height: 260, background: 'rgba(20,6,40,0.88)', borderRadius: 36, border: '5px solid #ff4fd8'}} />
      <Texto y={330} tamanho={84} cor="#fff" escala={s}>
        QUANTAS BOLINHAS
      </Texto>
      <Texto y={430} tamanho={96} cor="#ffd23f" escala={s}>
        PRETAS VOCÊ VÊ?
      </Texto>
      <Abs x={830} y={1170}>
        <Miragem tamanho={420} boca={bR} modo="convencido" />
      </Abs>
      {t >= fl[1] && (
        <>
          <Abs x={250} y={1200} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 9}})}>
            <Neuro tamanho={360} boca={bN} humor="surpreso" />
          </Abs>
          <Pilula y={960} cor="#ff2d6f" tamanho={52} escala={spring({frame: f - Math.round(fl[1] * 30), fps: 30, config: {damping: 9}})}>
            NÃO RESPONDE AINDA!
          </Pilula>
        </>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

export const GanchoTurbo: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const bR = useBoca('robo', cena.inicio);
  const s = spring({frame: f, fps: 30, from: 1.3, to: 1, config: {damping: 10}});
  const entra = spring({frame: f, fps: 30, config: {damping: 11, stiffness: 140}});
  const resto = Math.max(0, 2 - t * 0.8);
  const c = 2 * Math.PI * 70;
  return (
    <AbsoluteFill>
      <Fundo c1="#ffb300" c2="#5a1d00" c3="#fff6a0" />
      {Array.from({length: 14}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: 1100 - ((f * 60 + i * 140) % 1500), top: 250 + i * 95, width: 220, height: 8, borderRadius: 4, background: 'rgba(255,255,255,0.45)'}} />
      ))}
      <Texto y={330} tamanho={92} cor="#fff" escala={s}>
        VOCÊ RESPONDE
      </Texto>
      <Texto y={440} tamanho={104} cor="#ffd23f" escala={s} rot={-3}>
        EM 2 SEGUNDOS?
      </Texto>
      <Abs x={540 + (1 - entra) * 800} y={850}>
        <Turbo tamanho={620} boca={bR} modo="convencido" />
      </Abs>
      <Abs x={540} y={1260}>
        <svg width={190} height={190} viewBox="-95 -95 190 190">
          <circle r={82} fill="rgba(10,6,30,0.85)" stroke="#fff" strokeWidth={6} />
          <circle r={70} fill="none" stroke="#ff3b4f" strokeWidth={12} strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - resto / 2)} transform="rotate(-90)" />
          <text y={28} textAnchor="middle" fontFamily={TITULO} fontSize={78} fill="#fff">
            {resto.toFixed(1)}
          </text>
        </svg>
      </Abs>
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

export const VitoriaGen: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const ep = useEp();
  const R = ep.Rival;
  const b = useBoca('neuro', cena.inicio);
  const conf = useMemo(() => Array.from({length: 90}).map((_, i) => ({x: random(`cx${i}`) * 1080, y: -random(`cy${i}`) * 1900, v: 5 + random(`cv${i}`) * 9, c: ['#ff5c8a', '#ffd23f', '#5ac8ff', '#5dff9b', '#c38bff'][i % 5], r: random(`cr${i}`) * 360})), []);
  const pl = useMola(0.15, {damping: 8});
  return (
    <AbsoluteFill>
      <Fundo c1="#ff9a1f" c2="#3a0a00" c3="#ffe066" />
      {conf.map((c, i) => (
        <div key={i} style={{position: 'absolute', left: c.x + Math.sin(f / 8 + i) * 30, top: (c.y + f * c.v) % 2100, width: 18, height: 30, background: c.c, transform: `rotate(${c.r + f * 8}deg)`, borderRadius: 4}} />
      ))}
      <Texto y={340} tamanho={130} cor="#fff" escala={pl}>
        VENCEMOS!
      </Texto>
      <Pilula y={490} cor="#140a24" tamanho={60} escala={pl}>
        {cena.placar}
      </Pilula>
      <Abs x={400} y={950}>
        <Neuro tamanho={600} boca={b} humor="rindo" aceno />
      </Abs>
      <Abs x={830} y={1150}>
        <R tamanho={330} modo="erro" />
      </Abs>
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

export const OutroVidas: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const tiers = cena.tiers as [string, string, string][];
  return (
    <AbsoluteFill>
      <Fundo c1="#6a2ad6" c2="#12062e" c3="#ff8db6" />
      <Texto y={330} tamanho={92} cor="#ffd23f">
        QUANTAS VIDAS
      </Texto>
      <Texto y={430} tamanho={92} cor="#fff">
        SOBRARAM?
      </Texto>
      {tiers.map(([n, txt, cor], i) => {
        const e = spring({frame: f - 10 - i * 8, fps: 30, config: {damping: 11}});
        const cheios = n === '3' ? 3 : n === '1-2' ? 2 : 0;
        return (
          <div key={i} style={{position: 'absolute', left: 90, top: 560 + i * 160, width: 860, height: 130, transform: `scale(${e})`, background: cor, borderRadius: 34, border: '5px solid #fff', display: 'flex', alignItems: 'center', gap: 16, paddingLeft: 26, boxShadow: '0 10px 0 rgba(0,0,0,0.25)'}}>
            {[0, 1, 2].map((j) => (
              <Coracao key={j} tamanho={56} cor={j < cheios ? '#ff3d6e' : '#4a4a60'} />
            ))}
            <span style={{fontFamily: TITULO, fontSize: 54, color: '#fff', WebkitTextStroke: '8px #140a24', paintOrder: 'stroke fill', marginLeft: 12}}>{txt}</span>
          </div>
        );
      })}
      <Abs x={540} y={1200}>
        <Neuro tamanho={300} boca={b} humor="feliz" aceno />
      </Abs>
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

/** Gancho final: deixa a historia em aberto para o proximo episodio */
export const Cliffhanger: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const bN = useBoca('neuro', cena.inicio);
  const bR = useBoca('robo', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const fim = cena.clipes[cena.clipes.length - 1];
  const tFim = fim.ini + fim.dur;
  const turbo = cena.vilao === 'turbo';
  const apareceu = t >= fl[1] - 0.1;
  const glitch = apareceu && t < fl[1] + 0.5 ? (random(`g${f}`) - 0.5) * 40 : 0;
  const pisca = apareceu && Math.floor(f / 3) % 4 === 0 && t < fl[1] + 1.2;
  const cont = spring({frame: f - Math.round((tFim + 0.1) * 30), fps: 30, config: {damping: 9}});
  const entrada = spring({frame: f - Math.round((fl[1] - 0.1) * 30), fps: 30, config: {damping: 10, stiffness: 120}});
  return (
    <AbsoluteFill style={{transform: `translateX(${glitch}px)`}}>
      <Fundo c1={turbo ? '#3a1a5a' : '#1a0a2a'} c2="#000" c3={turbo ? '#ffd000' : '#c45cff'} />
      {apareceu && <AbsoluteFill style={{background: turbo ? 'rgba(255,208,0,0.08)' : 'rgba(0,0,0,0.55)'}} />}
      {pisca && <AbsoluteFill style={{background: turbo ? 'rgba(255,240,150,0.55)' : 'rgba(196,92,255,0.35)'}} />}
      {turbo ? (
        <>
          <Abs x={300} y={1180}>
            <Miragem tamanho={380} boca={bR} modo={apareceu ? 'erro' : 'convencido'} />
          </Abs>
          {apareceu && (
            <Abs x={560 + (1 - entrada) * 900} y={640}>
              <Turbo tamanho={640} silhueta />
            </Abs>
          )}
          {t >= fl[2] && (
            <Abs x={820} y={1210}>
              <Neuro tamanho={330} boca={bN} humor="surpreso" />
            </Abs>
          )}
        </>
      ) : (
        <>
          {apareceu && (
            <Abs x={540} y={620} escala={0.6 + 0.4 * entrada}>
              <DoutorSombra tamanho={720} />
            </Abs>
          )}
          <Abs x={540} y={apareceu ? 1170 : 900} escala={apareceu ? 0.75 : 1}>
            <Neuro tamanho={520} boca={bN} humor={apareceu ? 'surpreso' : 'feliz'} />
          </Abs>
          {t >= fl[2] && (
            <Texto y={330} tamanho={92} cor="#c45cff" escala={spring({frame: f - Math.round(fl[2] * 30), fps: 30, config: {damping: 9}})} rot={-3}>
              ELE VOLTOU...
            </Texto>
          )}
        </>
      )}
      {apareceu && (
        <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(255,255,255,0.05) 0 2px, transparent 2px 6px)', opacity: t < fl[1] + 0.6 ? 1 : 0.4}} />
      )}
      {t >= tFim + 0.1 && (
        <AbsoluteFill style={{background: `rgba(0,0,0,${0.6 * cont})`}}>
          <Texto y={860} tamanho={140} cor="#fff" escala={cont}>
            CONTINUA...
          </Texto>
          <Pilula y={1010} cor="#ff2d6f" tamanho={50} escala={cont}>
            SEGUE O NEURO PRA VER!
          </Pilula>
        </AbsoluteFill>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
      {durationInFrames < 0 ? null : null}
    </AbsoluteFill>
  );
};

export const EXTRA = {
  introCurta: IntroCurta,
  apresentaRival: ApresentaRival,
  ganchoGrade: GanchoGrade,
  ganchoTurbo: GanchoTurbo,
  vitoriaGen: VitoriaGen,
  outroTeaser: OutroVidas,
  cliffhanger: Cliffhanger,
};
export type _M = ModoRobo;
