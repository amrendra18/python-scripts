
"""
Creating my own chess database
"""
import os, sys
import urllib2
import zipfile

from bs4 import BeautifulSoup

base_url = "http://www.pgnmentor.com/"
url = base_url + "files.html"
extensions = [".zip",".pgn"]
links = []
linksCached = {}
count = 0
downloadedLinks = {}
downloadList = "backup.txt"

def saveAllDownloadedLinks():
    save = open(downloadList,'w')
    count = 1
    for key in sorted(linksCached.iterkeys()):
        line = ""+str(count)+". Downloaded "+key
        line = line.strip()
        print line
        save.write(line)
        save.write('\n')
        count = count + 1
    save.close()
        
    
def readAlreadyDownloadedLinks():
    with open(downloadList) as f:
        #print f
        #content = f.readLines()
        count = 1
        for line in f :
            link = line.split(' ')[2]
            link = link.strip()
            #print "--> Already downloaded ["+link+"]"
            linksCached[link]=True
            count = count + 1
        f.close()
        print 
        print "--> Already downloaded "+str(count-1)+" files"

def getAllLinks():
    resp = urllib2.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))
    for link in soup.find_all('a', href=True):
        for ext in extensions:
            if link["href"].endswith(ext):
                #print link["href"]
                try:
                    if linksCached[link["href"]] == True:
                        break
                except:
                    pass
                links.append(link["href"])
                break

"""
if its zip file, download in temp, then decompress at proper place
else directly download it at correct place.
"""
def processAllLinks():
    count = 0
    totalContentSize = 0
    print
    print "--> PREPARING DOWNLOADS..."
    for link in links:
        print "--> Downloading ["+link+"]"
        try:
            if linksCached[link] == True:
                print "--> Already downloaded ["+link+"]"
                print
                continue
        except:
            print "--> Need to download ["+link+"]"
            #continue
            if link.endswith(".pgn"):
                tempurl = base_url + link
                stream = urllib2.urlopen(tempurl)
                streamsize = stream.headers['content-length']
                totalContentSize = totalContentSize + int(streamsize)
                directory,filename = link.split("/")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                out_file = os.path.join(os.getcwd()+"\\"+directory, filename)
                temp = open(out_file,"wb")
                temp.write(stream.read())
                temp.close()
                print "--> Downloaded "+directory+"\\"+filename+" size: "+streamsize+" bytes."
                count = count + 1
                linksCached[link]=True
                #break
            elif link.endswith(".zip"):
                tempurl = base_url + link
                stream = urllib2.urlopen(tempurl)
                streamsize = stream.headers['content-length']
                totalContentSize = totalContentSize + int(streamsize)
                directory,filenamezip = link.split("/")
                temp_directory = "temp"
                if not os.path.exists(temp_directory):
                    os.makedirs(temp_directory)
                out_file = os.path.join(os.getcwd()+"\\"+temp_directory, filenamezip)
                temp = open(out_file,"wb")
                temp.write(stream.read())
                temp.close()
                
                zfile = zipfile.ZipFile(out_file)
                filedirectory = directory+"\\"+filenamezip[:filenamezip.find(".")]
                if not os.path.exists(filedirectory):
                    os.makedirs(filedirectory)
                for name in zfile.namelist():
                    (dirname, filename) = os.path.split(name)
                    print "--> Decompressing " + filename + " in " + filedirectory
                    zfile.extract(name, filedirectory)
                zfile.close()
                count = count + 1
                print "--> Downloaded and extracted "+directory+"\\"+filenamezip+" size: "+streamsize+" bytes."
                linksCached[link]=True
                try:
                    os.remove(out_file)
                except OSError:
                    print "--> Error deleting temp file : "+out_file
                #break
            else:
                print "--> UNKNOWN extension : "+link
            print
        
    print "================================================"
    print "Downloaded total "+str(count)+ " files Total Content Downloaded : "+str(totalContentSize/1000)+" Kb."
    

if __name__ == "__main__":
    getAllLinks()
    readAlreadyDownloadedLinks()
    try:
        processAllLinks()
    finally:
        saveAllDownloadedLinks()
