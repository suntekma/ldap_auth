# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import HttpResponse
from .models import User
from django.conf import settings
import ldaphelper

# Create your views here.
def index(request):
    ldap_authuser='spiceworks'
    ldap_authpass=settings.AUTH_LDAP_BIND_PASSWORD
    domainname='ABS_CORP'
    ldappath=settings.AUTH_LDAP_SERVER_URI 
    baseDN='DC=buyabs,DC=corp'  #ldap_authuser在连接到LDAP的时候不会用到baseDN，在验证其他用户的时候才需要使用
    p=ldaphelper.ldapc(ldappath,baseDN,domainname,ldap_authuser,ldap_authpass)
    alluser = User.objects.all()
    for user in alluser:
        if user.username == 'sm14':
            manager = user.manager
    manager = p.dn_get_users_sAMAccountName(manager)
    return HttpResponse(manager)
