import React from 'react';
import {AbsoluteFill, Series, useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {CounterRow, Chip, Card} from '../lib/ui';
import {fmt, lerp, pct, pop, prog, rise, signed} from '../lib/anim';
import N from '../data/M7E03.numbers.json';
import T from '../data/M7E03.timing.json';
import {Bed} from '../lib/episode';

const EB = 'BAF.60080 · W06 LDI · ③ 금리 위험을 재는 자';
const scenes = T.scenes as unknown as SceneT[];
const W = 1728; // 무대 폭 (1920 − 좌우 96)
const H = 630; // 무대 높이

/* ── S0 훅 ─────────────────────────────────────────── */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const p = prog(f, cue(0) + 20, 50);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E03" title="금리 위험을 재는 자" sub="듀레이션 · DV01 · 볼록성">
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 80, marginTop: 40}}>
        <Card style={{width: 560, textAlign: 'center', ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, color: C.muted}}>금리</div>
          <div style={{fontSize: 120, fontWeight: 800, color: C.asset}}>−1%p</div>
        </Card>
        <div style={{fontSize: 90, color: C.muted, opacity: prog(f, cue(0) + 12)}}>→</div>
        <Card style={{width: 560, textAlign: 'center', ...rise(f, cue(0) + 16)}}>
          <div style={{fontSize: 34, color: C.muted}}>잉여금</div>
          <div style={{fontSize: 120, fontWeight: 800, color: C.liab, fontVariantNumeric: 'tabular-nums'}}>
            {signed(N.surplus_chg * 100 * p, 0)}%
          </div>
        </Card>
      </div>
      <div style={{display: 'flex', justifyContent: 'center', gap: 36, marginTop: 70}}>
        {['듀레이션', 'DV01', '볼록성'].map((k, i) => (
          <Chip key={k} style={{fontSize: 40, padding: '14px 40px', transform: `scale(${pop(f, cue(1) + 10 + i * 10)})`}}>
            {k}
          </Chip>
        ))}
      </div>
    </Scene>
  );
};

/* ── S1 듀레이션 기본 지식 ─────────────────────────── */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const X = (yr: number) => 90 + yr * 44;
  const base = 540;
  const k = 3.6;
  const pIn = prog(f, cue(0) + 10, 30);
  const pDrop = prog(f, cue(1) + 10, 36);
  const pv = lerp(N.pv5, N.pv6, pDrop);
  return (
    <Scene
      t={t}
      eyebrow={EB}
      title="듀레이션은 현재가치로 가중한 평균 만기이자 금리 민감도입니다"
      sub="기본 지식 — 금리가 1%p 움직일 때 가치가 몇 % 변하는가"
    >
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X(0)} x2={X(20) + 40} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        {[0, 5, 10, 15, 20].map((y) => (
          <g key={y}>
            <line x1={X(y)} x2={X(y)} y1={base} y2={base + 10} stroke={C.muted} strokeWidth={2} />
            <text x={X(y)} y={base + 44} fill={C.muted} fontSize={26} textAnchor="middle">
              {y}년
            </text>
          </g>
        ))}
        {/* 20년 뒤 100 */}
        <g opacity={prog(f, 6)}>
          <rect x={X(20) - 34} y={base - 100 * k} width={68} height={100 * k} rx={6} fill={C.muted} opacity={0.35} />
          <text x={X(20)} y={base - 100 * k - 16} fill={C.text} fontSize={34} fontWeight={700} textAnchor="middle">
            100
          </text>
        </g>
        {/* 할인 화살표 */}
        <path
          d={`M ${X(20) - 40} ${base - 380} Q ${X(10)} ${base - 470} ${X(0) + 44} ${base - pv * k - 30}`}
          fill="none"
          stroke={C.accent}
          strokeWidth={3}
          strokeDasharray="10 8"
          opacity={pIn}
        />
        <text x={X(10)} y={base - 440} fill={C.accent} fontSize={28} textAnchor="middle" opacity={pIn}>
          ÷ (1 + r)²⁰
        </text>
        {/* 현재가치 막대 */}
        <rect x={X(0) - 34} y={base - pv * k * pIn} width={68} height={pv * k * pIn} rx={6} fill={C.accent} />
        <text x={X(0) + 50} y={base - pv * k - 4} fill={C.text} fontSize={36} fontWeight={700} opacity={pIn}>
          {fmt(pv, 1)}
          <tspan fill={C.muted} fontSize={26} fontWeight={400}>
            {'  '}r = {pDrop > 0.5 ? '6%' : '5%'}
          </tspan>
        </text>
        <g opacity={prog(f, cue(1) + 40)}>
          <rect x={X(0) + 50} y={base - 210} width={170} height={56} rx={28} fill={C.liab} opacity={0.18} />
          <text x={X(0) + 135} y={base - 172} fill={C.liab} fontSize={30} fontWeight={700} textAnchor="middle">
            {fmt(N.pv_chg * 100, 1)}%
          </text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 1080, top: 10, width: 640}}>
        <Card style={{...rise(f, cue(2))}}>
          <div style={{fontSize: 28, color: C.muted}}>① 한 번 받는 금액 — 듀레이션 = 만기</div>
          <Tex tex={String.raw`\frac{\Delta P}{P} \approx -D\,\Delta y = -20 \times 1\% = -20\%`} size={31} />
        </Card>
        <Card style={{marginTop: 24, ...rise(f, cue(3))}}>
          <div style={{fontSize: 28, color: C.muted}}>② 여러 번 받는 금액 — 현재가치 비중으로 평균</div>
          <Tex tex={String.raw`D = \sum_t w_t\, t,\qquad w_t = \frac{PV_t}{PV}`} size={40} />
        </Card>
      </div>
    </Scene>
  );
};

