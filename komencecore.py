import socket, time, re, requests
from datetime import datetime, timezone
from regex import E, P, Regex

TIMEOUT = 1 
PORT = 443  
IPV4REGEX = r'[0-9]'

tcp_endpoints = [
    "www.google.com",
    "www.github.com",
    "www.lumen.com",
    "www.slack.com",
    "www.microsoft.com"
]

download_endpoints = {
    '1GB' : 'http://ipv4.download.thinkbroadband.com/1GB.zip',
    '512MB' : 'http://ipv4.download.thinkbroadband.com/512MB.zip',
    '200MB' : 'http://ipv4.download.thinkbroadband.com/200MB.zip',
    '100MB' : 'http://ipv4.download.thinkbroadband.com/100MB.zip',
    '50MB' : 'http://ipv4.download.thinkbroadband.com/50MB.zip',
    '20MB' : 'http://ipv4.download.thinkbroadband.com/20MB.zip',
    '10MB' : 'http://ipv4.download.thinkbroadband.com/10MB.zip',
    '5MB' : 'http://ipv4.download.thinkbroadband.com/5MB.zip'
}

def getIsoStamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    utcDt = dt.replace(tzinfo=timezone.utc)
    return datetime.isoformat(utcDt)

def resolveHost(host: str) -> bool:
        try:
            ip = socket.gethostbyaddr(host)
            return True
        except Exception:
            return False

def getIpInfo(data: str) -> str:
    trimStr = 3
    match data:
        case 'ip':
            url = 'https://ipinfo.io/ip'
            trimStr = 1
        case 'isp':
            url = 'https://ipinfo.io/org'
        case 'region':
            url = 'https://ipinfo.io/region'
        case 'city':
            url = 'https://ipinfo.io/city'
        case 'country':
            url = 'https://ipinfo.io/country'
        case __:
            url = 'https://ipinfo.io/ip'
            trimStr = 1
    ispTest = requests.get(url)
    return str(str(ispTest.content)[2:(len(str(ispTest.content))-trimStr)])

def tcpSockTest(host: str, port: int) -> dict:
    if re.search(IPV4REGEX,host) is None:
        if resolveHost(host) is False:
            return {
            'HOST' : host,
            'PORT' : port,
            'TIME' : "10000",
            'TIMESTAMP' : getIsoStamp(datetime.timestamp(datetime.now())),
            'RESULT' : "Failed to Resolve Host"
            }
    testStart = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    results = sock.connect_ex((host,port))
    rttTime = round((time.time() - testStart) * 1000,2)
    return {
    'ISP' : getIpInfo('isp'),
    'HOST' : host,
    'PORT' : port,
    'TIME' : rttTime,
    'TIMESTAMP' : getIsoStamp(datetime.timestamp(datetime.now())),
    'RESULT' : results
    }

def getDownSpeed(url: str) -> dict:
    testStart = time.time()
    download = requests.get(url)
    downloadTime = round((time.time() - testStart),2)
    return {
        'SIZE' : (len(download.content) / 1.049e+6),
        'URL' : url,
        'TIME' : downloadTime,
        'SPEED' : round(((len(download.content) / 1.049e+6) / downloadTime) * 10, 2),
        'TIMESTAMP' : getIsoStamp(datetime.timestamp(datetime.now())),
        'ISP' : getIpInfo('isp')
    }