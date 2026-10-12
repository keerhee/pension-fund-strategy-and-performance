import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, HBar, RevealTable} from '../lib/ui';
import {fmt, lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E08.numbers.json';
import T from '../data/M8E08.timing.json';

const EB = 'BAF.60080 · W06 GBI · ⑧ 기관의 GBI · H대';

/* S0 세 숫자 다이얼 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const dials = [
    {k: 'x', n: '비유동 대체 상한', v: N.x, u: '%', d: 'PE · VC · 사모부동산 — 재간접 · 세컨더리', c: C.accent},
    {k: 'y', n: '안전 유동자산 하한', v: N.y, u: '%', d: '현금 · 국채 = GHP (Safety 버킷)', c: C.floor},
    {k: 'z', n: '지출률', v: N.z, u: '%', d: '고정 3.5%(175억) = Floor, 4.5%까지 희망', c: C.asset},
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E08" title="H대 IC는 철학의 이름을 고르지 않고 세 숫자 x · y · z를 정합니다" sub="H대(가상) 5,000억 기금 — 장학 · 연구 고정 지출(필수 목표)을 지키면서 팔 수 없는 사모를 어디까지 담을까">
      <div style={{display: 'flex', gap: 30}}>
        {dials.map((d, i) => {
          const p = prog(f, cue(2) + i * 16, 40);
          const ang = -120 + 240 * Math.min(1, (d.v * p) / (d.k === 'z' ? 6 : 50));
          return (
            <Card key={d.k} style={{flex: 1, textAlign: 'center', ...rise(f, cue(1) + i * 14)}}>
              <svg width={240} height={150}>
                <path d="M 30 130 A 90 90 0 1 1 210 130" fill="none" stroke={C.line} strokeWidth={12} strokeLinecap="round" />
                <line x1={120} y1={130} x2={120 + 80 * Math.sin((ang * Math.PI) / 180)} y2={130 - 80 * Math.cos((ang * Math.PI) / 180)} stroke={d.c} strokeWidth={8} strokeLinecap="round" />
                <circle cx={120} cy={130} r={10} fill={d.c} />
              </svg>
              <div style={{fontSize: 30, color: C.muted}}>
                {d.k} · {d.n}
              </div>
              <div style={{fontSize: 80, fontWeight: 900, color: d.c}}>
                {d.k === 'z' ? fmt(d.v * p, 1) : Math.round(d.v * p)}
                {d.u}
              </div>
              <div style={{fontSize: 24, color: C.muted}}>{d.d}</div>
            </Card>
          );
        })}
      </div>
    </Scene>
  );
};

/* S1 모방 3장벽 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="Yale을 흉내 낼 때 막히는 세 장벽은 접근권 · 시간 지평 · 인력입니다" sub="모방 3장벽 = 작은 기금이 Yale의 대체투자 60%를 따라 할 때 숫자로 막히는 세 조건">
      <div style={{display: 'flex', gap: 24}}>
        {[
          {k: '① 접근권', q: '좋은 매니저에 들어가나', v: '일류 펀드는 기존 출자자 우선 · 안 되면 재간접 −2%p'},
          {k: '② 시간 지평', q: '못 팔아도 버티나', v: '락업 10년 — 팔 수 없다'},
          {k: '③ 인력', q: '골라낼 사람이 있나', v: 'H대 대체 전담 1명 · 직접 투자는 3명 이상'},
        ].map((b, i) => (
          <Card key={b.k} style={{flex: 1, ...rise(f, cue(0) + i * 14)}}>
            <div style={{fontSize: 34, fontWeight: 800, color: C.accent}}>{b.k}</div>
            <div style={{fontSize: 28, marginTop: 6}}>{b.q}</div>
            <div style={{fontSize: 24, color: C.muted, marginTop: 10}}>{b.v}</div>
          </Card>
        ))}
      </div>
      <div style={{width: 1300, marginTop: 30}}>
        <div style={{fontSize: 28, color: C.muted, marginBottom: 10, ...rise(f, cue(1))}}>2022년형 충격 뒤 매도 없이 버티는 연수 (락업 10년)</div>
        <HBar f={f} at={cue(1) + 10} label="x = 20%" value={N.survive.x20} max={16} text={`${N.survive.x20}년 ✓`} color={C.floor} textWidth={200} />
        <HBar f={f} at={cue(1) + 30} label="x = 60% (Yale 추종)" value={N.survive.x60} max={16} text={`${N.survive.x60}년 ✗`} color={C.liab} textWidth={200} />
      </div>
    </Scene>
  );
};

/* S2 Floor 1,536억 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const parts = [
    {k: '앞 3년 고정 지출', v: 536, c: C.floor},
    {k: '공사비', v: 600, c: C.asset},
    {k: '남은 출자 요청 (400 × 40%)', v: 400, c: C.accent},
  ];
  let acc = 0;
  const k = 0.95;
  return (
    <Scene t={t} eyebrow={EB} title="Flexicure를 H대에 옮기면 Floor는 거절할 수 없는 유출 1,536억입니다" sub="다섯 단계 ① Floor · ② GHP로 덮기 · ③ 쿠션과 승수 — B안(주식 50 · 국채 25 · 현금 5 · 사모 20 · z 4.5%)">
      <svg width={1728} height={260} style={{position: 'absolute', left: 0, top: 0}}>
        {parts.map((p, i) => {
          const pp = prog(f, cue(0) + 10 + i * 24, 24);
          const x = 40 + acc * k;
          acc += p.v;
          return (
            <g key={p.k} opacity={pp}>
              <rect x={x} y={40} width={p.v * k * pp} height={120} rx={8} fill={p.c} stroke={C.bg} strokeWidth={3} />
              <text x={x + 16} y={92} fill={C.bg} fontSize={26} fontWeight={800}>
                {p.k}
              </text>
              <text x={x + 16} y={136} fill={C.bg} fontSize={32} fontWeight={900}>
                {p.v}억
              </text>
            </g>
          );
        })}
        <text x={40 + 1536 * k + 20} y={110} fill={C.text} fontSize={44} fontWeight={900} opacity={prog(f, cue(0) + 90)}>
          = 1,536억
        </text>
      </svg>
      <div style={{position: 'absolute', left: 40, top: 230, display: 'flex', gap: 24, width: 1650}}>
        <Card style={{flex: 1, ...rise(f, cue(1))}}>
          <div style={{fontSize: 30, fontWeight: 800, color: C.floor}}>② GHP로 덮기</div>
          <div style={{fontSize: 26, marginTop: 6}}>충격 뒤 현금 · 국채가 3년 지출 + 공사비를 매도 없이 댄다</div>
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(1) + 20)}}>
          <div style={{fontSize: 30, fontWeight: 800, color: C.accent}}>③ 쿠션과 승수</div>
          <div style={{fontSize: 26, marginTop: 6}}>m = (주식 + 사모) ÷ 쿠션 ≤ 2 — 디폴트옵션 기본 답과 같다</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S3 2008형 충격 — B vs C */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const side = (k: string, d: {liq: number; cushion: number; m: number; pe_share: number}, floor: number, at: number, bad: boolean) => {
    const p = prog(f, at + 10, 40);
    return (
      <Card style={{flex: 1, borderTop: `6px solid ${bad ? C.liab : C.floor}`, ...rise(f, at)}}>
        <div style={{fontSize: 34, fontWeight: 800, color: bad ? C.liab : C.floor}}>{k}</div>
        <div style={{display: 'flex', height: 70, marginTop: 16, borderRadius: 10, overflow: 'hidden', background: C.bg2}}>
          <div style={{width: `${(floor / 3200) * 100}%`, background: C.muted, display: 'flex', alignItems: 'center', paddingLeft: 14, fontSize: 24, fontWeight: 800, color: C.bg}}>Floor {floor.toLocaleString()}</div>
          <div style={{width: `${(d.cushion / 3200) * 100 * p}%`, background: bad ? C.liab : C.floor, display: 'flex', alignItems: 'center', paddingLeft: 14, fontSize: 24, fontWeight: 800, color: C.bg}}>쿠션 {Math.round(d.cushion * p).toLocaleString()}</div>
        </div>
        <div style={{fontSize: 24, color: C.muted, marginTop: 6}}>유동자산 {d.liq.toLocaleString()}억</div>
        <div style={{display: 'flex', justifyContent: 'space-between', marginTop: 16, fontSize: 30}}>
          <span>승수 m</span>
          <b style={{color: bad ? C.liab : C.floor, fontSize: 52, transform: `scale(${pop(f, at + 50)})`, display: 'inline-block'}}>{fmt(lerp(0, d.m, p), 2)}</b>
        </div>
        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 30}}>
          <span>사모 비중</span>
          <b>{fmt(d.pe_share, 1)}%</b>
        </div>
        <div style={{fontSize: 28, fontWeight: 800, color: bad ? C.liab : C.floor, marginTop: 10}}>{bad ? '상한 2 초과 — 사실상 갇힘' : 'm 상한 2 안 · 사모 22.5% > 22% → 신규 약정 중단'}</div>
      </Card>
    );
  };
  return (
    <Scene t={t} eyebrow={EB} title="사모는 팔 수 없으니 충격 뒤 쿠션으로 다시 잽니다" sub="④ 비유동성 — 2008형: 주식 −40 · 국채 +8 · 현금 +3 · 사모 −10% (단위 억 원)">
      <div style={{display: 'flex', gap: 30}}>
        {side('B안 (기본 답)', N.B, N.floor_B, cue(1), false)}
        {side('C안 (Yale 추종)', N.C, N.floor_C, cue(2), true)}
      </div>
      <div style={{fontSize: 30, fontWeight: 800, color: C.accent, marginTop: 18, ...rise(f, cue(3))}}>줄이는 수단은 신규 약정 중단뿐 — 사모가 목표 + 2%p를 넘으면 중단</div>
    </Scene>
  );
};

