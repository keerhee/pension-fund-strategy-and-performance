import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, Chip, HBar, RevealTable} from '../lib/ui';
import {fmt, lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E02.numbers.json';
import T from '../data/M7E02.timing.json';

const EB = 'BAF.60080 · W06 LDI · ② 할인율 — 같은 약속, 다른 숫자';
const H = 630;

/* S0 할인율 2%p → 부채 +47% */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const p = prog(f, cue(1) + 10, 44);
  const r = lerp(5, 3, p);
  const pv = 100 / Math.pow(1 + r / 100, 20);
  const k = 4;
  const base = 540;
  const X = (y: number) => 120 + y * 42;
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E02" title="할인율이 2%p 낮아지면 같은 약속이 47% 더 큰 부채가 됩니다" sub="20년 뒤 100을 한 번 지급하는 약속 — 할인은 분모의 (1 + r)ᵗ로 한다">
      <svg width={1100} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X(0) - 60} x2={X(20) + 60} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        <rect x={X(20) - 36} y={base - 100 * k} width={72} height={100 * k} rx={6} fill={C.muted} opacity={0.35} />
        <text x={X(20)} y={base - 100 * k - 16} fill={C.text} fontSize={34} fontWeight={700} textAnchor="middle">
          100
        </text>
        <text x={X(20)} y={base + 44} fill={C.muted} fontSize={26} textAnchor="middle">
          20년 뒤
        </text>
        <rect x={X(0) - 36} y={base - pv * k * prog(f, cue(0) + 10)} width={72} height={pv * k * prog(f, cue(0) + 10)} rx={6} fill={C.liab} />
        <text x={X(0) + 56} y={base - pv * k + 10} fill={C.liab} fontSize={46} fontWeight={900} opacity={prog(f, cue(0) + 10)}>
          {fmt(pv, 1)}
        </text>
        <text x={X(0)} y={base + 44} fill={C.muted} fontSize={26} textAnchor="middle">
          오늘
        </text>
        <rect x={X(0) - 36} y={base - N.p5 * k} width={72} height={2} fill={C.text} opacity={p} />
        <text x={X(0) + 56} y={base - N.p5 * k + 10} fill={C.muted} fontSize={28} opacity={p}>
          37.7 (5%)
        </text>
      </svg>
      <div style={{position: 'absolute', left: 1120, top: 0, width: 608}}>
        <Card style={{textAlign: 'center', ...rise(f, cue(0))}}>
          <div style={{fontSize: 30, color: C.muted}}>할인율 r</div>
          <div style={{fontSize: 96, fontWeight: 900, color: C.asset}}>{fmt(r, 1)}%</div>
        </Card>
        <div style={{fontSize: 56, fontWeight: 900, color: C.liab, textAlign: 'center', marginTop: 24, transform: `scale(${pop(f, cue(1) + 60)})`}}>
          +{fmt(N.chg * 100, 0)}%
        </div>
        <Card style={{marginTop: 24, ...rise(f, cue(2))}}>
          <Tex tex={String.raw`PV = \frac{100}{(1+r)^{20}}`} size={46} />
          <div style={{fontSize: 26, color: C.muted, textAlign: 'center'}}>r의 차이가 20번 곱해진다</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S1 할인율은 정치의 문제 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="어떤 할인율을 쓰느냐는 수학이 아니라 정치의 문제입니다" sub="할인율 선택이 부채 규모와 적립비율을 좌우한다">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['할인율', '사용 주체', '특징']}
          widths={[1, 1.1, 2]}
          rows={[
            {cells: ['예상 자산수익률 (7~8%)', '미국 공적연금 전통', '부채가 작아 보인다 — 순환 논리'], at: cue(0) + 10, hi: f >= cue(1) && f < cue(2)},
            {cells: ['국채 수익률 (3~5%)', '민간 연금 (ERISA · IAS 19)', '시장 가격 반영 — 부채가 크고 금리에 민감'], at: cue(0) + 26},
            {cells: ['AA 회사채', '미국 GAAP', '국채 + 스프레드 100~150bp'], at: cue(0) + 42},
          ]}
        />
      </div>
      <div style={{marginTop: 30, width: 1400}}>
        <HBar f={f} at={cue(2) + 6} label="국민연금 순부채 · 자체 할인율 5.5%" value={N.nps.own.L} max={2300} text={`${fmt(N.nps.own.L, 0)}조 · FR 95%`} color={C.asset} />
        <HBar f={f} at={cue(3) + 6} label="국민연금 순부채 · 국채 곡선 (10년 4.47 · 30년 4.60%)" value={N.nps.gov.L} max={2300} text={`${fmt(N.nps.gov.L, 0)}조 · FR 69%`} color={C.liab} />
      </div>
      <div style={{position: 'absolute', right: 0, top: 380, fontSize: 64, fontWeight: 900, color: C.accent, transform: `scale(${pop(f, cue(3) + 50)})`}}>×1.4</div>
      <div style={{position: 'absolute', right: 0, top: 470, fontSize: 22, color: C.muted, opacity: prog(f, cue(3) + 50)}}>적립비율은 우리 계산</div>
    </Scene>
  );
};

