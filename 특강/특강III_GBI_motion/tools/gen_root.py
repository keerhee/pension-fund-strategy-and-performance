"""src/episodes/*.tsx를 모두 Root.tsx에 등록한다."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parents[1]
ids = sorted(p.stem for p in (root / "src/episodes").glob("M*.tsx"))
imp = "".join(f"import {{{i}, {i}_TOTAL}} from './episodes/{i}';\n" for i in ids)
eps = "".join(f"  ['{i}', {i}, {i}_TOTAL],\n" for i in ids)
(root / "src/Root.tsx").write_text(f"""import React from 'react';
import {{Composition}} from 'remotion';
{imp}
const EPS: [string, React.FC, number][] = [
{eps}];

export const RemotionRoot: React.FC = () => (
  <>
    {{EPS.map(([id, C, n]) => (
      <Composition key={{id}} id={{id}} component={{C}} durationInFrames={{n}} fps={{30}} width={{1920}} height={{1080}} />
    ))}}
  </>
);
""")
print(len(ids), "episodes")
