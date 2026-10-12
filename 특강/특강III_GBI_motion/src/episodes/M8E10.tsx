import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card} from '../lib/ui';
import {fmt, pct, pop, prog, rise, typed} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E05.numbers.json';
import T from '../data/M8E10.timing.json';

const EB = 'BAF.60080 · W06 GBI · ⑨ 실습 · GBI 설계기';
const MONO = "'JetBrains Mono', 'D2Coding', 'Noto Sans Mono CJK KR', monospace";

const Term: React.FC<{text: string; style?: React.CSSProperties}> = ({text, style}) => (
  <div style={{background: '#050D1A', border: `1px solid ${C.line}`, borderRadius: 14, padding: '20px 26px', fontFamily: MONO, fontSize: 28, color: '#CFE3FF', whiteSpace: 'pre-wrap', ...style}}>
    <span style={{color: C.floor}}>&gt; </span>
    {text}
    <span style={{background: C.text, marginLeft: 2}}>&nbsp;</span>
  </div>
);

/* S0 네 단계 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const steps = [
    ['① 메타프롬프트', '원하는 바를 말로'],
    ['② 코드', 'Claude가 작성'],
    ['③ 실행', '“실행해줘” 한 줄'],
    ['④ 결과', '표 · 차트 · 해석'],
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E10" title="실습은 메타프롬프트에서 결과까지 네 단계를 말로 반복합니다" sub="[입력] 프롬프트 · [입력] 명령어 · [출력] 생성물 — 판단은 사람의 몫">
      <div style={{display: 'flex', gap: 14, alignItems: 'center'}}>
        {steps.map((s, i) => (
          <React.Fragment key={s[0]}>
            <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(0) + 10 + i * 16)}}>
              <div style={{fontSize: 32, fontWeight: 800}}>{s[0]}</div>
              <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>{s[1]}</div>
            </Card>
            {i < 3 ? <div style={{fontSize: 40, color: C.accent}}>→</div> : null}
          </React.Fragment>
        ))}
      </div>
      <Term text={typed('2022년식 주식 −20% 충격을 1년차에 넣고, 고정 40/60과 나란히 비교해줘.', f, cue(1) + 10, 14)} style={{marginTop: 34, opacity: prog(f, cue(1))}} />
    </Scene>
  );
};

/* S1 여섯 단계 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const st = [
    ['1', 'Floor', '월 300만 − NPS 150만 → 실질 1.5%, 88세까지'],
    ['2', '쿠션', '금융자산 5억 − Floor'],
    ['3', '필요 자본 K', '의료비 1억(70%) · 손주 교육 5천(30%) — 방법 1'],
    ['4', 'CPPI', 'w = m(A − F)/A · 월간 리밸런싱 · 65→75세 · 1,000 경로'],
    ['5', 'm 민감도', 'm = 1~6 — 중위 · 최악 10% · Floor 위반 · Cash Trap'],
    ['6', '비교', 'Flexicure(매년 F = 0.8A, m = 1) vs 고정 40/60'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="이순자 씨의 GBI 설계기는 여섯 단계로 강의 전체를 재현합니다" sub="Step 3은 방법 1, Step 4~6은 방법 3과 Flexicure — 약 20분 · 주식 연 로그수익 6% · σ 20% · GHP 실질 1.5% · seed 2026">
      {st.map((s, i) => (
        <div key={s[0]} style={{display: 'flex', gap: 22, alignItems: 'center', marginBottom: 14, ...rise(f, (i < 2 ? cue(0) : cue(1)) + 10 + i * 12)}}>
          <div style={{width: 56, height: 56, borderRadius: 12, border: `2px solid ${C.accent}`, background: i === 4 ? C.accent : C.panel, color: i === 4 ? C.bg : C.text, fontSize: 30, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
            {s[0]}
          </div>
          <div style={{width: 200, fontSize: 32, fontWeight: 800}}>{s[1]}</div>
          <div style={{fontSize: 28, color: C.muted}}>{s[2]}</div>
        </div>
      ))}
    </Scene>
  );
};

/* S2 결과 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const tr = N.trap as {m: number; med: number; worst: number; breach: number; trap: number}[];
  const rows: [string, (r: (typeof tr)[0]) => string][] = [
    ['중위 자산', (r) => `${fmt(r.med, 2)}억`],
    ['최악 10% 평균', (r) => `${fmt(r.worst, 2)}억`],
    ['Floor 위반', (r) => pct(r.breach, 1)],
    ['Cash Trap', (r) => pct(r.trap, 1)],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="m이 크면 평균은 좋고 최악은 나쁩니다" sub="[출력] Step 5 승수 민감도 — 75세 · 1,000 경로 · 75세 Floor 2.13억">
      <Card style={{padding: '8px 0', width: 1300}}>
        <div style={{display: 'flex', padding: '14px 30px', fontSize: 30, fontWeight: 800, borderBottom: `1px solid ${C.line}`}}>
          <span style={{flex: 1, color: C.muted}}>지표</span>
          <span style={{flex: 1, color: C.floor, textAlign: 'right'}}>m = 3</span>
          <span style={{flex: 1, color: C.liab, textAlign: 'right'}}>m = 6</span>
        </div>
        {rows.map(([k, fn], i) => (
          <div key={k} style={{display: 'flex', padding: '16px 30px', fontSize: 36, background: i === 3 ? 'rgba(242,140,40,0.12)' : undefined, ...rise(f, cue(0) + 10 + i * 18)}}>
            <span style={{flex: 1, color: C.muted}}>{k}</span>
            <span style={{flex: 1, textAlign: 'right', fontWeight: 700}}>{fn(tr[0])}</span>
            <span style={{flex: 1, textAlign: 'right', fontWeight: 700, opacity: prog(f, cue(1) + i * 12)}}>{fn(tr[1])}</span>
          </div>
        ))}
      </Card>
      <div style={{fontSize: 38, fontWeight: 800, color: C.accent, marginTop: 28, transform: `scale(${pop(f, cue(2) + 6)})`, transformOrigin: 'left'}}>Cash Trap 확률이 승수 선택의 진짜 비용</div>
    </Scene>
  );
};

/* S3 발언 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="시뮬레이션 숫자는 목표 언어의 IC 발언으로 번역해야 힘이 생깁니다" sub="결과 읽기 — 시뮬레이션은 재료일 뿐, 판단과 문장은 사람의 몫이다">
      <div style={{display: 'flex', gap: 34}}>
        <Card style={{flex: 1, borderTop: `6px solid ${C.liab}`, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab}}>나쁜 발언 — 수익률 언어</div>
          {['“수익률이 낮아 보인다”', '“주식을 더 담아야”', '근거 없는 형용사'].map((x) => (
            <div key={x} style={{fontSize: 32, marginTop: 16, textDecoration: f > cue(1) ? 'line-through' : 'none', color: f > cue(1) ? C.muted : C.text}}>
              {x}
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, borderTop: `6px solid ${C.floor}`, ...rise(f, cue(1))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor}}>좋은 발언 — 목표 언어 + 숫자</div>
          {['“m = 6이면 Cash Trap 21%”', '“m = 3이면 Floor 위반 0%”', '시뮬레이션 근거'].map((x, i) => (
            <div key={x} style={{fontSize: 32, marginTop: 16, ...rise(f, cue(1) + 20 + i * 14)}}>
              {x}
            </div>
          ))}
        </Card>
      </div>
      <div style={{fontSize: 36, fontWeight: 800, color: C.accent, marginTop: 30, ...rise(f, cue(1) + 80)}}>AI가 계산을, 사람이 판단을 — AI-Native 운용역의 분업</div>
    </Scene>
  );
};

export const M8E10 = makeEpisode(T, [S0, S1, S2, S3]);
export const M8E10_TOTAL = T.total;