/* ── S2 전형적 연기금 ──────────────────────────────── */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const k = 4.4;
  const base = 560;
  const pA = prog(f, cue(0) + 6, 30);
  const pL = prog(f, cue(0) + 18, 30);
  const pS = prog(f, cue(0) + 36, 24);
  const RX = (y: number) => 930 + y * 19; // 듀레이션 자: 0~40년
  const rulerY = 300;
  return (
    <Scene
      t={t}
      eyebrow={EB}
      title="전형적 연기금은 자산 듀레이션 3년, 부채 듀레이션 20년입니다"
      sub="자산 A = 100 (D_A = 3), 부채 L = 80 (D_L = 20) — 이후 계산은 모두 이 기금으로 한다"
    >
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        {/* 대차대조표 */}
        <rect x={120} y={base - N.A * k * pA} width={250} height={N.A * k * pA} rx={8} fill={C.asset} opacity={0.85} />
        <text x={245} y={base - 210} fill={C.bg} fontSize={40} fontWeight={800} textAnchor="middle" opacity={pA}>
          자산 100
        </text>
        <rect x={420} y={base - N.L * k * pL} width={250} height={N.L * k * pL} rx={8} fill={C.liab} opacity={0.85} />
        <text x={545} y={base - 170} fill={C.bg} fontSize={40} fontWeight={800} textAnchor="middle" opacity={pL}>
          부채 80
        </text>
        <rect
          x={420}
          y={base - N.L * k - N.S0 * k}
          width={250}
          height={N.S0 * k}
          rx={8}
          fill="none"
          stroke={C.accent}
          strokeWidth={3}
          strokeDasharray="10 7"
          opacity={pS}
        />
        <text x={545} y={base - N.L * k - 34} fill={C.accent} fontSize={32} fontWeight={700} textAnchor="middle" opacity={pS}>
          잉여금 20
        </text>
        <line x1={90} x2={700} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        {/* 듀레이션 자 */}
        <g opacity={prog(f, cue(1))}>
          <text x={RX(0)} y={rulerY - 120} fill={C.muted} fontSize={28}>
            듀레이션 (년)
          </text>
          <line x1={RX(0)} x2={RX(40)} y1={rulerY} y2={rulerY} stroke={C.muted} strokeWidth={3} />
          {[0, 10, 20, 30, 40].map((y) => (
            <g key={y}>
              <line x1={RX(y)} x2={RX(y)} y1={rulerY - 10} y2={rulerY + 10} stroke={C.muted} strokeWidth={2} />
              <text x={RX(y)} y={rulerY + 46} fill={C.muted} fontSize={24} textAnchor="middle">
                {y}
              </text>
            </g>
          ))}
        </g>
        <g transform={`translate(${RX(3)},${rulerY})`} opacity={prog(f, cue(1) + 8)}>
          <circle r={20 * pop(f, cue(1) + 8)} fill={C.asset} />
          <text y={-36} fill={C.asset} fontSize={30} fontWeight={700} textAnchor="middle">
            자산 3
          </text>
        </g>
        <g transform={`translate(${RX(20)},${rulerY})`} opacity={prog(f, cue(2) + 8)}>
          <circle r={20 * pop(f, cue(2) + 8)} fill={C.liab} />
          <text y={-36} fill={C.liab} fontSize={30} fontWeight={700} textAnchor="middle">
            부채 20
          </text>
        </g>
        <g opacity={prog(f, cue(2) + 20)}>
          <rect x={RX(5)} y={rulerY + 80} width={RX(40) - RX(5)} height={14} rx={7} fill={C.liab} opacity={0.3} />
          <text x={RX(22.5)} y={rulerY + 130} fill={C.muted} fontSize={26} textAnchor="middle">
            지급 시점 5~40년에 분산
          </text>
        </g>
        <g opacity={prog(f, cue(3))}>
          <path
            d={`M ${RX(3)} ${rulerY + 190} V ${rulerY + 210} H ${RX(20)} V ${rulerY + 190}`}
            fill="none"
            stroke={C.accent}
            strokeWidth={3}
          />
          <text x={RX(11.5)} y={rulerY + 262} fill={C.accent} fontSize={44} fontWeight={800} textAnchor="middle">
            갭 = {fmt(N.gap, 0).replace('-', '−')}년
          </text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 920, top: 0, display: 'flex', gap: 14, ...rise(f, cue(1) + 16)}}>
        {['주식 50% · D≈0', '채권 30% · D 6~8', '대체 15% · D 0~3'].map((s) => (
          <Chip key={s} color={C.asset} style={{fontSize: 24, padding: '8px 18px'}}>
            {s}
          </Chip>
        ))}
      </div>
    </Scene>
  );
};

