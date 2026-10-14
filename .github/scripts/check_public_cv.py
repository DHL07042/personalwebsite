"""Check that only the reviewed public PDF can be linked by this release."""
from pathlib import Path
import hashlib,json,re
meta=json.loads(Path('public-cv.json').read_text())
p=Path(meta['path'])
if not p.is_file():
    raise SystemExit('Required public CV is not attached yet. Upload the reviewed Daeho-Lee-CV.pdf to this PR branch; do not merge while missing.')
b=p.read_bytes()
checks={
 'sha256_matches_reviewed_file':hashlib.sha256(b).hexdigest()==meta['sha256'],
 'byte_length_matches':len(b)==meta['bytes'],
 'pdf_header':b.startswith(b'%PDF-'),
 'single_saved_revision':b.count(b'startxref')==1 and b.count(b'%%EOF')==1,
 'home_link_present':meta['path'] in Path('index.html').read_text(),
 'contact_link_present':meta['path'] in Path('contact.html').read_text(),
 'commendation_present':'Certificate of Commendation</strong>, Chief of Staff, Republic of Korea Army' in Path('index.html').read_text(),
}
report={'path':meta['path'],'version':meta['version'],'checks':checks,'pass':all(checks.values())}
print(json.dumps(report,indent=2))
if not report['pass']:raise SystemExit('Public CV verification failed; do not replace with another PDF without review.')
