import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, Chip, RevealTable} from '../lib/ui';
import {pop, prog, rise, shake} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import T from '../data/M7E08.timing.json';

const EB = 'BAF.60080 · W06 LDI · ⑨ 모의 IC';

/* S0 개요 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const steps = [
    ['브리핑', '10분'],
    ['팀 준비', '15분'],
    ['발표', '팀당 4분'],
    ['반대신문', '12분'],
    ['표결 · 강평', '7분'],
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E08" title="여러분은 국민연금 기금운용위원회 위원으로 표결합니다" sub="모의 IC 개요 — 상세 자료는 케이스 덱으로 배포">
      <Card style={{...rise(f, cue(0))}}>
        <div style={{fontSize: 28, color: C.muted}}>안건</div>
        <div style={{fontSize: 38, fontWeight: 800, marginTop: 6}}>LBP를 만들고 헤지 비율을 무엇으로 올리나</div>
      </Card>
      <div style={{display: 'flex', gap: 14, marginTop: 24, flexWrap: 'wrap', ...rise(f, cue(1))}}>
        {['운용전략(CIO)', '리스크관리', '재정 · 거버넌스', '글로벌자문'].map((x) => (
          <Chip key={x} color={C.asset}>
            {x}
          </Chip>
        ))}
        <Chip color={C.accent}>위원장 1</Chip>
        <Chip color={C.muted} style={{color: C.text}}>
          독립심사위원 3
        </Chip>
      </div>
      <div style={{display: 'flex', gap: 10, marginTop: 34, alignItems: 'center'}}>
        {steps.map((s, i) => (
          <React.Fragment key={s[0]}>
            <Card style={{flex: 1, textAlign: 'center', padding: '18px 10px', ...rise(f, cue(1) + 30 + i * 12)}}>
              <div style={{fontSize: 30, fontWeight: 800}}>{s[0]}</div>
              <div style={{fontSize: 26, color: C.muted}}>{s[1]}</div>
            </Card>
            {i < steps.length - 1 ? <div style={{fontSize: 36, color: C.accent, opacity: prog(f, cue(1) + 36 + i * 12)}}>→</div> : null}
          </React.Fragment>
        ))}
      </div>
    </Scene>
  );
};

/* S1 개념 → 판정 조건 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const rows = [
    ['FR = A/L · 할인율의 두 눈금 (①②)', '① 갭 실재 — FR 95%(자체 5.5%) vs 69%(국채) · 우리 계산'],
    ['DV01 · 듀레이션 갭 (③)', '① 순부채 D 35년 · 원화 자산 D 0.85년 · 갭 −34년 · 7.4조/bp'],
    ['면역화 · 두 블록 · CF 매칭의 한계 (④⑤)', '② 국고채 교체 ≤ 장기물 30%×5년(131조) · IRS ≤ 연 거래 5%(299조)'],
    ['2022 교훈 · 증거금 · 버퍼 (⑥~⑧)', '③ 3일 +200bp 증거금 401조 vs 유동자산 123조 · 250bp'],
    ['허들 5.5% · 기금운용지침 별표 1', '④ 헤지 후 μ ≥ 5.5% · ⑤ 국내채권 ≤ 21.8 + 7.0%p, 파생 조항 없음'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="이번 강의의 개념은 모두 오후 판정 조건 ①~⑤에 꽂힙니다" sub="발언 준비가 막히면 이 표로 돌아온다">
      <div style={{width: 1728}}>
        <RevealTable f={f} size={26} cols={['이번 강의의 개념', '오후 IC의 판정 조건']} widths={[0.9, 1.6]} rows={rows.map((r, i) => ({cells: r, at: cue(0) + 10 + i * 16}))} />
      </div>
    </Scene>
  );
};

/* S2 판정 — 안 B 조건부 승인 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const card = (
    k: string,
    h: string,
    items: [boolean, string][],
    at: number,
    verdict: string,
    good: boolean,
    stampAt: number,
  ) => {
    const sp = pop(f, stampAt);
    return (
      <Card style={{flex: 1, position: 'relative', border: good && f >= stampAt ? `3px solid ${C.floor}` : undefined, ...rise(f, at)}}>
        <div style={{fontSize: 32, fontWeight: 800}}>{k}</div>
        <div style={{fontSize: 44, fontWeight: 900, color: C.accent, marginTop: 4}}>{h}</div>
        {items.map(([ok, x], i) => (
          <div key={x} style={{display: 'flex', gap: 12, fontSize: 25, marginTop: 12, opacity: prog(f, at + 20 + i * 12)}}>
            <span style={{color: ok ? C.floor : C.liab, fontWeight: 900}}>{ok ? '✓' : '✗'}</span>
            <span>{x}</span>
          </div>
        ))}
        <div
          style={{
            position: 'absolute',
            right: 18,
            bottom: 18,
            border: `4px solid ${good ? C.floor : C.liab}`,
            color: good ? C.floor : C.liab,
            borderRadius: 10,
            padding: '6px 14px',
            fontSize: 28,
            fontWeight: 900,
            transform: `rotate(-8deg) scale(${sp}) translateX(${shake(f, stampAt, 6, 12)}px)`,
            opacity: sp,
          }}
        >
          {verdict}
        </div>
      </Card>
    );
  };
  return (
    <Scene t={t} eyebrow={EB} title="기본 답은 안 B — 부채 벤치마크 도입과 30년 국고채 교체의 조건부 승인입니다" sub="발언은 “조건 X가 Y이면 답은 Z” 형식으로, 수익률이 아니라 부채 언어로 한다">
      <div style={{display: 'flex', gap: 26, height: 520}}>
        {card('안 A · 현행 유지', '헤지 3%', [[false, '목표 비중을 채워도 3%, 갭 −34년 그대로'], [false, '부채 벤치마크가 없어 갭을 재지도 못한다']], cue(0), '기본 답 아님', false, cue(0) + 90)}
        {card('안 B · 30년 국고채 교체', '헤지 5%', [[true, '부채 벤치마크를 만들어 공시한다'], [true, '시장이 받아 줄 131조까지만 교체'], [true, '채권을 직접 사므로 증거금 없음']], cue(2), '조건부 승인', true, cue(2) + 80)}
        {card('안 C · 금리 스왑', '헤지 30%', [[false, '스왑 1,223조 = 시장 상한 299조의 4배'], [false, '3일 +200bp 증거금 401조 > 유동자산 123조'], [false, '지침에 파생 조항이 없다']], cue(1), '기본 답 아님', false, cue(1) + 110)}
      </div>
    </Scene>
  );
};

/* S3 의결문 · 과제 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const hw = [
    ['개인', '본인 기관 LDI 분석 (1쪽)'],
    ['개인', '2022 UK 위기 재분석 — 예방 가능했는가 (1~2쪽)'],
    ['팀', 'NPS LDI 도입 심층 분석 (12쪽 + 15분 발표)'],
    ['선택', 'LDI 6-Step 완전 구현 · 프롬프트 이력 제출'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="헤지 후에도 남는 갭의 부담자를 의결문에 반드시 적습니다" sub="채점 기준 — 수익률 언어가 아니라 부채 언어(FR · 갭 · 잉여금)로 논증했는가">
      <Card style={{borderLeft: `6px solid ${C.accent}`, ...rise(f, cue(0))}}>
        <div style={{fontSize: 30, color: C.muted}}>의결문 필수 항목</div>
        <div style={{fontSize: 38, fontWeight: 800, marginTop: 6}}>남는 갭 −34년 중 헤지되지 않은 몫을 누가 지는가</div>
      </Card>
      <div style={{fontSize: 40, fontWeight: 800, color: C.accent, margin: '28px 0', ...rise(f, cue(1))}}>“조건 X가 Y이면 답은 Z”</div>
      <div style={{display: 'flex', gap: 18}}>
        {hw.map((h, i) => (
          <Card key={h[1]} style={{flex: 1, ...rise(f, cue(2) + i * 14)}}>
            <div style={{fontSize: 26, color: C.accent, fontWeight: 800}}>{h[0]}</div>
            <div style={{fontSize: 26, marginTop: 6}}>{h[1]}</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

export const M7E08 = makeEpisode(T, [S0, S1, S2, S3]);
export const M7E08_TOTAL = T.total;
