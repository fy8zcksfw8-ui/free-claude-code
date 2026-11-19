import React from 'react';

/** explosao de brilhos coloridos (acerto) */
export const Brilhos: React.FC<{x: number; y: number; k: number}> = ({x, y, k}) => {
  if (k < 0 || k > 30) return null;
  const cores = ['#ff3d6e', '#3ff3ff', '#5dff9b', '#ffd23f', '#b46bff', '#ff9a3d'];
  return (
    <>
      {Array.from({length: 22}).map((_, i) => {
        const a = (i / 22) * Math.PI * 2 + i;
        const d = k * (9 + (i % 4) * 3);
        const s = 18 * (1 - k / 30);
        return (
          <div key={i} style={{position: 'absolute', left: x + Math.cos(a) * d - s, top: y + Math.sin(a) * d * 0.7 - s, width: s * 2, height: s * 2, background: cores[i % 6], clipPath: 'polygon(50% 0, 62% 38%, 100% 50%, 62% 62%, 50% 100%, 38% 62%, 0 50%, 38% 38%)', transform: `rotate(${k * 12 + i * 20}deg)`}} />
        );
      })}
    </>
  );
};

