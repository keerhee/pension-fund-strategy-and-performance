# W06 M8 실습 — 방법 3 몬테카를로 (강의본 단원 ③)

- `gbi_mc.py` — 방법 3 전체(방법 1 재현 · 한 계좌 격자 · CPPI). `python3 gbi_mc.py` → `gbi_mc_results.json`, `python3 gbi_mc.py --demo` → `gbi_mc_demo.json`.
- `priority_mc.py` — [실습 A] 목표 여럿 · 우선순위(방법 1 문제를 MC로). 프롬프트: `W06_M8_실습_우선순위MC_ClaudeCode_프롬프트.md`.
- `dm_mc.py` → `dm_mc_results.json` — [실습 B] Das–Markowitz(방법 2 문제를 MC로). 프롬프트: `W06_M8_실습_DasMarkowitzMC_ClaudeCode_프롬프트.md`.
- 모두 numpy만, 이 폴더에 결과를 쓴다(seed 2026 고정 — 다시 돌려도 같은 숫자). 같은 예제의 Colab 노트북은 `../W06_M8_실습_Colab/`.
