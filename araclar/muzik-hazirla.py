#!/usr/bin/env python3
"""Mr. Anduv! FM: şarkı klasörünü oyuna hazırlar.

    python3 araclar/muzik-hazirla.py <şarkı klasörü> [--paket 12] [--acilis "Ruhunu Bağla"] [--uzak URL] [--uzak-cikti dizin]

- Her şarkıyı -14 LUFS'a eşitler (mağaza/oyun düzeyi), AAC 96 kb/s stereo .m4a yapar.
- İlk --paket kadar şarkı uygulamanın içine (www/muzik/parca/) girer; uygulama boyu makul kalır.
- Geri kalanlar --uzak-cikti dizinine yazılır (GitHub Pages: emreanduv.github.io/muzik/);
  oyun çevrimiçiyken onları da radyoya katar.
- www/muzik/liste.json'u yazar. Açılış teması: --acilis adına en çok benzeyen şarkının ilk 75 sn'si, yumuşak bitişli döngü.
Sıra: dosya adında öne "01-", "02-" varsa ona göre; yoksa alfabetik.
"""
import argparse, json, os, re, subprocess, sys, unicodedata, difflib

UZANTI = ('.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.aiff', '.aif')
TR = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosuCGIOSU')


def slug(s):
    s = s.translate(TR)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') or 'parca'


def ad(dosya):
    b = os.path.splitext(os.path.basename(dosya))[0]
    b = re.sub(r'^\d+\s*[-_.)]\s*', '', b)                     # "01 - " sıra öneki
    b = re.sub(r'\s*[\[(](official|audio|master|final|v\d+)[^\])]*[\])]', '', b, flags=re.I)
    b = re.sub(r'^mr\.?\s*anduv!?\s*[-–—:]\s*', '', b, flags=re.I)
    return b.replace('_', ' ').strip()


def donustur(kaynak, hedef, ss=None, t=None, dongu=False):
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    af = 'loudnorm=I=-14:TP=-1.5:LRA=11'
    if dongu:
        af = f'afade=t=in:d=1.5,afade=t=out:st={t - 4}:d=4,' + af
    cmd = ['ffmpeg', '-y', '-loglevel', 'error']
    if ss is not None:
        cmd += ['-ss', str(ss)]
    cmd += ['-i', kaynak]
    if t is not None:
        cmd += ['-t', str(t)]
    cmd += ['-vn', '-map_metadata', '-1', '-af', af, '-ac', '2', '-ar', '44100', '-c:a', 'aac', '-b:a', '96k',
            '-movflags', '+faststart', hedef]
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('kaynak')
    p.add_argument('--paket', type=int, default=12)
    p.add_argument('--acilis', default='Ruhunu Bağla')
    p.add_argument('--uzak', default='https://emreanduv.github.io/muzik/')
    p.add_argument('--uzak-cikti', default='')
    p.add_argument('--www', default=os.path.join(os.path.dirname(__file__), '..', 'www'))
    a = p.parse_args()

    dosyalar = sorted(os.path.join(k, f) for k, _, fs in os.walk(a.kaynak) for f in fs
                      if f.lower().endswith(UZANTI) and not f.startswith('.'))
    if not dosyalar:
        sys.exit('Şarkı bulunamadı: ' + a.kaynak)
    adlar = [ad(f) for f in dosyalar]
    print(f'{len(dosyalar)} şarkı bulundu.')

    muz = os.path.join(a.www, 'muzik')
    parca_dir = os.path.join(muz, 'parca')
    os.makedirs(parca_dir, exist_ok=True)
    for f in os.listdir(parca_dir):
        os.remove(os.path.join(parca_dir, f))

    yakin = difflib.get_close_matches(a.acilis.lower(), [x.lower() for x in adlar], 1, 0.3)
    ai = [x.lower() for x in adlar].index(yakin[0]) if yakin else 0
    donustur(dosyalar[ai], os.path.join(parca_dir, 'acilis.m4a'), ss=0, t=75, dongu=True)
    print('Açılış teması:', adlar[ai])

    liste = {'acilis': 'parca/acilis.m4a', 'parcalar': [], 'uzak': a.uzak if a.uzak_cikti else '', 'uzakParcalar': []}
    goruldu = set()
    for i, (f, n) in enumerate(zip(dosyalar, adlar)):
        s = slug(n)
        while s in goruldu:
            s += '-2'
        goruldu.add(s)
        if i < a.paket:
            donustur(f, os.path.join(parca_dir, s + '.m4a'))
            liste['parcalar'].append({'d': 'parca/' + s + '.m4a', 'ad': n})
        elif a.uzak_cikti:
            donustur(f, os.path.join(a.uzak_cikti, s + '.m4a'))
            liste['uzakParcalar'].append({'d': s + '.m4a', 'ad': n})
        print(f'  [{i + 1}/{len(dosyalar)}] {n}')
    with open(os.path.join(muz, 'liste.json'), 'w', encoding='utf-8') as fp:
        json.dump(liste, fp, ensure_ascii=False, indent=1)
    boy = sum(os.path.getsize(os.path.join(parca_dir, x)) for x in os.listdir(parca_dir)) / 1e6
    print(f'Uygulamaya giren: {len(liste["parcalar"])} şarkı + açılış, {boy:.1f} MB; uzakta: {len(liste["uzakParcalar"])}.')


if __name__ == '__main__':
    main()
