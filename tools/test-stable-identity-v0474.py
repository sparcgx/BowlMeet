"""Formal release gate: exact identity-only delta from accepted RC.1."""
from pathlib import Path
import subprocess,json,hashlib
base='0d87a4310ac4ab76cb45e25955391534bcdcd9eb'
for n in ['index.html','sw.js','manifest.webmanifest']:
 s=subprocess.check_output(['git','show',base+':'+n],text=True)
 s=s.replace('0.4.7.4-RC.1','0.4.7.4').replace('0474rc1','0474')
 if n=='index.html':s=s.replace('Release Candidate · 發布候選凍結','Stable · 正式穩定版')
 if n=='manifest.webmanifest':s=s.replace('BowlMeet 開發測試：快取一致性、效能及桌面／手機介面修正；資料契約不變。','BowlMeet 正式版：球聚、現場計分、公開成績與本機資料安全管理。')
 assert Path(n).read_text()==s,'Unexpected product delta: '+n
subprocess.run(['git','diff','--exit-code',base,'--','assets','icons','*.sql'],check=True)
d=json.loads(Path('release-identity.json').read_text())
assert d['version']=='0.4.7.4' and d['channel']=='stable'
assert d['result_index_sha256']==hashlib.sha256(Path('index.html').read_bytes()).hexdigest()
assert d['rc_device_gate']=='PASS_USER_REPORTED'
assert d['db_version']==2 and d['public_history_code']=='PUBLIC' and not d['schema_migration']
print('PASS: formal version/hash, accepted RC equivalence, unchanged storage/scoring/PUBLIC/SQL/assets')
