import React from 'react';
import {C} from '../theme';
import {fmt, lerp, prog} from './anim';

/** 숫자가 from→to로 변하는 행 */
export const CounterRow: React.FC<{
  f: number;
  at: number;
  label: string;
  from: number;
  to: number;
  d?: number;
  unit?: string;
  color?: string;
  show?: number;
  note?: string;
}> = ({f, at, label, from, to, d = 1, unit = '', color = C.text, show = 0, note}) => {
  const p = prog(f, at, 36);
  const vis = prog(f, show, 14);
  const v = lerp(from, to, p);
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'baseline',
        justifyContent: 'space-between',
        padding: '18px 26px',
        borderBottom: `1px solid ${C.line}`,
        opacity: vis,
      }}
    >
      <span style={{fontSize: 32, color: C.muted}}>{label}</span>
      <span style={{fontSize: 48, fontWeight: 700, color, fontVariantNumeric: 'tabular-nums'}}>
        {fmt(v, d)}
        {unit}
        {note ? (
          <span style={{fontSize: 28, marginLeft: 14, color: C.accent, opacity: p}}>{note}</span>
        ) : null}
      </span>
    </div>
  );
};

export const Chip: React.FC<{color?: string; style?: React.CSSProperties; children: React.ReactNode}> = ({
  color = C.accent,
  style,
  children,
}) => (
  <div
    style={{
      display: 'inline-block',
      border: `2px solid ${color}`,
      color,
      borderRadius: 999,
      padding: '10px 26px',
      fontSize: 30,
      fontWeight: 600,
      background: 'rgba(255,255,255,0.03)',
      ...style,
    }}
  >
    {children}
  </div>
);

export const Card: React.FC<{style?: React.CSSProperties; children: React.ReactNode}> = ({style, children}) => (
  <div
    style={{
      background: C.panel,
      border: `1px solid ${C.line}`,
      borderRadius: 18,
      padding: '24px 30px',
      ...style,
    }}
  >
    {children}
  </div>
);

/** 가로 막대 하나 (값 0..max) */
export const HBar: React.FC<{
  f: number;
  at: number;
  label: string;
  value: number;
  max: number;
  text: string;
  color?: string;
  dashed?: boolean;
  height?: number;
  textWidth?: number;
}> = ({f, at, label, value, max, text, color = C.asset, dashed, height = 54, textWidth = 300}) => {
  const p = prog(f, at, 34);
  return (
    <div style={{marginBottom: 22, opacity: prog(f, at - 4, 10)}}>
      <div style={{fontSize: 28, color: C.muted, marginBottom: 8}}>{label}</div>
      <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
        <div style={{flex: 1, height, background: C.bg2, borderRadius: 10, position: 'relative'}}>
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: `${Math.max((value / max) * p, 0.004) * 100}%`,
              background: dashed ? 'transparent' : color,
              border: dashed ? `3px dashed ${color}` : undefined,
              borderRadius: 10,
            }}
          />
        </div>
        <div style={{width: textWidth, fontSize: 36, fontWeight: 800, color, opacity: p}}>{text}</div>
      </div>
    </div>
  );
};

/** 행이 하나씩 나타나는 표 */
export const RevealTable: React.FC<{
  f: number;
  cols: string[];
  rows: {cells: React.ReactNode[]; at: number; hi?: boolean}[];
  widths?: number[];
  size?: number;
}> = ({f, cols, rows, widths, size = 32}) => (
  <Card style={{padding: '8px 0'}}>
    <div style={{display: 'flex', padding: '12px 28px', fontSize: size - 6, color: C.muted, borderBottom: `1px solid ${C.line}`}}>
      {cols.map((c, i) => (
        <span key={i} style={{flex: widths ? widths[i] : 1}}>
          {c}
        </span>
      ))}
    </div>
    {rows.map((r, j) => (
      <div
        key={j}
        style={{
          display: 'flex',
          padding: '14px 28px',
          fontSize: size,
          background: r.hi ? 'rgba(242,140,40,0.12)' : undefined,
          opacity: prog(f, r.at, 14),
          transform: `translateY(${(1 - prog(f, r.at, 14)) * 16}px)`,
        }}
      >
        {r.cells.map((c, i) => (
          <span key={i} style={{flex: widths ? widths[i] : 1}}>
            {c}
          </span>
        ))}
      </div>
    ))}
  </Card>
);
