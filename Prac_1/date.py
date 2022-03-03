from datetime import date

d0 = date(1998, 1, 14)
d1 = date(2008, 2, 23)
delta = (d1 - d0).days % 3

print(delta)