#!/usr/bin/env python3
"""TestFlight: son derlemeyi bekle, dış test grubunu kur, testçileri ekle, derlemeyi ver, Beta incelemesine gönder."""
import os, time, jwt, requests
B='https://api.appstoreconnect.apple.com/v1'
APP=os.environ['APP_ID']; GRUP='Mr. Anduv! Testçileri'
def H():
    t=jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+900,'aud':'appstoreconnect-v1'},os.environ['P8'],algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
    return {'Authorization':'Bearer '+t,'Content-Type':'application/json'}
def get(p,**q):
    r=requests.get(B+p,headers=H(),params=q); r.raise_for_status(); return r.json()
def post(p,body):
    r=requests.post(B+p,headers=H(),json=body)
    if r.status_code>=400: print('!',p,r.status_code,r.text[:600])
    return r
def patch(p,body):
    r=requests.patch(B+p,headers=H(),json=body)
    if r.status_code>=400: print('!',p,r.status_code,r.text[:600])
    return r
# 1) son derleme işlensin
build=None
MIN=int(os.environ.get('MIN_BUILD') or (open('store/DERLEME').read().strip() if os.path.exists('store/DERLEME') else 0) or 0)
print('beklenen derleme no ≥',MIN)
for i in range(70):
    d=get('/builds',**{'filter[app]':APP,'sort':'-uploadedDate','limit':1})['data']
    if d and int(d[0]['attributes']['version'])<MIN: print('derleme',MIN,'henüz görünmüyor'); time.sleep(60); continue
    if d:
        st=d[0]['attributes']['processingState']; print('derleme',d[0]['attributes']['version'],st)
        if st=='VALID': build=d[0]; break
        if st in ('FAILED','INVALID'): raise SystemExit('Derleme işlenemedi: '+st)
    time.sleep(60)
if not build: raise SystemExit('Derleme 70 dakikada işlenmedi')
bid=build['id']
# 2) ihracat uyumu (şifreleme yok)
if build['attributes'].get('usesNonExemptEncryption') is None:
    patch(f'/builds/{bid}',{'data':{'type':'builds','id':bid,'attributes':{'usesNonExemptEncryption':False}}})
# 3) test bilgileri (Malazgirt'ten iletişim bilgisi kopyala)
src=get('/apps',**{'filter[bundleId]':os.environ['KAYNAK_BUNDLE']})['data']
if src:
    try:
        sd=get(f"/apps/{src[0]['id']}/betaAppReviewDetail")['data']['attributes']
        md=get(f'/apps/{APP}/betaAppReviewDetail')['data']
        at={k:sd.get(k) for k in ('contactFirstName','contactLastName','contactPhone','contactEmail')}
        at.update({'demoAccountRequired':False,'notes':'Tek kişilik, çevrimdışı tır simülasyonu (rüzgâr türbini lojistiği). Hesap/giriş yok. Sağda GAZ ve FREN pedalları, solda direksiyon okları. İlk 3 sefer ücretsiz.'})
        patch(f"/betaAppReviewDetails/{md['id']}",{'data':{'type':'betaAppReviewDetails','id':md['id'],'attributes':at}})
    except Exception as e: print('iletişim kopyalanamadı:',e)
    try:
        sl=get(f"/apps/{src[0]['id']}/betaAppLocalizations")['data']
        ml={x['attributes']['locale']:x for x in get(f'/apps/{APP}/betaAppLocalizations')['data']}
        for s in sl:
            loc=s['attributes']['locale']; a={'feedbackEmail':s['attributes'].get('feedbackEmail'),'description':'Kervan Yolu: tırla limandan rüzgâr sahasına kule, kanat, nasel ve yedek parça taşı; dört bölge, kanat kaldırıcı, kar zinciri, yan rüzgâr, forklift, drone ile hasar tespiti, 1923 sefer.'}
            if loc in ml: patch(f"/betaAppLocalizations/{ml[loc]['id']}",{'data':{'type':'betaAppLocalizations','id':ml[loc]['id'],'attributes':a}})
            else: post('/betaAppLocalizations',{'data':{'type':'betaAppLocalizations','attributes':dict(a,locale=loc),'relationships':{'app':{'data':{'type':'apps','id':APP}}}}})
    except Exception as e: print('yerelleştirme kopyalanamadı:',e)
