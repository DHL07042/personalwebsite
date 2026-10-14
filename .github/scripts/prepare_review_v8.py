"""One-use website preparation. Only the review branch may run this."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageChops
root=Path('.')
assert json.loads(Path('release.json').read_text())['release']=='2026-10-14.7'
REL='2026-10-14.8'
def replace(file,old,new,count=1):
 p=Path(file);s=p.read_text();assert s.count(old)==count,(file,old[:100],s.count(old));p.write_text(s.replace(old,new))
assets=[('assets/img/t1-shoe.webp','assets/img/t1-shoe-display.webp'),('assets/img/t1-threshold.webp','assets/img/t1-threshold-display.webp'),('assets/img/t1-phases.webp','assets/img/t1-phases-display.webp'),('assets/src/experiment-results.png','assets/img/grf-results-display.webp'),('assets/src/concept-assistance.png','assets/img/concept-assistance-display.webp')]
manifest=[]
for src,dst in assets:
 im=Image.open(src).convert('RGB');bbox=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox() or (0,0,*im.size)
 box=(max(0,bbox[0]-10),max(0,bbox[1]-10),min(im.width,bbox[2]+10),min(im.height,bbox[3]+10))
 out=im.crop(box);out.save(dst,'WEBP',lossless=True,method=6)
 decoded=Image.open(dst).convert('RGB');assert decoded.size==out.size and decoded.tobytes()==out.tobytes()
 manifest.append({'source':src,'output':dst,'source_sha256':hashlib.sha256(Path(src).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(Path(dst).read_bytes()).hexdigest(),'source_dimensions':list(im.size),'source_box':list(box),'output_dimensions':list(out.size),'operation':'Trim exactly-white external border only; retain source margin; lossless WebP; no resampling, recoloring, retouching or changed labels.','decoded_pixel_equality':True})
Path('media-processing.json').write_text(json.dumps({'release':REL,'assets':manifest},indent=2)+'\n')
p=Path('publications.html');s=p.read_text();a=s.index('<li class="pub" id="T1">');b=s.index('</li>',a);block=s[a:b];assert '<strong>D. Lee</strong>, H. Choi, and K. Kong' in block
s=s[:a]+block.replace('<strong>D. Lee</strong>, H. Choi, and K. Kong','<strong>D. Lee</strong>, K. Kong, and H. Choi')+s[b:];p.write_text(s)
replace('research.html','The approach was first presented at ASME ISPS 2021 [T1]; the journal article [J1] reports the overshoe‑type module and its evaluation.','This work was presented at ASME ISPS 2021 [T1] and subsequently reported in JKSPE [J1].')
replace('research.html','The 2021 presentation showed phase detection for three participants at walking speeds from 1.0 to 4.1 km/h with identical thresholds [T1].','The 2021 presentation includes recordings at 1.0, 2.1, and 4.1 km/h and during gradual deceleration for one participant, plus examples from two additional participants using the same thresholds [T1].')
replace('research.html','      <div class="media three">\n<figure class="fig cover">','      <p class="method-note"><strong>Measurement principle.</strong> With a fixed separation between the sensors, the two distances describe the foot’s position relative to the ground; their relative values help distinguish swing sub‑phases [T1].</p>\n      <div class="media study-figures" aria-label="Figures from the ISPS 2021 presentation">\n<figure class="fig">')
replace('research.html','Heel and MTP distance over the gait cycle (mean ± 1 s.d.) with the two thresholds used for phase detection [T1].','Left heel and MTP distances over the gait cycle (mean ± 1 s.d.), with the two detection thresholds [T1].')
replace('research.html','ToF measurements and the detected gait phase (0–5) while walking at 1.0 km/h [T1].','Representative right-foot recording from participant 1 at 1.0 km/h: measured distances and detected phases 0–5 [T1].')
p=Path('research.html');s=p.read_text();old='<figure class="fig">\n  <a href="assets/img/t1-phases.webp"';assert old in s;s=s.replace(old,'<figure class="fig figure-wide">\n  <a href="assets/img/t1-phases.webp"',1)
for item in manifest:
 current={'assets/src/experiment-results.png':'assets/img/grf-results.webp','assets/src/concept-assistance.png':'assets/img/concept-assistance.webp'}.get(item['source'],item['source'])
 s=s.replace(current,item['output'])
 pattern=r'(<img src="'+re.escape(item['output'])+r'"[^>]*?)width="\d+" height="\d+"'
 s,n=re.subn(pattern,lambda m:m.group(1)+f'width="{item["output_dimensions"][0]}" height="{item["output_dimensions"][1]}"',s);assert n==1
p.write_text(s)
replace('personal.html','Two things I\u00a0keep coming back to: a camera when I\u00a0travel, and a microphone whenever I\u00a0can get one.','Outside research, I\u00a0enjoy travel photography and music.')
replace('personal.html','I\u00a0sing and rap. In Korea that mostly means noraebang, the karaoke room, and I\u00a0take it more seriously than the setting suggests.','Singing and rapping are two of my hobbies. I\u00a0enjoy practicing both at noraebang, Korea’s karaoke rooms.')
p=Path('styles.css');s=p.read_text();s=re.sub(r'Release 2026-10-14\.\d+',f'Release {REL}',s,count=1)
s+='''\n/* Review .8: scientific figure readability without content crop or type reduction. */
.method-note{margin-top:1.1rem;max-width:74ch;color:var(--ink-2)}
.method-note strong{color:var(--ink);font-weight:500}
.media.study-figures{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.study-figures .figure-wide{grid-column:1/-1;width:min(100%,800px);justify-self:center}
.study-figures figure.fig img{padding:14px;object-fit:contain}
.study-figures .figure-wide img{aspect-ratio:auto;height:auto}
@media(max-width:720px){
 .media.study-figures{grid-template-columns:minmax(0,1fr)}
 .study-figures .figure-wide{grid-column:auto}
 .study-figures figure.fig img{aspect-ratio:auto;height:auto}
}
.lightbox figure{max-height:100%;min-height:0}
.lightbox figcaption{flex:0 1 auto;max-height:30dvh;overflow:auto;padding:0 2px}
''';p.write_text(s)
for p in root.glob('*.html'):p.write_text(p.read_text().replace('2026-10-14.7',REL))
p=Path('release.json');d=json.loads(p.read_text());d['release']=REL;d['base_content_commit']='e2839303868d84a6f81761dbad655d17c0286262';p.write_text(json.dumps(d,indent=2)+'\n')
p=Path('MAINTAINING.md');s=p.read_text();s+='''\n## Release .8 evidence and image handling
- T1's supplied one-page abstract and presentation both list D. Lee, K. Kong, H. Choi, in that order. Follow those sources rather than an older CV order unless contrary primary evidence is provided.
- T1 is a related earlier presentation of the J1 work. Do not describe overshoe packaging as a demonstrated new addition in 2026 or label the entries as independent replications.
- The T1 deck shows speed conditions for participant 1 and additional participant examples; do not imply a fully crossed participants-by-speeds validation without records.
- Retain [T1] provenance on the three figures. New display assets use lossless conversion and exactly-white exterior trim only; media-processing.json records source hashes, crop boxes and pixel checks. Source assets remain unmodified.
- The owner-approved GRF Case I/II/III mapping remains. Image preparation does not authorize revised analyses or additional effect claims.
- Music is a personal interest, not a research achievement. Driving text still requires owner-approved wording and images.
- Keep private correspondence and publication-administration review details outside this public repository.
- DNS TTL is cache lifetime, not a periodic connection timer. Do not change DNS based only on a speculative latency diagnosis.
''';p.write_text(s)
# Regression checks use only the standard library; CI need not install Pillow.
p=Path('.github/scripts/check_review.py');s=p.read_text();marker="report={'base':BASE";assert marker in s
addition='''# Display asset provenance and source-based scope checks.
import hashlib
media=json.loads(Path('media-processing.json').read_text())
checks['media_manifest_integrity']=all(hashlib.sha256(Path(x['source']).read_bytes()).hexdigest()==x['source_sha256'] and hashlib.sha256(Path(x['output']).read_bytes()).hexdigest()==x['output_sha256'] and x['decoded_pixel_equality'] for x in media['assets'])
checks['t1_byline_matches_supplied_sources']='<strong>D. Lee</strong>, K. Kong, and H. Choi' in Path('publications.html').read_text().split('id="T1"')[1]
checks['t1_scope_is_not_fully_crossed']='for one participant, plus examples from two additional participants' in research
checks['grf_owner_mapping_retained']='off (Case I), weak (Case II) and strong (Case III)' in research
checks['t1_provenance_retained']=research.count('[T1]')>=6
'''
s=s.replace(marker,addition+marker,1);p.write_text(s)
print('Prepared release .8 and five faithful display assets; no source figures removed.')
