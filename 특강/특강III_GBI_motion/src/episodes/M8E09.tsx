import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, Chip, RevealTable} from '../lib/ui';
import {pop, prog, rise, shake} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import T from '../data/M8E09.timing.json';

const EB = 'BAF.60080 · W06 GBI · ⑩ 모의 IC';

const Stamp: React.FC<{f: number; at: number; text: string}> = ({f, at, text}) => {
  const sp = pop(f, at);
  return (
    <div
      style={{
        position: 'absolute',
        right: 30,
        top: -30,
        background: C.bg,
        border: `5px solid ${C.floor}`,
        color: C.floor,
        borderRadius: 12,
        padding: '8px 20px',
        fontSize: 36,
        fontWeight: 900,
        opacity: sp,
        transform: `rotate(-8deg) scale(${sp}) translateX(${shake(f, at, 6, 12)}px)`,
      }}
    >
      {text}
    </div>
  );
};

/* S0 하나의 언어 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E09" title="두 안건은 하나의 언어 — Floor · 쿠션 · 달성 확률로 심의합니다" sub="이번 강의의 개념은 두 안건의 쟁점에 그대로 꽂힌다">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['이번 강의의 개념', 'IC에서 꽂히는 쟁점']}
          widths={[1.2, 1.3]}
          rows={[
            {cells: ['위험 = P(W < G) · 필요 자본 K · 방법 1 · 2 · 3', '공통 — 수익률이 아니라 달성 확률로'], at: cue(0) + 10},
            {cells: ['RB → GHP → Floor 연쇄', '안건 1 — Floor를 한국에서 무엇으로 만드는가'], at: cue(1)},
            {cells: ['쿠션 공식 · m의 세 기준 · Cash Trap', '안건 1 — 승수 m 상한, 급락 락인 방어'], at: cue(1) + 14},
            {cells: ['4대 도전 · 비용 0.8~1.5%', '안건 1 — 수수료가 디폴트옵션 자격이 있는가'], at: cue(1) + 28},
            {cells: ['Flexicure 다섯 단계 · 모방 3장벽', '안건 2 — Floor 1,536억 위의 쿠션으로 x · y · z'], at: cue(1) + 42},
          ]}
        />
      </div>
    </Scene>
  );
};

/* S1 안건 1 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="제1호 디폴트옵션 Flexicure형 — 기본 답은 조건부 승인입니다" sub="발언은 “조건 X가 Y이면 답은 Z” 형식으로, 수익률이 아니라 목표 언어로 한다">
      <Card style={{position: 'relative', ...rise(f, cue(0))}}>
        <div style={{fontSize: 30, color: C.muted}}>제1호 · 퇴직연금 디폴트옵션 Flexicure형 도입</div>
        <div style={{display: 'flex', gap: 24, marginTop: 24}}>
          {[
            ['Floor', '0.90'],
            ['m 상한', '≤ 2'],
            ['총보수', '≤ 0.5%'],
          ].map(([k, v], i) => (
            <Card key={k} style={{flex: 1, textAlign: 'center', background: C.bg2, ...rise(f, cue(1) + i * 14)}}>
              <div style={{fontSize: 30, color: C.muted}}>{k}</div>
              <div style={{fontSize: 72, fontWeight: 900, color: C.floor}}>{v}</div>
            </Card>
          ))}
        </div>
        <Stamp f={f} at={cue(0) + 30} text="조건부 승인" />
      </Card>
      <Card style={{marginTop: 24, borderLeft: `6px solid ${C.liab}`, ...rise(f, cue(2))}}>
        <div style={{fontSize: 30, fontWeight: 800}}>Floor를 낮추고 m을 키우면 평균은 좋아지지만 Cash Trap과 수수료가 디폴트 자격을 위협한다</div>
      </Card>
    </Scene>
  );
};

/* S2 안건 2 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="제2호 H대 기금 — 세 숫자 (20, 30, 4.5)의 조건부 승인입니다" sub="기본 답 = 과제 B안 (주식 50 · 국채 25 · 현금 5 · 사모 20)">
      <Card style={{position: 'relative', ...rise(f, cue(0))}}>
        <div style={{display: 'flex', gap: 24, marginTop: 10}}>
          {[
            ['x 비유동', '≤ 20%', '재간접 · 세컨더리'],
            ['y 유동', '≥ 30%', '현금 · 국채'],
            ['z 지출률', '4.5%', '고정 3.5%가 Floor'],
          ].map(([k, v, d], i) => (
            <Card key={k} style={{flex: 1, textAlign: 'center', background: C.bg2, ...rise(f, cue(0) + 10 + i * 14)}}>
              <div style={{fontSize: 30, color: C.muted}}>{k}</div>
              <div style={{fontSize: 72, fontWeight: 900, color: C.floor}}>{v}</div>
              <div style={{fontSize: 24, color: C.muted}}>{d}</div>
            </Card>
          ))}
        </div>
        <Stamp f={f} at={cue(0) + 50} text="조건부 승인" />
      </Card>
      <div style={{display: 'flex', gap: 14, marginTop: 24, flexWrap: 'wrap', ...rise(f, cue(1))}}>
        {['충격 뒤 m ≤ 2', '사모 22% 넘으면 약정 중단', '매년 쿠션 재측정'].map((x) => (
          <Chip key={x} color={C.accent}>
            {x}
          </Chip>
        ))}
      </div>
    </Scene>
  );
};

/* S3 발언 · 과제 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const hw = [
    ['개인', '본인의 GBI 설계 — 세 목표 → 버킷 → 달성 확률 (2쪽)'],
    ['개인', 'Flexicure vs 전통 TDF — 65세 · 10년 · 중위 · Floor 위반 · 최악 10%'],
    ['팀', '한국 GBI 플랫폼 상세 설계 (15쪽 + 15분 발표)'],
    ['선택', 'GBI 6-Step 완전 구현 — Cash Trap의 정량화가 채점 핵심'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="과제는 개인 2건과 팀 1건, 그리고 선택 구현 1건입니다" sub="채점 기준 — 수익률이 아니라 목표 달성 확률의 언어로 논증했는가">
      <div style={{fontSize: 44, fontWeight: 900, color: C.accent, marginBottom: 24, ...rise(f, cue(0))}}>“조건 X가 Y이면 답은 Z”</div>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18}}>
        {hw.map((h, i) => (
          <Card key={h[1]} style={{...rise(f, cue(1) + i * 12)}}>
            <div style={{fontSize: 28, color: C.accent, fontWeight: 800}}>{h[0]}</div>
            <div style={{fontSize: 28, marginTop: 6}}>{h[1]}</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

export const M8E09 = makeEpisode(T, [S0, S1, S2, S3]);
export const M8E09_TOTAL = T.total;
void prog;
