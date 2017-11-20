import argparse
import cairo
import os 
import qrcode 
import array

def pil2cairo(img):
    imgd = img.tobytes()
    a = array.array('B',imgd)
    w = img.width
    h = img.height
    return cairo.ImageSurface.create_for_data (a, cairo.FORMAT_ARGB32,w,h,w*4)

# image is white over alpha
def draw_image(ctx, image, top, left, height, width,blackize=False):
    """Draw a scaled image on a given context."""
    if type(image) is str:
        image_surface = cairo.ImageSurface.create_from_png(image)
    else:
        image_surface = image
    if blackize:
        x = image_surface.get_data()
        for i in range(0,len(x),4):
            x[i] = "\x00"
            x[i+1] = "\x00"
            x[i+2] = "\x00"

    # calculate proportional scaling
    img_height = image_surface.get_height()
    img_width = image_surface.get_width()
    width_ratio = float(width) / float(img_width)
    height_ratio = float(height) / float(img_height)
    scale_xy = min(height_ratio, width_ratio)
    ctx.save()
    ctx.translate(left, top)
    ctx.scale(scale_xy, scale_xy)
    ctx.set_source_surface(image_surface)
    ctx.paint()
    ctx.restore()


def main():
    parser = argparse.ArgumentParser(description='QR Icon Gen')
    parser.add_argument('--url',default="")
    parser.add_argument('--name',default="")
    parser.add_argument('--icon',default="")
    parser.add_argument('--output',required=True)
    
    args = parser.parse_args()

    mm2pts = 2.83464567
    page = (41,31)
    width_pts, height_pts = page[0]*mm2pts,page[1]*mm2pts
    surface = cairo.PDFSurface (args.output, width_pts, height_pts)
    ctx = cairo.Context (surface)
    ctx.scale(mm2pts,mm2pts)
    ctx.set_line_width(0.5)
    ctx.rectangle(0,0,page[0],page[1])
    ctx.stroke()
    if args.icon != "":
        ctx.set_source_rgb(0.0, 0.0, 0.0)
        draw_image(ctx,args.icon,1,0,20,20,blackize=True) # origin 20mm
    if args.url != "":
        img = pil2cairo(qrcode.make(args.url).convert("RGBA"))
        draw_image(ctx,img,1,20,20,20)
    if args.name != "":
        ctx.set_source_rgb(0, 0, 0)
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,         cairo.FONT_WEIGHT_NORMAL)
        ctx.move_to(2,25)
        ctx.scale(0.5,0.5)
        ctx.show_text(args.name)

    ctx.show_page()

if __name__ == "__main__":
    main();