# 4) "Neyi test etmeli"
for loc,txt in [('tr','YENİ (17): Takograf (4,5 saat sürüş, dinlenme tesisinde 45 dk mola, ihlalde ceza) ve kanat seferinde 15 m/s üstü rüzgârda limanda bekleme. (16): Limanda gemiden tahliye, gümrük muayenesi, sefer evrakı (izin belgesi, kullanım bedeli, yol düzenlemesi protokolü) ve çıkış kapısı; Egede aktarma sahasında vinçle blade liftera aktarma; raporda kalem kalem masraf. (15): Uzun yükte (kanat, kule) arkada da eskort aracı. (14): Kanat taşıması gerçeğe uygun: 72 m kanat, uzayan dorse, uç çerçevesi, kendi dönen arka boji; Ege köyünde kanat kalkınca dorse içeri kayar. Virajlarda kanadın ucunun nereden geçtiğine bakın. Mr. Anduv! FM. Ana menüde açılış teması (Kervan Dönüyor); kabinde FM düğmesiyle radyo: dokun aç/kapat, basılı tut sonraki şarkı. 12 şarkı internetsiz, internet varken 123 şarkının hepsi. Uyarı gelince müzik kısılıyor mu, başka uygulamadan dönünce müzik sürüyor mu, Ayarlardaki müzik sesi çalışıyor mu bakın. Dört bölge: Marmara, Ege (dar köy sokağında kanat kaldırıcı, ardından enerji hattı), İç Anadolu/Sivas (buzlu yol, mavi halkada kar zinciri), Trakya (yan rüzgâr ve rüzgâr göstergesi). Yeni yükler: nasel, hub, güç aktarma, ankraj kafesi, malzeme konteyneri. Yeni: hız sınırları ve EDS, karşı trafik ve sağ şerit kuralı, geniş yükte eskort aracı, üretici etiketleri ve saha tabelaları. Serbest Sürüş\'te bölge seç; uyarıların ne yapacağını söyleyip söylemediğine, yatay ve dikey ekrana bakın.'),('en-US','NEW (17): Tachograph (4.5 h driving, 45 min break at the rest area, fine if broken) and blade jobs waiting at port in winds over 15 m/s. (16): Ship discharge, customs inspection, trip permits and the port exit gate; blade lifter transfer by crane on the Aegean route; itemised costs in the report. (15): Rear escort vehicle for long loads (blade, tower). (14): Realistic blade haul: 72 m blade, extendable trailer, tip frame, self-steering rear bogie; the trailer retracts when the blade is lifted in the Aegean village. Mr. Anduv! FM. Opening theme on the main menu; in-cab radio via the FM button: tap on/off, hold for next song. 12 songs offline, all 123 online. Four regions: Marmara, Aegean (blade lifter in a narrow village street, then a power line), Central Anatolia/Sivas (icy road, snow chains in the blue ring), Thrace (crosswind and wind gauge). New loads: nacelle, hub, drive train, anchor cage, material container. New: speed limits and speed cameras, oncoming traffic and keep-right rule, escort vehicle for wide loads, manufacturer labels and site signs. Pick a region in Free Drive; check that every warning tells you what to do, in landscape and portrait.')]:
    ex=[x for x in get(f'/builds/{bid}/betaBuildLocalizations')['data'] if x['attributes']['locale']==loc]
    if ex: patch(f"/betaBuildLocalizations/{ex[0]['id']}",{'data':{'type':'betaBuildLocalizations','id':ex[0]['id'],'attributes':{'whatsNew':txt}}})
    else: post('/betaBuildLocalizations',{'data':{'type':'betaBuildLocalizations','attributes':{'locale':loc,'whatsNew':txt},'relationships':{'build':{'data':{'type':'builds','id':bid}}}}})
# 5) dış grup
g=[x for x in get(f'/apps/{APP}/betaGroups')['data'] if x['attributes']['name']==GRUP]
if g: gid=g[0]['id']
else:
    r=post('/betaGroups',{'data':{'type':'betaGroups','attributes':{'name':GRUP,'publicLinkEnabled':False},'relationships':{'app':{'data':{'type':'apps','id':APP}}}}}); r.raise_for_status(); gid=r.json()['data']['id']
print('grup',gid)
# 6) testçiler
var={t['attributes']['email'].lower() for t in get(f'/betaGroups/{gid}/betaTesters',limit=200)['data']}
for e in open('store/testflight-testciler.txt').read().split():
    if e.lower() in var: print('✓ zaten var',e); continue
    r=post('/betaTesters',{'data':{'type':'betaTesters','attributes':{'email':e},'relationships':{'betaGroups':{'data':[{'type':'betaGroups','id':gid}]}}}})
    print('testçi',e,r.status_code)
# 6b) dahili test (Emre'nin kuralı, 22 Kas 2026): emreanduv@hotmail.com her üründe varsayılan dahili testçi;
#     dahili grup Apple beta incelemesini beklemez, derleme işlenir işlenmez telefona düşer
IC='Mr. Anduv! İç Test'; IC_MAIL='emreanduv@hotmail.com'
try:
    ig=[x for x in get(f'/apps/{APP}/betaGroups')['data'] if x['attributes'].get('isInternalGroup')]
    if ig: igid=ig[0]['id']
    else:
        r=post('/betaGroups',{'data':{'type':'betaGroups','attributes':{'name':IC,'isInternalGroup':True,'hasAccessToAllBuilds':True},'relationships':{'app':{'data':{'type':'apps','id':APP}}}}})
        igid=r.json()['data']['id'] if r.status_code<400 else None
    if igid:
        iv={t['attributes']['email'].lower() for t in get(f'/betaGroups/{igid}/betaTesters',limit=200)['data']}
        if IC_MAIL not in iv:
            r=post('/betaTesters',{'data':{'type':'betaTesters','attributes':{'email':IC_MAIL,'firstName':'Emre','lastName':'Anduv'},'relationships':{'betaGroups':{'data':[{'type':'betaGroups','id':igid}]}}}})
            print('dahili testçi',IC_MAIL,r.status_code)
        post(f'/betaGroups/{igid}/relationships/builds',{'data':[{'type':'builds','id':bid}]})
        print('✓ dahili grup',igid)
except Exception as e: print('dahili grup kurulamadı:',e)
# 7) derlemeyi gruba ver + incelemeye gönder
post(f'/betaGroups/{gid}/relationships/builds',{'data':[{'type':'builds','id':bid}]})
# Aynı sürümde başka derleme beta incelemesindeyse (ANOTHER_BUILD_IN_REVIEW) o bitene kadar bekle ve yeniden dene
for den in range(13):
    r=post('/betaAppReviewSubmissions',{'data':{'type':'betaAppReviewSubmissions','relationships':{'build':{'data':{'type':'builds','id':bid}}}}})
    print('beta incelemesi',r.status_code)
    if r.status_code<400 or 'ANOTHER_BUILD_IN_REVIEW' not in r.text: break
    print('önceki derleme incelemede; 5 dk sonra yeniden…'); time.sleep(300)
print('✓ Bitti: derleme',build['attributes']['version'],'→',GRUP)
