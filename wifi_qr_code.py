import qrcode

# stole most of this from wifi_qrcode-generator module
# the make_wifi_code function allows the size of the qr code to be changed 

def wifi_code(ssid, hidden, authentication_type, password=None):
    """Generate a wifi code for the given parameters
    
    :ssid str: SSID
    :hidden bool: Specify if the network is hidden
    :authentication_type str: Specify the authentication type. Supported types: WPA, WEP, nopass
    :password Optional[str]: Password. Not required if authentication type is nopass
    
    :return: The wifi code for the given parameters
    :rtype: str
    """
    hidden = 'true' if hidden else 'false'
    if authentication_type in ('WPA', 'WEP'):
        if password is None:
            raise TypeError('For WPA and WEP, password should not be None.')
        return 'WIFI:T:{type};S:{ssid};P:{password};H:{hidden};;'.format(
            type=authentication_type, ssid=ssid, password=password, hidden=hidden
        )
    elif authentication_type == 'nopass':
        if password is not None:
            raise TypeError('For nopass, password should be None.')
        return 'WIFI:T:nopass;S:{ssid};H:{hidden};;'.format(
            ssid=ssid, hidden=hidden
        )
    raise ValueError('Unknown authentication_type: {!r}'.format(authentication_type))


def make_wifi_code(ssid, hidden, authentication_type, password=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=0,
    )
    qr.add_data(wifi_code(ssid, hidden, authentication_type, password))
    qr.make(fit=True)

    img = qr.make_image()
    img.save(f'{ssid}_qr.png')
    return img
