# -*- coding: utf-8 -*-
import ldap

class ldapc:
    def __init__(self,ldap_path,baseDN,domainname,ldap_authuser,ldap_authpass):
        self.baseDN = baseDN
        self.ldap_error = None
        ldap_authduser = '%s\%s' %(domainname,ldap_authuser)
        self.l=ldap.initialize(ldap_path)
        self.l.protocol_version = ldap.VERSION3
        try:
            self.l.simple_bind_s(ldap_authduser,ldap_authpass)
        except ldap.LDAPError,err:
            self.ldap_error = 'Connect to %s failed, Error:%s.' %(ldap_path,err.message['desc'])
            print self.ldap_error
        #finally:
        #     self.l.unbind_s()
        #     del self.l

    def search_users(self,username): #模糊查找，返回一个list，使用search_s()
        if self.ldap_error is None:
            try:
                searchScope = ldap.SCOPE_SUBTREE
                searchFiltername = "sAMAccountName" #通过samaccountname查找用户
                retrieveAttributes = None
                searchFilter = '(' + searchFiltername + "=" + username +'*)'
                ldap_result =self.l.search_s(self.baseDN, searchScope, searchFilter, retrieveAttributes)
                if len(ldap_result) == 0: #ldap_result is a list.
                    return "%s doesn't exist." %username
                else:
                    # result_type, result_data = self.l.result(ldap_result, 0)  
                    # return result_type, ldap_result
                    return ldap_result
            except ldap.LDAPError,err:
                return err
            
    def search_userDN(self,username): #精确查找，最后返回该用户的DN值  
        if self.ldap_error is None:  
            try:  
                searchScope = ldap.SCOPE_SUBTREE  
                searchFiltername = "sAMAccountName" #通过samaccountname查找用户  
                retrieveAttributes = None  
                searchFilter = '(' + searchFiltername + "=" + username +')'  
                ldap_result_id =self.l.search(self.baseDN, searchScope, searchFilter, retrieveAttributes)  
                result_type, result_data = self.l.result(ldap_result_id, 0)  
                if result_type == ldap.RES_SEARCH_ENTRY:  
                    print 'flag:',1  
                    return result_data[0][0] #list第一个值为用户的DN，第二个值是一个dict，包含了用户属性信息  
                else:  
                    print 'flag:',0  
                    return "%s doesn't exist." %username  
            except ldap.LDAPError,err:  
                return err         
            
    def search_user(self,username): #精确查找，返回值为list，使用search()  
        if self.ldap_error is None:  
            try:  
                searchScope = ldap.SCOPE_SUBTREE  
                searchFiltername = "sAMAccountName" #通过samaccountname查找用户  
                retrieveAttributes = None  
                searchFilter = '(' + searchFiltername + "=" + username +')'  
                ldap_result_id =self.l.search(self.baseDN, searchScope, searchFilter, retrieveAttributes)  
                result_type, result_data = self.l.result(ldap_result_id, 0)  
                if result_type == ldap.RES_SEARCH_ENTRY:  
                    return result_data  
                else:  
                    return "%s doesn't exist." %username  
            except ldap.LDAPError,err:  
                return err
                                     
    def dn_get_users_sAMAccountName(self,userdn):#通过用户dn获取LDAP用户sAMAccountName
        try:
            res =self.l.search_s(userdn, ldap.SCOPE_SUBTREE)
            for dn,entry in res:
                sAMAccountName = entry['sAMAccountName']
                return sAMAccountName
        except ldap.LDAPError,err: 
            return err    