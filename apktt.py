# -*- coding:utf-8 -*-
import os
import sys
from xml.dom import minidom

if __name__=="__main__":
    assert len(sys.argv)==3
    flag=sys.argv[1]
    currentdir=os.path.dirname(__file__)
    keystore=os.path.join(currentdir,'utils','playboy.keystore')
    os.environ['path']=os.path.join(currentdir,'utils')+';'+os.environ['path']
    if flag=='d':
        apkfile=sys.argv[2]
        workdir=os.path.dirname(apkfile)
        tempdir=os.path.join(workdir,'temp')
        os.system('apktool d -f "'+apkfile+'" -o "'+tempdir+'"')
    elif flag=='x':
        folder=sys.argv[2]
        workdir=os.path.dirname(folder)
        appname=minidom.parse(os.path.join(folder,'AndroidManifest.xml')).documentElement.getAttribute('package').split('.')[-1]
        i=0
        newapk=os.path.join(workdir,appname+str(i)+'.apk')
        while os.path.exists(newapk):
            i=i+1
            newapk=os.path.join(workdir,appname+str(i)+'.apk')
        os.system('apktool b "'+folder+'" -o "'+newapk+'"')
        os.system('jarsigner -verbose -keystore "'+keystore+'" -sigalg SHA1withRSA -digestalg SHA1 -storepass e2.71828182 -keypass e2.71828182 "'+newapk+'" playboy')
        os.system('jarsigner -verify -keystore "'+keystore+'" "'+newapk+'"')
        os.rename(newapk,newapk+'.apk')
        os.system('zipalign -v -f 4 "'+newapk+'.apk'+'" "'+newapk+'"')
        os.remove(newapk+'.apk')
    elif flag=='b':
        folder=sys.argv[2]
        workdir=os.path.dirname(folder)
        appname=minidom.parse(os.path.join(folder,'AndroidManifest.xml')).documentElement.getAttribute('package').split('.')[-1]
        i=0
        newapk=os.path.join(workdir,appname+str(i)+'.apk')
        while os.path.exists(newapk):
            i=i+1
            newapk=os.path.join(workdir,appname+str(i)+'.apk')
        os.system('apktool b "'+folder+'" -o "'+newapk+'"')
    elif flag=='sign':
        newapk=sys.argv[2]
        os.system('jarsigner -verbose -keystore "'+keystore+'" -sigalg SHA1withRSA -digestalg SHA1 -storepass e2.71828182 -keypass e2.71828182 "'+newapk+'" playboy')
        os.system('jarsigner -verify -keystore "'+keystore+'" "'+newapk+'"')
        os.rename(newapk,newapk+'.apk')
        os.system('zipalign -v -f 4 "'+newapk+'.apk'+'" "'+newapk+'"')
        os.remove(newapk+'.apk')
    elif flag=='install':
        apkfile=sys.argv[2]
        os.system('adb install '+apkfile)
    elif flag=='uninstall':
        appname=sys.argv[2]
        if '.' not in appname:
            os.system('adb uninstall cn.playboy.'+appname)
        else:
            os.system('adb uninstall '+appname)
    