/* S4 같은 기법, 다른 주인 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="정리 — H대 문제는 기관판 GBI입니다: 같은 기법, 다른 주인" sub="이순자 씨의 노후 소득과 H대의 지출 약속을 나란히 놓는다">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={27}
          cols={['GBI 기법', '이순자 씨 (개인)', 'H대 기금 (기관)']}
          widths={[0.8, 1.1, 1.5]}
          rows={[
            {cells: ['필수 목표 → Floor', '월 부족분 150만 → 3.50억', '3년 지출 + 공사비 + 출자 = 1,536억'], at: cue(0) + 10},
            {cells: ['GHP (Safety 버킷)', '물가연동국채 사다리', '현금 · 국채 30% (y)'], at: cue(0) + 24},
            {cells: ['쿠션 · 위험 예산', '쿠션 1.50억의 m배', '(주식 + 사모) ≤ 쿠션의 2배 (x)'], at: cue(0) + 38},
            {cells: ['확률 제약', 'Safety ≥ 95% · Market ≥ 70%', '3년 지출 유지 ≥ 95% · 30년 실질 ≥ 50%'], at: cue(1)},
            {cells: ['Flexicure 재설정', '매년 Floor = 자산의 80%', '희망 지출 동결 · 80/20 평활 (z)'], at: cue(1) + 14},
          ]}
        />
      </div>
      <div style={{fontSize: 30, fontWeight: 800, color: C.liab, marginTop: 18, ...rise(f, cue(1) + 40)}}>차이 하나 — 비유동 자산은 쿠션이 줄어도 팔 수 없다</div>
    </Scene>
  );
};

export const M8E08 = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M8E08_TOTAL = T.total;
