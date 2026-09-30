"""RC identity / no functional delta guard against the accepted dev.2 commit."""
from pathlib import Path
import hashlib,json,subprocess
base='40df653f3df7070a9332de9ba1ea40c60444c74d'
for name in ['index.html','sw.js','manifest.webmanifest']:
 old=subprocess.check_output(['git','show',base+':'+name],text=True)
 expected=old.replace('0.4.7.4-dev.2','0.4.7.4-RC.1').replace('0474d2','0474rc1')
 if name=='index.html':expected=expected.replace('Performance & UI Hardening · 開發測試','Release Candidate · 發布候選凍結')
 assert Path(name).read_text()==expected, 'Unexpected functional delta: '+name
subprocess.run(['git','diff','--exit-code',base,'--','assets','icons','*.sql'],check=True)
d=json.loads(Path('release-identity.json').read_text())
assert d['version']=='0.4.7.4-RC.1'
assert d['result_index_sha256']==hashlib.sha256(Path('index.html').read_bytes()).hexdigest()
assert d['dev2_device_gate']=='PASS_USER_REPORTED'
assert d['stable_promotion']=='NOT_EXECUTED'
print('PASS: RC identity, source hash, accepted dev.2 ancestry, unchanged scoring/storage/PUBLIC/SQL/assets')
