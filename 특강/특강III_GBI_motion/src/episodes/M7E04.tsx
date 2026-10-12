import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, HBar, RevealTable} from '../lib/ui';
import {fmt, lerp, pop, prog, rise, signed} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E04.numbers.json';
import T from '../data/M7E04.timing.json';

const EB = 'BAF.60080 · W06 LDI · ④ 면역화와 Redington';
const H = 630;

/* S0 1952 에피소드 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const ev = [
    {y: '1952', v: 'Redington — “Immunization” 제안', at: cue(0) + 10},
    {y: '1990s', v: 'DB 연기금 LDI의 표준', at: cue(2) + 4},
    {y: '2000s', v: 'IRS 기반 LDI 확산', at: cue(2) + 30},
    {y: '2022', v: '영국 위기 해석에도 유효', at: cue(2) + 56},
  ];
  const lineP = prog(f, cue(2), 70);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E04" title="Redington은 테일러 전개 한 줄로 현대 LDI의 기초를 놓았습니다" sub="에피소드 · 1952 — 런던 보험사 액추어리의 질문 “금리가 움직여도 잉여금을 지키려면?”">
      <div style={{position: 'relative', height: 220}}>
        <div style={{position: 'absolute', left: 40, right: 40, top: 60, height: 4, background: C.line}} />
        <div style={{position: 'absolute', left: 40, top: 60, height: 4, width: `${(0.1 + lineP * 0.9) * 94}%`, background: C.accent}} />
        {ev.map((e, i) => (
          <div key={e.y} style={{position: 'absolute', left: `${2 + i * 26}%`, top: 40, width: 340, ...rise(f, e.at)}}>
            <div style={{width: 44, height: 44, borderRadius: 22, background: i === 0 ? C.accent : C.panel, border: `3px solid ${C.accent}`}} />
            <div style={{fontSize: 44, fontWeight: 900, color: C.accent, marginTop: 14}}>{e.y}</div>
            <div style={{fontSize: 28, marginTop: 4}}>{e.v}</div>
          </div>
        ))}
      </div>
      <Card style={{marginTop: 30, ...rise(f, cue(1))}}>
        <Tex
          tex={String.raw`\Delta S \approx \underbrace{-(D_A A - D_L L)\,\Delta y}_{\text{1차 항} \,=\, 0} + \underbrace{\tfrac{1}{2}(C_A A - C_L L)(\Delta y)^2}_{\text{2차 항} \,\ge\, 0}`}
          size={46}
        />
      </Card>
    </Scene>
  );
};

/* S1 세 조건 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cs = [
    {k: '조건 1 · 현재가치', tex: String.raw`A \ge L`, v: '막는 것: 출발선 부족'},
    {k: '조건 2 · 금액 듀레이션', tex: String.raw`D_A A = D_L L`, v: '막는 것: 1차 항(방향)'},
    {k: '조건 3 · 금액 볼록성', tex: String.raw`C_A A \ge C_L L`, v: '막는 것: 2차 항(휘어짐)'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="Redington 면역화는 현재가치 · 듀레이션 · 볼록성 세 조건입니다" sub="Redington(1952) — 잉여금 변화의 전개식에서 1차 항을 0으로, 2차 항을 양수로 만든다">
      <div style={{display: 'flex', gap: 30}}>
        {cs.map((c, i) => (
          <Card key={c.k} style={{flex: 1, textAlign: 'center', borderTop: `6px solid ${[C.asset, C.accent, C.floor][i]}`, ...rise(f, cue(i))}}>
            <div style={{fontSize: 32, fontWeight: 800}}>{c.k}</div>
            <Tex tex={c.tex} size={58} />
            <div style={{fontSize: 28, color: C.muted}}>{c.v}</div>
            <div style={{fontSize: 70, color: C.floor, transform: `scale(${pop(f, cue(i) + 30)})`}}>✓</div>
          </Card>
        ))}
      </div>
      <div style={{fontSize: 26, color: C.muted, marginTop: 24, ...rise(f, cue(2) + 40)}}>
        ※ 세 조건은 모두 금액(×A, ×L) 꼴 — A = L일 때만 “자산 D = 부채 D · 자산 C &gt; 부채 C”로 줄어든다 · 증명은 부록 B-3
      </div>
    </Scene>
  );
};

/* S2 금액 듀레이션 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const p = prog(f, cue(1) + 60, 50);
  return (
    <Scene t={t} eyebrow={EB} title="금액 듀레이션을 맞추면 금리 방향과 무관하게 1차 효과가 사라집니다" sub="조건 2의 근거 — 전개식 전체에서 첫 항(1차, 방향)만 본다">
      <div style={{width: 1300}}>
        <HBar f={f} at={cue(0) + 10} label={p > 0.5 ? "자산 금액 듀레이션 — 헤지로 부채와 일치" : "자산 금액 듀레이션 D_A × A = 3 × 100"} value={lerp(N.dd_A, N.dd_L, p)} max={1700} text={fmt(lerp(N.dd_A, N.dd_L, p), 0)} color={C.asset} />
        <HBar f={f} at={cue(0) + 30} label="부채 금액 듀레이션 D_L × L = 20 × 80" value={N.dd_L} max={1700} text={fmt(N.dd_L, 0)} color={C.liab} />
      </div>
      <Card style={{marginTop: 20, width: 1300, ...rise(f, cue(1))}}>
        <Tex tex={String.raw`-(300 - 1{,}600)\times(-0.01) = -13`} size={48} />
      </Card>
      <div style={{position: 'absolute', left: 1360, top: 60, width: 360, textAlign: 'center', opacity: prog(f, cue(1) + 60)}}>
        <div style={{fontSize: 30, color: C.muted}}>괄호가 0이 되면</div>
        <div style={{fontSize: 72, fontWeight: 900, color: C.floor, whiteSpace: 'nowrap', transform: `scale(${pop(f, cue(1) + 100)})`}}>h = 100%</div>
        <div style={{fontSize: 30, color: C.muted, marginTop: 10}}>1차 효과 {signed(lerp(N.first, 0, p), 1)}</div>
      </div>
    </Scene>
  );
};

/* S3 바벨 vs 불일치 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  // 왼쪽: 현금흐름
  const X = (yr: number) => 70 + yr * 44;
  const base = 470;
  const k = 3.2;
  const showBar = prog(f, cue(1), 24);
  const showMis = prog(f, cue(2), 24);
  // 오른쪽: 잉여금-금리 곡선
  const CX = (d: number) => 830 + ((d + 0.03) / 0.06) * 820;
  const CY = (s: number) => 300 - s * 26;
  const drawP = prog(f, cue(3), 60);
  const n = Math.max(2, Math.round(N.curve.length * drawP));
  const pts = N.curve.slice(0, n);
  const path = (key: 'bar' | 'mis') => pts.map((p, i) => `${i ? 'L' : 'M'} ${CX(p.d)} ${CY(p[key])}`).join(' ');
  const hit = prog(f, cue(3) + 60, 20);
  return (
    <Scene t={t} eyebrow={EB} title="부채를 양쪽에서 감싸는 바벨은 면역되고 짧은 자산은 금리 하락에 무너집니다" sub="숫자 검증 — 부채 10년 뒤 100(PV 60.65), y = 5% 연속복리">
      <svg width={1728} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X(0)} x2={X(16)} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        {[0, 5, 10, 15].map((y) => (
          <text key={y} x={X(y)} y={base + 40} fill={C.muted} fontSize={24} textAnchor="middle">
            {y}년
          </text>
        ))}
        <g opacity={prog(f, cue(0))}>
          <rect x={X(10) - 26} y={base - 100 * k} width={52} height={100 * k} rx={6} fill={C.liab} opacity={0.85} />
          <text x={X(10)} y={base - 100 * k - 14} fill={C.liab} fontSize={28} fontWeight={800} textAnchor="middle">
            부채 100
          </text>
        </g>
        <g opacity={showBar * (1 - 0.6 * showMis)}>
          <rect x={X(5) - 60} y={base - N.f5 * k} width={52} height={N.f5 * k} rx={6} fill={C.asset} />
          <rect x={X(15) - 26} y={base - N.f15 * k} width={52} height={N.f15 * k} rx={6} fill={C.asset} />
          <text x={X(5) - 34} y={base - N.f5 * k - 12} fill={C.asset} fontSize={24} fontWeight={700} textAnchor="middle">
            {fmt(N.f5, 2)}
          </text>
          <text x={X(15)} y={base - N.f15 * k - 12} fill={C.asset} fontSize={24} fontWeight={700} textAnchor="middle">
            {fmt(N.f15, 2)}
          </text>
          <text x={X(10)} y={base + 80} fill={C.asset} fontSize={26} fontWeight={700} textAnchor="middle">
            바벨 D = 10 · C = 125
          </text>
        </g>
        <g opacity={showMis}>
          <rect x={X(5) + 6} y={base - N.fm * k} width={52} height={N.fm * k} rx={6} fill={C.accent} />
          <text x={X(5) + 32} y={base - N.fm * k - 12} fill={C.accent} fontSize={24} fontWeight={700} textAnchor="middle">
            {fmt(N.fm, 2)}
          </text>
          <text x={X(10)} y={base + 116} fill={C.accent} fontSize={26} fontWeight={700} textAnchor="middle">
            불일치 D = 5
          </text>
        </g>
        {/* 잉여금 곡선 */}
        <g opacity={prog(f, cue(3) - 10)}>
          <text x={CX(-0.03)} y={40} fill={C.muted} fontSize={26}>
            잉여금 변화 ΔS
          </text>
          <line x1={CX(-0.03)} x2={CX(0.03)} y1={CY(0)} y2={CY(0)} stroke={C.muted} strokeWidth={2} />
          <line x1={CX(0)} x2={CX(0)} y1={60} y2={560} stroke={C.line} strokeWidth={2} />
          {[-0.02, 0, 0.02].map((d) => (
            <text key={d} x={CX(d)} y={600} fill={C.muted} fontSize={24} textAnchor="middle">
              {d === 0 ? '0' : `${d > 0 ? '+' : '−'}2%p`}
            </text>
          ))}
          <path d={path('mis')} fill="none" stroke={C.accent} strokeWidth={5} />
          <path d={path('bar')} fill="none" stroke={C.asset} strokeWidth={5} />
        </g>
        <g opacity={hit}>
          <circle cx={CX(-0.02)} cy={CY(N.s_bar_m2)} r={10} fill={C.asset} />
          <text x={CX(-0.02) + 16} y={CY(N.s_bar_m2) - 14} fill={C.asset} fontSize={30} fontWeight={800}>
            바벨 {signed(N.s_bar_m2, 2)}
          </text>
          <circle cx={CX(-0.02)} cy={CY(N.s_mis_m2)} r={10} fill={C.accent} />
          <text x={CX(-0.02) + 16} y={CY(N.s_mis_m2) + 10} fill={C.accent} fontSize={30} fontWeight={800}>
            불일치 {signed(N.s_mis_m2, 2)}
          </text>
        </g>
      </svg>
    </Scene>
  );
};

