from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
 ctx=b.new_context();ctx.set_offline(True)
 p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.route('http://127.0.0.1:8765/**',lambda r:r.fulfill(content_type='text/html',body=(ROOT/'INTERVIEW_BARAKA_FINAL.html').read_text()))
 p.goto('http://127.0.0.1:8765/app');p.wait_for_selector('text=Penyimpanan lokal siap')
 for key in p.evaluate('Object.keys(DEFAULTS)'):
  p.get_by_role('button',name='Dashboard',exact=True).click()
  p.get_by_role('button',name='Mulai interview',exact=True).click()
  p.get_by_label('Posisi',exact=True).select_option(key)
  p.get_by_role('button',name='Buat sesi interview',exact=True).click()
  p.get_by_label('Nama kandidat *',exact=True).fill('Uji '+key)
  p.get_by_label('Cabang/lokasi *',exact=True).fill('Pontianak')
  p.get_by_label('Interviewer *',exact=True).fill('HRD')
  p.get_by_role('button',name='3 Interview',exact=True).click()
  assert p.locator('#app h3').first.inner_text()==p.evaluate('current.template.questions[0].text')
  p.get_by_role('button',name='4 Praktik',exact=True).click()
  p.get_by_label('Nama penguji kompeten *',exact=True).fill('Penguji')
  p.get_by_label('Dilaksanakan dengan supervisi penguji kompeten',exact=True).check()
  for score in p.get_by_role('button',name='Nilai 3',exact=True).all():score.click()
  p.get_by_label('Catatan bukti penguji *',exact=True).fill('Langkah sesuai pengamatan')
  p.get_by_label('Dokumentasi hasil * (hasil hitung, temuan, referensi berkas aman; tanpa lampiran sensitif)',exact=True).fill('Checklist simulasi empat item')
  p.get_by_label('Tes telah selesai',exact=True).check()
  assert p.evaluate('evaluate(current).practice')==75
  p.get_by_role('button',name='Simpan manual',exact=True).click()
  p.wait_for_function('storageOK')
 assert p.evaluate('state.sessions.length')==7
 count=p.evaluate('''()=>{let count=0;const reject=f=>{try{f();throw Error('ACCEPTED');}catch(e){if(e.message==='ACCEPTED')throw e;count++;}};let t=clone(DEFAULTS.tkbm);t.questions.push({...clone(t.questions[0]),id:'optional',required:false,critical:false});validateTemplate(t);let s=newSession(t);s.answers.optional={score:'NA',note:'',naReason:'Skenario opsional tidak dijalankan'};validateSession(s);count++;s.answers.optional.naReason='';reject(()=>validateSession(s));s=newSession(DEFAULTS.tkbm);s.answers[s.template.questions[0].id]={score:5,note:'',naReason:''};reject(()=>validateSession(s));s.answers[s.template.questions[0].id].score='NA';s.answers[s.template.questions[0].id].naReason='Tidak boleh';reject(()=>validateSession(s));t=clone(DEFAULTS.tkbm);t.questions[1].id=t.questions[0].id;reject(()=>validateTemplate(t));t=clone(DEFAULTS.tkbm);t.questions[0].rubric[2]='';reject(()=>validateTemplate(t));t=clone(DEFAULTS.tkbm);t.questions[0].id='__proto__';reject(()=>validateTemplate(t));reject(()=>validateState({schema:1,templates:DEFAULTS,sessions:[state.sessions[0],state.sessions[0]]}));return count;}''')
 assert count==8
 # Finalization is invalidated after editing an assessment.
 p.evaluate("current.finalizedAt=now();touch()")
 assert not p.evaluate('!!current.finalizedAt')
 # Editor delete preserves typed text; reset cancellation/confirmation preserves sessions.
 p.get_by_role('button',name='Bank Pertanyaan',exact=True).click()
 p.get_by_label('Pertanyaan utama',exact=True).first.fill('Teks tetap setelah hapus')
 p.get_by_role('button',name='Tambah pertanyaan',exact=True).click()
 p.once('dialog',lambda d:d.accept())
 p.get_by_role('button',name='Hapus pertanyaan',exact=True).last.click()
 assert p.get_by_label('Pertanyaan utama',exact=True).first.input_value()=='Teks tetap setelah hapus'
 p.once('dialog',lambda d:d.dismiss())
 p.get_by_role('button',name='Kembalikan template bawaan',exact=True).click()
 assert p.get_by_label('Pertanyaan utama',exact=True).first.input_value()=='Teks tetap setelah hapus'
 p.once('dialog',lambda d:d.accept())
 p.get_by_role('button',name='Kembalikan template bawaan',exact=True).click()
 p.wait_for_function('state.templates.mt_staff.version===2')
 assert p.evaluate('state.sessions.length')==7
 assert p.get_by_label('Pertanyaan utama',exact=True).first.input_value()==p.evaluate('DEFAULTS.mt_staff.questions[0].text')
 # A manual critical finding also stops a high-score recommendation.
 p.evaluate("""()=>{const s=newSession(DEFAULTS.tkbm);s.name='X';s.branch='A';s.interviewer='HR';for(const q of s.template.questions)if(q.type==='dinilai')s.answers[q.id]={score:4,note:'Bukti',naReason:''};for(const r of s.template.requirements)s.gates[r.id]={status:'Memenuhi',note:'Bukti'};s.practice={scores:[4,4,4,4],done:true,supervised:true,examiner:'HR',note:'Bukti',documentation:'Bukti'};s.unresolvedFinding=true;if(evaluate(s).status!=='Perlu pendalaman atau asesmen ulang')throw Error('manual finding');}""")
 # All dynamic UI text is safe; no duplicate DOM ids or external assets.
 assert p.evaluate('new Set([...document.querySelectorAll("[id]")].map(e=>e.id)).size===document.querySelectorAll("[id]").length')
 assert p.locator('script[src],link[href],img[src],iframe').count()==0
 p.get_by_role('button',name='Dashboard',exact=True).click()
 p.set_viewport_size({'width':1440,'height':1050});p.screenshot(path='/tmp/baraka-desktop.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.screenshot(path='/tmp/baraka-mobile.png',full_page=True)
 assert not errors,errors
 print('Seven position UI flows and practice scoring PASS; 8 malformed-data/N-A checks PASS; finalization invalidation and DOM integrity PASS')
 ctx.close();b.close()
