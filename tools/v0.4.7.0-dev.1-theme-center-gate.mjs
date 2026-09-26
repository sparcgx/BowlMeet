import fs from 'node:fs';

const read=p=>fs.readFileSync(p,'utf8');
const h=read('index.html');
const c=read('assets/liquid-glass-dev4.css');
const m=read('manifest.webmanifest');
const w=read('sw.js');
const d=read('deployment-test.html');

const tests=[];
const t=(name,ok)=>tests.push({name,ok:!!ok});

const themeIds=['default','liquid-glass','clear-blue','soft-violet','dark-night','high-contrast'];
const presetIds=['standard','mobile','field','glass','night'];

t('APP_VERSION v0.4.7.0-dev.1',h.includes("const APP_VERSION='0.4.7.0-dev.1'"));
t('Document title v0.4.7.0-dev.1',h.includes('BowlMeet v0.4.7.0-dev.1'));
t('Theme preference local key',h.includes("const THEME_PREFS_KEY='bowlingMeetup.themePreferences.v1'"));
t('Existing layout preference key preserved',h.includes("const LAYOUT_PREFS_KEY='bowlingMeetup.layoutPreferences.v1'"));
t('Theme Center page title',h.includes('<h2>版面設計</h2>'));
t('Six theme cards',themeIds.every(id=>h.includes(`data-theme-option="${id}"`)));
t('Six theme CSS token scopes',themeIds.every(id=>h.includes(`:root[data-theme="${id}"]`)));
t('Theme selector initializes',h.includes('function initThemeCenter()')&&h.includes('initThemeCenter();'));
t('Theme applies data-theme',h.includes('root.dataset.theme=p.theme'));
t('Theme persists to localStorage',h.includes('localStorage.setItem(THEME_PREFS_KEY,JSON.stringify(p))'));
t('Theme reset removes local key',h.includes('localStorage.removeItem(THEME_PREFS_KEY)'));
t('Legacy theme aliases migrate',h.includes("liquid:'liquid-glass'")&&h.includes("clearblue:'clear-blue'")&&h.includes("contrast:'high-contrast'"));
t('Motion setting',h.includes('themeMotionToggle')&&h.includes('motionEnabled'));
t('Transparency setting',h.includes('themeTransparencyToggle')&&h.includes('transparencyEnabled'));
t('Card radius setting',h.includes('themeCardRadiusSelect')&&h.includes('cardRadius'));
t('Shadow level setting',h.includes('themeShadowLevelSelect')&&h.includes('shadowLevel'));
t('Color intensity setting',h.includes('themeColorIntensitySelect')&&h.includes('colorIntensity'));
t('Five design presets',presetIds.every(id=>h.includes(`data-design-preset="${id}"`)));
t('Design preset persists theme + layout',h.includes('localStorage.setItem(THEME_PREFS_KEY,JSON.stringify(theme))')&&h.includes('localStorage.setItem(LAYOUT_PREFS_KEY,JSON.stringify(layout))'));
t('Reduced Motion fallback',h.includes('@media(prefers-reduced-motion:reduce)'));
t('Reduced Transparency fallback',h.includes('@media(prefers-reduced-transparency:reduce)'));
t('No backdrop-filter fallback',h.includes('@supports not ((-webkit-backdrop-filter:blur(1px)) or (backdrop-filter:blur(1px)))'));
t('Mobile Theme Center responsive layout',h.includes('@media(max-width:620px)')&&h.includes('.theme-card-grid{grid-template-columns:1fr}'));
t('Dark Night theme present',h.includes(':root[data-theme="dark-night"]'));
t('High Contrast focus present',h.includes('html[data-theme="high-contrast"] *:focus-visible'));
t('DB_VERSION unchanged',h.includes('const DB_VERSION=2;'));
t('PUBLIC history code unchanged',h.includes("const PUBLIC_HISTORY_CODE='PUBLIC';"));
t('PUBLIC control key unchanged',h.includes("const PUBLIC_CONTROL_KEY='bowlingMeetup.publicControl.v044';"));
t('Theme preferences excluded from captureState',!(/function captureState\(\)\{[^}]*THEME_PREFS_KEY/s.test(h)));
t('Manifest version aligned',m.includes('BowlMeet v0.4.7.0-dev.1'));
t('Manifest documents local-only theme scope',m.includes('不修改 PUBLIC')&&m.includes('Backup / Restore'));
t('Service worker cache isolated',w.includes("bowlmeet-v0.4.7.0-dev.1-theme-shell")&&w.includes("bowlmeet-v0.4.7.0-dev.1-theme-runtime"));
t('Service worker caches new CSS fingerprint',w.includes('./assets/liquid-glass-dev4.css?v=0470d1'));
t('Index uses new CSS fingerprint',h.includes('./assets/liquid-glass-dev4.css?v=0470d1'));
t('Deployment test version aligned',d.includes('BowlMeet v0.4.7.0-dev.1'));
t('Deployment test includes Theme Center acceptance',d.includes('Theme Center 驗收重點')&&d.includes('六主題切換'));
t('Shared Liquid Glass stylesheet remains present',h.includes('assets/liquid-glass-dev4.css')&&c.length>1000);
t('No SQL embedded in visual stylesheet',!c.includes('CREATE TABLE')&&!c.includes('ALTER TABLE'));
t('No script embedded in visual stylesheet',!c.includes('<script')&&!c.includes('javascript:'));

const failed=tests.filter(x=>!x.ok);
const result={
  version:'v0.4.7.0-dev.1',
  gate:'Theme Center Foundation Static Gate',
  baseline:'stable/v0.4.6.7',
  total:tests.length,
  pass:tests.length-failed.length,
  fail:failed.length,
  decision:failed.length?'BLOCKED':'STATIC_GATE_PASS',
  tests
};
console.log(JSON.stringify(result,null,2));
if(failed.length)process.exit(1);
