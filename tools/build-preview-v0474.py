"""Build a self-contained, cloud-disabled preview. No production DB/keys/cache reuse."""
from pathlib import Path
import re,shutil,json,sys
root=Path('.');out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
for folder in ['assets','icons']:shutil.copytree(root/folder,out/folder,dirs_exist_ok=True)
html=(root/'index.html').read_text()
for old in ['bowlingMeetup.','bowlingScoreWorkstation.']:
 html=html.replace("'"+old,"'bowlmeet.preview.v0474d1."+old)
html=html.replace("const PUBLIC_HISTORY_CODE='PUBLIC';","const PUBLIC_HISTORY_CODE='V474D1';")
html=html.replace("const PUBLIC_HISTORY_PIN='042042';","const PUBLIC_HISTORY_PIN='047401';")
html=re.sub(r"const BUILTIN_SUPABASE_URL='[^']*';","const BUILTIN_SUPABASE_URL='';",html)
html=re.sub(r"const BUILTIN_SUPABASE_PUBLISHABLE_KEY='[^']*';","const BUILTIN_SUPABASE_PUBLISHABLE_KEY='';",html)
html=html.replace('const BUILTIN_CLOUD=true;','const BUILTIN_CLOUD=false;')
html=html.replace('<head>','<head>\n<meta http-equiv="Content-Security-Policy" content="connect-src \'self\' blob: data:;" />')
html=html.replace('<main id="mainContent" tabindex="-1">','<main id="mainContent" tabindex="-1"><aside style="padding:8px 12px;margin-bottom:12px;border:1px solid #dae2ee;border-radius:12px;font-size:12px" role="note">v0.4.7.4-dev.1 PREVIEW · 獨立測試資料 · 雲端停用 · 不影響正式版</aside>')
assert "const DB_VERSION=2;" in html and "const PUBLIC_HISTORY_CODE='PUBLIC';" not in html
assert "const DB_NAME='bowlmeet.preview.v0474d1." in html
(out/'index.html').write_text(html)
manifest=json.loads((root/'manifest.webmanifest').read_text());manifest['name']='BowlMeet v0.4.7.4-dev.1 Preview';manifest['short_name']='BowlMeet TEST'
(out/'manifest.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
sw=(root/'sw.js').read_text().replace("const PRODUCTION_CACHE_ROOT='bowlmeet-v';","const PRODUCTION_CACHE_ROOT='bowlmeet-preview-v0474d1-';").replace('bowlmeet-v0.4.7.4-dev.1-','bowlmeet-preview-v0474d1-')
(out/'sw.js').write_text(sw)
for name in ['release-identity.json','deployment-test.html']:shutil.copy2(root/name,out/name)
identity=json.loads((out/'release-identity.json').read_text());identity['channel']='isolated-preview-cloud-disabled';(out/'release-identity.json').write_text(json.dumps(identity,indent=2)+'\n')
print('Isolated preview built at',out)
