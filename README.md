# machine_label
labeling and indexing of physical machines using QR Code and Mmemonic

The idea is that:
1) Humans recognize machine via avatar and QR Code pointing to specs
2) Machine uses Mac address to lookup

Workflow:
1) Spreadsheet with device specs. Each machine is unique by id and by one of the Mac addresses

2) Label maker: prepares QR Code + Id + Avatar Icons for each device. Printable PDF stickers

3) Website maker: takes the sheet and produces the following structure
	
	devices/<device>.html: linked by QR-Code
	devices/<device>.json
	bymac/<mac>: contains the <device>


python make1.py --url http://www.percro.org/dev/1 --name SSSA-1 --icon icons/icons/Alligator.png --output p1.pdf

python paginate.py --page A3 p*.pdf --output x.pdf --allsame --margin 15 --spacing 10