import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, Chip, HBar, RevealTable} from '../lib/ui';
import {fmt, lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E07.numbers.json';
import T from '../data/M7E07.timing.json';

const EB = 'BAF.60080 · W06 LDI · ⑦ 실패 사례 — 2022 영국 · 2023 SVB';
const H = 630;

/* S0 왜 레버리지 LDI였나 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const dur = lerp(1, 3.5, prog(f, cue(1) + 20, 50));
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E07" title="영국 DB는 합리적인 선택을 쌓아 시스템의 취약성을 만들었습니다" sub="왜 레버리지 LDI를 썼는가 — 2010년대 영국 DB 연금의 상황">
      <div style={{display: 'flex', gap: 34}}>
        <Card style={{flex: 1, ...rise(f, cue(0))}}>
          <div style={{fontSize: 36, fontWeight: 800, color: C.liab}}>저금리 · 적립비율 압박</div>
          {['저금리 → 부채 급증', '장기 Gilt만으로는 여력 없음', 'IAS 19가 시가 부채 강제'].map((x) => (
            <div key={x} style={{fontSize: 30, marginTop: 14}}>
              • {x}
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(1))}}>
          <div style={{fontSize: 36, fontWeight: 800, color: C.asset}}>해법 — 레버리지 LDI</div>
          <div style={{display: 'flex', alignItems: 'baseline', gap: 16, marginTop: 10}}>
            <span style={{fontSize: 28, color: C.muted}}>듀레이션</span>
            <span style={{fontSize: 72, fontWeight: 900, color: C.asset}}>×{dur < 3.49 ? fmt(dur, 1) : '3~4'}</span>
          </div>
          <div style={{fontSize: 28, marginTop: 6}}>IRS · 레포로 헤지, 남은 자금은 성장자산</div>
          <div style={{fontSize: 28, color: C.muted, marginTop: 6}}>2021년 약 £{N.aum2021}조 — 업계 표준</div>
        </Card>
      </div>
      <div style={{fontSize: 38, fontWeight: 800, color: C.accent, marginTop: 36, ...rise(f, cue(2))}}>
        문제는 단 하나 — 금리가 “빠르게” 오를 때 증거금을 낼 현금이 있는가
      </div>
    </Scene>
  );
};

/* S1 타임라인 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const ev = [
    {d: '9/23', v: '미니예산 — £45B 감세(GDP 1.5%), 파운드 −3.6%', at: cue(0) + 10, c: C.accent},
    {d: '9/26', v: '파운드 역대 최저(1.03) · LDI 증거금 경보', at: cue(1), c: C.liab},
    {d: '9/27', v: '30년 Gilt 나흘 새 +1%p 이상 · Gilt 대량 매각', at: cue(1) + 50, c: C.liab},
    {d: '9/28', v: 'BOE £65B 매입 발표 — 13일 한정', at: cue(2), c: C.asset},
    {d: '10/25', v: 'Truss 사임 — 재임 49일', at: cue(2) + 60, c: C.muted},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="미니예산에서 Truss 사임까지 32일이 걸렸습니다" sub="에피소드 — Liz Truss의 49일, 역대 최단 총리">
      {ev.map((e) => (
        <div key={e.d} style={{display: 'flex', alignItems: 'center', gap: 30, marginBottom: 20, ...rise(f, e.at)}}>
          <div style={{width: 150, fontSize: 44, fontWeight: 900, color: e.c, textAlign: 'right'}}>{e.d}</div>
          <div style={{width: 20, height: 20, borderRadius: 10, background: e.c}} />
          <div style={{fontSize: 34}}>{e.v}</div>
        </div>
      ))}
      <div style={{fontSize: 30, color: C.muted, marginTop: 14, ...rise(f, cue(2) + 80)}}>
        시장은 신뢰를 잃은 정부를 처벌한다 — 일부 연기금 FR −30%p
      </div>
    </Scene>
  );
};

/* S2 Doom Loop 순환 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cx = 520;
  const cy = 300;
  const R = 230;
  const nodes = ['금리 급등', '마진콜', 'Gilt 강제 매도', '금리 추가 급등'];
  // 회전 속도가 점점 빨라진다
  const s = Math.max(0, f - cue(0));
  const ang = 0.0004 * s * s + 0.01 * s;
  const pIn = prog(f, cue(0), 30);
  const sellers = Math.round(lerp(1, 1000, prog(f, cue(2) + 10, 60)));
  return (
    <Scene t={t} eyebrow={EB} title="마진콜이 매도를 부르고 매도가 다시 마진콜을 불렀습니다" sub="Doom Loop — 1개 기금의 매도는 무해하지만 1,000개의 동시 매도는 시장을 무너뜨린다">
      <svg width={1050} height={H} style={{position: 'absolute', left: 0, top: -20}}>
        <defs>
          <marker id="dl-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M0 0L10 5L0 10z" fill={C.liab} />
          </marker>
        </defs>
        <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.line} strokeWidth={3} opacity={pIn} />
        {[0, 1, 2, 3].map((i) => {
          const a1 = ((i * 90 + 18) * Math.PI) / 180;
          const a2 = ((i * 90 + 72) * Math.PI) / 180;
          return (
            <path
              key={i}
              d={`M ${cx + R * Math.sin(a1)} ${cy - R * Math.cos(a1)} A ${R} ${R} 0 0 1 ${cx + R * Math.sin(a2)} ${cy - R * Math.cos(a2)}`}
              fill="none"
              stroke={C.liab}
              strokeWidth={5}
              markerEnd="url(#dl-arrow)"
              opacity={pIn}
            />
          );
        })}
        {/* 도는 점 */}
        {[0, 1, 2].map((k) => {
          const a = ang + (k * 2 * Math.PI) / 3;
          return <circle key={k} cx={cx + R * Math.sin(a)} cy={cy - R * Math.cos(a)} r={12} fill={C.accent} opacity={prog(f, cue(1))} />;
        })}
        {nodes.map((n, i) => {
          const a = (i * Math.PI) / 2;
          const x = cx + R * Math.sin(a);
          const y = cy - R * Math.cos(a);
          return (
            <g key={n} opacity={prog(f, cue(0) + i * 12)}>
              <rect x={x - 130} y={y - 34} width={260} height={68} rx={34} fill={C.panel} stroke={i % 2 ? C.liab : C.accent} strokeWidth={3} />
              <text x={x} y={y + 11} fill={C.text} fontSize={30} fontWeight={800} textAnchor="middle">
                {n}
              </text>
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: 1100, top: 60, width: 628}}>
        <Card style={{textAlign: 'center', ...rise(f, cue(2))}}>
          <div style={{fontSize: 30, color: C.muted}}>동시에 파는 기금 수</div>
          <div style={{fontSize: 110, fontWeight: 900, color: sellers > 100 ? C.liab : C.floor}}>{sellers.toLocaleString()}</div>
          <div style={{fontSize: 32, fontWeight: 700, color: sellers > 100 ? C.liab : C.floor}}>{sellers > 100 ? '시장 붕괴' : '무해'}</div>
        </Card>
        <div style={{fontSize: 28, color: C.muted, marginTop: 20, ...rise(f, cue(2) + 70)}}>개별적으로 합리적인 매도가 집합적으로는 시장 붕괴</div>
      </div>
    </Scene>
  );
};

