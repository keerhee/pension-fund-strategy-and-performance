import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, RevealTable} from '../lib/ui';
import {lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import T from '../data/M8E02.timing.json';

const EB = 'BAF.60080 · W06 GBI · ② 심리계정';
const H = 630;

/* S0 Thaler 심리계정 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const jars = [
    {k: '월급', v: '아낀다', c: C.floor},
    {k: '보너스', v: '쉽게 쓴다', c: C.accent},
    {k: '여행 적금', v: '지킨다', c: C.asset},
    {k: '노후 계좌', v: '건드리지 않는다', c: C.floor},
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E02" title="GBI는 Mental Accounting을 오류가 아니라 인터페이스로 씁니다" sub="Thaler(1985) — 자금에는 꼬리표가 붙는다">
      <div style={{display: 'flex', gap: 30, justifyContent: 'center'}}>
        {jars.map((j, i) => (
          <div key={j.k} style={{textAlign: 'center', ...rise(f, (i < 3 ? cue(1) : cue(2)) + (i % 3) * 14)}}>
            <div style={{width: 300, height: 260, borderRadius: '30px 30px 60px 60px', border: `5px solid ${j.c}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: C.panel}}>
              <div style={{fontSize: 40, fontWeight: 900, color: j.c}}>{j.k}</div>
              <div style={{fontSize: 28, marginTop: 10}}>{j.v}</div>
            </div>
          </div>
        ))}
      </div>
      <div style={{fontSize: 36, fontWeight: 800, color: C.accent, textAlign: 'center', marginTop: 40, ...rise(f, cue(2) + 30)}}>
        편향을 설계에 쓴다 — 계좌별 목표 → 패닉 매도 감소, 행동의 방화벽
      </div>
    </Scene>
  );
};

/* S1 BPT · 7번 거절 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const rej = Math.min(7, Math.floor(prog(f, cue(1) + 6, 60) * 7.99));
  const cites = Math.round(lerp(0, 5000, prog(f, cue(1) + 80, 40)));
  return (
    <Scene t={t} eyebrow={EB} title="행동 포트폴리오 이론은 계좌별로 나눠 생각하는 사람의 최적화입니다" sub="Shefrin–Statman(2000) — Thaler의 Mental Accounting(1985)을 최적화 문제로 쓴다">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\max \;\sum_{\text{계좌 } k} \mathbb{E}[W_k] \quad \text{s.t.}\quad P(W_k < \text{열망 수준}_k) \le \alpha_k`} size={46} />
      </Card>
      <div style={{display: 'flex', gap: 40, marginTop: 30}}>
        <Card style={{flex: 1, ...rise(f, cue(1))}}>
          <div style={{fontSize: 30, color: C.muted}}>1994~2000 · 주요 학술지</div>
          <div style={{display: 'flex', gap: 12, marginTop: 14}}>
            {Array.from({length: 7}).map((_, i) => (
              <div key={i} style={{width: 64, height: 84, borderRadius: 8, border: `3px solid ${i < rej ? C.liab : C.line}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 40, color: C.liab, fontWeight: 900}}>
                {i < rej ? '✗' : ''}
              </div>
            ))}
          </div>
          <div style={{fontSize: 30, marginTop: 14}}>“너무 비주류 · 엄밀성 부족” → 2000년 게재</div>
        </Card>
        <Card style={{width: 520, textAlign: 'center', ...rise(f, cue(1) + 80)}}>
          <div style={{fontSize: 30, color: C.muted}}>재평가 — 인용</div>
          <div style={{fontSize: 96, fontWeight: 900, color: C.floor}}>{cites.toLocaleString()}+</div>
          <div style={{fontSize: 26, color: C.muted}}>Thaler 노벨상(2017) · GBI의 이론적 표준</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S2 Das–Markowitz (H, α) */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="Das–Markowitz는 계좌마다 (H, α) 두 숫자만 묻습니다" sub="Das–Markowitz–Scheid–Statman(2010) — 계좌 나누기는 그대로, 평균-분산으로 풀 수 있는 꼴로">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\max_{w}\; \mu_p \quad \text{s.t.}\quad P(R_p < H) \le \alpha \;\;\Longleftrightarrow\;\; \mu_p - z_{\alpha}\,\sigma_p \ge H`} size={46} />
      </Card>
      <div style={{display: 'flex', gap: 30, marginTop: 30}}>
        <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(1))}}>
          <div style={{fontSize: 30, color: C.muted}}>H · 최소 수익률</div>
          <div style={{fontSize: 80, fontWeight: 900, color: C.floor}}>−10%</div>
        </Card>
        <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(1) + 14)}}>
          <div style={{fontSize: 30, color: C.muted}}>α · 미달 확률 한도</div>
          <div style={{fontSize: 80, fontWeight: 900, color: C.floor}}>5%</div>
        </Card>
        <div style={{fontSize: 70, color: C.accent, alignSelf: 'center', opacity: prog(f, cue(2))}}>⇔</div>
        <Card style={{flex: 1, textAlign: 'center', border: `3px solid ${C.accent}`, transform: `scale(${pop(f, cue(2) + 10)})`}}>
          <div style={{fontSize: 30, color: C.muted}}>위험회피도</div>
          <div style={{fontSize: 80, fontWeight: 900, color: C.accent}}>γ 3.8</div>
        </Card>
      </div>
      <div style={{fontSize: 30, color: C.muted, marginTop: 24, ...rise(f, cue(2) + 30)}}>
        “5% 확률로도 −10% 아래는 안 된다”는 목표 언어가 γ = 3.795와 같은 말 — 풀이는 단원 ③ 방법 2
      </div>
    </Scene>
  );
};

/* S3 세 방식 비교 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="심리계정 세 방식 — 관찰 · 행동의 최적화 · 운용의 최적화" sub="같은 심리계정, 세 가지 쓰임">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={27}
          cols={['구분', 'Thaler (1985)', 'Shefrin–Statman (2000) BPT', 'Das–Markowitz (2010)']}
          widths={[0.6, 1, 1.2, 1.2]}
          rows={[
            {cells: ['입력', '없음 — 습관을 묘사', '계좌별 열망 수준 · α', '계좌별 (H, α) + μ · Σ'], at: cue(0) + 10},
            {cells: ['푸는 문제', '풀지 않는다', '미달 ≤ α 아래 기대 부 최대', '미달 ≤ α 아래 기대수익 최대 → γ'], at: cue(0) + 24},
            {cells: ['해의 성질', '—', '합치면 평균-분산 비효율', '공매도 허용 시 합쳐도 효율선 위'], at: cue(1), hi: f >= cue(1)},
            {cells: ['실무 한계', '설계 지침이 없다', '해가 복잡 · 비효율', '정규 가정 · 미달의 크기는 못 막음'], at: cue(1) + 30},
          ]}
        />
      </div>
    </Scene>
  );
};

/* S4 3계층 버킷 — 아래층부터 채운다 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const fill = prog(f, cue(0) + 10, 120); // 0..1 전체 물 높이
  const tiers = [
    {k: 'Safety', a: 'RB / GHP', c: C.floor, cap: 0.49},
    {k: 'Market', a: '60/40', c: C.asset, cap: 0.22},
    {k: 'Aspirational', a: '주식 · 대체', c: C.accent, cap: 0.29},
  ];
  let acc = 0;
  const x0 = 80;
  const wB = 700;
  const hB = 170;
  return (
    <Scene t={t} eyebrow={EB} title="아래층이 채워져야 위층에 자금이 가는 3계층 버킷이 GBI의 골격입니다" sub="Safety는 RB/GHP, Market은 60/40, Aspirational은 주식·대체">
      <svg width={900} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        {tiers.map((x, i) => {
          const lv = Math.max(0, Math.min(1, (fill - acc) / x.cap));
          acc += x.cap;
          const y = 440 - i * (hB + 14);
          return (
            <g key={x.k}>
              <rect x={x0} y={y} width={wB} height={hB} rx={14} fill="none" stroke={x.c} strokeWidth={4} />
              <rect x={x0 + 4} y={y + hB - (hB - 8) * lv - 4} width={wB - 8} height={(hB - 8) * lv} rx={10} fill={x.c} opacity={0.75} />
              <text x={x0 + 24} y={y + 56} fill={C.text} fontSize={36} fontWeight={800}>
                {x.k}
              </text>
              <text x={x0 + 24} y={y + 100} fill={C.text} fontSize={28}>
                {x.a}
              </text>
              {i < 2 ? <path d={`M ${x0 + wB - 30} ${y - 4} l 0 -12`} stroke={C.muted} strokeWidth={3} /> : null}
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: 900, top: 20, width: 828}}>
        <Card style={{...rise(f, cue(1))}}>
          <div style={{fontSize: 30, fontWeight: 800}}>이론적 뿌리</div>
          {['Thaler (1985) 마음속 계좌', 'Shefrin–Statman (2000) BPT', 'Chhabra (2005) 3계층'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 10}}>
              • {x}
            </div>
          ))}
        </Card>
        <div style={{fontSize: 34, fontWeight: 800, color: C.accent, marginTop: 30, ...rise(f, cue(2))}}>계층은 독립 운용 — 실패해도 무엇이 실패했는지 안다</div>
      </div>
    </Scene>
  );
};

export const M8E02 = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M8E02_TOTAL = T.total;
