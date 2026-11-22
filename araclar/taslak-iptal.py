#!/usr/bin/env python3
"""Gönderilmemiş (taslak) inceleme başvurusunu iptal eder: sürüm yeniden düzenlenebilir olur. Gönderilmiş başvuruya dokunmaz."""
import os, time, jwt, requests
B='https://api.appstoreconnect.apple.com'
APP=os.environ['APP_ID']; SURUM=os.environ['SURUM']
def H():
    t=jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+900,'aud':'appstoreconnect-v1'},os.environ['P8'],algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
    return {'Authorization':'Bearer '+t,'Content-Type':'application/json'}
def get(p,**q):
    r=requests.get(B+p,headers=H(),params=q); r.raise_for_status(); return r.json()
def send(m,p,body=None):
    r=requests.request(m,B+p,headers=H(),json=body)
    ok=r.status_code<400; print(('✓' if ok else '✗'),m,p,r.status_code,'' if ok else r.text[:800]); return r
for st in ('READY_FOR_REVIEW',):
    for x in get('/v1/reviewSubmissions',**{'filter[app]':APP,'filter[platform]':'IOS','filter[state]':st})['data']:
        for it in get(f"/v1/reviewSubmissions/{x['id']}/items")['data']:
            send('DELETE',f"/v1/reviewSubmissionItems/{it['id']}")
time.sleep(8)
v=get(f'/v1/apps/{APP}/appStoreVersions',**{'filter[platform]':'IOS','filter[versionString]':SURUM})['data']
print('sürüm',SURUM,v and v[0]['attributes']['appStoreState'])
