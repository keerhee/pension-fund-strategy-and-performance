import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, RevealTable} from '../lib/ui';
import {fmt, lerp, pct, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E05.numbers.json';
import T from '../data/M8E05.timing.json';

const EB = 'BAF.60080 · W06 GBI · ⑤ 쿠션과 승수 · CPPI · Flexicure';
const H = 630;

/* S0 Flexicure · 비유 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const m = [
    {k: 'RB = 노후 월세 선불', v: '20년치 월세를 오늘 산다 — 그 가격이 Floor'},
    {k: 'Floor = 체육관 매트', v: '떨어져도 다치지 않는 선 — 매트가 담력을 만든다'},
    {k: '쿠션 두께만큼 뛴다', v: '쿠션 = A − F · 얇아지면 스스로 낮춘다'},
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E05" title="Flexicure는 하한을 보장한 위에서 효용을 극대화합니다" sub="Martellini–Milhau — Flexibility + Security">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\max\; \mathbb{E}[u(W_T)] \quad \text{s.t.}\quad W_t \ge F_t \;\;\forall t`} size={50} />
      </Card>
      <div style={{display: 'flex', gap: 24, marginTop: 24}}>
        {m.map((x, i) => (
          <Card key={x.k} style={{flex: 1, ...rise(f, cue(1) + i * 20)}}>
            <div style={{fontSize: 32, fontWeight: 800, color: C.accent}}>{x.k}</div>
            <div style={{fontSize: 26, color: C.muted, marginTop: 10}}>{x.v}</div>
          </Card>
        ))}
      </div>
      <div style={{fontSize: 32, fontWeight: 800, color: C.liab, marginTop: 24, ...rise(f, cue(2))}}>LTCM은 매트 없이 27배 높이에서 뛰었다 — 케이스 1부의 반면교사</div>
    </Scene>
  );
};

/* S1 규칙 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="위험자산을 쿠션의 m배로 두면 1/m 미만의 급락에는 Floor가 지켜집니다" sub="원리 — 위험자산이 x만큼 떨어지면 손실은 m(A − F)·x, 이것이 쿠션보다 작아야 한다">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`E_t = m\,(A_t - F_t), \qquad w_t = \frac{E_t}{A_t} = m\Big(1 - \frac{F_t}{A_t}\Big)`} size={44} />
      </Card>
      <Card style={{marginTop: 16, ...rise(f, cue(1))}}>
        <Tex tex={String.raw`\underbrace{m\,C\,x}_{\text{손실}} \;<\; \underbrace{C}_{\text{쿠션}} \;\;\Longleftrightarrow\;\; x < \frac{1}{m}`} size={44} />
      </Card>
      <div style={{fontSize: 34, fontWeight: 800, color: C.floor, marginTop: 24, transform: `scale(${pop(f, cue(2) + 6)})`, transformOrigin: 'left'}}>
        m = 4면 25% 미만의 급락에는 Floor가 지켜진다
      </div>
    </Scene>
  );
};

/* S2 자동 축소 — CPPI 라이브 차트 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const X = (a: number) => 120 + ((a - 4) / 8) * 880;
  const Y = (w: number) => 540 - w * 440;
  const m4 = N.m4 as {A: number; w: number}[];
  const m2 = N.m2 as {A: number; w: number}[];
  const path = (d: {A: number; w: number}[]) => d.map((p, i) => `${i ? 'L' : 'M'} ${X(p.A)} ${Y(p.w)}`).join(' ');
  // 자산이 10 → 5로 내려간다
  const s1 = prog(f, cue(1), 50);
  const s2 = prog(f, cue(2), 40);
  const A = s1 < 1 ? lerp(10, 6, s1) : lerp(6, 5, s2);
  const w = Math.min(1, Math.max(0, (4 * (A - 5)) / A));
  return (
    <Scene t={t} eyebrow={EB} title="자산이 10억에서 5억으로 떨어지면 PSP 비중이 100%에서 0%로 줄어듭니다" sub="Flexicure 동적 배분 — 쿠션이 줄면 PSP가 자동 축소된다 (F = 5억, m = 4 · 레버리지 금지로 상한 100%)">
      <svg width={1100} height={H} style={{position: 'absolute', left: 0, top: 0, opacity: prog(f, cue(0))}}>
        <rect x={X(4)} y={Y(1)} width={X(5) - X(4)} height={440} fill={C.liab} opacity={0.12} />
        <text x={X(4.5)} y={Y(0.5)} fill={C.liab} fontSize={24} textAnchor="middle">
          Floor 아래
        </text>
        <line x1={X(5)} x2={X(5)} y1={Y(1)} y2={540} stroke={C.floor} strokeWidth={3} strokeDasharray="8 6" />
        <text x={X(5) + 10} y={Y(1) - 10} fill={C.floor} fontSize={26} fontWeight={800}>
          F = 5억
        </text>
        <line x1={X(4)} x2={X(12)} y1={540} y2={540} stroke={C.muted} strokeWidth={2} />
        {[4, 6, 8, 10, 12].map((a) => (
          <text key={a} x={X(a)} y={578} fill={C.muted} fontSize={24} textAnchor="middle">
            {a}억
          </text>
        ))}
        {[0, 0.5, 1].map((v) => (
          <text key={v} x={X(4) - 12} y={Y(v) + 8} fill={C.muted} fontSize={24} textAnchor="end">
            {Math.round(v * 100)}%
          </text>
        ))}
        <path d={path(m2)} fill="none" stroke={C.muted} strokeWidth={3} strokeDasharray="8 6" />
        <text x={X(11.5)} y={Y(m2[m2.length - 6].w) + 34} fill={C.muted} fontSize={24}>
          m = 2
        </text>
        <path d={path(m4)} fill="none" stroke={C.asset} strokeWidth={5} />
        <text x={X(8)} y={Y(1) - 14} fill={C.asset} fontSize={26} fontWeight={800}>
          m = 4
        </text>
        <circle cx={X(A)} cy={Y(w)} r={16} fill={C.accent} />
      </svg>
      <div style={{position: 'absolute', left: 1140, top: 20, width: 588}}>
        <Card style={{textAlign: 'center'}}>
          <div style={{fontSize: 28, color: C.muted}}>자산 A</div>
          <div style={{fontSize: 80, fontWeight: 900}}>{fmt(A, 1)}억</div>
        </Card>
        <Card style={{textAlign: 'center', marginTop: 18}}>
          <div style={{fontSize: 28, color: C.muted}}>PSP 비중</div>
          <div style={{fontSize: 80, fontWeight: 900, color: w < 0.01 ? C.liab : C.asset}}>{pct(w, 0)}</div>
        </Card>
        <div style={{fontSize: 28, fontWeight: 700, color: C.liab, marginTop: 18, opacity: prog(f, cue(2) + 40)}}>쿠션 0 → 전액 안전자산 → Cash Trap</div>
      </div>
    </Scene>
  );
};

/* S3 Black–Jones */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const legacy = [
    {y: '1973', k: 'Black–Scholes'},
    {y: '1987', k: 'CPPI (Black–Jones)'},
    {y: '1992', k: 'Black–Litterman'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="Black과 Jones의 CPPI는 수학 한 줄로 동적 보호를 구현했습니다" sub="에피소드 · Black–Jones(1987) · Black–Perold(1992) — Flexicure의 직계 조상">
      <div style={{display: 'flex', gap: 30}}>
        <Card style={{flex: 1, ...rise(f, cue(0))}}>
          <div style={{fontSize: 32, fontWeight: 800, color: C.asset}}>단순함의 힘 — 두 변수 m과 F</div>
          {['델타헤지 없이 규칙 기반', '1987 블랙먼데이 상대적 선방', 'Martellini가 은퇴로 재포장'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 12}}>
              • {x}
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(0) + 20)}}>
          <div style={{fontSize: 32, fontWeight: 800, color: C.accent}}>진화의 연속성</div>
          {['보험에서 은퇴 목표로', '2008 일부 Cash Trap 노출', 'TIPP · Dynamic Floor'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 12}}>
              • {x}
            </div>
          ))}
        </Card>
      </div>
      <div style={{display: 'flex', gap: 20, marginTop: 30}}>
        {legacy.map((l, i) => (
          <Card key={l.y} style={{flex: 1, textAlign: 'center', border: i === 1 ? `3px solid ${C.accent}` : undefined, ...rise(f, cue(1) + i * 16)}}>
            <div style={{fontSize: 42, fontWeight: 900, color: C.accent}}>{l.y}</div>
            <div style={{fontSize: 28, fontWeight: 700}}>{l.k}</div>
          </Card>
        ))}
      </div>
      <div style={{fontSize: 28, color: C.muted, marginTop: 16, ...rise(f, cue(1) + 60)}}>Fischer Black의 유산 — BS(73) · CPPI(87) · BL(92), 이 과목에서 모두 만난다</div>
    </Scene>
  );
};

