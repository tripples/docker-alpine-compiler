import os
import requests
import math

class size( long ):
    """ define a size class to allow custom formatting
        Implements a format specifier of S for the size class - which displays a human readable in b, kb, Mb etc 
    """
    def __format__(self, fmt):
        if fmt == "" or fmt[-1] != "S":
            if fmt[-1].tolower() in ['b','c','d','o','x','n','e','f','g','%']:
                # Numeric format.
                return long(self).__format__(fmt)
            else:
                return str(self).__format__(fmt)

        val, s = float(self), ["b ","Kb","Mb","Gb","Tb","Pb"]
        if val<1:
            # Can't take log(0) in any base.
            i,v = 0,0
        else:
            i = int(math.log(val,1024))+1
            v = val / math.pow(1024,i)
            v,i = (v,i) if v > 0.5 else (v*1024,i-1)
        return ("{0:{1}f}"+s[i]).format(v, fmt[:-1])

def sz(num):
    return "{0:.2S}".format(size(num))

resp = requests.get("https://hub.docker.com/v2/repositories/tripples/alpine-compiler/tags/?page=1&page_size=100")
resp_data = resp.json()['results']
size_data = { data['name']: data['full_size'] for data in resp_data }

dirs = sorted(filter(os.path.isdir, os.listdir('.')))
dirs.remove('.git')
for _dir in dirs:
	print("* `{0}` [({0}/Dockerfile [{1}])](https://github.com/tripples/docker-alpine-compiler/blob/master/{0}/Dockerfile)".format(_dir, sz(size_data[_dir])))

