st='''psit @students @are @good@
abc
efg'''
l1=st.split()
print(l1)
l2=st.split("@")
print(l2)
l3=st.rsplit()
print(l3)
l4=st.splitlines()
print(l4)
#slicing
s="aadhya"
print(s[1:3])
print(s[:6])
print(s[::-1])
#striding
print(st[2:10:2])
#find
b=st.find("g")
print(b)
l5=[1,2,3,4,5,6]
l6=[i ** 3 for i in l5]
print(l6)