/* S4 VaR로 m 정하기 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pB = prog(f, cue(2) + 20, 40);
  return (
    <Scene t={t} eyebrow={EB} title="승수 m은 VaR로 정한다 — 손실이 쿠션을 넘지 않게" sub="쿠션 C = A − F, 위험 노출 E = m × C · 최악 하락률 x(리밸런싱 사이 VaR)에서 손실 E × x ≤ C">
      <div style={{display: 'flex', gap: 30}}>
        <div style={{width: 700}}>
          <RevealTable
            f={f}
            size={28}
            cols={['최악 하락률 x', 'm 상한 = 1/x']}
            rows={N.var.map((v, i) => ({cells: [`${Math.round(v.x * 100)}%${['  (월간 99%)', '  (하루 −20%, 1987)', '', '  (기본 답 m ≤ 2)'][i]}`, String(v.m)], at: cue(1) + i * 14}))}
          />
        </div>
        <div style={{flex: 1}}>
          <div style={{fontSize: 28, color: C.muted, ...rise(f, cue(2))}}>A = 100 · F = 80 · m = 3 → 쿠션 20 · 노출 60</div>
          {[
            {x: 0.2, loss: 12, ok: true},
            {x: 0.4, loss: 24, ok: false},
          ].map((s, i) => (
            <div key={s.x} style={{marginTop: 22, ...rise(f, cue(2) + 10 + i * 20)}}>
              <div style={{fontSize: 28, marginBottom: 6}}>
                x = {Math.round(s.x * 100)}% → 손실 60 × {Math.round(s.x * 100)}% = <b style={{color: s.ok ? C.floor : C.liab}}>{s.loss}</b>
              </div>
              <div style={{height: 50, background: C.bg2, borderRadius: 10, position: 'relative'}}>
                <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${(s.loss / 30) * 100 * pB}%`, background: s.ok ? C.floor : C.liab, borderRadius: 10}} />
                <div style={{position: 'absolute', left: `${(20 / 30) * 100}%`, top: -8, bottom: -8, width: 4, background: C.text}} />
                <div style={{position: 'absolute', left: `${(20 / 30) * 100 + 1}%`, top: 8, fontSize: 24, fontWeight: 700}}>쿠션 20</div>
              </div>
              <div style={{fontSize: 28, fontWeight: 800, color: s.ok ? C.floor : C.liab, marginTop: 6, opacity: pB}}>{s.ok ? 'Floor 지킴 (m 3 ≤ 1/x = 5)' : 'Floor 뚫림 (m 3 > 1/x = 2.5)'}</div>
            </div>
          ))}
        </div>
      </div>
    </Scene>
  );
};

/* S5 Cash Trap — m의 진짜 비용 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const tr = N.trap as {m: number; med: number; worst: number; breach: number; trap: number}[];
  return (
    <Scene t={t} eyebrow={EB} title="m이 크면 평균은 좋아지지만 최악은 나빠지고 Cash Trap에 갇힙니다" sub="실습 Step 5 — 이순자 씨 65→75세 · 1,000 경로 · 출발 Floor 3.50억 → 75세 2.13억">
      <div style={{display: 'flex', gap: 30}}>
        {tr.map((r, i) => (
          <Card key={r.m} style={{flex: 1, borderTop: `6px solid ${i ? C.liab : C.floor}`, ...rise(f, cue(1) + i * 30)}}>
            <div style={{fontSize: 44, fontWeight: 900, color: i ? C.liab : C.floor}}>m = {r.m}</div>
            {[
              ['중위 자산', `${fmt(r.med, 2)}억`],
              ['최악 10% 평균', `${fmt(r.worst, 2)}억`],
              ['Floor 위반', pct(r.breach, 1)],
            ].map(([k, v]) => (
              <div key={k} style={{display: 'flex', justifyContent: 'space-between', fontSize: 30, marginTop: 12}}>
                <span style={{color: C.muted}}>{k}</span>
                <span style={{fontWeight: 700}}>{v}</span>
              </div>
            ))}
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: 16}}>
              <span style={{fontSize: 30, color: C.muted}}>Cash Trap</span>
              <span style={{fontSize: 64, fontWeight: 900, color: i ? C.liab : C.floor, transform: `scale(${pop(f, cue(1) + 20 + i * 30)})`, display: 'inline-block'}}>{pct(r.trap, 1)}</span>
            </div>
          </Card>
        ))}
      </div>
      <div style={{fontSize: 38, fontWeight: 800, color: C.accent, marginTop: 30, ...rise(f, cue(2))}}>갇힐 확률이 m의 진짜 비용 — 2008 CPPI의 경험</div>
    </Scene>
  );
};

export const M8E05 = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M8E05_TOTAL = T.total;
