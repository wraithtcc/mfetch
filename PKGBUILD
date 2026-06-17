# Maintainer: rxlok <madql@tuta.io>
pkgname=mfetch
pkgver=1.0.0
pkgrel=1
pkgdesc="A minimal system info tool written in Python"
arch=('any')
url="https://github.com/larprxlokm/mfetch"
license=('MIT')
depends=('python')
optdepends=('pciutils: GPU detection via lspci'
            'mesa-utils: GPU fallback via glxinfo')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$pkgname-$pkgver"
    install -Dm755 mfetch "$pkgdir/usr/bin/mfetch"
    install -dm755 "$pkgdir/usr/share/mfetch/ascii"
    cp ascii/*.txt "$pkgdir/usr/share/mfetch/ascii/"
}