/* ── S3 시소 ──────────────────────────────────────── */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const p = prog(f, cue(1) + 10, 40);
  const px = 470;
  const py = 400;
  const u = 28; // 1년 = 28px
  const ang = lerp(4, 10, p);
  const rA = Math.sqrt(lerp(N.A, N.A1, p)) * 6.6;
  const rL = Math.sqrt(lerp(N.L, N.L1, p)) * 6.6;
  return (
    <Scene t={t} eyebrow={EB} title="자산과 부채는 시소의 서로 다른 자리에 앉아 있습니다" sub="듀레이션 갭을 말로 읽기 — 문제는 앉은 위치가 다르다는 것">
      <svg width={1100} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <polygon points={`${px},${py} ${px - 46},${py + 90} ${px + 46},${py + 90}`} fill={C.muted} opacity={0.5} />
        <line x1={60} x2={1080} y1={py + 90} y2={py + 90} stroke={C.line} strokeWidth={3} />
        <g transform={`rotate(${ang} ${px} ${py})`} opacity={prog(f, 4)}>
          <rect x={px - 220} y={py - 10} width={220 + 21 * u} height={20} rx={10} fill={C.muted} />
          <circle cx={px - 3 * u} cy={py - 10 - rA} r={rA} fill={C.asset} />
          <text x={px - 3 * u} y={py - 10 - rA + 12} fill={C.bg} fontSize={34} fontWeight={800} textAnchor="middle">
            {fmt(lerp(N.A, N.A1, p), 0)}
          </text>
          <text x={px - 3 * u} y={py + 52} fill={C.asset} fontSize={28} fontWeight={700} textAnchor="middle">
            자산 D≈3
          </text>
          <circle cx={px + 20 * u} cy={py - 10 - rL} r={rL} fill={C.liab} />
          <text x={px + 20 * u} y={py - 10 - rL + 12} fill={C.bg} fontSize={34} fontWeight={800} textAnchor="middle">
            {fmt(lerp(N.L, N.L1, p), 0)}
          </text>
          <text x={px + 20 * u} y={py + 52} fill={C.liab} fontSize={28} fontWeight={700} textAnchor="middle">
            부채 D=20
          </text>
        </g>
        <g opacity={prog(f, cue(1))}>
          <rect x={60} y={20} width={250} height={70} rx={35} fill={C.asset} opacity={0.18} />
          <text x={185} y={67} fill={C.asset} fontSize={34} fontWeight={800} textAnchor="middle">
            금리 −1%p ↓
          </text>
        </g>
      </svg>
      <Card style={{position: 'absolute', left: 1130, top: 0, width: 598, padding: '6px 0'}}>
        <CounterRow f={f} show={cue(1)} at={cue(1) + 10} label="자산" from={N.A} to={N.A1} color={C.asset} note="+3%" />
        <CounterRow f={f} show={cue(1)} at={cue(1) + 10} label="부채" from={N.L} to={N.L1} color={C.liab} note="+20%" />
        <CounterRow
          f={f}
          show={cue(2)}
          at={cue(2) + 6}
          label="잉여금"
          from={N.S0}
          to={N.S1}
          color={C.accent}
          note={`${fmt(N.surplus_chg * 100, 0).replace('-', '−')}%`}
        />
        <CounterRow f={f} show={cue(2)} at={cue(2) + 20} label="적립비율" from={N.FR0 * 100} to={N.FR1 * 100} d={0} unit="%" />
      </Card>
      <div
        style={{
          position: 'absolute',
          left: 1130,
          top: 470,
          width: 598,
          fontSize: 32,
          fontWeight: 700,
          color: C.accent,
          ...rise(f, cue(3)),
        }}
      >
        부채 = 숨어 있는 거대한 공매도 포지션
      </div>
    </Scene>
  );
};

