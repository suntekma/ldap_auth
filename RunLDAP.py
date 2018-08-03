# -*- coding: utf-8 -*-
#-----------------------------------------
# @Time    : 7/28/2018 9:34 AM
# @Author  : Mason
# @File    : run_ldap.py
# @Software: NeweggFlow_project
#-----------------------------------------


'''
DROP TABLE IF EXISTS `users_info`;
CREATE TABLE `users_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `manager` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `employee_id` varchar(255) NOT NULL,
  `department` varchar(255) NOT NULL,
  `street_address` varchar(255) NOT NULL,
  `is_superuser` varchar(255) NOT NULL,
  `note` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2780 DEFAULT CHARSET=utf8;

'''

import os
import sys
import ldap3
from ldap3 import Server, Connection, SUBTREE, ALL
import pymysql.cursors


def get_ldap_user():
    try:
        print ("Start get the users in ldap....")
        server = Server('sxdcs01.buyabs.corp', get_info=ALL)
        conn = Connection(server, user='spiceworks', password=')9*7^7*9)%Y@#')
        conn.bind()
        conn.search(search_base='dc=buyabs,dc=corp',
                    search_filter='(&(objectCategory=person)(objectClass=user)(name=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))',
                    search_scope=SUBTREE,
                    attributes=['sAMAccountName','givenName', 'sn', 'mail','telephoneNumber', 'company', 'displayName', 'employeeID', 'l', 'streetAddress',
                                'manager', 'department', 'st'])
        print("End get the users in ldap....")
        result = []
        for each in conn.response:
            temp_dict = {}
            try:
                msg = each['attributes']
                msg1 = each['dn']
                temp_dict = each.get('attributes', {})
                temp_dict['cn'] = each.get('dn', '')
                result.append(temp_dict)
            except Exception as e:
                print (each)
        return result
    except Exception as e:
        print (e)

def analyse_user_attribute(user):
    result = []

    result.append(user.get('sAMAccountName', '') if user.get('sAMAccountName', '') != [] else " ")
    result.append(user.get('givenName', '') if user.get('givenName', '') != [] else " ")
    result.append(user.get('sn', '') if user.get('sn', '') != [] else " ")
    result.append(user.get('displayName', '') if user.get('displayName', '') != [] else " ")
    result.append(user.get('mail', '') if user.get('mail', '') != [] else " ")
    result.append(user.get('telephoneNumber', '') if user.get('telephoneNumber', '') != [] else " ")
    result.append(user.get('manager', '') if user.get('manager', '') != [] else " ")
    result.append(user.get('company', '') if user.get('company', '') != [] else " ")
    result.append(user.get('l', '') if user.get('l', '') != []  else " ")
    result.append(user.get('st', '') if user.get('st', '') != [] else " ")
    result.append(user.get('employeeID', '') if user.get('employeeID', '') != [] else " ")
    result.append(user.get('department', '') if user.get('department', '') != [] else " ")
    result.append(user.get('streetAddress', '') if user.get('streetAddress', '') != [] else " ")

    return result

def ladp_write_mysql(ladp_info):
    insert_list = []
    insert_list = [analyse_user_attribute(each) for each in ladp_info]

    conn = pymysql.connect(host='*********', user='****', password='********',db='it_workflow')
    cur = conn.cursor()
    try:
        sql_str = """INSERT INTO users_info(user_name,first_name,last_name,display_name,email,phone,manager,company,city,state,employee_id,department,street_address,is_superuser,note) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'no','')"""
        cur.executemany(sql_str,insert_list)
        conn.commit()
    except Exception as err:
        print(err)
    finally:
        cur.close()

def test_db():
    insert_list = [[1,'A'],[2,'B']]

    conn = pymysql.connect(host='*********', user='****', password='********',db='it_workflow')
    cur = conn.cursor()
    try:
        sql_str = """INSERT INTO test_db(num,name) VALUES(%s,%s)"""
        cur.executemany(sql_str,insert_list)
        conn.commit()
    except Exception as err:
        print(err)
    finally:
        cur.close()

def main():
    ldap_msg = get_ldap_user()
    if len(ldap_msg) != 0:
        ladp_write_mysql(ladp_info=ldap_msg)



def keyInList(k, l):
        return bool([True for i in l if k in i.values()])

def synchronous_ldap_data():
    user_info = get_ldap_user()

    #search user_name exist or not.
    conn = pymysql.connect(host='*********', user='****', password='********', db='it_workflow',cursorclass = pymysql.cursors.DictCursor)
    cur = conn.cursor()
    sql_str = """ select user_name from users_info"""
    insert_list = []
    try:
        cur.execute(sql_str)
        result = cur.fetchall()
        for each in user_info:
            if not keyInList(each.get('sAMAccountName', ''),result) and each.get('sAMAccountName', '') != '' and each.get('sAMAccountName', '') != []:
                insert_list.append(analyse_user_attribute(each))
        sql_str = """INSERT INTO user_info(user_name,first_name,last_name,display_name,email,phone,manager,company,city,state,employee_id,department,street_address,is_superuser,note) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'no','')"""
        cur.executemany(sql_str, insert_list)
        conn.commit()
    except Exception as e:
        print(e)

    finally:
        cur.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[Warning...] Please input the correct parameters")
        sys.exit(1)
    if sys.argv[1] == "Initial":
        main()
    #test_db()
    elif sys.argv[1] == "Update":
        synchronous_ldap_data()
    else:
        print("[Warning...] Please input the correct parameters")
