import string


def count(s):
    for str in s.split():
        s="&".join(str)
    return s
print(count("Python is fun to learn."))