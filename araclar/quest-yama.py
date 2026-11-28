#!/usr/bin/env python3
"""Capacitor Android projesini Meta Horizon Store (Quest, 2D panel uygulaması) için uyarlar.

Meta, web uygulaması (PWA/TWA) paketlerini yalnız ücretsiz satıyor; Kervan Yolu Quest'te 1,99 $ tam oyun
olduğu için doğal Android paketi gerekir. Meta'nın sürüm bildirimi şartları
(developers.meta.com/vr/distribute/publish-mobile-manifest):
  minSdk 29-34, targetSdk 34, allowBackup false (Quest'te Google yedeği yok; Meta güvenlik testi uyarıyor), installLocation auto, başlatıcı etkinlikte excludeFromRecents,
  com.oculus.supportedDevices, 2D uygulamada headtracking required=false.
Kullanım: python3 araclar/quest-yama.py android
"""
import re
import sys
from pathlib import Path

PAKET = "com.anduv.kervanyolu.vr"
CIHAZ = "quest2|questpro|quest3|quest3s|vrglasses"

kok = Path(sys.argv[1] if len(sys.argv) > 1 else "android")

g = kok / "app" / "build.gradle"
t = g.read_text()
t, n = re.subn(r'applicationId "[^"]+"', f'applicationId "{PAKET}"', t)
assert n == 1, "applicationId bulunamadı"
g.write_text(t)

v = kok / "variables.gradle"
t = v.read_text()
t, a = re.subn(r"minSdkVersion = \d+", "minSdkVersion = 29", t)
t, b = re.subn(r"targetSdkVersion = \d+", "targetSdkVersion = 34", t)
assert a == 1 and b == 1, "SDK sürümleri bulunamadı"
v.write_text(t)

m = kok / "app" / "src" / "main" / "AndroidManifest.xml"
t = m.read_text()
if "installLocation" not in t:
    t = t.replace(
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">',
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:installLocation="auto">', 1)
if "com.oculus.supportedDevices" not in t:
    t = t.replace("<activity", f'<meta-data android:name="com.oculus.supportedDevices" android:value="{CIHAZ}" />\n        <activity', 1)
if "excludeFromRecents" not in t:
    t = t.replace('android:name=".MainActivity"', 'android:name=".MainActivity"\n            android:excludeFromRecents="true"', 1)
if "android.hardware.vr.headtracking" not in t:
    t = t.replace("</manifest>", '    <uses-feature android:name="android.hardware.vr.headtracking" android:required="false" android:version="1" />\n</manifest>', 1)
t = t.replace('android:allowBackup="true"', 'android:allowBackup="false"')
for yasak in ("com.android.vending.BILLING", "android.permission.POST_NOTIFICATIONS", "android.permission.SCHEDULE_EXACT_ALARM"):
    t = re.sub(r'\s*<uses-permission android:name="' + re.escape(yasak) + r'"\s*/>', "", t)
m.write_text(t)

for kosul in ("installLocation", "com.oculus.supportedDevices", "excludeFromRecents", "android.hardware.vr.headtracking"):
    assert kosul in t, kosul + " eklenemedi"
print("Quest uyarlaması tamam:", PAKET)
print(t)
