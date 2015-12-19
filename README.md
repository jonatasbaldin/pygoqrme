# pygoqrme #

Very simple Python library for create QR Code from [goqr.me](http://goqr.me/)            
I just developed what I needed, but I would appreciate contributors to make it a full library.
Tested on Python3.

## Examples

```python
import pygoqrme
qr = pygoqrme.Api()
qr.create("I'm just some text who needs a QRCode!")
qr.save('qrtext.png')
```
