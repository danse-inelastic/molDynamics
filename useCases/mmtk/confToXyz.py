f=file('argon.conf')
o=file('argon.xyz','w')
o.write('864\n')
o.write('\n')
lines=f.readlines()
for line in lines[1:]:
    o.write('Ar '+line)
