import React, {createContext, useContext, useId} from 'react';

/** acessorio do Neuro por episodio (ex.: 'explorador' na fase do Egito) */
export const AcessorioNeuro = createContext<string | null>(null);
import {useCurrentFrame} from 'remotion';

export type Humor = 'feliz' | 'rindo' | 'surpreso' | 'bravo' | 'triste' | 'tonto';
import {random} from 'remotion';

// Lobos do cerebro (x, y, raio) em unidades de 100px
const LOBOS: [number, number, number][] = [
  [-1.0, -0.25, 0.85], [0, -0.75, 0.95], [1.0, -0.25, 0.85], [-0.65, 0.45, 0.85],
  [0.65, 0.45, 0.85], [0, 0.15, 1.0], [-0.5, -0.6, 0.8], [0.5, -0.6, 0.8],
];

/** Neuro em SVG vetorial. `boca` vai de 0 (fechada) a 1 (bem aberta). */
export const Neuro: React.FC<{
  tamanho: number;
  boca?: number;
  humor?: Humor;
  bracos?: boolean;
  aceno?: boolean;
}> = ({tamanho, boca = 0, humor = 'feliz', bracos = true, aceno = false}) => {
  const f = useCurrentFrame();
  const acessorio = useContext(AcessorioNeuro);
  const id = useId().replace(/:/g, '');
  const piscar = f % 96 < 4 && humor !== 'rindo';
  const olhar = Math.sin(f / 25) * 6;
  const pulo = humor === 'rindo' ? Math.abs(Math.sin(f / 4)) * -10 : Math.sin(f / 8) * 4;
  const u = 100;
  const angBraco = (lado: number) =>
    humor === 'surpreso' ? 1.35 : aceno && lado === 1 ? 0.9 + 0.5 * Math.sin(f / 3.5) : 0.55 + 0.25 * Math.sin(f / 6 + lado);
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      <defs>
        <radialGradient id={`pele${id}`} cx="35%" cy="25%" r="80%">
          <stop offset="0%" stopColor="#ffd0e2" />
          <stop offset="45%" stopColor="#ff8db6" />
          <stop offset="100%" stopColor="#e9558f" />
        </radialGradient>
        <radialGradient id={`olho${id}`} cx="40%" cy="35%" r="70%">
          <stop offset="0%" stopColor="#4a3a7a" />
          <stop offset="100%" stopColor="#140a24" />
        </radialGradient>
      </defs>
      <ellipse cx={0} cy={190} rx={150} ry={22} fill="rgba(0,0,0,0.28)" />
      <g transform={`translate(${(random(`bx${Math.floor(f / 2.5)}`) - 0.5) * 2.4} ${pulo + (random(`by${Math.floor(f / 2.5)}`) - 0.5) * 2.4}) rotate(${humor === 'tonto' ? Math.sin(f / 6) * 6 : 0})`}>
        {bracos &&
          [-1, 1].map((lado) => {
            const a = angBraco(lado);
            const sx = lado * 1.5 * u, sy = 0.3 * u;
            const ex = sx + lado * Math.cos(a) * 0.95 * u, ey = sy - Math.sin(a) * 0.95 * u;
            return (
              <g key={lado}>
                <path d={`M ${sx} ${sy} Q ${sx + lado * 40} ${sy + 10} ${ex} ${ey}`} stroke="#c8407a" strokeWidth={18} fill="none" strokeLinecap="round" />
                <circle cx={ex} cy={ey} r={20} fill="#fff" stroke="#c8407a" strokeWidth={6} />
              </g>
            );
          })}
        {LOBOS.map(([x, y, r], i) => (
          <circle key={`b${i}`} cx={x * u} cy={y * u} r={r * u + 7} fill="#b8336e" />
        ))}
        {LOBOS.map(([x, y, r], i) => (
          <circle key={`l${i}`} cx={x * u} cy={y * u} r={r * u} fill={`url(#pele${id})`} />
        ))}
        <ellipse cx={-70} cy={-120} rx={60} ry={28} fill="#fff" opacity={0.35} transform="rotate(-25 -70 -120)" />
        <path d="M 0 -165 Q 8 -120 0 -72" stroke="#d24a86" strokeWidth={7} fill="none" strokeLinecap="round" />
        {[[-110, -50], [110, -50], [-60, -110], [60, -110]].map(([x, y], i) => (
          <path key={`d${i}`} d={`M ${x - 28} ${y + 6} Q ${x} ${y - 16} ${x + 28} ${y + 6}`} stroke="#d24a86" strokeWidth={6} fill="none" strokeLinecap="round" />
        ))}
        {/* olhos */}
        {[-42, 42].map((ex) => {
          if (humor === 'tonto') {
            return (
              <g key={ex}>
                <ellipse cx={ex} cy={5} rx={28} ry={30} fill="#fff" stroke="#3c1428" strokeWidth={5} />
                <path d={`M ${ex} 5 m -15 0 a 15 15 0 1 1 15 15 a 9 9 0 1 1 -9 -9`} fill="none" stroke="#7a3df0" strokeWidth={5} transform={`rotate(${f * 18 * Math.sign(ex)} ${ex} 5)`} />
              </g>
            );
          }
          if (humor === 'rindo') {
            return <path key={ex} d={`M ${ex - 22} 10 Q ${ex} -16 ${ex + 22} 10`} stroke="#3c1428" strokeWidth={9} fill="none" strokeLinecap="round" />;
          }
          const ry = piscar ? 3 : humor === 'surpreso' ? 38 : 30;
          const rx = humor === 'surpreso' ? 32 : 27;
          return (
            <g key={ex}>
              <ellipse cx={ex} cy={5} rx={rx} ry={ry} fill="#fff" stroke="#3c1428" strokeWidth={5} />
              {!piscar && (
                <>
                  <circle cx={ex + olhar} cy={10} r={humor === 'surpreso' ? 11 : 14} fill={`url(#olho${id})`} />
                  <circle cx={ex + olhar - 4} cy={5} r={4.5} fill="#fff" />
                  <circle cx={ex + olhar + 5} cy={15} r={2.2} fill="#fff" opacity={0.9} />
                </>
              )}
              {humor === 'bravo' && <path d={`M ${ex - 30 * Math.sign(ex)} -42 L ${ex + 26 * Math.sign(ex)} -22`} stroke="#3c1428" strokeWidth={10} strokeLinecap="round" />}
              {humor === 'surpreso' && <path d={`M ${ex - 24} -50 Q ${ex} -66 ${ex + 24} -50`} stroke="#3c1428" strokeWidth={7} fill="none" strokeLinecap="round" />}
            </g>
          );
        })}
        {/* bochechas */}
        <ellipse cx={-80} cy={45} rx={18} ry={10} fill="#ff7fae" opacity={0.75} />
        <ellipse cx={80} cy={45} rx={18} ry={10} fill="#ff7fae" opacity={0.75} />
        {acessorio === 'explorador' && (
          <g transform={`rotate(${Math.sin(f / 14) * 2} 0 -150)`}>
            <ellipse cx={0} cy={-150} rx={165} ry={34} fill="#c9a36a" stroke="#6b4a1e" strokeWidth={7} />
            <path d="M -105 -152 Q -100 -255 0 -262 Q 100 -255 105 -152 Z" fill="#e2c28a" stroke="#6b4a1e" strokeWidth={7} />
            <path d="M -103 -175 Q 0 -160 103 -175 L 104 -152 Q 0 -138 -104 -152 Z" fill="#c62828" />
            <ellipse cx={-40} cy={-230} rx={30} ry={12} fill="#fff" opacity={0.35} />
          </g>
        )}
        {/* boca */}
        {humor === 'rindo' ? (
          <g>
            <path d={`M -38 45 Q 0 ${95 + boca * 25} 38 45 Z`} fill="#7a1435" stroke="#3c1428" strokeWidth={5} />
            <ellipse cx={0} cy={72 + boca * 8} rx={16} ry={9} fill="#ff6f8e" />
          </g>
        ) : boca > 0.06 || humor === 'surpreso' ? (
          <g>
            <ellipse cx={0} cy={62} rx={humor === 'surpreso' ? 17 : 24} ry={(humor === 'surpreso' ? 14 : 5) + boca * 22} fill="#7a1435" stroke="#3c1428" strokeWidth={4.5} />
            {boca > 0.3 && <ellipse cx={0} cy={62 + boca * 13} rx={11} ry={6} fill="#ff6f8e" />}
          </g>
        ) : humor === 'triste' || humor === 'bravo' ? (
          <path d="M -24 70 Q 0 54 24 70" stroke="#3c1428" strokeWidth={7} fill="none" strokeLinecap="round" />
        ) : (
          <path d="M -26 52 Q 0 76 26 52" stroke="#3c1428" strokeWidth={7} fill="none" strokeLinecap="round" />
        )}
      </g>
    </svg>
  );
};

