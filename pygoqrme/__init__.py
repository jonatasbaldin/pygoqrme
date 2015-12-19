"""
Small API to create QR-Codes from gorq.me
APIs documentatation: http://goqr.me/api/
"""
import requests, re, os
from urllib.parse import quote

class Api(object):
    """
    Main class
    """

    def __init__(self):
            """
        Just sets an url regex validator
        """

        # Django's Validator (modified)
        self.url_regex = re.compile(
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def create(self, data, size='200x200', fmt='png'):
        """
        Creates the QRCode, using some parameters available in goqr.me
        Parameters:
        data: the data to create qrcode, this library supports just text or urls
        size: string to identify the size
        fmt: identifies the output file format
        """
        self.data = data
        self.size = size
        self.fmt = fmt

        # test if its url
        # and if it is, encoded it
        data_url = re.findall(self.url_regex, data)
        if data_url.__len__() != 0:
            data = quote(data)

        # makes the request
        url = 'https://api.qrserver.com/v1/create-qr-code/?data={}&size={}&format={}'.format(
            data, size, fmt)
        qr_request = requests.get(url)
        self.qrcode = qr_request.content

        return self.qrcode

    def save(self, filename):
        """
        Saves the QRCode to a file
        Parameters:
        filename: file to be saved, if it has no extensions, automatically adds it
        """
        # if file has no extension, add extension to it
        if not os.path.splitext(filename)[-1]:
            filename = filename + '.' + self.fmt

        # writes qrcode to file
        with open(filename, 'bw') as f:
            f.write(self.qrcode)
