import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Calculino, Neuro, Trofeu} from './personagens';
import type {Humor, ModoRobo} from './personagens';
import {Contagem, Coracao, Engrenagem, Fundo, Hud, Legendas, Opcoes, Pilula, Texto, TITULO, useMola} from './ui';
import type {Clipe} from './ui';
import dados from './data/s2e1.json';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Cena = any;
const BOCA = dados.boca as Record<string, number[]>;

const useBoca = (quem: string, inicio: number) => {
  const f = useCurrentFrame();
  const arr = BOCA[quem] ?? [];
  return arr[inicio + f] ?? 0;
};
const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};
const Abs: React.FC<{x: number; y: number; children: React.ReactNode; escala?: number; rot?: number}> = ({x, y, children, escala = 1, rot = 0}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${escala}) rotate(${rot}deg)`}}>{children}</div>
);

// ---------------------------------------------------------------- HOOK
export const CenaHook: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const bRobo = useBoca('robo', cena.inicio);
  const bNeuro = useBoca('neuro', cena.inicio);
  const t = useT();
  const s = spring({frame: f, fps: 30, from: 1.35, to: 1, config: {damping: 10}});
  const neuroFala = t >= cena.clipes[1].ini - 0.05;
  return (
    <AbsoluteFill>
      <Fundo c1="#0f5a6e" c2="#04121c" c3="#3ff3ff" />
      <AbsoluteFill style={{clipPath: 'polygon(0 58%, 100% 46%, 100% 100%, 0 100%)'}}>
        <Fundo c1="#7a2ad6" c2="#1a0838" c3="#ff8db6" />
      </AbsoluteFill>
      <Abs x={540} y={520}>
        <Calculino tamanho={620} boca={bRobo} modo={neuroFala ? 'pensando' : 'convencido'} />
      </Abs>
      <Abs x={540} y={1230} escala={neuroFala ? 1 : 0.92}>
        <Neuro tamanho={560} boca={bNeuro} humor={neuroFala ? 'bravo' : 'surpreso'} />
      </Abs>
      <Texto y={900} tamanho={118} cor="#ffd23f" escala={s} rot={-3}>
        VOCÊ VENCE UM ROBÔ?
      </Texto>
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- INTRO (padrao de todo episodio)
export const CenaIntro: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const logo = useMola(0.2, {damping: 12});
  const temp = useMola(fl[1], {damping: 7, stiffness: 140});
  const bora = useMola(fl[3], {damping: 9});
  const tremor = t >= fl[1] && t < fl[1] + 0.35 ? Math.sin(f * 3) * 10 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${tremor}px)`}}>
      <Fundo c1="#7d3df0" c2="#1a0838" c3="#ffd23f" />
      <Pilula y={300} cor="#ff3d8b" tamanho={52} escala={logo}>
        DESAFIOS DO NEURO
      </Pilula>
      <Abs x={540} y={700}>
        <Neuro tamanho={640} boca={b} humor={t < fl[1] ? 'rindo' : 'feliz'} aceno />
      </Abs>
      {t >= fl[1] && (
        <Abs x={540} y={1065} escala={temp} rot={-5}>
          <div
            style={{
              fontFamily: TITULO,
              fontSize: 112,
              color: '#fff',
              background: 'linear-gradient(180deg,#ffe066,#ffb300 60%,#e08600)',
              padding: '6px 46px',
              borderRadius: 28,
              border: '7px solid #fff',
              WebkitTextStroke: '10px #7a3d00',
              paintOrder: 'stroke fill',
              boxShadow: '0 14px 0 rgba(0,0,0,0.3), 0 0 60px rgba(255,210,63,0.7)',
              whiteSpace: 'nowrap',
            }}
          >
            TEMPORADA 2
          </div>
        </Abs>
      )}
      {t >= fl[2] &&
        [0, 1, 2].map((i) => {
          const s = spring({frame: f - Math.round((fl[2] + 0.25 + i * 0.18) * 30), fps: 30, config: {damping: 8}});
          return (
            <Abs key={i} x={540 + (i - 1) * 150} y={1225} escala={s}>
              <Coracao tamanho={120} />
            </Abs>
          );
        })}
      {t >= fl[3] && (
        <Pilula y={1345} cor="#7a3df0" tamanho={60} escala={bora * (1 + 0.05 * Math.sin(f / 3))}>
          BORA?
        </Pilula>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- TEMA
export const CenaTema: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const fl: number[] = cena.eventos.falas;
  const tr = useMola(0.3, {damping: 10});
  const tit = useMola(0.5, {damping: 11});
  const rival = useMola(fl[1], {damping: 9});
  return (
    <AbsoluteFill>
      <Fundo c1="#e0861a" c2="#2a1003" c3="#ffe066" />
      <Abs x={540} y={610}>
        <div
          style={{
            width: 900,
            height: 900,
            borderRadius: '50%',
            background: 'repeating-conic-gradient(rgba(255,240,180,0.18) 0deg 12deg, transparent 12deg 24deg)',
            transform: `rotate(${f * 0.6}deg) scale(${tr})`,
          }}
        />
      </Abs>
      <Abs x={540} y={600} escala={tr}>
        <Trofeu tamanho={430} />
      </Abs>
      <Texto y={920} tamanho={120} cor="#fff" escala={tit}>
        TORNEIO
      </Texto>
      <Texto y={1040} tamanho={104} cor="#ffd23f" escala={tit}>
        DOS GÊNIOS
      </Texto>
      {t >= fl[1] && (
        <>
          <Pilula y={1200} cor="#0e6b80" tamanho={50} escala={rival}>
            RIVAL Nº 1: ???
          </Pilula>
          <Abs x={820} y={1290} escala={rival * 0.5}>
            <Calculino tamanho={360} silhueta />
          </Abs>
        </>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- APRESENTACAO DO ROBO
const fmt = (n: number) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
export const CenaRobo: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const b = useBoca('robo', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const nome = useMola(0.35, {damping: 10});
  const card = useMola(fl[0] + 0.5, {damping: 12});
  const carimbo = useMola(fl[1], {damping: 7, stiffness: 160});
  const n = interpolate(t, [fl[0] + 0.5, fl[0] + 2.2], [0, 1000000], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill>
      <Fundo c1="#0d4d63" c2="#020a12" c3="#3ff3ff" />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(160,255,255,0.22), transparent 70%)', clipPath: 'polygon(42% 0, 58% 0, 88% 75%, 12% 75%)'}} />
      {t >= fl[1] && (
        <Texto y={350} tamanho={86} cor="#ff4d5e" escala={carimbo} rot={-6}>
          HUMANOS SÃO LENTOS
        </Texto>
      )}
      <Abs x={540} y={740}>
        <Calculino tamanho={720} boca={b} modo={t >= fl[1] ? 'convencido' : 'normal'} />
      </Abs>
      <Pilula y={1115} cor="#0e6b80" tamanho={64} escala={nome}>
        CALCULINO
      </Pilula>
      {t >= fl[0] + 0.5 && (
        <Abs x={540} y={1265} escala={card}>
          <div
            style={{
              fontFamily: TITULO,
              color: '#3ff3ff',
              fontSize: 54,
              background: 'rgba(4,20,30,0.9)',
              border: '4px solid #3ff3ff',
              borderRadius: 24,
              padding: '10px 30px',
              whiteSpace: 'nowrap',
              boxShadow: '0 0 40px rgba(63,243,255,0.4)',
            }}
          >
            {fmt(n)} CONTAS/SEG
          </div>
        </Abs>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
      {f < 0 ? null : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- REGRAS
export const CenaRegras: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const bN = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const c1 = useMola(fl[0], {damping: 12});
  const c2 = useMola(fl[1], {damping: 12});
  const Card: React.FC<{y: number; e: number; num: string; children: React.ReactNode; cor: string}> = ({y, e, num, children, cor}) => (
    <div
      style={{
        position: 'absolute',
        left: 90,
        top: y,
        width: 860,
        transform: `translateX(${(1 - e) * 900}px)`,
        display: 'flex',
        alignItems: 'center',
        gap: 22,
        background: 'rgba(15,8,40,0.88)',
        border: `5px solid ${cor}`,
        borderRadius: 30,
        padding: '18px 22px',
        fontFamily: TITULO,
        color: '#fff',
        fontSize: 46,
        lineHeight: 1.1,
      }}
    >
      <div style={{minWidth: 76, height: 76, borderRadius: 38, background: cor, color: '#140a24', fontSize: 50, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{num}</div>
      <div>{children}</div>
    </div>
  );
  return (
    <AbsoluteFill>
      <Fundo c1="#3b2a9e" c2="#0a0622" c3="#ff8db6" />
      <Texto y={330} tamanho={96} cor="#ffd23f">
        AS REGRAS
      </Texto>
      <Abs x={290} y={650}>
        <Neuro tamanho={460} boca={bN} humor="feliz" />
      </Abs>
      <Abs x={790} y={650}>
        <Calculino tamanho={440} modo="convencido" />
      </Abs>
      <Texto y={640} tamanho={90} cor="#fff">
        VS
      </Texto>
      {t >= fl[0] && (
        <Card y={950} e={c1} num="1" cor="#3ff3ff">
          O ROBÔ RESPONDE PRIMEIRO
        </Card>
      )}
      {t >= fl[1] && (
        <Card y={1115} e={c2} num="2" cor="#ffd23f">
          ROBÔ ERRA + VOCÊ ACERTA = PONTO PRO TIME!
        </Card>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- VISUAIS DAS RODADAS
const Ovelha: React.FC<{fantasma?: boolean}> = ({fantasma}) => (
  <svg width={92} height={80} viewBox="-50 -42 100 84" style={{filter: fantasma ? 'grayscale(1)' : undefined}}>
    {[-22, -6, 10, 24].map((x, i) => (
      <circle key={i} cx={x} cy={i % 2 ? -8 : -2} r={18} fill="#fff" stroke="#bbb" strokeWidth={3} />
    ))}
    <circle cx={2} cy={8} r={22} fill="#fff" stroke="#bbb" strokeWidth={3} />
    <ellipse cx={36} cy={-2} rx={14} ry={17} fill="#2c2335" />
    <circle cx={40} cy={-6} r={3.5} fill="#fff" />
    <rect x={-20} y={24} width={7} height={14} rx={3} fill="#2c2335" />
    <rect x={12} y={24} width={7} height={14} rx={3} fill="#2c2335" />
  </svg>
);

const VisualOvelhas: React.FC<{revela: number}> = ({revela}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  return (
    <>
      {Array.from({length: 17}).map((_, i) => {
        const linha = Math.floor(i / 6), col = i % 6;
        const x = 240 + col * 120 + (linha === 2 ? 60 : 0);
        const y = 610 + linha * 100;
        const some = i >= 9 && t >= revela;
        const k = Math.max(0, f - revela * 30 - (i - 9) * 2);
        const e = spring({frame: f - 4 - i, fps: 30, config: {damping: 12}});
        return (
          <Abs key={i} x={x} y={y - (some ? Math.min(60, k * 3) : 0)} escala={e}>
            <div style={{opacity: some ? Math.max(0.15, 1 - k / 15) : 1}}>
              <Ovelha fantasma={some} />
            </div>
          </Abs>
        );
      })}
      {t >= revela + 0.8 && (
        <Pilula y={905} cor="#1fb85c" tamanho={44} escala={spring({frame: f - Math.round((revela + 0.8) * 30), fps: 30, config: {damping: 10}})}>
          SOBRARAM 9!
        </Pilula>
      )}
    </>
  );
};

const VisualCorrida: React.FC<{revela: number}> = ({revela}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const p = interpolate(t, [revela, revela + 0.9], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const corredores = [
    {r: '1º', x: 760, cor: '#ffc928'},
    {r: p > 0.5 ? '3º' : '2º', x: 560 - p * 60, cor: '#c0c8d6'},
  ];
  const voceX = 330 + p * 340;
  return (
    <>
      <div style={{position: 'absolute', left: 160, top: 660, width: 760, height: 190, background: '#c2563b', borderRadius: 30, border: '5px solid #fff'}} />
      <div style={{position: 'absolute', left: 180, top: 752, width: 720, height: 0, borderTop: '6px dashed rgba(255,255,255,0.8)'}} />
      <div style={{position: 'absolute', left: 860, top: 650, width: 34, height: 210, background: 'repeating-linear-gradient(0deg,#fff 0 26px,#140a24 26px 52px)', borderRadius: 6}} />
      {corredores.map((c, i) => (
        <Abs key={i} x={c.x} y={755}>
          <div style={{width: 120, height: 120, borderRadius: 60, background: c.cor, border: '6px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: TITULO, fontSize: 56, color: '#140a24'}}>
            {c.r}
          </div>
        </Abs>
      ))}
      <Abs x={voceX} y={755}>
        <div style={{width: 130, height: 130, borderRadius: 65, background: '#ff6fa8', border: '6px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: TITULO, fontSize: p > 0.5 ? 56 : 36, color: '#fff', WebkitTextStroke: '6px #7a1435', paintOrder: 'stroke fill'}}>
          {p > 0.5 ? '2º' : 'VOCÊ'}
        </div>
      </Abs>
      {t >= revela + 0.9 && (
        <Pilula y={905} cor="#1fb85c" tamanho={42} escala={spring({frame: f - Math.round((revela + 0.9) * 30), fps: 30, config: {damping: 10}})}>
          VOCÊ FICA EM 2º!
        </Pilula>
      )}
    </>
  );
};

const VisualEngrenagens: React.FC<{revela: number}> = ({revela}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const gira = Math.max(0, f - revela * 30);
  const G = [
    {x: 300, y: 690, r: 95, n: 'A', cor: '#ff8db6', dir: 1},
    {x: 455, y: 815, r: 80, n: 'B', cor: '#7fc8ff', dir: -1},
    {x: 615, y: 690, r: 95, n: 'C', cor: '#ffd23f', dir: 1},
    {x: 770, y: 815, r: 80, n: 'D', cor: '#9dffb0', dir: -1},
  ];
  return (
    <svg width={1080} height={1000} style={{position: 'absolute', left: 0, top: 0}}>
      {G.map((g, i) => (
        <g key={i} transform={`translate(${g.x} ${g.y})`}>
          <Engrenagem r={g.r} dentes={10} cor={g.cor} ang={(gira * 4 * g.dir * 95) / g.r + i * 9} rotulo={g.n} destaque={t >= revela + 0.4 && (g.n === 'C' || g.n === 'A')} />
        </g>
      ))}
      <g transform="translate(300 690)">
        <path d="M -120 -60 A 135 135 0 0 1 60 -120" fill="none" stroke="#fff" strokeWidth={12} strokeLinecap="round" />
        <path d="M 40 -142 L 78 -118 L 42 -92" fill="#fff" />
      </g>
      <text x={300} y={560} textAnchor="middle" fontFamily={TITULO} fontSize={40} fill="#fff" stroke="#140a24" strokeWidth={8} paintOrder="stroke">
        DIREITA
      </text>
    </svg>
  );
};

const VisualConta: React.FC<{revela: number; texto: string}> = ({revela, texto}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const k = f - revela * 30;
  const destaque = t >= revela;
  const partes = texto.split('1×0');
  const res = spring({frame: k - 30, fps: 30, config: {damping: 8}});
  return (
    <>
      <div
        style={{
          position: 'absolute',
          left: 60,
          width: 960,
          top: 620,
          textAlign: 'center',
          fontFamily: TITULO,
          fontSize: 76,
          color: '#fff',
          WebkitTextStroke: '10px #140a24',
          paintOrder: 'stroke fill',
          letterSpacing: 1,
        }}
      >
        {partes[0]}
        <span
          style={{
            display: 'inline-block',
            background: destaque ? '#ff3b4f' : 'transparent',
            borderRadius: 18,
            padding: '0 8px',
            transform: `scale(${destaque ? 1 + 0.12 * spring({frame: k, fps: 30, config: {damping: 8}}) : 1})`,
          }}
        >
          {destaque && k > 18 ? '0' : '1×0'}
        </span>
        {partes[1]}
      </div>
      {destaque && k > 30 && (
        <Texto y={820} tamanho={150} cor="#5dff9b" escala={res}>
          = 9
        </Texto>
      )}
      {!destaque && (
        <Texto y={820} tamanho={150} cor="#ffd23f" escala={1 + 0.04 * Math.sin(f / 4)}>
          = ?
        </Texto>
      )}
    </>
  );
};

// ---------------------------------------------------------------- RODADA
const TEMAS: Record<number, [string, string, string]> = {
  1: ['#2f6fe0', '#06102e', '#7fc8ff'],
  2: ['#e0532f', '#2a0806', '#ffb36b'],
  3: ['#1fa86a', '#03200f', '#9dffb0'],
  4: ['#b0123c', '#1e0208', '#ff6f8e'],
};
export const CenaRodada: React.FC<{cena: Cena; placarAntes: [number, number]; placarDepois: [number, number]}> = ({cena, placarAntes, placarDepois}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const ev = cena.eventos;
  const bN = useBoca('neuro', cena.inicio);
  const bR = useBoca('robo', cena.inicio);
  const tema = TEMAS[cena.n];
  const tit = useMola(0.35, {damping: 11});
  const revelado = t >= ev.revelaEm;
  const roboErrou = cena.robo !== cena.certa;
  const bug = ev.bugEm !== undefined && t >= ev.bugEm;
  const pontuou = t >= ev.pontoEm;
  const kPonto = f - ev.pontoEm * 30;
  const pulso = pontuou ? Math.max(0, 1 - kPonto / 12) : 0;
  const placar = pontuou ? placarDepois : placarAntes;
  const humorN: Humor = revelado ? (cena.ponto === 'neuro' ? 'rindo' : 'surpreso') : t >= ev.contaIni ? 'surpreso' : 'feliz';
  const modoR: ModoRobo = bug || (revelado && roboErrou) ? 'erro' : t >= ev.roboEm && !revelado ? 'convencido' : revelado ? 'convencido' : 'pensando';
  const balao = spring({frame: f - Math.round(ev.roboEm * 30), fps: 30, config: {damping: 10}});
  const jitter = bug ? (random(`j${f}`) - 0.5) * 24 : 0;
  const voar = pontuou && kPonto < 22;
  return (
    <AbsoluteFill style={{transform: `translate(${jitter}px, ${jitter * 0.5}px)`}}>
      <Fundo c1={tema[0]} c2={tema[1]} c3={tema[2]} />
      <Hud placar={placar} rodada={cena.n} pulsoPlacar={pulso} />
      <Texto y={392} tamanho={cena.final ? 92 : 70} cor={cena.final ? '#ff4d5e' : '#fff'} escala={tit}>
        {cena.titulo}
      </Texto>
      {!cena.final &&
        (cena.texto as string[]).map((l, i) => (
          <Texto key={i} y={474 + i * 62} tamanho={54} cor="#ffd23f" escala={spring({frame: f - 12 - i * 6, fps: 30, config: {damping: 12}})} contorno={10}>
            {l}
          </Texto>
        ))}
      {cena.visual === 'ovelhas' && <VisualOvelhas revela={ev.revelaEm} />}
      {cena.visual === 'corrida' && <VisualCorrida revela={ev.revelaEm} />}
      {cena.visual === 'engrenagens' && <VisualEngrenagens revela={ev.revelaEm} />}
      {cena.visual === 'conta' && <VisualConta revela={ev.revelaEm} texto={cena.texto[0]} />}
      <Abs x={120} y={960} escala={0.95}>
        <Neuro tamanho={230} boca={bN} humor={humorN} bracos={false} />
      </Abs>
      <Abs x={900} y={960} escala={0.95}>
        <Calculino tamanho={230} boca={bR} modo={modoR} />
      </Abs>
      {t >= ev.roboEm && t < ev.revelaEm && (
        <Abs x={760} y={862} escala={balao}>
          <div style={{background: '#0e2a3a', border: '5px solid #3ff3ff', borderRadius: 26, padding: '6px 22px', fontFamily: TITULO, fontSize: 46, color: '#3ff3ff', whiteSpace: 'nowrap'}}>
            É {cena.opcoes[cena.robo].toUpperCase()}!
          </div>
        </Abs>
      )}
      <Opcoes itens={cena.opcoes} inicio={0.55} certa={cena.certa} robo={cena.robo} roboEm={ev.roboEm} revelaEm={ev.revelaEm} />
      <Contagem ini={ev.contaIni} fim={ev.contaFim} y={985} />
      {voar && (
        <Abs x={interpolate(kPonto, [0, 20], [540, cena.ponto === 'neuro' ? 470 : 610])} y={interpolate(kPonto, [0, 20], [700, 250])} escala={1.2 - kPonto / 30}>
          <div style={{fontFamily: TITULO, fontSize: 90, color: cena.ponto === 'neuro' ? '#ffd23f' : '#3ff3ff', WebkitTextStroke: '10px #140a24', paintOrder: 'stroke fill'}}>+1</div>
        </Abs>
      )}
      {bug && (
        <AbsoluteFill
          style={{
            background: `repeating-linear-gradient(0deg, rgba(255,0,60,0.16) 0 3px, transparent 3px 7px)`,
            mixBlendMode: 'screen',
            opacity: 0.6 + 0.4 * Math.sin(f),
          }}
        />
      )}
      {bug && (
        <Texto y={555} tamanho={84} cor="#ff4d5e" escala={1 + 0.05 * Math.sin(f)} rot={-4}>
          ERRO! ERRO!
        </Texto>
      )}
      <Legendas clipes={cena.clipes as Clipe[]} y={1440} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- VITORIA
export const CenaVitoria: React.FC<{cena: Cena}> = ({cena}) => {
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const conf = useMemo(
    () =>
      Array.from({length: 90}).map((_, i) => ({
        x: random(`cx${i}`) * 1080,
        y: -random(`cy${i}`) * 1900,
        v: 5 + random(`cv${i}`) * 9,
        c: ['#ff5c8a', '#ffd23f', '#5ac8ff', '#5dff9b', '#c38bff'][i % 5],
        r: random(`cr${i}`) * 360,
      })),
    [],
  );
  const pl = useMola(0.2, {damping: 8});
  return (
    <AbsoluteFill>
      <Fundo c1="#ff9a1f" c2="#3a0a00" c3="#ffe066" />
      {conf.map((c, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: c.x + Math.sin(f / 8 + i) * 30,
            top: (c.y + f * c.v) % 2100,
            width: 18,
            height: 30,
            background: c.c,
            transform: `rotate(${c.r + f * 8}deg)`,
            borderRadius: 4,
          }}
        />
      ))}
      <Texto y={330} tamanho={130} cor="#fff" escala={pl}>
        VENCEMOS!
      </Texto>
      <Pilula y={470} cor="#140a24" tamanho={70} escala={pl}>
        TIME 3 × 1 ROBÔ
      </Pilula>
      <Abs x={540} y={740} escala={pl}>
        <Trofeu tamanho={360} />
      </Abs>
      <Abs x={390} y={1120}>
        <Neuro tamanho={520} boca={b} humor="rindo" aceno />
      </Abs>
      <Abs x={830} y={1200}>
        <Calculino tamanho={300} modo="erro" />
      </Abs>
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- OUTRO
export const CenaOutro: React.FC<{cena: Cena}> = ({cena}) => {
  const t = useT();
  const f = useCurrentFrame();
  const b = useBoca('neuro', cena.inicio);
  const fl: number[] = cena.eventos.falas;
  const tiers: [number, number, string, string][] = [
    [1, 3, 'GÊNIO DO TORNEIO', '#ffb300'],
    [2, 2, 'CLASSIFICADO', '#1fb85c'],
    [3, 0, 'ELIMINADO', '#6b6b85'],
  ];
  const segue = useMola(fl[4], {damping: 9});
  return (
    <AbsoluteFill>
      <Fundo c1="#6a2ad6" c2="#12062e" c3="#ff8db6" />
      <Texto y={330} tamanho={92} cor="#ffd23f">
        QUANTAS VIDAS
      </Texto>
      <Texto y={430} tamanho={92} cor="#fff">
        SOBRARAM?
      </Texto>
      {tiers.map(([p, n, txt, cor], i) => {
        if (t < fl[p]) return null;
        const e = spring({frame: f - Math.round(fl[p] * 30), fps: 30, config: {damping: 11}});
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 90,
              top: 560 + i * 160,
              width: 860,
              height: 130,
              transform: `scale(${e})`,
              background: cor,
              borderRadius: 34,
              border: '5px solid #fff',
              display: 'flex',
              alignItems: 'center',
              gap: 18,
              paddingLeft: 26,
              boxShadow: '0 10px 0 rgba(0,0,0,0.25)',
            }}
          >
            {[0, 1, 2].map((j) => (
              <Coracao key={j} tamanho={58} cor={j < n || (n === 2 && j < 2) ? '#ff3d6e' : '#4a4a60'} />
            ))}
            <span style={{fontFamily: TITULO, fontSize: 58, color: '#fff', WebkitTextStroke: '8px #140a24', paintOrder: 'stroke fill', marginLeft: 14}}>{txt}</span>
          </div>
        );
      })}
      <Abs x={540} y={1180}>
        <Neuro tamanho={330} boca={b} humor={t >= fl[1] && t < fl[4] ? 'rindo' : 'feliz'} aceno={t >= fl[4]} />
      </Abs>
      {t >= fl[4] && (
        <Pilula y={1350} cor="#ff2d6f" tamanho={60} escala={segue * (1 + 0.05 * Math.sin(f / 3))}>
          SEGUE O NEURO
        </Pilula>
      )}
      <Legendas clipes={cena.clipes} y={1440} />
    </AbsoluteFill>
  );
};