/* S4 TDF = 개인 면역화 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="TDF의 글라이드패스는 면역화의 개인 버전으로 읽을 수 있습니다" sub="DC 가입자의 부채 = 미래 은퇴 소비의 현재가치, 젊을 때 개인 듀레이션 40~50년">
      <div style={{display: 'flex', gap: 30}}>
        <Card style={{flex: 1, ...rise(f, cue(1))}}>
          <div style={{fontSize: 30, color: C.muted}}>젊을 때</div>
          <div style={{fontSize: 40, fontWeight: 800, color: C.liab}}>부채 D가 길다 → 주식</div>
          <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>인적자본이 채권 역할 (W7)</div>
        </Card>
        <div style={{fontSize: 70, color: C.accent, alignSelf: 'center', opacity: prog(f, cue(1) + 30)}}>→</div>
        <Card style={{flex: 1, ...rise(f, cue(1) + 30)}}>
          <div style={{fontSize: 30, color: C.muted}}>은퇴가 가까울수록</div>
          <div style={{fontSize: 40, fontWeight: 800, color: C.asset}}>부채 D가 짧다 → 채권</div>
          <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>자산 D도 따라 줄인다</div>
        </Card>
      </div>
      <div style={{marginTop: 26, width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['구분', 'To 방식 (한국 주류)', 'Through 방식 (미국 · Vanguard)']}
          rows={[
            {cells: ['보수화', '은퇴 시점에 가장 보수적 (주식 30%)', '은퇴 이후에도 점진 보수화'], at: cue(0) + 30},
            {cells: ['은퇴 후', '변화 없음', '20년 후 주식 10~15%'], at: cue(0) + 46},
          ]}
        />
      </div>
      <div style={{fontSize: 34, fontWeight: 800, color: C.accent, marginTop: 24, ...rise(f, cue(2))}}>
        그러나 TDF는 나이 하나로 모든 것을 정한다 → M8 GBI
      </div>
    </Scene>
  );
};

/* S5 한계 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="현금흐름 매칭은 완벽하지만 한국 시장에서는 공급이 부족합니다" sub="면역화의 한계 — 작은 변화 · 평행 이동에 대한 보장이며 계속 다시 맞춰야 한다">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['구분', '현금흐름 매칭', '듀레이션 매칭']}
          rows={[
            {cells: ['방식', '각 시점 CF를 똑같이 보유', 'D 일치 · C_A ≥ C_L만 맞춘다'], at: cue(0) + 10},
            {cells: ['헤지', '완벽 — 금리에 완전 면역', '부분 — 비평행 이동에 실패'], at: cue(0) + 26, hi: f >= cue(1) && f < cue(2)},
            {cells: ['비용 · 유연성', '높은 비용 · 낮은 유연성', '저렴 · 유연 · 초과수익 가능'], at: cue(0) + 42},
          ]}
        />
      </div>
      <div style={{width: 1400, marginTop: 28}}>
        <HBar f={f} at={cue(2)} label="30 · 50년 국고채 잔액" value={437} max={2200} text="437조" color={C.asset} />
        <HBar f={f} at={cue(2) + 16} label="국민연금 순부채 (국채 눈금)" value={2122} max={2200} text="2,122조" color={C.liab} />
      </div>
    </Scene>
  );
};

export const M7E04 = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M7E04_TOTAL = T.total;
