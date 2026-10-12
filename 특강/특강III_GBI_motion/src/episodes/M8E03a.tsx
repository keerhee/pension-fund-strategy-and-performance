import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, RevealTable} from '../lib/ui';
import {fmt, lerp, pct, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E03a.numbers.json';
import T from '../data/M8E03a.timing.json';

const EB = 'BAF.60080 · W06 GBI · ③ 필요 자본 · 방법 1';
const H = 630;
const GC = [C.floor, C.asset, C.accent];

/* S0 GHP · PSP */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E03a" title="GHP는 목표를 확실히 맞추고 PSP는 수익을 추구합니다" sub="기본 지식 — 두 개의 포트폴리오">
      <div style={{display: 'flex', gap: 34}}>
        <Card style={{flex: 1, borderTop: `6px solid ${C.floor}`, ...rise(f, cue(0))}}>
          <div style={{fontSize: 40, fontWeight: 800, color: C.floor}}>GHP</div>
          <div style={{fontSize: 26, color: C.muted}}>Goal-Hedging Portfolio</div>
          <div style={{fontSize: 32, marginTop: 14}}>목표 금액을 확실히 맞춘다</div>
          <div style={{fontSize: 28, color: C.muted, marginTop: 8}}>물가연동국채 사다리 · 명목 국채 + TIPS + 금리스왑</div>
        </Card>
        <Card style={{flex: 1, borderTop: `6px solid ${C.accent}`, ...rise(f, cue(0) + 16)}}>
          <div style={{fontSize: 40, fontWeight: 800, color: C.accent}}>PSP</div>
          <div style={{fontSize: 26, color: C.muted}}>Performance-Seeking Portfolio</div>
          <div style={{fontSize: 32, marginTop: 14}}>수익을 추구한다</div>
          <div style={{fontSize: 28, color: C.muted, marginTop: 8}}>주식 · 대체투자</div>
        </Card>
      </div>
      <div style={{display: 'flex', gap: 30, marginTop: 30, alignItems: 'center', ...rise(f, cue(1))}}>
        <Card style={{flex: 1, textAlign: 'center'}}>
          <div style={{fontSize: 26, color: C.muted}}>LDI</div>
          <div style={{fontSize: 32, fontWeight: 700}}>부채 복제 + 잉여금 성장</div>
        </Card>
        <div style={{fontSize: 50, color: C.accent}}>=</div>
        <Card style={{flex: 1, textAlign: 'center'}}>
          <div style={{fontSize: 26, color: C.muted}}>GBI</div>
          <div style={{fontSize: 32, fontWeight: 700}}>목표 복제 + 쿠션 성장</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S1 운의 크기 — 성장 ∝ T, 흔들림 ∝ √T */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const X = (yr: number) => 100 + yr * 90;
  const m = 0.06;
  const s = 0.2;
  const Y = (v: number) => 330 - Math.log(v) * 330;
  const p = prog(f, cue(0) + 10, 60);
  const yrs = Array.from({length: 41}, (_, i) => (i / 4) * p);
  const mid = yrs.map((y, i) => `${i ? 'L' : 'M'} ${X(y)} ${Y(Math.exp(m * y))}`).join(' ');
  const band = (z: number) => yrs.map((y, i) => `${i ? 'L' : 'M'} ${X(y)} ${Y(Math.exp(m * y + z * s * Math.sqrt(y)))}`).join(' ');
  return (
    <Scene t={t} eyebrow={EB} title="위험자산은 평균적으로 불어나지만 운에 따라 더 또는 덜 불어납니다" sub="기본 지식 — 95% 확률이면 나쁜 운까지, 30% 확률이면 좋은 운을 기대해도 된다">
      <svg width={1100} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X(0)} x2={X(10)} y1={Y(1)} y2={Y(1)} stroke={C.line} strokeWidth={2} strokeDasharray="6 6" />
        {[0, 5, 10].map((y) => (
          <text key={y} x={X(y)} y={590} fill={C.muted} fontSize={24} textAnchor="middle">
            {y}년
          </text>
        ))}
        <path d={band(-1.645)} fill="none" stroke={C.liab} strokeWidth={4} opacity={prog(f, cue(1))} />
        <path d={band(-0.524)} fill="none" stroke={C.asset} strokeWidth={3} strokeDasharray="8 6" opacity={prog(f, cue(1) + 20)} />
        <path d={band(0.524)} fill="none" stroke={C.accent} strokeWidth={3} strokeDasharray="8 6" opacity={prog(f, cue(1) + 40)} />
        <path d={mid} fill="none" stroke={C.text} strokeWidth={5} />
        <g opacity={prog(f, cue(1) + 50)}>
          <text x={X(10) + 12} y={Y(Math.exp(0.6 - 1.645 * 0.2 * Math.sqrt(10))) + 8} fill={C.liab} fontSize={26} fontWeight={700}>
            95%
          </text>
          <text x={X(10) + 12} y={Y(Math.exp(0.6 - 0.524 * 0.632)) + 8} fill={C.asset} fontSize={26} fontWeight={700}>
            70%
          </text>
          <text x={X(10) + 12} y={Y(Math.exp(0.6)) + 8} fill={C.text} fontSize={26} fontWeight={700}>
            50%
          </text>
          <text x={X(10) + 12} y={Y(Math.exp(0.6 + 0.524 * 0.632)) + 8} fill={C.accent} fontSize={26} fontWeight={700}>
            30%
          </text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 1200, top: 20, width: 528}}>
        <Card style={{...rise(f, cue(0) + 20)}}>
          <div style={{fontSize: 26, color: C.muted}}>운이 없을 때의 성장</div>
          <Tex tex={String.raw`e^{mT}`} size={46} />
        </Card>
        <Card style={{marginTop: 18, ...rise(f, cue(0) + 50)}}>
          <div style={{fontSize: 26, color: C.muted}}>운의 크기</div>
          <Tex tex={String.raw`\sigma\sqrt{T}\;\;(10\text{년} = 3.16\,\sigma)`} size={40} />
        </Card>
        <div style={{fontSize: 28, color: C.muted, marginTop: 18, ...rise(f, cue(1) + 20)}}>주식 연 성장 6% · σ 20% 예</div>
      </div>
    </Scene>
  );
};

