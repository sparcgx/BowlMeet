#!/usr/bin/env python3
"""Apply a narrowly scoped test-harness correction, not an application patch.
The original harness recognized bowlingMeetup keys but omitted the older
bowlingScoreWorkstation keys when reading root source (Preview was already
prefixed). Preserve all 24 safety assertions; save the exact executed harness.
"""
from pathlib import Path
import hashlib
import sys

path=Path(__file__).with_name('test-data-safety-v0474.py')
text=path.read_text(encoding='utf-8')
old="source=original.replace('bowlingMeetup.',RUN)"
new="source=original.replace('bowlingMeetup.',RUN).replace('bowlingScoreWorkstation.',RUN)"
if text.count(old)!=1:
    raise SystemExit('Unexpected harness revision; refusing an ambiguous correction')
text=text.replace(old,new)
if len(sys.argv)<3:
    raise SystemExit('Usage: python tools/run-data-safety-fi.py ROOT OUTPUT [--browser chromium|webkit]')
out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
(out/'executed-harness.py').write_text(text,encoding='utf-8')
(out/'executed-harness.sha256').write_text(hashlib.sha256(text.encode()).hexdigest()+'\n')
exec(compile(text,str(path),'exec'),{'__name__':'__main__','__file__':str(path)})
