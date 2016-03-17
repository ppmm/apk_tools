# -*- coding:utf-8 -*-
import os
import sys
import shutil
from xml.dom import minidom

def get_package_name(manifest):
    return minidom.parse(manifest).documentElement.getAttribute('package')
    
def replace_text(srcfile,srcstr,dststr):
    os.rename(srcfile, srcfile+'.tmp')
    input_file=open(srcfile+'.tmp',encoding='utf-8')
    output_file=open(srcfile,'w',encoding='utf-8')
    output_file.write(input_file.read().replace(srcstr, dststr))
    input_file.close()
    output_file.close()
    os.remove(srcfile+'.tmp') 
    
def replace_text_by_dir(path,srcstr,dststr):
    for dirpath,dirnames,filenames in os.walk(path):
        for name in filenames:
            if os.path.splitext(name)[1] in ['.xml','.smali','.yml']: 
                replace_text(os.path.join(dirpath,name),srcstr,dststr)
                             
def change_pkg(path,pkg1,pkg2):
    assert not pkg1==pkg2
    z=os.path.join(path,'smali')
    for i in pkg1.split('.'):
        z=os.path.join(z,i)
    v=os.path.join(path,'smali')
    for i in pkg2.split('.'):
        v=os.path.join(v,i)
    assert os.path.exists(z)
    assert not os.path.exists(v)
    shutil.copytree(z,v)
    del_pkg(z)
        
def del_pkg(p):  
    assert os.path.exists(p)
    shutil.rmtree(p)
    head,=os.path.split(p)
    while os.path.split(head)[1]!='smali' and len(os.listdir(head)==0):
        shutil.rmtree(head)
        head,=os.path.split(head)

def replace_pkg(p):
    assert os.path.exists(p)
    oldpkg=get_package_name(os.path.join(p,'AndroidManifest.xml'))
    oldStr=oldpkg.replace('.','/')
    newpkg='cn.playboy.'+oldpkg.split('.')[-1]
    newStr=newpkg.replace('.','/')
    assert oldpkg!=newpkg
    replace_text_by_dir(p,oldpkg,newpkg)
    replace_text_by_dir(p,oldStr,newStr)
    change_pkg(p,oldpkg,newpkg)

def keep_path(p):
    return '"'+p+'"'

def change_appid(path,appid,appsec):
    for i in minidom.parse(os.path.join(path,'AndroidManifest.xml')).getElementsByTagName('meta-data'):
        if i.getAttribute('android:name')=='BaiduMobAd_APP_ID':
            i.setAttribute('android:value',appid)
        elif i.getAttribute('android:name')=='BaiduMobAd_APP_SEC':
            i.setAttribute('android:value',appsec)

def insert_metadata(doc,name,value):    
    app=doc.getElementsByTagName('application').item(0)
    for i in doc.getElementsByTagName('meta-data'):
        if i.getAttribute('android:name')==name:
            i.setAttribute('android:value',value)
            return             
    app.appendChild(doc.createTextNode('\t'))
    m=doc.createElement('meta-data')
    m.setAttribute('android:name', name)
    m.setAttribute('android:value',value)
    app.appendChild(m)
    app.appendChild(doc.createTextNode('\n\t'))

def get_app_mode(path):
    for i in minidom.parse(os.path.join(path,'AndroidManifest.xml')).getElementsByTagName('meta-data'):
        if i.getAttribute('android:name')=='BaiduMobAd_APP_ID':
            return i.getAttribute('android:value')
    return "nothing"

def insert_mobads_activity(doc):    
    app=doc.getElementsByTagName('application').item(0)    
    for i in doc.getElementsByTagName('activity'):
        if i.getAttribute('android:name')=='com.baidu.mobads.AppActivity':
            return    
    app.appendChild(doc.createTextNode('\t'))
    m=doc.createElement('activity')
    m.setAttribute('android:name','com.baidu.mobads.AppActivity')
    m.setAttribute('android:configChanges','keyboard|keyboardHidden|orientation')
    app.appendChild(m)
    app.appendChild(doc.createTextNode('\n\t'))

def insert_permission(doc,name):
    root=doc.documentElement
    for i in doc.getElementsByTagName('uses-permission'):
        if i.getAttribute('android:name')==name:
            return
    root.appendChild(doc.createTextNode('\t'))
    m=doc.createElement('uses-permission')
    m.setAttribute('android:name',name)
    root.appendChild(m)
    root.appendChild(doc.createTextNode('\n'))

def modify_manifest(path,appid,appsec):
    manifest=os.path.join(path,'AndroidManifest.xml')
    doc=minidom.parse(manifest)    
    insert_permission(doc,'android.permission.INTERNET')
    insert_permission(doc,'android.permission.READ_PHONE_STATE')
    insert_permission(doc,'android.permission.ACCESS_NETWORK_STATE')
    insert_permission(doc,'android.permission.ACCESS_COARSE_LOCATION')
    insert_permission(doc,'android.permission.WRITE_EXTERNAL_STORAGE')
    insert_permission(doc,'android.permission.ACCESS_WIFI_STATE')
    insert_permission(doc,'android.permission.CHANGE_WIFI_STATE')
    insert_permission(doc,'android.permission.RECORD_AUDIO')
    insert_permission(doc,'android.permission.VIBRATE')
    insert_permission(doc,'android.permission.CAMERA')
    insert_permission(doc,'com.android.browser.permission.READ_HISTORY_BOOKMARKS')
    insert_permission(doc,'android.permission.ACCESS_FINE_LOCATION')
    insert_metadata(doc,'BaiduMobAd_APP_ID',appid)
    insert_metadata(doc,'BaiduMobAd_APP_SEC',appsec)
    insert_mobads_activity(doc)
    with open(manifest+'.tmp','w') as new:
        doc.writexml(new,encoding='utf-8')
    os.remove(manifest)
    os.rename(manifest+'.tmp',manifest)