/* ── S4 DV01 ──────────────────────────────────────── */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const rows = [
    {k: '자산', calc: '3 × 100 × 0.0001', v: N.dv_a, c: C.asset},
    {k: '부채', calc: '20 × 80 × 0.0001', v: N.dv_l, c: C.liab},
    {k: '차이', calc: '자산 − 부채', v: N.dv_gap, c: C.accent},
  ];
  const pS = prog(f, cue(3) + 10, 40);
  return (
    <Scene t={t} eyebrow={EB} title="DV01은 금리 1bp에 몇 원이 움직이는지를 금액으로 보여 줍니다" sub="자산과 부채는 크기가 달라 %로는 바로 비교할 수 없다">
      <div style={{display: 'flex', gap: 30, alignItems: 'center', ...rise(f, cue(0))}}>
        <Chip color={C.asset}>자산 +3% (기준 100)</Chip>
        <span style={{fontSize: 40, color: C.muted}}>≠</span>
        <Chip color={C.liab}>부채 +20% (기준 80)</Chip>
      </div>
      <div style={{position: 'absolute', left: 0, top: 110, ...rise(f, cue(1))}}>
        <Tex tex={String.raw`\mathrm{DV01} = D \times V \times 0.0001`} size={50} style={{textAlign: 'left'}} />
      </div>
      <Card style={{position: 'absolute', left: 0, top: 240, width: 900, padding: '8px 0'}}>
        {rows.map((r, i) => (
          <div
            key={r.k}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              padding: '16px 30px',
              borderBottom: i < 2 ? `1px solid ${C.line}` : undefined,
              fontSize: 36,
              ...rise(f, cue(2) + i * 14),
            }}
          >
            <span style={{color: r.c, fontWeight: 700, width: 120}}>{r.k}</span>
            <span style={{color: C.muted, flex: 1}}>{r.calc}</span>
            <span style={{fontWeight: 800, color: r.c, fontVariantNumeric: 'tabular-nums'}}>
              {signed(r.v, 2).replace('+', '')}
            </span>
          </div>
        ))}
      </Card>
      <div style={{position: 'absolute', left: 980, top: 240, width: 740, ...rise(f, cue(3))}}>
        <div style={{fontSize: 30, color: C.muted, marginBottom: 14}}>금리 100bp 하락 → 잉여금 −0.13 × 100 = −13</div>
        <div style={{height: 80, background: C.bg2, borderRadius: 12, position: 'relative', overflow: 'hidden'}}>
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: `${lerp(N.S0, N.S1, pS) * 5}%`,
              background: C.accent,
              borderRadius: 12,
            }}
          />
          <div style={{position: 'absolute', left: 24, top: 14, fontSize: 40, fontWeight: 800, color: C.bg}}>
            잉여금 {fmt(lerp(N.S0, N.S1, pS), 1)}
          </div>
        </div>
        <div style={{fontSize: 28, color: C.muted, marginTop: 14}}>앞 장면의 20 → 7과 같은 답</div>
      </div>
    </Scene>
  );
};

