# -*- coding:utf-8 -*-
import os
import sys
import shutil
from xml.dom import minidom
                
def replace_pkg(p):
    oldpkg=minidom.parse(os.path.join(p,'AndroidManifest.xml')).documentElement.getAttribute('package')
    appname=oldpkg.split('.')[-1]
    oldstr=oldpkg.replace('.','/')
    newpkg='cn.playboy.'+appname
    newstr=newpkg.replace('.','/')
    if oldpkg!=newpkg:
        for dirpath,dirnames,filenames in os.walk(p):
            for name in filenames:
                if os.path.splitext(name)[-1] in ['.xml','.smali','.yml']: 
                    srcfile=os.path.join(dirpath,name)
                    print("@"+srcfile)
                    os.rename(srcfile, srcfile+'.tmp')
                    input_file=open(srcfile+'.tmp',encoding='utf-8')
                    output_file=open(srcfile,'w',encoding='utf-8')
                    output_file.write(input_file.read().replace(oldpkg, newpkg).replace(oldstr, newstr))
                    input_file.close()
                    output_file.close()
                    os.remove(srcfile+'.tmp')
        z=os.path.join(p,'smali')
        for i in oldpkg.split('.'):
            z=os.path.join(z,i)
        v=os.path.join(p,'smali')
        for i in newpkg.split('.'):
            v=os.path.join(v,i)
        shutil.copytree(z,v)
        shutil.rmtree(z)
        head,tail=os.path.split(z)
        while os.path.split(head)[-1]!='smali' and len(os.listdir(head))==0:
            shutil.rmtree(head)
            head,tail=os.path.split(head)
    return appname

def add_ads(folder,mobads,appid,appsec):
    
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
    
    p=os.path.join(folder,'smali','com','baidu','mobads')
    if os.path.exists(p):
        shutil.rmtree(p)
    shutil.copytree(mobads,p)
    for i in os.listdir(os.path.join(folder,'res','layout')):
        x=input('是否在 '+i+' 中添加广告：')
        if x=='n':
            continue
        i=os.path.join(os.path.join(folder,'res','layout'),i)
        if os.path.isfile(i):
            dom=minidom.parse(i)
            root=dom.documentElement
            root.appendChild(dom.createTextNode('\t'))
            m=dom.createElement('com.baidu.mobads.AdView')
            m.setAttribute('android:layout_width','fill_parent')
            m.setAttribute('android:layout_height','wrap_content')
            m.setAttribute('android:layout_alignParentLeft','true')
            m.setAttribute('android:layout_alignParentBottom','true')
            root.appendChild(m)
            root.appendChild(dom.createTextNode('\n'))
            with open(i+'.tmp','w') as new:
                dom.writexml(new,encoding='utf-8')
            os.remove(i)
            os.rename(i+'.tmp',i)
            
    manifest=os.path.join(folder,'AndroidManifest.xml')
    doc=minidom.parse(manifest)    
    insert_permission(doc,'android.permission.INTERNET')
    insert_permission(doc,'android.permission.READ_PHONE_STATE')
    insert_permission(doc,'android.permission.ACCESS_NETWORK_STATE')
    insert_permission(doc,'android.permission.ACCESS_COARSE_LOCATION')
    insert_permission(doc,'android.permission.WRITE_EXTERNAL_STORAGE')
    insert_permission(doc,'android.permission.ACCESS_WIFI_STATE')
    insert_metadata(doc,'BaiduMobAd_APP_ID',appid)
    insert_metadata(doc,'BaiduMobAd_APP_SEC',appsec)
    insert_mobads_activity(doc)
    with open(manifest+'.tmp','w') as new:
        doc.writexml(new,encoding='utf-8')
    os.remove(manifest)
    os.rename(manifest+'.tmp',manifest)
    
def sign_apk(newapk,tempdir,keystore):
    os.system('apktool b "'+tempdir+'" -o "'+newapk+'"')
    os.system('jarsigner -verbose -keystore "'+keystore+'" -sigalg SHA1withRSA -digestalg SHA1 -storepass e2.71828182 -keypass e2.71828182 "'+newapk+'" playboy')
    os.system('jarsigner -verify -keystore "'+keystore+'" "'+newapk+'"')
    os.rename(newapk,newapk+'.apk')
    os.system('zipalign -v -f 4 "'+newapk+'.apk'+'" "'+newapk+'"')
    os.remove(newapk+'.apk')
    
def change_appid(tempdir,appid,appsec):
    manifest=os.path.join(tempdir,'AndroidManifest.xml')
    doc=minidom.parse(manifest)
    for i in doc.getElementsByTagName('meta-data'):
        if i.getAttribute('android:name')=='BaiduMobAd_APP_ID':
            i.setAttribute('android:value',appid)
        elif i.getAttribute('android:name')=='BaiduMobAd_APP_SEC':
            i.setAttribute('android:value',appsec)
    with open(manifest+'.tmp','w') as new:
        doc.writexml(new,encoding='utf-8')
    os.remove(manifest)
    os.rename(manifest+'.tmp',manifest)
    
if __name__=="__main__":
    assert len(sys.argv)==4
    apkfile=sys.argv[1]
    appid=sys.argv[2]
    appsec=sys.argv[3]
    workdir=os.path.dirname(apkfile)
    tempdir=os.path.join(workdir,'temp') 
    currentdir=os.path.dirname(__file__)
    extra=os.path.join(tempdir,'unknown','extra')
    keystore=os.path.join(currentdir,'utils','playboy.keystore')
    os.environ['path']=os.path.join(currentdir,'utils')+';'+os.environ['path']

    os.system('apktool d -f "'+apkfile+'" -o "'+tempdir+'"')
    if input('是否生成生成无广告版本:')=='y':
        appname=minidom.parse(os.path.join(tempdir,'AndroidManifest.xml')).documentElement.getAttribute('package').split('.')[-1]
        newapk=os.path.join(workdir,appname+'-noads.apk')
        sign_apk(newapk,tempdir,keystore)
    if input('是否开始添加广告：')=='y':
        builddir=os.path.join(tempdir,'build')
        if os.path.exists(builddir):
            shutil.rmtree(builddir)
        if os.path.exists(extra):
            shutil.rmtree(extra)
        shutil.copytree(os.path.join(currentdir,'utils','extra'),extra)
        if os.path.exists(os.path.join(tempdir,'original')):
            shutil.rmtree(os.path.join(tempdir,'original'))
        with open(os.path.join(tempdir,'apktool.yml'),'a',encoding='utf-8') as yml:
            yml.write("unknownFiles:\n  extra/__pasys_remote_banner.jar: '8'")
        appname=replace_pkg(tempdir)
        add_ads(tempdir,os.path.join(currentdir,'utils','mobads'),'a5fb3056','a5fb3056')
        input('按任意键继续生成测试版和发行版......')
        newapk1=os.path.join(workdir,appname+'-debug.apk')
        sign_apk(newapk1,tempdir,keystore)
        change_appid(tempdir,appid,appsec)
        newapk2=os.path.join(workdir,appname+'-release.apk')
        sign_apk(newapk2,tempdir,keystore)
    print("结束！")