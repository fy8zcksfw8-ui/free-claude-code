import React from 'react';
import {AbsoluteFill, Composition, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/lilita-one';

const Teste: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 8}});
  const o = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: 'linear-gradient(#5b2bd6,#120a2e)', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontFamily: 'Lilita One', fontSize: 160, color: '#ffd23f', transform: `scale(${s})`, opacity: o, textAlign: 'center'}}>
        TEMPORADA 2 ção
      </div>
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => (
  <Composition id="Teste" component={Teste} durationInFrames={30} fps={30} width={1080} height={1920} />
);
