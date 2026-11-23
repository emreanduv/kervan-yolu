#!/usr/bin/env python3
"""App Store sürümünün yayın biçimini ayarlar: onaydan sonra, en erken TARIH'te (store/YAYIN-TARIHI, ISO 8601, ör. 2026-11-28T07:00:00+00:00)."""
import os, time, jwt, requests
B='https://api.appstoreconnect.apple.com'
APP=os.environ['APP_ID']; SURUM=os.environ['SURUM']; T=open('store/YAYIN-TARIHI').read().strip()
def H():
    t=jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+900,'aud':'appstoreconnect-v1'},os.environ['P8'],algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
    return {'Authorization':'Bearer '+t,'Content-Type':'application/json'}
v=requests.get(B+f'/v1/apps/{APP}/appStoreVersions',headers=H(),params={'filter[platform]':'IOS','filter[versionString]':SURUM}).json()['data'][0]
print('sürüm',SURUM,v['attributes']['appStoreState'],v['attributes'].get('releaseType'),v['attributes'].get('earliestReleaseDate'))
r=requests.patch(B+f"/v1/appStoreVersions/{v['id']}",headers=H(),json={'data':{'type':'appStoreVersions','id':v['id'],'attributes':{'releaseType':'SCHEDULED','earliestReleaseDate':T}}})
print(r.status_code,r.text[:600])
if r.status_code>=400: raise SystemExit(1)
v=requests.get(B+f"/v1/appStoreVersions/{v['id']}",headers=H()).json()['data']['attributes']
print('SONUÇ',v.get('releaseType'),v.get('earliestReleaseDate'))
