import React from 'react';
import {AbsoluteFill, Html5Audio, Series, staticFile} from 'remotion';
import {C} from '../theme';
import {SceneT} from './Scene';

/** 배경음(사운드 베드) — timing.json에 bed가 있으면 깐다 */
export const Bed: React.FC<{T: {bed?: string}}> = ({T}) => (T.bed ? <Html5Audio src={staticFile(T.bed)} volume={0.9} /> : null);

/** 타이밍 JSON + 장면 컴포넌트 목록 → 에피소드 컴포넌트 */
export const makeEpisode = (T: {scenes: unknown[]; bed?: string}, LIST: React.FC<{t: SceneT}>[]) => {
  const scenes = T.scenes as SceneT[];
  const Ep: React.FC = () => (
    <AbsoluteFill style={{background: C.bg}}>
      <Bed T={T} />
      <Series>
        {scenes.map((s, i) => {
          const Comp = LIST[i];
          return (
            <Series.Sequence key={s.id} durationInFrames={s.dur}>
              <Comp t={s} />
            </Series.Sequence>
          );
        })}
      </Series>
    </AbsoluteFill>
  );
  return Ep;
};