def add_smali(path,smali):
    p=os.path.join(path,'smali','com','baidu','mobads')
    if os.path.exists(p):
        shutil.rmtree(p)
    shutil.copytree(smali,p)

def insert_attr(doc,name,value):
    root=doc.documentElement
    for i in doc.getElementsByTagName('attr'):
        if i.getAttribute('name')==name:
            return
    root.appendChild(doc.createTextNode('\t'))
    m=doc.createElement('attr')
    m.setAttribute('name',name)
    m.setAttribute('format',value)
    root.appendChild(m)
    root.appendChild(doc.createTextNode('\n'))    

def add_attrs(p,f):
    attrs=os.path.join(p,'res','values','attrs.xml')
    if not os.path.exists(attrs):
        shutil.copy(f,attrs)
    else:
        doc=minidom.parse(attrs)
        insert_attr(doc,'adSize','integer')
        insert_attr(doc,'adId','string')
        with open(attrs+'.tmp','w') as new:
            doc.writexml(new,encoding='utf-8')
        os.remove(attrs)
        os.rename(attrs+'.tmp',attrs)

def add_ads_bar(p,pkg):
    for i in os.listdir(p):
        i=os.path.join(p,i)
        if os.path.isfile(i):
            dom=minidom.parse(i)
            root=dom.documentElement
            root.appendChild(dom.createTextNode('\t'))
            #root.setAttribute('xmlns:baiduadsdk','http://schemas.android.com/apk/res/'+pkg)
            m=dom.createElement('com.baidu.mobads.AdView')
            m.setAttribute('android:layout_width','fill_parent')
            m.setAttribute('android:layout_height','wrap_content')
            m.setAttribute('android:layout_alignParentLeft','true')
            m.setAttribute('android:layout_alignParentBottom','true')
            #m.setAttribute('baiduadsdk:adSize','0')
            #m.setAttribute('baiduadsdk:adId','debug_m0000001')
            root.appendChild(m)
            root.appendChild(dom.createTextNode('\n'))
            with open(i+'.tmp','w') as new:
                dom.writexml(new,encoding='utf-8')
            os.remove(i)
            os.rename(i+'.tmp',i)

def sign_apk(apk,key):
    assert os.path.exists(apk)
    assert os.path.exists(key)
    #os.system('jarsigner -verbose -keystore '+keepPath(key)+' -sigalg SHA1withRSA -digestalg SHA1 -storepass android -keypass android '+keepPath(apk)+' androiddebugkey')
    os.system('jarsigner -verbose -keystore '+keep_path(key)+' -sigalg SHA1withRSA -digestalg SHA1 -storepass e2.71828182 -keypass e2.71828182 '+keep_path(apk)+' playboy')
    os.system('jarsigner -verify -keystore '+keep_path(key)+' '+keep_path(apk))
    os.rename(apk,apk+'.apk')
    os.system('zipalign -v -f 4 '+keep_path(apk+'.apk')+' '+keep_path(apk))
    os.remove(apk+'.apk')

def decompile_apk(apk,folder):
    assert os.path.exists(apk)
    os.system('apktool d -f -b '+keep_path(apk)+' '+keep_path(folder))

def compile_apk(folder,apk):
    assert os.path.exists(folder)
    os.system('apktool b '+keep_path(folder)+' '+keep_path(apk))

def add_ads(folder,mobads,appname,appid,appsec):
    assert os.path.exists(folder)
    assert os.path.exists(mobads)
    add_smali(folder,mobads)
    #addAttrs(temp,os.path.join(currentdir,'baidu','attrs.xml'))
    add_ads_bar(os.path.join(folder,'res','layout'),'cn.playboy.'+appname)
    modify_manifest(folder,appid,appsec)

def insert_apk(apk,extra):
    assert os.path.exists(apk)
    assert os.path.exists(extra)
    os.system('winrar a -ibck -o+ '+keep_path(apk)+' '+keep_path(extra))

def install(apk):
    assert os.path.exists(apk)
    os.system('adb install '+apk)

def uninstall(appname):
    os.system('adb uninstall cn.playboy.'+appname)

if __name__=="__main__":
    assert len(sys.argv)==2
    apkfile=sys.argv[1]
    workdir=os.path.dirname(apkfile)
    temp=os.path.join(workdir,'temp') 
    currentdir=os.path.dirname(__file__)
    keystore=os.path.join(currentdir,'playboy.keystore')
    debugkey=os.path.join(currentdir,'debug.keystore')
    extra=os.path.join(currentdir,'extra')
    os.environ['path']=os.path.join(currentdir,'apktool')+';'+os.environ['path']
    decompile_apk(apkfile,temp)
    appname=get_package_name(os.path.join(temp,'AndroidManifest.xml')).split('.')[-1]
    replace_pkg(temp)
    add_ads(temp,os.path.join(currentdir,'baidu','mobads'),appname,'debug','debug')
    assert os.path.exists(temp)
    if get_app_mode(temp)=='debug':
        newapk=os.path.join(workdir,appname+'-debug.apk')
    else:
        newapk=os.path.join(workdir,appname+'-release.apk')
    compile_apk(temp,newapk)
    insert_apk(newapk,os.path.join(currentdir,'extra'))
    sign_apk(newapk,keystore)
    input('按任意键安装到虚拟机......')
    install(newapk)
    input('按任意键卸载应用......')
    uninstall(appname)
    os.rename(temp,temp+'x')
    


