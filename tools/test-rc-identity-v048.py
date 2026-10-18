"""Verify RC runtime equals user-accepted dev.3 except release identity/copy."""
from pathlib import Path
import subprocess,json,hashlib
base='7b11081c0b1edfd972f8008f70b570b694b2f567'
for name in ['index.html','sw.js','manifest.webmanifest']:
 old=subprocess.check_output(['git','show',base+':'+name],text=True)
 expected=old.replace('0.4.8-dev.3','0.4.8-RC.2').replace('048dev3','048rc2').replace('Development · 球聚賽制與系列賽','Release Candidate · 發布候選凍結').replace('開發測試','發布候選測試')
 assert Path(name).read_text()==expected,name
for name in subprocess.check_output(['git','ls-tree','-r','--name-only',base],text=True).splitlines():
 if name.startswith(('assets/','icons/')) or name.endswith('.sql'):
  assert Path(name).read_bytes()==subprocess.check_output(['git','show',base+':'+name]),name
x=json.loads(Path('release-identity.json').read_text());assert x['result_index_sha256']==hashlib.sha256(Path('index.html').read_bytes()).hexdigest()
assert x['db_version']==2 and x['public_history_code']=='PUBLIC' and not x['schema_migration']
print('PASS: accepted dev.3 equivalence, immutable assets/schema and RC identity')