/* ── S5 볼록성 ────────────────────────────────────── */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const X = (y: number) => 110 + ((y - 0.01) / 0.08) * 800;
  const Y = (v: number) => 560 - ((v - 35) / 60) * 520;
  const path = N.curve.map((p, i) => `${i ? 'L' : 'M'} ${X(p.y)} ${Y(p.v)}`).join(' ');
  const tan = (y: number) => N.V - N.D * N.V * (y - 0.05);
  const pc = prog(f, cue(0) + 4, 40);
  const pt = prog(f, cue(0) + 40, 30);
  const p2 = prog(f, cue(1) + 10, 24);
  const exact7 = N.V + N.conv[2].exact;
  const first7 = N.V + N.conv[2].first;
  const hiRow = f >= cue(1);
  const hiCol = f >= cue(2);
  return (
    <Scene
      t={t}
      eyebrow={EB}
      title="가격 변화는 기울기(듀레이션)와 휘어짐(볼록성) 두 항으로 근사됩니다"
      sub="10년 뒤 100을 주는 부채, y = 5%(연속복리): V = 60.65, D = 10, C = 100"
    >
      <svg width={980} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={110} x2={930} y1={560} y2={560} stroke={C.muted} strokeWidth={2} />
        <line x1={110} x2={110} y1={30} y2={560} stroke={C.muted} strokeWidth={2} />
        {[0.01, 0.03, 0.05, 0.07, 0.09].map((y) => (
          <text key={y} x={X(y)} y={600} fill={C.muted} fontSize={24} textAnchor="middle">
            {Math.round(y * 100)}%
          </text>
        ))}
        {[40, 60, 80].map((v) => (
          <text key={v} x={96} y={Y(v) + 8} fill={C.muted} fontSize={24} textAnchor="end">
            {v}
          </text>
        ))}
        <text x={930} y={540} fill={C.muted} fontSize={24} textAnchor="end">
          금리 y
        </text>
        <path d={path} fill="none" stroke={C.liab} strokeWidth={5} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - pc} />
        <line
          x1={X(0.015)}
          y1={Y(tan(0.015))}
          x2={X(lerp(0.015, 0.085, pt))}
          y2={Y(tan(lerp(0.015, 0.085, pt)))}
          stroke={C.text}
          strokeWidth={3}
          strokeDasharray="12 8"
          opacity={pt}
        />
        <circle cx={X(0.05)} cy={Y(N.V)} r={10} fill={C.accent} opacity={pc} />
        <text x={X(0.05) + 16} y={Y(N.V) - 18} fill={C.text} fontSize={26} opacity={pt}>
          기울기 = −D·V
        </text>
        <g opacity={p2}>
          <line x1={X(0.07)} x2={X(0.07)} y1={Y(N.V)} y2={Y(first7) + 30} stroke={C.muted} strokeDasharray="4 6" strokeWidth={2} />
          <circle cx={X(0.07)} cy={Y(exact7)} r={9} fill={C.liab} />
          <circle cx={X(0.07)} cy={Y(first7)} r={9} fill={C.text} />
          <text x={X(0.07) + 18} y={Y(exact7) - 12} fill={C.liab} fontSize={26} fontWeight={700}>
            정확 {signed(N.conv[2].exact, 1)}
          </text>
          <text x={X(0.07) - 18} y={Y(first7) + 40} fill={C.text} fontSize={26} fontWeight={700} textAnchor="end">
            1차만 {signed(N.conv[2].first, 1)}
          </text>
        </g>
      </svg>
      <Card style={{position: 'absolute', left: 1010, top: 10, width: 718, padding: '10px 0', ...rise(f, cue(0) + 30)}}>
        <div style={{display: 'flex', padding: '10px 24px', fontSize: 26, color: C.muted, borderBottom: `1px solid ${C.line}`}}>
          <span style={{width: 130}}>Δy</span>
          <span style={{flex: 1, textAlign: 'right'}}>정확</span>
          <span style={{flex: 1, textAlign: 'right'}}>1차만</span>
          <span style={{flex: 1, textAlign: 'right', color: hiCol ? C.floor : C.muted}}>1차+2차</span>
        </div>
        {N.conv.map((r, i) => {
          const on = hiRow && i === 2;
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                padding: '14px 24px',
                fontSize: 32,
                fontVariantNumeric: 'tabular-nums',
                background: on ? 'rgba(242,140,40,0.12)' : undefined,
              }}
            >
              <span style={{width: 130, color: C.muted}}>{signed(r.dy * 100, 0)}%p</span>
              <span style={{flex: 1, textAlign: 'right'}}>{signed(r.exact, 3)}</span>
              <span style={{flex: 1, textAlign: 'right', color: on ? C.liab : C.text}}>{signed(r.first, 3)}</span>
              <span style={{flex: 1, textAlign: 'right', color: hiCol ? C.floor : C.text, fontWeight: hiCol ? 700 : 400}}>
                {signed(r.second, 3)}
              </span>
            </div>
          );
        })}
      </Card>
      <div style={{position: 'absolute', left: 1010, top: 330, width: 718, ...rise(f, cue(2) + 6)}}>
        <Tex tex={String.raw`\frac{\Delta V}{V} \approx \underbrace{-D\,\Delta y}_{\text{기울기}} + \underbrace{\tfrac{1}{2}C\,(\Delta y)^2}_{\text{휘어짐}}`} size={40} />
      </div>
    </Scene>
  );
};

