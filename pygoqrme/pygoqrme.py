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

    def __init__(self,
        size='200x200',
        charset_source='UTF-8',
        charset_target='UTF-8',
        ecc='L',
        color='0-0-0',
        bgcolor='255-255-255',
        margin=1,
        qzone=0,
        fmt='png'):
        """
        Define common parameters to all QRCode types
        """

        self.size = size
        self.charset_source = charset_source
        self.charset_target = charset_target
        self.ecc = ecc
        self.color = color
        self.bgcolor = bgcolor
        self.margin = margin
        self.qzone = qzone
        self.fmt = fmt

    def text(self, text):
        """
        Creates QRCode with simple text
        Parameters:
        data: text to be created
        """

        return self.req(text)

    def url(self, url):
        """
        Creates QRCode with url
        Parameters:
        url: url to be created
        """

        # Django's Validator (modified)
        url_regex = re.compile(
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # test if its url
        # and if it is, encoded it
        data_url = re.findall(url_regex, url)
        if data_url.__len__() != 0:
            url = quote(url)
        else:
            return 'Inavlid URL'

        return self.req(url)

    def wifi(self, ssid, security, password):
        """
        Creates QRCode to WiFi connection
        Parameters:
        ssid: wifi connection name
        security: wifi security, WEP or WPA
        password: wifi password
        """

        data = 'WIFI:S:{};T:{};P:{};;'.format(ssid, security, password)

        return self.req(data)

    def geo(self, latitude, longitude, distance):
        """
        Creates QRCode with geolocation
        Parameters:
        latitude: specifies latitude
        longitude: specifies longitude
        distance: specifies distance to map
        """

        data = 'geo:{},{},{}'.format(latitude, longitude, distance)

        return self.req(data)

    def call(self, phone):
        """
        Creates QRCode with a number to call
        Parameters:
        phone: number to call
        """

        data = 'tel:{}'.format(phone)

        return self.req(data)

    def sms(self, phone, message=''):
        """
        Creates QRCode with message to be sent via sms
        Parameters:
        phone: number to send
        message: sms message to send
        """

        data = 'SMSTO:{}:{}'.format(phone, message)

        return self.req(data)

    def mail(self, email, subject, body):
        """
        Creates QRCode to send an email
        Parameters:
        email: destination email
        subject: email subject
        body: email body
        """

        data = 'mailto:{}?subject={}&body={}'.format(email, subject, body)

        return self.req(data)

    def save(self, filename):
        """
        Saves the QRCode to a file
        Parameters:
        filename: file to be saved, if it has no extensions,
            automatically adds it
        """
        # if file has no extension, add extension to it
        if not os.path.splitext(filename)[-1]:
            filename = filename + '.' + self.fmt

        # writes qrcode to file
        with open(filename, 'bw') as f:
            f.write(self.qrcode)

    def req(self, data):
        """
        Makes the requests
        Parameters:
        data: data to be sent to goqr.me
        """
        url = 'https://api.qrserver.com/v1/create-qr-code/?data={}&size={}&charset-source={}&charset_target={}&ecc={}&color={}&bgcolor={}&margin={}&qzone={}&format={}'.format(
            data, self.size, self.charset_source, self.charset_target, self.ecc, self.color, self.bgcolor, self.margin, self.qzone, self.fmt)
        qr_request = requests.get(url)
        self.qrcode = qr_request.content

        return self.qrcode
