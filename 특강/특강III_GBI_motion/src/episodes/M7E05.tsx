import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, HBar} from '../lib/ui';
import {pct, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E05.numbers.json';
import T from '../data/M7E05.timing.json';

const EB = 'BAF.60080 · W06 LDI · ⑤ 잉여금 최적화와 두 블록';
const H = 630;

/* S0 목적 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cs = [
    {k: '목적 — 무엇을 키우나', v: '잉여금 수익률 R_S', s: '평균은 크게, 분산에는 벌점 γ/2'},
    {k: '선택 변수', v: '자산 비중 w', s: '주식 · 장기채 · 현금'},
    {k: '제약', v: '비중의 합 = 1뿐', s: '듀레이션 매칭은 제약이 아니라 해'},
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E05" title="잉여금 최적화의 목적은 잉여금이고, 듀레이션은 제약이 아닙니다" sub="Sharpe–Tint(1990) 잉여금 평균-분산 — Redington과 같은 헤지에 ‘최적화의 답’으로 도달한다">
      <div style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\max_{w}\; \mathbb{E}[R_S] - \frac{\gamma}{2}\,\mathrm{Var}(R_S), \qquad R_S = r_A - \frac{L}{A}\,r_L`} size={50} />
      </div>
      <div style={{display: 'flex', gap: 28, marginTop: 30}}>
        {cs.map((c, i) => (
          <Card key={c.k} style={{flex: 1, border: i === 2 ? `3px solid ${C.accent}` : undefined, ...rise(f, cue(0) + 30 + i * 14)}}>
            <div style={{fontSize: 26, color: C.muted}}>{c.k}</div>
            <div style={{fontSize: 38, fontWeight: 800, marginTop: 6}}>{c.v}</div>
            <div style={{fontSize: 26, color: i === 2 ? C.accent : C.muted, marginTop: 6}}>{c.s}</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

/* S1 두 블록 — 130% 막대 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pP = prog(f, cue(1) + 10, 30);
  const pL = prog(f, cue(1) + 60, 30);
  const pS = prog(f, cue(2) + 10, 30);
  const k = 7; // 1% = 7px
  const x0 = 60;
  return (
    <Scene t={t} eyebrow={EB} title="최적해는 수익 추구(PSP)와 헤지(LHP) 두 블록으로 갈라집니다" sub="한 요인 모형 — 주식 기대초과수익 4% · 변동성 15% · γ = 3.6 · 30년 국채 D_H = 20 · A = 100 · L = 80">
      <div style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`w^* = \underbrace{\frac{1}{\gamma}\,\frac{\lambda}{\sigma^2}}_{\text{PSP · 투기적 수요}} + \underbrace{\frac{L}{A}\,\frac{D_L}{D_H}}_{\text{LHP · 헤지 수요}}`} size={46} />
      </div>
      <svg width={1728} height={300} style={{position: 'absolute', left: 0, top: 270}}>
        <rect x={x0} y={60} width={N.psp_r * 100 * k * pP} height={110} fill={C.asset} rx={8} />
        <text x={x0 + 20} y={128} fill={C.bg} fontSize={34} fontWeight={800} opacity={pP}>
          PSP 주식 ≈{pct(N.psp_r, 0)}
        </text>
        <rect x={x0 + N.psp_r * 100 * k} y={60} width={(1 - N.psp_r) * 100 * k * pL} height={110} fill={C.floor} rx={8} />
        <rect x={x0 + 100 * k} y={60} width={N.swap * 100 * k * pS} height={110} fill="none" stroke={C.liab} strokeWidth={4} strokeDasharray="12 8" rx={8} />
        <text x={x0 + N.psp_r * 100 * k + 20} y={128} fill={C.bg} fontSize={34} fontWeight={800} opacity={pL}>
          LHP 30년 국채 {pct(N.lhp, 0)}
        </text>
        <text x={x0 + 100 * k + 20} y={128} fill={C.liab} fontSize={30} fontWeight={800} opacity={pS}>
          스왑 {pct(N.swap, 0)}
        </text>
        <line x1={x0 + 100 * k} x2={x0 + 100 * k} y1={30} y2={200} stroke={C.text} strokeWidth={3} strokeDasharray="6 6" opacity={pL} />
        <text x={x0 + 100 * k} y={232} fill={C.text} fontSize={26} textAnchor="middle" opacity={pL}>
          자산 100%
        </text>
        <text x={x0 + N.total * 100 * k + 14} y={128} fill={C.accent} fontSize={44} fontWeight={900} opacity={pS}>
          {pct(N.total, 0)}
        </text>
      </svg>
      <div style={{position: 'absolute', left: 60, top: 560, fontSize: 28, color: C.muted, ...rise(f, cue(1) + 80)}}>
        PSP = 4% ÷ (3.6 × 0.15²) = {pct(N.psp, 1)} ≈ 50% · LHP = (1 ÷ 1.25) × (20 ÷ 20) = 80% — 헤지 몫 80 × 20 = 부채 80 × 20
      </div>
    </Scene>
  );
};

/* S2 헤지는 부채가 정한다 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="헤지 몫은 부채가 정하고, 남는 위험 예산만 수익 추구에 씁니다" sub="해의 실무적 함의 — 헤지 비율을 감이 아니라 규칙으로 정한다">
      <div style={{display: 'flex', gap: 30}}>
        <Card style={{flex: 1, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor}}>헤지 몫 식에는 μ도 γ도 없다</div>
          <div style={{fontSize: 28, color: C.muted, marginTop: 8}}>공격적인 기금도 보수적인 기금도 헤지 몫은 같다</div>
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(1))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab}}>성향을 이유로 헤지를 깎으면</div>
          <div style={{fontSize: 28, color: C.muted, marginTop: 8}}>그것은 헤지 조정이 아니라 금리 베팅</div>
        </Card>
      </div>
      <div style={{marginTop: 40, width: 1300}}>
        <div style={{fontSize: 30, marginBottom: 16, ...rise(f, cue(2))}}>주식 50%일 때 잉여금 변동성</div>
        {N.vol.map((v, i) => (
          <HBar key={v.k} f={f} at={cue(2) + 10 + i * 30} label={v.k} value={v.v} max={0.15} text={pct(v.v, 1)} color={i ? C.floor : C.liab} />
        ))}
      </div>
      <div style={{position: 'absolute', right: 0, top: 300, width: 400, fontSize: 30, fontWeight: 700, color: C.accent, ...rise(f, cue(2) + 80)}}>
        운용팀은 두 블록을 만들고, 이사회는 헤지 비율 하나를 정한다
      </div>
    </Scene>
  );
};

/* S3 적립이 부족할수록 헤지에 자금이 더 든다 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const X = (fr: number) => 120 + ((fr - 0.7) / 0.8) * 1000;
  const Y = (h: number) => 560 - ((h - 0.6) / 0.9) * 500;
  const draw = prog(f, cue(0) + 20, 50);
  const n = Math.max(2, Math.round(N.hedge_curve.length * draw));
  const path = N.hedge_curve.slice(0, n).map((p, i) => `${i ? 'L' : 'M'} ${X(p.fr)} ${Y(p.h)}`).join(' ');
  return (
    <Scene t={t} eyebrow={EB} title="적립이 부족할수록 헤지에 자금이 더 들고 수익 추구 몫은 줄어듭니다" sub="D_L = D_H = 20일 때 헤지 비중 = D_L L ÷ (D_H A) = 1 / FR">
      <svg width={1200} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={X(0.7)} y={Y(1.5)} width={X(1.0) - X(0.7)} height={Y(1.0) - Y(1.5)} fill={C.liab} opacity={0.12 * prog(f, cue(2))} />
        <text x={X(0.72)} y={Y(1.45)} fill={C.liab} fontSize={28} fontWeight={700} opacity={prog(f, cue(2))}>
          헤지 &gt; 100% → 스왑 레버리지
        </text>
        <line x1={X(0.7)} x2={X(1.5)} y1={Y(1)} y2={Y(1)} stroke={C.text} strokeWidth={2} strokeDasharray="8 6" />
        <text x={X(1.5)} y={Y(1) - 12} fill={C.text} fontSize={24} textAnchor="end">
          헤지 100%
        </text>
        <line x1={X(0.7)} x2={X(1.5)} y1={560} y2={560} stroke={C.muted} strokeWidth={2} />
        <line x1={X(0.7)} x2={X(0.7)} y1={40} y2={560} stroke={C.muted} strokeWidth={2} />
        {[0.8, 1.0, 1.2, 1.4].map((fr) => (
          <text key={fr} x={X(fr)} y={600} fill={C.muted} fontSize={24} textAnchor="middle">
            FR {Math.round(fr * 100)}%
          </text>
        ))}
        {[0.8, 1.0, 1.2, 1.4].map((h) => (
          <text key={h} x={X(0.7) - 12} y={Y(h) + 8} fill={C.muted} fontSize={24} textAnchor="end">
            {Math.round(h * 100)}%
          </text>
        ))}
        <path d={path} fill="none" stroke={C.floor} strokeWidth={5} />
        {N.pts.map((p, i) => (
          <g key={i} opacity={prog(f, cue(1) + 10 + i * 30)}>
            <circle cx={X(p.fr)} cy={Y(p.h)} r={12} fill={p.h > 1 ? C.liab : C.floor} />
            <text x={i === 1 ? X(p.fr) - 20 : X(p.fr) + 20} y={i === 1 ? Y(p.h) + 44 : Y(p.h) - 16} textAnchor={i === 1 ? 'end' : 'start'} fill={p.h > 1 ? C.liab : C.text} fontSize={30} fontWeight={800}>
              FR {Math.round(p.fr * 100)}% → {pct(p.h, 0)}
            </text>
          </g>
        ))}
      </svg>
      <div style={{position: 'absolute', left: 1240, top: 20, width: 488}}>
        <Card style={{...rise(f, cue(0))}}>
          <Tex tex={String.raw`w_{LHP} = \frac{D_L\,L}{D_H\,A} = \frac{1}{FR}`} size={36} />
        </Card>
        <div style={{fontSize: 32, fontWeight: 800, color: C.liab, marginTop: 30, transform: `scale(${pop(f, cue(2) + 30)})`}}>
          이 레버리지가 2022 위기의 원인
        </div>
        <div style={{fontSize: 26, color: C.muted, marginTop: 10, ...rise(f, cue(2) + 40)}}>모자란 헤지는 IRS로 → 증거금 = 레버리지</div>
      </div>
    </Scene>
  );
};

export const M7E05 = makeEpisode(T, [S0, S1, S2, S3]);
export const M7E05_TOTAL = T.total;
