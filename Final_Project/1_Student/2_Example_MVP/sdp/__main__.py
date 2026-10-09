"""명령 모음 — 채점자는 start.command / start.bat 만 누르면 된다(= serve).

python -m sdp serve        채점 콘솔(브라우저) 열기
python -m sdp all          평가 구간 전체를 처음부터 다시 실행 (CIO 결정은 data/cio_decisions.csv)
python -m sdp quarter Q    한 분기만 다시 실행 (예: 2024-11)
python -m sdp check        공개 점검 T1~T8 → reports/selfcheck.md
python -m sdp report       성과 보고서·CHANGELOG·INTERVENTIONS·dashboard.html 갱신
"""
import sys
from . import pipeline

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "serve":
        from .server import serve
        serve(open_browser="--no-browser" not in sys.argv)
    elif cmd == "all":
        pipeline.run_all_quarters()
    elif cmd == "quarter":
        pipeline.run_quarter(sys.argv[2])
    elif cmd == "check":
        from . import selfcheck as S
        r = S.run(); S.write(r)
        print(f"통과 {sum(x['pass'] for x in r)}/{len(r)} → reports/selfcheck.md")
    elif cmd == "report":
        from . import perf, dashboard
        perf.write_reports(); dashboard.build()
        print("reports/performance.md · CHANGELOG.md · INTERVENTIONS.md · dashboard.html 갱신")
    else:
        print(__doc__)
