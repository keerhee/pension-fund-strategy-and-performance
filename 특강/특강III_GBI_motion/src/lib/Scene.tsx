import React from 'react';
import {AbsoluteFill, Html5Audio, Sequence, staticFile, useCurrentFrame, interpolate} from 'remotion';
import {C, FONT} from '../theme';
import {rise} from './anim';

export type Line = {start: number; dur: number; cap: string; audio: string | null};
export type SceneT = {id: string; from_: number; dur: number; lines: Line[]};

/** 장면 공통 틀: eyebrow · 주장문 제목 · 부제 · 자막 · 문장별 음성 */
export const Scene: React.FC<{
  t: SceneT;
  eyebrow: string;
  title: string;
  sub?: string;
  captions?: boolean;
  children: React.ReactNode;
}> = ({t, eyebrow, title, sub, captions = true, children}) => {
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 10, t.dur - 12, t.dur], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const cur = [...t.lines].reverse().find((l) => f >= l.start);
  return (
    <AbsoluteFill style={{background: C.bg, fontFamily: FONT, color: C.text, opacity: fade}}>
      {t.lines.map((l, i) =>
        l.audio ? (
          <Sequence key={i} from={l.start} durationInFrames={l.dur + 6}>
            <Html5Audio src={staticFile(l.audio)} />
          </Sequence>
        ) : null,
      )}
      <div style={{position: 'absolute', left: 96, top: 64, right: 96}}>
        <div style={{fontSize: 26, color: C.accent, fontWeight: 600, letterSpacing: 1, ...rise(f, 2)}}>
          {eyebrow}
        </div>
        <div style={{fontSize: 54, fontWeight: 700, marginTop: 14, lineHeight: 1.25, ...rise(f, 6)}}>
          {title}
        </div>
        {sub ? (
          <div style={{fontSize: 30, color: C.muted, marginTop: 12, ...rise(f, 12)}}>{sub}</div>
        ) : null}
      </div>
      <div style={{position: 'absolute', left: 96, right: 96, top: 300, bottom: 150}}>{children}</div>
      {captions && cur ? (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            bottom: 48,
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <div
            key={cur.start}
            style={{
              background: 'rgba(6,16,32,0.78)',
              border: `1px solid ${C.line}`,
              borderRadius: 12,
              padding: '14px 32px',
              fontSize: 32,
              maxWidth: 1600,
              textAlign: 'center',
              ...rise(f, cur.start, 10, 8),
            }}
          >
            {cur.cap}
          </div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

/** i번째 문장이 시작하는 프레임 */
export const cueOf = (t: SceneT) => (i: number) => t.lines[Math.min(i, t.lines.length - 1)].start;
