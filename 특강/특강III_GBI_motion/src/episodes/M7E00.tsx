import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, Chip} from '../lib/ui';
import {pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import T from '../data/M7E00.timing.json';

const EB = 'BAF.60080 · W06 LDI · 도입';

/* S0 대차대조표 반대편이 드러난다 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pL = prog(f, cue(1) + 10, 40);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E00" title="LDI — 부채연계투자" sub="Liability-Driven Investing · 자산이 아니라 자산 대 부채">
      <div style={{display: 'flex', gap: 0, justifyContent: 'center', marginTop: 10}}>
        <div style={{width: 520, height: 520, borderRight: `4px solid ${C.muted}`, padding: 30, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, color: C.muted, textAlign: 'center', marginBottom: 20}}>자산</div>
          {['주식', '채권', '대체'].map((k, i) => (
            <div
              key={k}
              style={{
                height: 120,
                marginBottom: 16,
                borderRadius: 12,
                background: C.asset,
                opacity: 0.35 + i * 0.25,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 36,
                fontWeight: 700,
                color: C.bg,
              }}
            >
              {k}
            </div>
          ))}
        </div>
        <div style={{width: 520, height: 520, padding: 30, position: 'relative'}}>
          <div style={{fontSize: 34, color: C.muted, textAlign: 'center', marginBottom: 20, opacity: 0.3 + pL * 0.7}}>부채</div>
          <div
            style={{
              height: 300,
              borderRadius: 12,
              background: C.liab,
              opacity: pL,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 36,
              fontWeight: 700,
              color: C.bg,
            }}
          >
            연금 약속의 현재가치
          </div>
          <div
            style={{
              height: 120,
              marginTop: 16,
              borderRadius: 12,
              border: `3px dashed ${C.accent}`,
              opacity: prog(f, cue(1) + 40),
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 32,
              color: C.accent,
            }}
          >
            잉여금
          </div>
          <div
            style={{
              position: 'absolute',
              inset: 30,
              top: 90,
              border: `3px dashed ${C.line}`,
              borderRadius: 12,
              opacity: 1 - pL,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 80,
              color: C.line,
            }}
          >
            ?
          </div>
        </div>
      </div>
    </Scene>
  );
};

/* S1 자산 중심 vs 부채 중심 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const col = (title: string, color: string, rows: string[], q: string, at: number) => (
    <Card style={{flex: 1, borderTop: `6px solid ${color}`, ...rise(f, at)}}>
      <div style={{fontSize: 38, fontWeight: 800, color}}>{title}</div>
      {rows.map((r) => (
        <div key={r} style={{fontSize: 30, marginTop: 18}}>
          • {r}
        </div>
      ))}
      <div style={{fontSize: 40, fontWeight: 800, marginTop: 28, color}}>{q}</div>
    </Card>
  );
  return (
    <Scene t={t} eyebrow={EB} title="DB 연기금의 목표는 수익률 극대화가 아니라 약속의 이행입니다" sub="W1~W5는 자산 중심 — μ, Σ로 자산 수익률을 최대화했다">
      <div style={{display: 'flex', gap: 40}}>
        {col('자산 중심 (W1~W5)', C.asset, ['μ, Σ, 뷰, 제약이 입력', '부채는 입력에 없다', '위험 = 변동성 σ'], '“얼마나 벌었나”', cue(0))}
        {col('부채 중심 (LDI · W6)', C.liab, ['부채 현재가치·듀레이션 추정', '적립비율 FR이 성적표', '위험 = 듀레이션 갭'], '“부채보다 더 벌었나”', cue(1))}
      </div>
      <div
        style={{
          marginTop: 34,
          fontSize: 34,
          fontWeight: 700,
          color: C.accent,
          textAlign: 'center',
          ...rise(f, cue(2)),
        }}
      >
        IPS의 진짜 목표 — 30년 뒤 퇴직자에게 월 200만 원을 지급할 수 있도록 관리한다
      </div>
    </Scene>
  );
};

/* S2 LDI ↔ GBI 공통 문법 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const rows = [
    ['지켜야 할 것', '부채 L (연금 약속)', '목표 G (노후 생활비 등)'],
    ['지키는 자산', '부채 벤치마크 (장기채)', 'GHP (물가연동국채 등)'],
    ['버틸 여유', '잉여금 S = A − L', '쿠션 A − F'],
    ['수익 추구', 'Return-Seeking', 'PSP (Performance-Seeking)'],
    ['위험의 뜻', '적립비율이 떨어질 위험', '목표를 못 이룰 확률'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="기관은 부채, 개인은 목표를 먼저 안전자산으로 복제합니다" sub="두 틀의 공통 문법 — 지킬 것을 복제하고 남는 자금으로 수익을 추구한다">
      <Card style={{padding: '6px 0'}}>
        <div style={{display: 'flex', padding: '14px 30px', fontSize: 30, fontWeight: 800, borderBottom: `1px solid ${C.line}`}}>
          <span style={{flex: 0.8, color: C.muted}}>구분</span>
          <span style={{flex: 1, color: C.liab}}>LDI (기관 · M7)</span>
          <span style={{flex: 1, color: C.floor}}>GBI (개인 · M8)</span>
        </div>
        {rows.map((r, i) => {
          const at = (i < 2 ? cue(0) : cue(1)) + 20 + (i % 3) * 14;
          return (
            <div key={r[0]} style={{display: 'flex', padding: '16px 30px', fontSize: 32, ...rise(f, at, 14)}}>
              <span style={{flex: 0.8, color: C.muted}}>{r[0]}</span>
              <span style={{flex: 1}}>{r[1]}</span>
              <span style={{flex: 1}}>{r[2]}</span>
            </div>
          );
        })}
      </Card>
    </Scene>
  );
};

/* S3 세 가지 메시지 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const msgs = [
    {n: '1', k: '관점의 전환', v: '자산이 아니라 자산 대 부채. FR = A/L — 자산 +7.5%여도 부채 +15%면 나쁜 해', c: C.asset},
    {n: '2', k: '면역화는 수학적 방패', v: 'Redington 3조건으로 금리 방향과 무관하게 잉여금을 지킨다 — 실무는 헤지 + 수익 추구 2펀드', c: C.floor},
    {n: '3', k: '레버리지를 두려워하라', v: '2022 영국 — IRS 레버리지 LDI의 Doom Loop. 손실 추정 £150B, BOE £65B 개입', c: C.liab},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="이번 주가 던지는 메시지는 세 가지입니다" sub="부채를 무시하는 것은 거대한 공매도 포지션을 무시하는 것과 같다">
      {msgs.map((m, i) => (
        <Card key={m.n} style={{display: 'flex', gap: 30, alignItems: 'center', marginBottom: 22, ...rise(f, cue(i))}}>
          <div
            style={{
              width: 76,
              height: 76,
              borderRadius: 38,
              background: m.c,
              color: C.bg,
              fontSize: 42,
              fontWeight: 900,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            {m.n}
          </div>
          <div>
            <div style={{fontSize: 38, fontWeight: 800, color: m.c}}>{m.k}</div>
            <div style={{fontSize: 28, color: C.muted, marginTop: 6}}>{m.v}</div>
          </div>
        </Card>
      ))}
    </Scene>
  );
};

/* S4 아홉 단원 → 헤지비율 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const groups = [
    {k: '1교시', u: ['① 부채와 적립비율', '② 할인율']},
    {k: '2교시', u: ['③ 듀레이션·DV01', '④ Redington 면역화', '⑤ 두 블록', '⑥ 헤지 수단']},
    {k: '3교시', u: ['⑦ 2022 영국 · SVB']},
    {k: '4교시', u: ['⑧ 실습', '⑨ 모의 IC']},
  ];
  const pIn = prog(f, cue(1) + 6, 30);
  return (
    <Scene t={t} eyebrow={EB} title="아홉 단원은 오후 IC의 헤지 비율 한 숫자로 모입니다" sub="단원마다 푸는 질문이 하나씩 있다">
      <div style={{display: 'flex', gap: 30, alignItems: 'stretch'}}>
        <div style={{flex: 1}}>
          {groups.map((g, i) => (
            <div key={g.k} style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 20, ...rise(f, cue(0) + i * 16)}}>
              <div style={{width: 110, fontSize: 28, color: C.accent, fontWeight: 700}}>{g.k}</div>
              <div style={{display: 'flex', gap: 12, flexWrap: 'wrap'}}>
                {g.u.map((u) => (
                  <Chip key={u} color={C.muted} style={{fontSize: 26, padding: '8px 20px', color: C.text}}>
                    {u}
                  </Chip>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div style={{width: 140, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 100, color: C.accent, opacity: pIn}}>
          →
        </div>
        <div
          style={{
            width: 420,
            borderRadius: 24,
            border: `4px solid ${C.accent}`,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            transform: `scale(${pop(f, cue(1) + 16)})`,
          }}
        >
          <div style={{fontSize: 34, color: C.muted}}>오후 IC</div>
          <div style={{fontSize: 64, fontWeight: 900, color: C.accent}}>헤지 비율</div>
          <div style={{fontSize: 30, color: C.muted}}>한 숫자</div>
        </div>
      </div>
    </Scene>
  );
};

/* S5 IC 안건 미리보기 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const opts = [
    {k: '안 A · 현행 유지', h: '2.1% → 3%', v: '새로 사지도, 계약하지도 않는다 · 갭 −34년 그대로'},
    {k: '안 B · 30년 국고채 교체', h: '3% → 5%', v: '보유 채권 131조를 30년 국고채로 · 증거금 없음'},
    {k: '안 C · 금리 스왑', h: '3% → 30%', v: '명목 1,223조 · 사흘 +200bp에 증거금 401조'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="세 시간 뒤 여러분은 국민연금 LDI 안건에 표결합니다" sub="헤지 비율 = 자산 DV01 ÷ 부채 DV01 · 지금 2.1%">
      <div style={{display: 'flex', gap: 28}}>
        {opts.map((o, i) => (
          <Card key={o.k} style={{flex: 1, ...rise(f, cue(1) + i * 14)}}>
            <div style={{fontSize: 32, fontWeight: 800}}>{o.k}</div>
            <div style={{fontSize: 52, fontWeight: 900, color: C.accent, marginTop: 10}}>{o.h}</div>
            <div style={{fontSize: 26, color: C.muted, marginTop: 10}}>{o.v}</div>
          </Card>
        ))}
      </div>
      <div style={{display: 'flex', gap: 14, marginTop: 30, ...rise(f, cue(1) + 50)}}>
        {['① 갭 실재', '② 시장 수용', '③ 버퍼', '④ 허들 5.5%', '⑤ 지침'].map((c) => (
          <Chip key={c} color={C.muted} style={{fontSize: 26, color: C.text}}>
            {c}
          </Chip>
        ))}
      </div>
      <div style={{fontSize: 38, fontWeight: 800, color: C.accent, marginTop: 34, ...rise(f, cue(2))}}>
        “LDI를 하느냐”가 아니라 “몇 %를, 무엇으로, 얼마의 버퍼로”
      </div>
    </Scene>
  );
};

export const M7E00 = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M7E00_TOTAL = T.total;
