from playwright.sync_api import sync_playwright
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium')
 context=browser.new_context(accept_downloads=True)
 context.set_offline(True)
 page=context.new_page(); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 # Managed Chromium blocks file: URLs; serve the single document from memory,
 # with the browser offline. No network assets are allowed or needed.
 page.route('http://127.0.0.1:8765/**',lambda route:route.fulfill(status=200,content_type='text/html',body=(ROOT/'INTERVIEW_BARAKA_FINAL.html').read_text()))
 page.goto('http://127.0.0.1:8765/INTERVIEW_BARAKA_FINAL.html')
 page.wait_for_selector('text=Penyimpanan lokal siap')
 assert page.get_by_text('Belum ada kandidat.',exact=False).count()==1
 # Every template, weighted arithmetic, legal/safety gates, snapshots and missing answers.
 result=page.evaluate('''()=>{let checks=0;for(const t of Object.values(DEFAULTS)){validateTemplate(t);const s=newSession(t);validateSession(s);let r=evaluate(s);if(r.total!==null||r.complete||r.status!=='Belum selesai dinilai')throw Error('empty');s.name='Uji';s.branch='Pontianak';s.interviewer='Penguji';s.template.vehicle='Kendaraan uji';s.template.license='Sesuai kendaraan, terverifikasi HRD';for(const q of t.questions)if(q.type==='dinilai')s.answers[q.id]={score:3,note:'Bukti',naReason:''};for(const g of t.requirements)s.gates[g.id]={status:'Memenuhi',note:'Bukti'};if(evaluate(s).status!=='Lanjut tes praktik')throw Error('practice gate');s.practice={scores:t.practice.checks.map(()=>3),done:true,supervised:true,examiner:'Penguji',note:'Teramati',documentation:'Hasil uji'};r=evaluate(s);if(!r.complete||Math.abs(r.total-75)>1e-8)throw Error('weighted 75 '+r.total);s.gates.identity.status='Belum memenuhi';if(evaluate(s).status!=='Belum memenuhi persyaratan wajib')throw Error('legal gate');s.gates.identity.status='Memenuhi';let q=t.questions.find(q=>q.type==='dinilai');s.answers[q.id].score=null;if(evaluate(s).interview!==null||evaluate(s).total!==null)throw Error('partial');s.answers[q.id].score=3;const snap=JSON.stringify(s.template);let edited=clone(t);edited.questions[0].text='Berubah';if(JSON.stringify(s.template)!==snap)throw Error('snapshot');const bad=clone(t);bad.categories[0].weight++;try{validateTemplate(bad);throw Error('accepted weight');}catch(e){if(e.message==='accepted weight')throw e;}checks+=7;}const s=newSession(DEFAULTS.tkbm);s.name='Safety';s.branch='A';s.interviewer='HR';for(const q of s.template.questions)if(q.type==='dinilai')s.answers[q.id]={score:4,note:'Bukti',naReason:''};for(const g of s.template.requirements)s.gates[g.id]={status:'Memenuhi',note:'Bukti'};s.practice={scores:[4,4,4,4],done:true,supervised:true,examiner:'X',note:'Bukti',documentation:'Hasil'};s.answers[s.template.questions.find(q=>q.critical).id].score=1;if(evaluate(s).status!=='Perlu pendalaman atau asesmen ulang')throw Error('critical hidden');checks++;return checks;}''')
 print('Domain assertions:',result)
 # Create and save through UI, score, notes, refresh and second candidate isolation.
 page.get_by_role('button',name='Interview Baru',exact=True).click()
 page.get_by_label('Posisi',exact=True).select_option('tkbm')
 page.get_by_role('button',name='Buat sesi interview',exact=True).click()
 page.get_by_label('Nama kandidat *',exact=True).fill('<img src=x onerror="window.xss=1"> Kandidat A')
 page.get_by_label('Cabang/lokasi *',exact=True).fill('Pontianak')
 page.get_by_label('Interviewer *',exact=True).fill('HRD')
 page.get_by_role('button',name='3 Interview',exact=True).click()
 page.get_by_text('Buka rubrik dan indikator',exact=True).click()
 assert page.get_by_text('Tetap memuat tanpa memberi tahu',exact=False).count()>0
 page.get_by_role('button',name='Nilai 3',exact=True).click()
 page.get_by_label('Catatan bukti jawaban kandidat',exact=True).fill('Melapor sebelum barang dimuat')
 page.get_by_role('button',name='Simpan manual',exact=True).click()
 page.wait_for_function('storageOK')
 first=page.evaluate('current.id')
 page.reload();page.wait_for_selector('text=Penyimpanan lokal siap')
 page.get_by_role('button',name='Riwayat Kandidat',exact=True).click()
 assert page.locator('img').count()==0
 page.get_by_role('button',name='Buka interview',exact=True).click()
 page.get_by_role('button',name='3 Interview',exact=True).click()
 assert page.get_by_label('Catatan bukti jawaban kandidat',exact=True).input_value()=='Melapor sebelum barang dimuat'
 assert page.get_by_role('button',name='Nilai 3',exact=True).get_attribute('aria-pressed')=='true'
 page.get_by_role('button',name='Dashboard',exact=True).click()
 page.get_by_role('button',name='Mulai interview',exact=True).click()
 page.get_by_label('Posisi',exact=True).select_option('driver_distribusi')
 page.get_by_role('button',name='Buat sesi interview',exact=True).click()
 assert page.get_by_label('Nama kandidat *',exact=True).input_value()==''
 assert page.evaluate('Object.keys(current.answers).length')==0
 page.get_by_label('Nama kandidat *',exact=True).fill('Kandidat B')
 page.get_by_role('button',name='Simpan manual',exact=True).click()
 # Edit draft retains input when adding/reordering/deleting; active session snapshot preserved.
 page.get_by_role('button',name='Bank Pertanyaan',exact=True).click()
 page.get_by_label('Posisi',exact=True).select_option('tkbm')
 old=page.evaluate('state.sessions.find(s=>s.id=== '+json.dumps(first)+').template.questions[0].text')
 page.get_by_label('Pertanyaan utama',exact=True).first.fill('Teks tersimpan <script>window.xss=1</script>')
 page.get_by_role('button',name='Tambah pertanyaan',exact=True).click()
 assert page.get_by_label('Pertanyaan utama',exact=True).first.input_value().startswith('Teks tersimpan')
 page.get_by_label('Pertanyaan utama',exact=True).last.fill('Pertanyaan informasi tambahan')
 page.get_by_label('Jenis',exact=True).last.select_option('informasi')
 page.get_by_role('button',name='Naik',exact=True).last.click()
 page.get_by_role('button',name='Validasi dan terapkan versi baru',exact=True).click()
 page.wait_for_function('state.templates.tkbm.version===2')
 assert page.evaluate('state.sessions.find(s=>s.id=== '+json.dumps(first)+').template.questions[0].text')==old
 # weight validation and correction
 page.get_by_role('button',name='Pengaturan Penilaian',exact=True).click()
 page.get_by_label('Bobot %',exact=True).first.fill('36')
 page.get_by_role('button',name='Validasi dan terapkan versi baru',exact=True).click()
 assert '100%' in page.locator('#notice').inner_text()
 page.get_by_label('Bobot %',exact=True).first.fill('35')
 page.get_by_role('button',name='Validasi dan terapkan versi baru',exact=True).click()
 page.wait_for_function('state.templates.tkbm.version===3')
 # backup actual browser download and reimport: no duplication.
 with page.expect_download() as d:page.get_by_role('button',name='Backup JSON',exact=True).click()
 backup=Path('/tmp/baraka-test-backup.json');d.value.save_as(backup)
 assert len(json.loads(backup.read_text())['sessions'])==2
 page.once('dialog',lambda dialog:dialog.accept())
 page.locator('#import').set_input_files(backup)
 page.wait_for_function('document.querySelector("#notice").textContent.includes("2 dilewati")')
 assert page.evaluate('state.sessions.length')==2
 bad=Path('/tmp/baraka-invalid.json');bad.write_text('{"schema":999}')
 page.locator('#import').set_input_files(bad)
 page.wait_for_function('document.querySelector("#notice").textContent.includes("Impor dibatalkan")')
 assert page.evaluate('state.sessions.length')==2
 with page.expect_download() as d:page.get_by_role('button',name='Export CSV',exact=True).click()
 csv=Path('/tmp/baraka-test.csv');d.value.save_as(csv);assert 'Kandidat B' in csv.read_text()
 # Cancel reset, then report draft and A4 PDF.
 page.once('dialog',lambda dialog:dialog.dismiss())
 page.get_by_role('button',name='Reset database',exact=True).click()
 assert page.evaluate('state.sessions.length')==2
 page.get_by_role('button',name='Laporan',exact=True).first.click()
 assert page.get_by_text('DRAFT — PENILAIAN BELUM LENGKAP',exact=True).count()==1
 page.pdf(path='/tmp/baraka-draft.pdf',format='A4',print_background=True)
 assert Path('/tmp/baraka-draft.pdf').stat().st_size>10000
 # responsive overflow and no injection; offline served no dependencies.
 for width in [1440,768,390]:
  page.set_viewport_size({'width':width,'height':900})
  assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),width
 assert page.evaluate('window.xss||0')==0
 # Complete through data model; render functional final report and verify persistence.
 page.evaluate('''async()=>{current=state.sessions[0];const s=current;s.name='Kandidat A';for(const q of s.template.questions)if(q.type==='dinilai')s.answers[q.id]={score:3,note:'Langkah aman sesuai simulasi',naReason:''};for(const g of s.template.requirements)s.gates[g.id]={status:'Memenuhi',note:'Bukti diverifikasi'};s.practice={scores:[3,3,3,3],done:true,supervised:true,examiner:'Penguji kompeten',note:'Seluruh langkah dasar benar',documentation:'Checklist simulasi'};await save();navigate('Interview Baru');step=4;render();}''')
 page.get_by_label('Alasan keputusan HRD',exact=True).fill('Bukti lengkap dan memenuhi ambang internal')
 page.get_by_label('Keputusan pihak berwenang',exact=True).select_option('Tahap berikutnya')
 page.get_by_role('button',name='Simpan keputusan final HRD',exact=True).click()
 page.wait_for_function('!!current.finalizedAt')
 page.get_by_role('button',name='Preview Laporan',exact=True).click()
 assert page.get_by_text('DRAFT — PENILAIAN BELUM LENGKAP',exact=True).count()==0
 page.pdf(path='/tmp/baraka-complete.pdf',format='A4')
 # accepted reset atomic and empty state
 page.once('dialog',lambda dialog:dialog.accept())
 page.get_by_role('button',name='Reset database',exact=True).click()
 page.wait_for_function('state.sessions.length===0')
 page.reload();page.wait_for_selector('text=Penyimpanan lokal siap')
 assert page.evaluate('state.sessions.length')==0
 assert errors==[],errors
 print('Browser: offline, create/refresh/isolation, rubrics, scores, editor/version, weights, JSON/CSV, invalid import, reset/cancel, XSS, responsive, finalization, draft/complete PDFs: PASS')
 context.close();browser.close()