/* S3 BOE 개입 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="BOE의 개입은 치료가 아니라 루프의 한 고리를 끊은 지혈이었습니다" sub="최종 대부자(lender of last resort)의 13일">
      <div style={{width: 1200}}>
        <HBar f={f} at={cue(0) + 10} label="매입 한도 (13일 한정)" value={N.boe_cap} max={70} text={`£${N.boe_cap}B`} color={C.asset} />
        <HBar f={f} at={cue(0) + 50} label="실제 매입" value={N.boe_bought} max={70} text={`£${N.boe_bought}B`} color={C.floor} />
      </div>
      <div style={{position: 'absolute', left: 1260, top: 0, width: 468, fontSize: 30, fontWeight: 700, color: C.accent, ...rise(f, cue(0) + 90)}}>
        “무제한 의지”의 신호가 핵심 — 기한으로 도덕적 해이 차단
      </div>
      <div style={{display: 'flex', gap: 18, marginTop: 30, alignItems: 'center', ...rise(f, cue(1))}}>
        {['10/3 감세 일부 철회', '10/14 재무장관 경질', '11월 Gilt 안정 · 자본 확충'].map((x) => (
          <Chip key={x} color={C.muted} style={{color: C.text}}>
            {x}
          </Chip>
        ))}
        <span style={{fontSize: 40, color: C.accent}}>→</span>
        <Chip color={C.floor} style={{transform: `scale(${pop(f, cue(1) + 50)})`}}>
          구조 개혁: 버퍼 의무화
        </Chip>
      </div>
    </Scene>
  );
};

/* S4 다섯 가지 교훈 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const rows = [
    ['① 레버리지 LDI의 위험', '평상시 작동, 급격한 금리 변화 시 증거금 고갈'],
    ['② 시스템 위험', '1개 매도는 무해, 1,000개 동시 매도는 시장 붕괴'],
    ['③ 유동성 관리', '담보 현금 1~2% 보유 → 위기 시 5~10% 필요'],
    ['④ 규제의 지연', '2020년부터 경고했으나 강제 규제는 위기 후'],
    ['⑤ 거시-미시 연결', '금리 충격의 원인은 재정 정책 — 자산배분만으로는 예측 불가'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="개별적으로 합리적인 선택이 시스템 전체에서는 재앙이 되었습니다" sub="2022 영국 위기의 다섯 가지 교훈">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={30}
          cols={['교훈', '내용']}
          widths={[0.7, 1.6]}
          rows={rows.map((r, i) => ({cells: r, at: cue(0) + 10 + i * 18, hi: f >= cue(1) && [1, 2, 4].includes(i)}))}
        />
      </div>
    </Scene>
  );
};

/* S5 SVB — 반대 방향의 갭 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const side = (title: string, aLen: number, lLen: number, note: string, at: number) => (
    <Card style={{flex: 1, ...rise(f, at)}}>
      <div style={{fontSize: 32, fontWeight: 800}}>{title}</div>
      <div style={{marginTop: 16, fontSize: 26, color: C.muted}}>자산 듀레이션</div>
      <div style={{height: 34, width: `${aLen * prog(f, at + 10, 30)}%`, background: C.asset, borderRadius: 8}} />
      <div style={{marginTop: 12, fontSize: 26, color: C.muted}}>부채 듀레이션</div>
      <div style={{height: 34, width: `${lLen * prog(f, at + 20, 30)}%`, background: C.liab, borderRadius: 8}} />
      <div style={{fontSize: 26, marginTop: 14}}>{note}</div>
    </Card>
  );
  return (
    <Scene t={t} eyebrow={EB} title="SVB는 반대 방향의 갭으로 같은 현금 시험에서 무너졌습니다" sub="2022년 말 SVB — 총자산 2,090억 · 예금 1,755억(비보호 약 86%) · 채권 1,170억 달러">
      <div style={{display: 'flex', gap: 30}}>
        {side('2022 영국 연기금', 25, 90, '터진 곳: 스왑 증거금 콜', cue(0))}
        {side('2023 SVB', 85, 15, '터진 곳: 예금 인출 (뱅크런)', cue(0) + 20)}
        <div style={{width: 640}}>
          <Card style={{...rise(f, cue(1))}}>
            <div style={{fontSize: 26, color: C.muted}}>손계산 (D 6년 · +2.5%p는 가정치)</div>
            <Tex tex={String.raw`1{,}170 \times 6 \times 2.5\% \approx ${fmt(N.svb.loss_calc, 0)}`} size={40} />
            <div style={{fontSize: 28}}>
              억 달러 ≈ 공시 평가손실 <b style={{color: C.accent}}>150억+</b>
            </div>
          </Card>
          <div style={{display: 'flex', gap: 12, marginTop: 18, ...rise(f, cue(2))}}>
            {[
              ['3/8', '매각 손실 18억'],
              ['3/9', '하루 420억 인출'],
              ['3/10', '폐쇄'],
            ].map(([d, v], i) => (
              <Card key={d} style={{flex: 1, padding: '14px 16px', ...rise(f, cue(2) + i * 30)}}>
                <div style={{fontSize: 30, fontWeight: 900, color: i === 2 ? C.liab : C.accent}}>{d}</div>
                <div style={{fontSize: 24}}>{v}</div>
              </Card>
            ))}
          </div>
        </div>
      </div>
      <div style={{fontSize: 30, fontWeight: 700, color: C.accent, marginTop: 24, ...rise(f, cue(3))}}>
        숨긴 평가손실도 팔면 실제 손실 · 2022년 스왑 110억 달러를 정리해 헤지도 없었다
      </div>
    </Scene>
  );
};

/* S6 정리 */
const S6: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="갭의 방향은 달라도 시험은 현금입니다" sub="다음 편 — ⑧ 실습 · LDI 미니 시뮬레이터">
      <div style={{display: 'flex', gap: 30}}>
        <Card style={{flex: 1, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.asset}}>영국</div>
          <div style={{fontSize: 30, marginTop: 8}}>짧은 자산을 스왑으로 늘림 → 증거금에서 붕괴</div>
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(0) + 20)}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab}}>SVB</div>
          <div style={{fontSize: 30, marginTop: 8}}>짧은 예금 앞에 긴 채권 → 인출에서 붕괴</div>
        </Card>
      </div>
      <div style={{marginTop: 40, width: 1300}}>
        <HBar f={f} at={cue(1)} label="안 C · 3일 +200bp 증거금" value={401} max={420} text="401조" color={C.liab} />
        <HBar f={f} at={cue(1) + 20} label="국민연금 유동자산" value={123} max={420} text="123조" color={C.asset} />
      </div>
    </Scene>
  );
};

export const M7E07 = makeEpisode(T, [S0, S1, S2, S3, S4, S5, S6]);
export const M7E07_TOTAL = T.total;