/* ── S6 헤지비율 ──────────────────────────────────── */
const S6: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const bar = (label: string, num: string, h: number, at: number, color: string) => {
    const p = prog(f, at, 40);
    return (
      <div style={{marginBottom: 26, ...rise(f, at - 6)}}>
        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 30, marginBottom: 8}}>
          <span>{label}</span>
          <span style={{color: C.muted}}>{num}</span>
        </div>
        <div style={{height: 46, background: C.bg2, borderRadius: 10, position: 'relative'}}>
          <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${Math.max(h * p, 0.004) * 100}%`, background: color, borderRadius: 10}} />
          <div style={{position: 'absolute', right: 16, top: 2, fontSize: 34, fontWeight: 800, color: C.text}}>{pct(h * p, h < 0.05 ? 1 : 0)}</div>
        </div>
      </div>
    );
  };
  const done = f >= cue(2);
  return (
    <Scene t={t} eyebrow={EB} title="헤지비율은 부채의 금리 민감도를 얼마나 덮었는지 보여 줍니다" sub="h = 100%면 금리가 움직여도 잉여금이 거의 변하지 않는다 — 이것이 금리 헤지">
      <div style={{position: 'absolute', left: 0, top: 0, width: 560, ...rise(f, cue(0))}}>
        <Tex tex={String.raw`h = \frac{\mathrm{DV01}_A}{\mathrm{DV01}_L}`} size={64} />
        <div style={{fontSize: 28, color: C.muted, textAlign: 'center'}}>부채 DV01 = {fmt(N.dv_l, 2)}</div>
      </div>
      <div style={{position: 'absolute', left: 620, top: 0, width: 1108}}>
        {bar(N.hedge[0].label, `${fmt(N.hedge[0].dv, 3)} ÷ ${fmt(N.dv_l, 2)}`, N.hedge[0].h, cue(1) + 6, C.asset)}
        {bar(N.hedge[1].label, `${fmt(N.hedge[1].dv, 3)} ÷ ${fmt(N.dv_l, 2)}`, N.hedge[1].h, cue(1) + 70, C.asset)}
        {bar(N.hedge[2].label, `${fmt(N.hedge[2].dv, 3)} ÷ ${fmt(N.dv_l, 2)}`, N.hedge[2].h, cue(1) + 140, done ? C.floor : C.asset)}
        {bar('국민연금 (현 보유)', '갭 약 −34년 · 2027 목표 비중 이행 시 3%', N.nps_h, cue(3) + 6, C.liab)}
      </div>
      <div style={{position: 'absolute', left: 0, top: 400, width: 560, fontSize: 30, color: C.floor, fontWeight: 700, ...rise(f, cue(2) + 6)}}>
        h = 100% → 금리가 움직여도 잉여금이 거의 그대로
      </div>
    </Scene>
  );
};

/* ── S7 정리 ──────────────────────────────────────── */
const S7: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const items = [
    {k: '듀레이션 + 볼록성', v: '가격이 얼마나 변하나'},
    {k: 'DV01', v: '1bp에 몇 원'},
    {k: '헤지비율', v: '부채 민감도를 얼마나 덮었나'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="금리 위험은 세 개의 자로 잽니다" sub="다음 편 — ④ 면역화와 Redington">
      <div style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\frac{\Delta P}{P} \approx -D\,\Delta y + \tfrac{1}{2}C\,(\Delta y)^2 \qquad h = \frac{\mathrm{DV01}_A}{\mathrm{DV01}_L}`} size={50} />
      </div>
      <div style={{display: 'flex', gap: 30, marginTop: 30}}>
        {items.map((it, i) => (
          <Card key={it.k} style={{flex: 1, ...rise(f, cue(0) + 20 + i * 12)}}>
            <div style={{fontSize: 34, fontWeight: 800, color: C.accent}}>{it.k}</div>
            <div style={{fontSize: 30, color: C.muted, marginTop: 8}}>{it.v}</div>
          </Card>
        ))}
      </div>
      <div
        style={{
          marginTop: 40,
          border: `3px solid ${C.accent}`,
          borderRadius: 18,
          padding: '22px 34px',
          fontSize: 38,
          fontWeight: 700,
          transform: `scale(${pop(f, cue(1) + 6)})`,
        }}
      >
        오후 IC — 국민연금 LDI 안건의 표결 숫자는 헤지비율 하나입니다
      </div>
    </Scene>
  );
};

const LIST = [S0, S1, S2, S3, S4, S5, S6, S7];

export const M7E03: React.FC = () => (
  <AbsoluteFill style={{background: C.bg}}>
    <Bed T={T as {bed?: string}} />
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
export const M7E03_TOTAL = T.total;
