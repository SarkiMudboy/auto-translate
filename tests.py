import re



r = re.compile(r'(\d+|\*)[\t]+([a-zA-Z]|\«)+')

string = ' 1	Georges Lichtheim, The Concept of Ideology and Other'

m = r.findall(string)
print(m)
# print(m.group(1))
