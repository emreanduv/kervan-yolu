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
if T.upper()=='HEMEN':
    # onaylanmış sürümü hemen yayına al: yayın biçimi elle (MANUAL) yapılır, sonra yayın isteği gönderilir
    st=v['attributes']['appStoreState']
    if st=='READY_FOR_SALE': print('Zaten yayında'); raise SystemExit(0)
    if v['attributes'].get('releaseType')!='MANUAL':
        r=requests.patch(B+f"/v1/appStoreVersions/{v['id']}",headers=H(),json={'data':{'type':'appStoreVersions','id':v['id'],'attributes':{'releaseType':'MANUAL','earliestReleaseDate':None}}});print('MANUAL',r.status_code,r.text[:500])
    for k in range(10):
        st=requests.get(B+f"/v1/appStoreVersions/{v['id']}",headers=H()).json()['data']['attributes']['appStoreState'];print('durum',st)
        if st=='PENDING_DEVELOPER_RELEASE':break
        time.sleep(15)
    r=requests.post(B+'/v1/appStoreVersionReleaseRequests',headers=H(),json={'data':{'type':'appStoreVersionReleaseRequests','relationships':{'appStoreVersion':{'data':{'type':'appStoreVersions','id':v['id']}}}}})
    print('YAYIN İSTEĞİ',r.status_code,r.text[:600])
    if r.status_code>=400: raise SystemExit(1)
    time.sleep(20);print('SONUÇ',requests.get(B+f"/v1/appStoreVersions/{v['id']}",headers=H()).json()['data']['attributes']['appStoreState']);raise SystemExit(0)
r=requests.patch(B+f"/v1/appStoreVersions/{v['id']}",headers=H(),json={'data':{'type':'appStoreVersions','id':v['id'],'attributes':{'releaseType':'SCHEDULED','earliestReleaseDate':T}}})
print(r.status_code,r.text[:600])
if r.status_code>=400: raise SystemExit(1)
v=requests.get(B+f"/v1/appStoreVersions/{v['id']}",headers=H()).json()['data']['attributes']
print('SONUÇ',v.get('releaseType'),v.get('earliestReleaseDate'))
