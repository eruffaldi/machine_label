
# Takes a set of PDF with arbitrary size and paginates them with page marging and spacing for packing them
import PyPDF2
from rectpack import newPacker
import argparse
import StringIO

def main():
    parser = argparse.ArgumentParser(description='Merge PDFs')
    parser.add_argument('--page',default="A3",help="A3 or A4")
    parser.add_argument('--maxpages',default=20,type=int)
    parser.add_argument('--landscape',default=True)
    parser.add_argument('file',nargs="+")
    parser.add_argument('--output',required=True)
    parser.add_argument('--margin',default=10,help="mm",type=int)
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
    packer = newPacker()
    for i in range(0,args.maxpages): # 10 pages
        packer.add_bin(*pagebin)

    contents ={}
    for x in args.file:
        a =PyPDF2.PdfFileReader(open(x,"rb"))
        # all pages
        for j in range(0,a.getNumPages()):
            mb = a.getPage(j).mediaBox
            ll =mb.lowerLeft
            ur =mb.upperRight
            w = float(ur[0]-ll[0])/mm2pts
            h = float(ur[1]-ll[1])/mm2pts
            print ll,ur
            contents[(x,j)] =(a,j)
            # add spacing in mm
            packer.add_rect(w+args.spacing,h+args.spacing,(x,j))

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
            print rect,rect.rid
            a,pagenum =contents[rect.rid]
            page.mergeTranslatedPage(a.getPage(pagenum), (args.margin+rect.x)*mm2pts,(args.margin+rect.y)*mm2pts)

    outfile.write(open(args.output,"wb"))




if __name__ == '__main__':
    main()