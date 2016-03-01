# -*- coding: utf-8 -*-
# #
##  #
# # class A:
# #     def __init__(self):
# #         self.s="aa"
# #
# #     def test(self):
# #         print self.__dict__
# #
# #
# # class B(A):
# #
# #     def __init__(self):
# #         A.__init__(self)
# #         self.q = "fufu"
# #
# #
# # c = B()
# #
# # c.test()
#
# class A:
#     def __init__(self):
#         pass
#
#     @classmethod
#     def get_new_instance(cls):
#         return cls()
#
# a=A.get_new_instance()
# b=A.get_new_instance()
#
# print a
# print b

# import MySQLdb
#
# DB = ("127.0.0.1", "root", "", "django_ito")
# con = MySQLdb.connect(*DB)
# print "\\xE6\\xB5\\x8B\\xE8\\xAF\\x95"
# cur = con.cursor()
# cur.execute(""" update ticketmgr_incidentaction set action_detail='测试' where id ='21'  """)
# con.commit()
# con.close()


class A:
    def __init__(self):
        self.kk= "a"
        self.bb= "c"

    def update_s(self, **kwargs):
        for k, v in kwargs.items():
            print k, v
            self.k = v
            self.__dict__.update()



a = A()
a.update_s(kk="c")
print
print a.__dict__
