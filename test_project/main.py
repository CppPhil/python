from functools import partial


def lazy_range(n):
    """a lazy version of range"""
    i = 0
    while i < n:
        yield i
        i += 1


def exp(base, power):
    return base ** power


print "Hello Python"

for i in lazy_range(10):
    print i

two_to_the = partial(exp, 2)
print two_to_the(3)

list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]
pairs = zip(list1, list2)

# unzip
letters, numbers = zip(*pairs)
print letters
print numbers
