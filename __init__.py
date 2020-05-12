import requests

class   DownloadStation():
    def __init__( self, ip, login, password ):
        self.ip = ip
        self.login = login
        self.password = password
        self.cookies = None
        self.sid = None
        self.token = '--------' 
        self.session = None
    def connect( self ):
        data = { 'api': 'SYNO.API.Auth',
                 'version': '2',
                 'method': 'login',
                 'account': self.login,
                 'passwd': self.password,
                 'session': 'DownloadStation',
                 'format': 'sid'
                }
        r = requests.post( url='http://{}/webapi/auth.cgi'.format( self.ip ), data=data, verify=False )
        if r.status_code != 200:
            return False
        if not r.json()['success']:
            return False
        self.sid = r.json()['data']['sid']
        self.session = requests.session()
        return True
       
    def disconnect( self ):
        data = { 'api': 'SYNO.API.Auth',
                 'version': '1',
                 'method': 'logout',
                 'session': 'DownloadStation',
               }
        r = self.session.post( url='http://{}/webapi/auth.cgi'.format( self.ip ), data=data, verify=False )
        if r.status_code != 200:
            return False
        if not r.json()['success']:
            return False
        return True

    def give_url( self, url ):
        data = {
            'api': 'SYNO.DownloadStation.Task',
            'version': '1',
            'method': 'create',
            'session': 'DownloadStation',
            '_sid': self.sid,
            'uri': url
        }
        r = self.session.post( 'http://{}/webapi/DownloadStation/task.cgi'.format( self.ip ), data=data, verify=False)
        print(r.url)
        print(r.content)
        if r.status_code != 200:
            print('[ERROR] Load URL torrent file fail.') 
            return False
        if not r.json()['success']:
            print('[ERROR] Load URL torrent response fail.') 
            return False
        return True

    def give_file( self, filename ):
        torrent = open( filename,'rb')
        data = {
                'api': 'SYNO.DownloadStation.Task',
                'version': '1',
                'method': 'create',
                'session': 'DownloadStation',
                '_sid': self.sid
                }
        files = {'file': (filename, torrent)}
        r = self.session.post( 'http://{}/webapi/DownloadStation/task.cgi'.format( self.ip ), data=data, files=files, verify=False)
        print(r.url)
        print(r.content)
        if r.status_code != 200:
            print('[ERROR] Upload torrent file fail.') 
            return False
        if not r.json()['success']:
            print('[ERROR] Upload torrent response fail.') 
            return False
        return True