/* S2 CalPERS · 공무원연금 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pR = prog(f, cue(0) + 20, 50);
  const ev = [
    ['2014 초', '적자 보전금 누적 — 개혁 논의 점화'],
    ['2014.9', '정부 개혁안 — 기여율 인상 · 지급률 인하'],
    ['2015.5', '국회 통과 — 기여율 7% → 9%, 지급률 1.9% → 1.7%'],
    ['2016~', '보전금 증가세 둔화 — 기금은 충당부채의 2% 미만'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="할인율 하나를 바꾸는 데도, 모수 하나를 바꾸는 데도 정치 비용이 듭니다" sub="에피소드 — CalPERS 할인율 하향(2016~2024) · 공무원연금 개혁(2014~2015)">
      <div style={{display: 'flex', gap: 40}}>
        <Card style={{width: 620, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800}}>CalPERS</div>
          <div style={{fontSize: 26, color: C.muted}}>미국 최대 공적연금 · 할인율</div>
          <div style={{fontSize: 110, fontWeight: 900, color: C.asset, marginTop: 10}}>{fmt(lerp(7.5, 6.8, pR), 1)}%</div>
          <div style={{fontSize: 28, color: C.muted}}>7.5% → 6.8% · 8년</div>
          <div style={{fontSize: 28, marginTop: 20, ...rise(f, cue(1))}}>부채 ↑ → 주·지자체 부담 ↑</div>
          <div style={{fontSize: 28, color: C.muted, ...rise(f, cue(1) + 14)}}>세대 간 공정성 vs 납세자 · 일리노이 신용등급 추락</div>
        </Card>
        <div style={{flex: 1}}>
          <div style={{fontSize: 34, fontWeight: 800, marginBottom: 14, ...rise(f, cue(2))}}>공무원연금 — “더 내고 덜 받는” 타협</div>
          {ev.map((e, i) => (
            <div key={e[0]} style={{display: 'flex', gap: 22, alignItems: 'center', marginBottom: 16, ...rise(f, (i < 3 ? cue(2) : cue(3)) + 10 + (i % 3) * 14)}}>
              <div style={{width: 18, height: 18, borderRadius: 9, background: i === 2 ? C.accent : C.muted, flexShrink: 0}} />
              <div style={{width: 120, fontSize: 28, color: C.accent, fontWeight: 700}}>{e[0]}</div>
              <div style={{fontSize: 28}}>{e[1]}</div>
            </div>
          ))}
          <div style={{fontSize: 32, fontWeight: 800, color: C.liab, marginTop: 20, ...rise(f, cue(3) + 40)}}>모수는 바뀌었지만 구조는 남았다</div>
        </div>
      </div>
    </Scene>
  );
};

/* S3 세 연금 비교 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cols = [C.liab, C.asset, C.floor, C.accent];
  return (
    <Scene t={t} eyebrow={EB} title="같은 “연금”이라도 적립 철학과 할인율이 전혀 다릅니다" sub="적립비율은 회계가 아니라 선택의 산물 — 공시값은 CalPERS뿐, 한국 두 연금의 비율은 우리 계산">
      <div style={{width: 1500, marginTop: 10}}>
        {N.funds.map((d, i) => (
          <HBar key={d.k} f={f} at={cue(1) + i * 16} label={d.k} value={d.fr} max={1} text={d.note} color={cols[i]} textWidth={420} />
        ))}
      </div>
    </Scene>
  );
};

/* S4 영국 DB — 세 개의 자 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="영국 DB 적립비율은 자에 따라 130.8%에서 114%까지 달라집니다" sub="위기 4년 후 2026년 2월 (PPF 7800) — 흑자지만, 자산은 같고 부채를 재는 자가 다르다">
      <div style={{display: 'flex', gap: 40}}>
        <div style={{flex: 1}}>
          <RevealTable
            f={f}
            size={27}
            cols={['자', '묻는 질문', '부채']}
            widths={[0.8, 1.7, 0.6]}
            rows={[
              {cells: ['PPF (s179)', '회사가 망하면 물어줄 금액은?', '가장 작다'], at: cue(1), hi: f >= cue(1) && f < cue(2)},
              {cells: ['저의존', '회사 없이도 버틸 수 있나?', '중간'], at: cue(1) + 16},
              {cells: ['바이아웃', '지금 보험사에 넘기려면 얼마?', '가장 크다'], at: cue(1) + 32},
            ]}
          />
          <div style={{display: 'flex', gap: 20, marginTop: 26, ...rise(f, cue(0))}}>
            <Chip color={C.floor}>잉여금 £{fmt(N.uk.S, 1)}B</Chip>
            <Chip color={C.accent}>FR 130.8% ↔ 114%</Chip>
          </div>
        </div>
        <div style={{width: 640}}>
          <HBar f={f} at={cue(2)} label="부채 · PPF 기준 (역산)" value={N.uk.L_ppf} max={1200} text={`£${fmt(N.uk.L_ppf, 0)}B`} color={C.liab} />
          <HBar f={f} at={cue(2) + 20} label="부채 · 바이아웃 기준 (역산)" value={N.uk.L_bo} max={1200} text={`약 £${fmt(N.uk.L_bo, 0)}B`} color={C.liab} />
          <div style={{fontSize: 40, fontWeight: 900, color: C.accent, ...rise(f, cue(2) + 50)}}>
            부채 약 +12%
          </div>
          <div style={{fontSize: 24, color: C.muted, marginTop: 6, ...rise(f, cue(2) + 50)}}>FR = A/L, S = A − L에서 역산</div>
        </div>
      </div>
    </Scene>
  );
};

/* S5 세 비유 + IC */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const m = [
    {k: '부채 = 전세보증금', v: '장부에 안 보여도 갚는다 · 미래 약속의 오늘 가격'},
    {k: '할인율 = 저울 눈금', v: '같은 빚, 다른 무게 · 눈금 싸움이 곧 연금 개혁'},
    {k: '듀레이션 = 지렛대 길이', v: '긴 약속이 크게 흔들린다 · 금리 1%p에 부채 20%'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="부채는 세 가지 비유로 읽을 수 있습니다" sub="단원 ③~⑤의 수식은 이 비유의 정밀한 번역이다 — 다음 편: ③ 금리 위험을 재는 자">
      <div style={{display: 'flex', gap: 28}}>
        {m.map((x, i) => (
          <Card key={x.k} style={{flex: 1, ...rise(f, cue(0) + i * 30)}}>
            <div style={{fontSize: 36, fontWeight: 800, color: C.accent}}>{x.k}</div>
            <div style={{fontSize: 28, color: C.muted, marginTop: 12}}>{x.v}</div>
          </Card>
        ))}
      </div>
      <div
        style={{
          marginTop: 50,
          border: `3px solid ${C.accent}`,
          borderRadius: 18,
          padding: '22px 34px',
          fontSize: 38,
          fontWeight: 700,
          transform: `scale(${pop(f, cue(1) + 4)})`,
        }}
      >
        오후 IC 조건 ① 갭의 실재 — “어느 눈금의 적립비율인가”가 첫 공방입니다
      </div>
    </Scene>
  );
};

export const M7E02 = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M7E02_TOTAL = T.total;
