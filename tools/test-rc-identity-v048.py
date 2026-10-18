"""Verify RC runtime equals user-accepted dev.1 except release identity/copy."""
from pathlib import Path
import subprocess,json,hashlib
base='00f45866aa8bf89ce6df6d294d3e6fc7b1f0a984'
for name in ['index.html','sw.js','manifest.webmanifest']:
 old=subprocess.check_output(['git','show',base+':'+name],text=True)
 expected=old.replace('0.4.8-dev.1','0.4.8-RC.1').replace('048dev1','048rc1').replace('Development · 球道分組與現場順序','Release Candidate · 發布候選凍結').replace('BowlMeet 開發版','BowlMeet 發布候選版')
 assert Path(name).read_text()==expected,name
for name in subprocess.check_output(['git','ls-tree','-r','--name-only',base],text=True).splitlines():
 if name.startswith(('assets/','icons/')) or name.endswith('.sql'):
  assert Path(name).read_bytes()==subprocess.check_output(['git','show',base+':'+name]),name
x=json.loads(Path('release-identity.json').read_text());assert x['result_index_sha256']==hashlib.sha256(Path('index.html').read_bytes()).hexdigest()
assert x['db_version']==2 and x['public_history_code']=='PUBLIC' and not x['schema_migration']
print('PASS: accepted dev.1 equivalence, immutable assets/schema and RC identity')
