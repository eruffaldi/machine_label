
# Takes a set of PDF with arbitrary size and paginates them with page marging and spacing for packing them
import PyPDF2
from rectpack import newPacker
import argparse
import StringIO

class Rect:
    def __init__(self,x,y,w,h,rid):
        self.x =x
        self.y =y
        self.width=w
        self.height=h
        self.rid=rid
    def __repr__(self):
        return str((self.x,self.y,self.width,self.height,self.rid))

class BinAllocated(list):
    def __init__(self,w,h):
        self.width=w
        self.height=h
class samePacker(list):
    def __init__(self):
        self.bins=[]
        self.rects=[]
    def pack(self):
        bini=-1
        xleft=0
        yleft=0
        bino=[]
        pw=0
        iw =max([r[0] for r in self.rects])
        ih =min([r[1] for r in self.rects])
        x=0
        y=0
        for a in self.rects:
            w,h,id=a
            if xleft < iw:
                xleft=pw
                yleft-=ih
                y += ih
                x = 0
                if yleft < ih:
                    bini += 1
                    if  bini >=len(self.bins):
                        return
                    pw,ph=self.bins[bini]
                    bino=BinAllocated(pw,ph)
                    xleft=pw
                    yleft=ph
                    y=0
                    self.append(bino)            
            bino.append(Rect(x,y,w,h,id))
            x += iw
            xleft -= iw

    def add_bin(self,width,height):
        self.bins.append((width,height))
    def add_rect(self,width,height,id):
        self.rects.append((width,height,id))
    #rect_list

def main():
    parser = argparse.ArgumentParser(description='Merge PDFs')
    parser.add_argument('--page',default="A3",help="A3 or A4")
    parser.add_argument('--maxpages',default=20,type=int)
    parser.add_argument('--landscape',default=True)
    parser.add_argument('file',nargs="+")
    parser.add_argument('--output',required=True)
    parser.add_argument('--allsame',action="store_true")
    parser.add_argument('--margin',default=20,help="mm",type=int)
    parser.add_argument('--spacing',default=10,help="mm",type=int)

    args = parser.parse_args()

    mm2pts = 2.83464567
    if args.page =="A3":
        page = (297,420)
    elif args.page =="A4":
        page = (210,297)
    elif args.page =="Aq":
        page = (120,120)
    else:
        print "unknown pagetype A4,A3"
        return

    if args.landscape:
        page =(page[1],page[0])

    pagept = (page[0]*mm2pts,page[1]*mm2pts)

    pagebin = (page[0]-2*args.margin,page[1]-2*args.margin)

    if args.allsame:
        packer = samePacker()
    else:
        packer = newPacker()
    for i in range(0,args.maxpages): # 10 pages
        packer.add_bin(*pagebin)

    contents ={}
    for x in sorted(args.file):
        a =PyPDF2.PdfFileReader(open(x,"rb"))
        # all pages
        for j in range(0,a.getNumPages()):
            print "adding",x,j
            mb = a.getPage(j).mediaBox
            ll =mb.lowerLeft
            ur =mb.upperRight
            w = float(ur[0]-ll[0])/mm2pts
            h = float(ur[1]-ll[1])/mm2pts
            print ll,ur
            contents[(x,j)] =(a,j)
            # add spacing in mm
            packer.add_rect(w+args.spacing*2,h+args.spacing*2,(x,j))

    packer.pack()


    # Obtain number of bins used for packing
    nbins = len(packer)
    print "pages",nbins


    outfile = PyPDF2.PdfFileWriter()

    for i in range(0,nbins):        
        page =outfile.addBlankPage(*pagept)

        # Index first bin
        abin = packer[i]

        # Bin dimmensions (bins can be reordered during packing)
        width, height = abin.width, abin.height
        nrect = len(packer[i])
        for j in range(0,nrect):
            rect = packer[i][j]
            print "result",i,j,rect,rect.rid
            a,pagenum =contents[rect.rid]
            page.mergeTranslatedPage(a.getPage(pagenum), (args.margin+args.spacing+rect.x)*mm2pts,(args.margin+args.spacing+rect.y)*mm2pts)

    outfile.write(open(args.output,"wb"))




if __name__ == '__main__':
    main()