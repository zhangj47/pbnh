import hashlib
import io
import json
import magic

from pbnh import conf
from pbnh.db import paste

config = conf.get_config().get('database')

def filedata(files, addr=None, sunset=None):
    try:
        buf = files.stream
        if buf and isinstance(buf, io.BytesIO) or isinstance(buf,
                io.BufferedRandom):
            data = buf.read()
            mime = magic.from_buffer(data, mime=True)
            with paste.Paster(dialect=config.get('dialect'), dbname=config.get('dbname'),
                              driver=config.get('driver'), host=config.get('host'),
                              password=config.get('password'), port=config.get('port'),
                              username=config.get('username')) as pstr:
                j = pstr.create(data, mime=mime.decode('utf-8'), ip=addr,
                        sunset=sunset)
                return json.dumps(j)
        #if buf and isinstance(buf, io.BufferedRandom):
            #data = buf.read()
            #mime = magic.from_buffer(data, mime=True)
            #with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
                #j = pstr.create(data, mime=mime.decode('utf-8'), ip=addr,
                        #sunset=sunset)
                #return json.dumps(j)
    except IOError as e:
        return 'caught exception in filedata' + str(e)
    return 'File save error, your file is probably too big'

def stringdata(inputstr, addr=None, sunset=None):
    encoded = inputstr.encode('utf-8')
    return hashlib.sha1(encoded).hexdigest()

def redirectdata(redirect, addr=None, sunset=None):
    with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
        j = pstr.create(redirect.encode('utf-8'), mime='redirect', ip=addr,
                sunset=sunset)
        return json.dumps(j)
