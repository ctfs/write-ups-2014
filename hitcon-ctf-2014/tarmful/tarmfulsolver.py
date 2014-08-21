import zipfile,tarfile,magic,os
root="/home/sp3ctr3/work/ctf/"
path="/home/sp3ctr3/work/ctf/tarm.zip"
# print path
while True:
    try:
        with magic.Magic() as m:
            types=m.id_filename(path)
        if types.startswith('Zip'):
            opener, mode = zipfile.ZipFile, 'r'
        elif types.startswith('gzip'):
            opener, mode = tarfile.open, 'r:gz'
        elif types.startswith('bzip2'):
            opener, mode = tarfile.open, 'r:bz2'
        zip=opener(path)#"/home/sp3ctr3/work/ctf/"+str(n)+"/"+str(n)+".zip")
        zip.extractall(path="/home/sp3ctr3/work/ctf/")
        if opener==zipfile.ZipFile:
#             print zip.namelist()[1]
            path=root+zip.namelist()[1]
        elif opener==tarfile.open:
            files=zip.getnames()
#             print files
            if len(files)>2:
                path=root+files[::-1][0]
            else:
                path=root+files[1]
            if files[1].endswith("flag"):
                print "Flag is:",open(root+"/"+files[1]).read()
    except UnicodeEncodeError:
        os.renames(path,root+"uni")
        path=root+"uni"
    except:
        break