export type ModoRobo = 'normal' | 'convencido' | 'erro' | 'pensando';

/** Calculino, o robo rival. A boca e um equalizador que reage a voz. */
export const Calculino: React.FC<{tamanho: number; boca?: number; modo?: ModoRobo; silhueta?: boolean}> = ({
  tamanho,
  boca = 0,
  modo = 'normal',
  silhueta = false,
}) => {
  const f = useCurrentFrame();
  const id = useId().replace(/:/g, '');
  const erro = modo === 'erro';
  const tremor = erro ? Math.sin(f * 2.3) * 6 : 0;
  const luz = Math.floor(f / 10) % 2 === 0;
  const tela = erro ? '#3a0710' : '#08131f';
  const olhoCor = erro ? '#ff3b4f' : '#3ff3ff';
  const flutua = Math.sin(f / 9) * 5;
  const sil = (c: string) => (silhueta ? '#120d22' : c);
  return (
    <svg width={tamanho} height={tamanho} viewBox="-250 -250 500 500" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id={`metal${id}`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#f2f6fb" />
          <stop offset="55%" stopColor="#b7c3d3" />
          <stop offset="100%" stopColor="#7d8ba0" />
        </linearGradient>
        <filter id={`brilho${id}`} x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <ellipse cx={0} cy={215} rx={140} ry={20} fill="rgba(0,0,0,0.3)" />
      <g transform={`translate(${tremor} ${flutua})`}>
        {/* antena */}
        <line x1={0} y1={-150} x2={0} y2={-205} stroke={sil('#5d6b80')} strokeWidth={10} strokeLinecap="round" />
        <circle cx={0} cy={-212} r={16} fill={silhueta ? '#ff3b4f' : luz || erro ? '#ff3b4f' : '#7a1f2a'} filter={`url(#brilho${id})`} />
        {/* orelhas */}
        <rect x={-188} y={-70} width={30} height={90} rx={12} fill={sil('#8f9cb0')} />
        <rect x={158} y={-70} width={30} height={90} rx={12} fill={sil('#8f9cb0')} />
        {/* cabeca */}
        <rect x={-160} y={-155} width={320} height={250} rx={46} fill={silhueta ? '#120d22' : `url(#metal${id})`} stroke={sil('#2b3440')} strokeWidth={7} />
        {!silhueta && [[-135, -130], [135, -130], [-135, 70], [135, 70]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={7} fill="#6f7c90" />)}
        {/* tela do rosto */}
        <rect x={-125} y={-118} width={250} height={180} rx={30} fill={silhueta ? '#1b1430' : tela} stroke={sil('#2b3440')} strokeWidth={5} />
        {!silhueta && (
          <g filter={`url(#brilho${id})`}>
            {erro ? (
              [-55, 55].map((x) => (
                <g key={x}>
                  <line x1={x - 22} y1={-62} x2={x + 22} y2={-18} stroke={olhoCor} strokeWidth={11} strokeLinecap="round" />
                  <line x1={x + 22} y1={-62} x2={x - 22} y2={-18} stroke={olhoCor} strokeWidth={11} strokeLinecap="round" />
                </g>
              ))
            ) : modo === 'pensando' ? (
              [-55, 55].map((x) => <rect key={x} x={x - 24} y={-74} width={48} height={22} rx={10} fill={olhoCor} />)
            ) : (
              [-55, 55].map((x) => (
                <rect key={x} x={x - 22} y={modo === 'convencido' ? -48 : -70} width={44} height={modo === 'convencido' ? 18 : f % 110 < 4 ? 6 : 44} rx={10} fill={olhoCor} />
              ))
            )}
            {/* boca equalizador */}
            {Array.from({length: 7}).map((_, i) => {
              const h = 6 + boca * (18 + 22 * Math.abs(Math.sin(f * 0.9 + i * 1.7)));
              return <rect key={i} x={-63 + i * 18} y={20 - h / 2} width={12} height={h} rx={5} fill={olhoCor} />;
            })}
          </g>
        )}
        {silhueta && [-55, 55].map((x) => <rect key={x} x={x - 22} y={-70} width={44} height={44} rx={10} fill="#ff3b4f" filter={`url(#brilho${id})`} />)}
        {/* corpo */}
        <rect x={-110} y={100} width={220} height={100} rx={28} fill={silhueta ? '#120d22' : `url(#metal${id})`} stroke={sil('#2b3440')} strokeWidth={7} />
        {!silhueta && (
          <>
            <rect x={-70} y={120} width={140} height={58} rx={12} fill="#1d2a3a" />
            {[0, 1, 2].map((i) => (
              <circle key={i} cx={-40 + i * 40} cy={149} r={11} fill={(Math.floor(f / 7) + i) % 3 === 0 ? (erro ? '#ff3b4f' : '#ffd23f') : '#3b4a5e'} />
            ))}
          </>
        )}
        {erro && (
          <g opacity={0.85}>
            {[0, 1, 2].map((i) => {
              const k = (f + i * 12) % 36;
              return <circle key={i} cx={-60 + i * 55 + k} cy={-170 - k * 4} r={18 + k * 0.9} fill="#6b6b78" opacity={1 - k / 36} />;
            })}
          </g>
        )}
      </g>
    </svg>
  );
};

/** Trofeu dourado */
export const Trofeu: React.FC<{tamanho: number}> = ({tamanho}) => {
  const id = useId().replace(/:/g, '');
  return (
    <svg width={tamanho} height={tamanho} viewBox="-150 -170 300 340">
      <defs>
        <linearGradient id={`ouro${id}`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#fff3a8" />
          <stop offset="45%" stopColor="#ffc928" />
          <stop offset="100%" stopColor="#d48a00" />
        </linearGradient>
      </defs>
      <path d="M -95 -140 L 95 -140 L 85 -20 Q 70 50 0 60 Q -70 50 -85 -20 Z" fill={`url(#ouro${id})`} stroke="#a86a00" strokeWidth={6} />
      <path d="M -90 -110 Q -150 -110 -140 -50 Q -130 0 -78 0" stroke="#ffc928" strokeWidth={18} fill="none" />
      <path d="M 90 -110 Q 150 -110 140 -50 Q 130 0 78 0" stroke="#ffc928" strokeWidth={18} fill="none" />
      <rect x={-22} y={55} width={44} height={50} fill="#e7a400" />
      <rect x={-80} y={100} width={160} height={40} rx={10} fill="#7a4a1e" stroke="#4d2c0e" strokeWidth={5} />
      <ellipse cx={-40} cy={-95} rx={18} ry={40} fill="#fff" opacity={0.45} transform="rotate(15 -40 -95)" />
      <text x={0} y={-35} textAnchor="middle" fontFamily="Lilita One" fontSize={90} fill="#fff8d0" stroke="#a86a00" strokeWidth={4}>
        1
      </text>
    </svg>
  );
};
