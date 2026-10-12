import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, Chip, HBar} from '../lib/ui';
import {fmt, lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E06.numbers.json';
import T from '../data/M7E06.timing.json';

const EB = 'BAF.60080 · W06 LDI · ⑥ 실무 헤지 수단';

/* S0 LBP · IRS 오버레이 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const col = (k: string, s: string, items: string[], tag: string, c: string, at: number) => (
    <Card style={{flex: 1, borderTop: `6px solid ${c}`, ...rise(f, at)}}>
      <div style={{fontSize: 44, fontWeight: 800, color: c}}>{k}</div>
      <div style={{fontSize: 28, color: C.muted, marginTop: 4}}>{s}</div>
      {items.map((x) => (
        <div key={x} style={{fontSize: 34, marginTop: 18}}>
          • {x}
        </div>
      ))}
      <div style={{fontSize: 30, fontWeight: 700, color: c, marginTop: 20}}>{tag}</div>
    </Card>
  );
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E06" title="LBP는 성과의 기준이고 IRS 오버레이는 듀레이션을 늘리는 지렛대입니다" sub="LDI 실무 도구 — 바로 이 IRS 기반 LDI에서 2022년 영국 위기가 발생했다">
      <div style={{display: 'flex', gap: 34}}>
        {col('Liability Benchmark Portfolio', '부채를 채권으로 표현', ['현금흐름 · 할인곡선 · DV01', 'D · C · 곡선 민감도 일치', '성과 측정의 기준점'], '안 B · C의 공통 조건', C.asset, cue(0))}
        {col('LDI Overlay (IRS)', '현물 대신 스왑으로', ['고정 수취로 D를 가상 확대', '현금을 거의 쓰지 않는다', '증거금 · 거래상대방 위험'], '평상시 효율, 위기에 현금 고갈', C.liab, cue(1))}
      </div>
    </Scene>
  );
};

/* S1 PIMCO 에피소드 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const ev = [
    {y: '2000년대 초', v: '채권 명가들이 LDI 솔루션 시장 선점 — Long Duration 펀드 · LBP · 자문', at: cue(0) + 10},
    {y: '2008 위기', v: '적립비율 급락 → LDI 수요 급증', at: cue(1)},
    {y: '2012', v: 'PIMCO LDI 부문 $600B+ — 업계 최대', at: cue(1) + 50},
    {y: '2022', v: '영국 위기 — 운용사의 증거금 관리 역량이 시험대에', at: cue(1) + 90},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="위기는 LDI 수요를 만들었고 LDI는 거대 산업이 되었습니다" sub="에피소드 — PIMCO의 LDI 왕국 (2000~현재)">
      <div style={{position: 'relative'}}>
        <div style={{position: 'absolute', left: 16, top: 20, bottom: 40, width: 4, background: C.line}} />
        {ev.map((e, i) => (
          <div key={e.y} style={{display: 'flex', alignItems: 'center', gap: 26, marginBottom: 34, ...rise(f, e.at)}}>
            <div style={{position: 'relative', width: 28, height: 28, borderRadius: 14, flexShrink: 0, background: i === 2 ? C.accent : C.panel, border: `3px solid ${C.accent}`}} />
            <div style={{width: 240, fontSize: 38, fontWeight: 800, color: C.accent}}>{e.y}</div>
            <div style={{fontSize: 34}}>{e.v}</div>
          </div>
        ))}
      </div>
      <Card style={{marginTop: 10, borderLeft: `6px solid ${C.accent}`, ...rise(f, cue(2))}}>
        <div style={{fontSize: 32, fontWeight: 800}}>한국의 함의 — 장기물 발행 연 {N.issue}조 · IRS 거래가 헤지 규모의 상한 (조건 ②)</div>
      </Card>
    </Scene>
  );
};

/* S2 증거금 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const days = prog(f, cue(1) + 10, 60);
  return (
    <Scene t={t} eyebrow={EB} title="증거금은 스왑의 DV01에 금리 변동 bp를 곱한 만큼 현금으로 냅니다" sub="증거금의 원리 — 단원 ③의 DV01이 그대로 현금 수요가 된다">
      <div style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\text{변동증거금} = \mathrm{DV01}_{\text{swap}} \times \Delta\text{bp}`} size={52} />
      </div>
      <div style={{display: 'flex', gap: 40, marginTop: 20}}>
        <div style={{flex: 1}}>
          <div style={{fontSize: 30, marginBottom: 16, ...rise(f, cue(1))}}>
            안 C · 사흘간 금리 <b style={{color: C.liab}}>+{Math.round(lerp(0, 200, days))}bp</b>
          </div>
          <HBar f={f} at={cue(1) + 10} label="필요한 변동증거금" value={N.vm * days + 0.001} max={420} text={`${fmt(N.vm * days, 0)}조`} color={C.liab} />
          <HBar f={f} at={cue(1) + 40} label="국민연금 유동자산" value={N.liquid} max={420} text={`${N.liquid}조`} color={C.asset} />
        </div>
        <div style={{width: 460}}>
          <Card style={{...rise(f, cue(2))}}>
            <div style={{fontSize: 26, color: C.muted}}>영국 감독당국 (TPR · 영란은행 · FCA)</div>
            <div style={{fontSize: 30, fontWeight: 700, marginTop: 6}}>2022 위기 이후 요구</div>
            <div style={{display: 'flex', gap: 14, marginTop: 14}}>
              <Chip color={C.floor} style={{fontSize: 24, whiteSpace: 'nowrap'}}>버퍼 {N.buffer_bp}bp</Chip>
              <Chip color={C.floor} style={{fontSize: 24, whiteSpace: 'nowrap'}}>재충전 {N.refill_days}영업일</Chip>
            </div>
          </Card>
          <div style={{fontSize: 30, fontWeight: 800, color: C.accent, marginTop: 30, transform: `scale(${pop(f, cue(1) + 90)})`}}>
            조건 ③ — 401조 vs 123조가 안 C를 가른다
          </div>
        </div>
      </div>
    </Scene>
  );
};

/* S3 체크포인트 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pts = [
    {k: '듀레이션 갭 −17년이 위험의 원천', v: '금리 1%p 하락에 잉여금 −65% · NPS는 갭 −34년'},
    {k: 'Redington 3조건이 수학적 방패', v: '1차 항 소멸, 2차 항 ≥ 0'},
    {k: '실무는 두 블록 + 스왑 오버레이', v: '모자란 헤지를 스왑으로 채우면 증거금 · 버퍼가 따라온다'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="단원 ③~⑥은 금리 위험을 재고 막는 수학과 수단을 다뤘습니다" sub="체크포인트 — 다음 편: ⑦ 2022 영국 · 2023 SVB">
      {pts.map((p, i) => (
        <Card key={p.k} style={{marginBottom: 18, display: 'flex', gap: 26, alignItems: 'center', ...rise(f, cue(0) + i * 18)}}>
          <div style={{fontSize: 44, fontWeight: 900, color: C.accent, width: 50}}>{i + 1}</div>
          <div>
            <div style={{fontSize: 34, fontWeight: 800}}>{p.k}</div>
            <div style={{fontSize: 26, color: C.muted, marginTop: 4}}>{p.v}</div>
          </div>
        </Card>
      ))}
      <div style={{fontSize: 40, fontWeight: 800, color: C.liab, marginTop: 20, transform: `scale(${pop(f, cue(1) + 10)})`}}>
        “이론적으로 완결” — 그러나 시스템 전체가 같은 방향으로 움직이면?
      </div>
    </Scene>
  );
};

export const M7E06 = makeEpisode(T, [S0, S1, S2, S3]);
export const M7E06_TOTAL = T.total;