/* S2 필요 자본 공식 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const g0 = N.goals[0];
  return (
    <Scene t={t} eyebrow={EB} title="필요 자본은 성장만큼 할인하고 확률만큼 안전마진을 더한 값입니다" sub="로그정규 가정 — T년 뒤 목표 G를 확률 p로 이루려면 오늘 K를 떼어 둔다 (유도는 부록 B-1)">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`K = G \cdot \exp\!\Big(\underbrace{-\,mT}_{\text{성장만큼 할인}} \;+\; \underbrace{z_p\,\sigma\sqrt{T}}_{\text{확률만큼 안전마진}}\Big)`} size={54} />
      </Card>
      <div style={{display: 'flex', gap: 30, marginTop: 26}}>
        <Card style={{flex: 1.3, ...rise(f, cue(1))}}>
          <div style={{fontSize: 28, color: C.muted}}>Safety 6억 · 95% · GHP (m 2%, σ 0)</div>
          <Tex tex={String.raw`K = 6 \times e^{-0.02 \times 10} = ${fmt(g0.K, 2)}\text{억}`} size={46} />
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(2))}}>
          <div style={{fontSize: 28, color: C.muted}}>p &lt; 50%이면</div>
          <div style={{fontSize: 34, fontWeight: 800, color: C.accent, marginTop: 8}}>z가 음수 → 오히려 덜 든다</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S3 K를 키우면 꼬리가 줄어든다 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const xs = N.xs as number[];
  const D = N.dens as number[][];
  const st = prog(f, cue(1), 30) + prog(f, cue(1) + 60, 30); // 0..2
  const i0 = Math.min(1, Math.floor(st));
  const fr = st - i0;
  const d = xs.map((_, i) => lerp(D[i0][i], D[Math.min(2, i0 + 1)][i], fr));
  const Kv = lerp(N.Ks[i0], N.Ks[Math.min(2, i0 + 1)], fr);
  const ph = lerp(N.phit[i0], N.phit[Math.min(2, i0 + 1)], fr);
  const maxd = Math.max(...D[0]);
  const X = (x: number) => 80 + (x / 7.2) * 1000;
  const Y = (v: number) => 540 - (v / maxd) * 420;
  const G = 3;
  const line = xs.map((x, i) => `${i ? 'L' : 'M'} ${X(x)} ${Y(d[i])}`).join(' ');
  const below = xs.map((x, i) => [x, d[i]] as const).filter(([x]) => x <= G);
  const area = `M ${X(below[0][0])} 540 ` + below.map(([x, v]) => `L ${X(x)} ${Y(v)}`).join(' ') + ` L ${X(G)} 540 Z`;
  return (
    <Scene t={t} eyebrow={EB} title="떼어 두는 자금 K를 늘릴수록 목표 미달 꼬리가 줄어듭니다" sub="Market 계좌 — 10년 뒤 3억을 70%로 · 주식 67% 혼합 (로그정규)">
      <svg width={1150} height={H} style={{position: 'absolute', left: 0, top: 0, opacity: prog(f, cue(0))}}>
        <line x1={80} x2={1100} y1={540} y2={540} stroke={C.muted} strokeWidth={2} />
        {[0, 2, 4, 6].map((v) => (
          <text key={v} x={X(v)} y={580} fill={C.muted} fontSize={24} textAnchor="middle">
            {v}억
          </text>
        ))}
        <path d={area} fill={C.liab} opacity={0.35} />
        <path d={line} fill="none" stroke={C.asset} strokeWidth={5} />
        <line x1={X(G)} x2={X(G)} y1={70} y2={540} stroke={C.floor} strokeWidth={4} strokeDasharray="10 8" />
        <text x={X(G) + 12} y={92} fill={C.floor} fontSize={30} fontWeight={800}>
          G = 3억
        </text>
      </svg>
      <div style={{position: 'absolute', left: 1180, top: 20, width: 548}}>
        <Card style={{textAlign: 'center'}}>
          <div style={{fontSize: 28, color: C.muted}}>오늘 떼어 두는 K</div>
          <div style={{fontSize: 90, fontWeight: 900, color: C.asset}}>{fmt(Kv, 2)}억</div>
        </Card>
        <Card style={{textAlign: 'center', marginTop: 20, border: ph > 0.695 ? `3px solid ${C.floor}` : undefined}}>
          <div style={{fontSize: 28, color: C.muted}}>달성 확률</div>
          <div style={{fontSize: 90, fontWeight: 900, color: ph > 0.695 ? C.floor : C.liab}}>{pct(ph, 0)}</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S4 최적 주식 비중 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="목표별 최적 주식 비중은 Merton 비중에서 확률 조정을 뺀 값입니다" sub="방법 1 — 목표마다 확률 p를 딱 채우는 가장 싼 K · 가정 λ 6% · σ 20% · T 10년 (유도는 부록 B-5)">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`w^* = \underbrace{\frac{\lambda}{\sigma^2}}_{\text{Merton } =\, 1.5} \;-\; \underbrace{\frac{z_p}{\sigma\sqrt{T}}}_{\text{확률 조정}}, \qquad K \text{ 최소} \iff g = m - \frac{z\sigma}{\sqrt{T}} \text{ 최대}`} size={46} />
      </Card>
      <div style={{display: 'flex', gap: 26, marginTop: 26}}>
        {N.goals.map((g, i) => (
          <Card key={g.goal} style={{flex: 1, borderTop: `6px solid ${GC[i]}`, ...rise(f, cue(1) + i * 18)}}>
            <div style={{fontSize: 32, fontWeight: 800, color: GC[i]}}>
              {g.goal} {Math.round(g.p * 100)}%
            </div>
            <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>
              1.5 {g.z < 0 ? '+' : '−'} {fmt(Math.abs(g.z), 3)} ÷ 0.632 = {fmt(g.w_raw, 2)}
            </div>
            <div style={{height: 26, background: C.bg2, borderRadius: 8, marginTop: 16, position: 'relative'}}>
              <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${g.w * 100 * prog(f, cue(2) + i * 14, 30)}%`, background: GC[i], borderRadius: 8}} />
            </div>
            <div style={{fontSize: 52, fontWeight: 900, color: GC[i], marginTop: 10}}>주식 {Math.round(g.w * 100)}%</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

/* S5 합계 9.13억 · 49/22/28 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const k = 120; // 1억 = 120px
  const x0 = 60;
  let acc = 0;
  const pL = prog(f, cue(1), 30);
  return (
    <Scene t={t} eyebrow={EB} title="목표마다 공식 비중으로 사면 9.13억이 들고 남는 0.87억은 꿈의 계좌로 갑니다" sub="55세 · 금융자산 10억 · 10년 뒤 은퇴 — 목표 금액과 확률은 개인이, 자본과 배분은 계산이 정한다">
      <svg width={1728} height={300} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={x0} y={60} width={10 * k} height={120} rx={10} fill="none" stroke={C.line} strokeWidth={3} strokeDasharray="10 8" />
        <text x={x0 + 10 * k + 16} y={130} fill={C.muted} fontSize={30}>
          자산 10억
        </text>
        {N.goals.map((g, i) => {
          const p = prog(f, cue(0) + 10 + i * 20, 24);
          const x = x0 + acc * k;
          acc += g.K;
          return (
            <g key={g.goal} opacity={p}>
              <rect x={x} y={60} width={g.K * k * p} height={120} rx={8} fill={GC[i]} stroke={C.bg} strokeWidth={3} />
              <text x={x + 16} y={112} fill={C.bg} fontSize={30} fontWeight={800}>
                {g.goal}
              </text>
              <text x={x + 16} y={152} fill={C.bg} fontSize={30} fontWeight={800}>
                {fmt(g.K, 2)}억
              </text>
            </g>
          );
        })}
        <g opacity={pL}>
          <rect x={x0 + N.total * k} y={60} width={N.left * k} height={120} rx={8} fill={C.accent} opacity={0.5} stroke={C.accent} strokeWidth={3} />
          <text x={x0 + N.total * k + N.left * k / 2} y={230} fill={C.accent} fontSize={28} fontWeight={800} textAnchor="middle">
            남는 {fmt(N.left, 2)}억 → 꿈의 계좌
          </text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 60, top: 280, display: 'flex', gap: 26, width: 1600}}>
        {N.alloc.map((a, i) => (
          <Card key={i} style={{flex: 1, textAlign: 'center', ...rise(f, cue(1) + 30 + i * 12)}}>
            <div style={{fontSize: 30, color: GC[i], fontWeight: 800}}>{N.goals[i].goal}</div>
            <div style={{fontSize: 70, fontWeight: 900, color: GC[i]}}>{Math.round((a / 10) * 100)}%</div>
            <div style={{fontSize: 26, color: C.muted}}>{fmt(a, 2)}억</div>
          </Card>
        ))}
      </div>
      <div style={{position: 'absolute', left: 60, top: 520, fontSize: 32, fontWeight: 800, color: C.accent, transform: `scale(${pop(f, cue(2) + 10)})`, transformOrigin: 'left'}}>
        49 / 22 / 28은 입력이 아니라 결과다
      </div>
    </Scene>
  );
};

export const M8E03a = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M8E03a_TOTAL = T.total;
void RevealTable;
