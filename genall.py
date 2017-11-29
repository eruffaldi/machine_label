import os


o = open("list.txt","w")
pa ="icons/icons"
i=1
for x in sorted(os.listdir(pa)):
	if not x.endswith(".png"):
		continue
	o.write("%d\t%s\n"%(i,x))
	fp = os.path.join(pa,x)
	ss ="python make1.py --url http://www.percro.org/dev/%d --name PERCRO-%d --icon \"%s\" --output p%02d.pdf" % (i,i,fp,i)
	print ss
	os.system(ss)
	i += 1

o.close()