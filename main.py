from tkinter import *

import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk, PSDraw
from tkinter import filedialog, messagebox
import os
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile, askopenfilename


# -------------------------IMAGE PROCESSING---------------------#
def upload_image():
    filetypes = (
        ('Jpg files', '*.jpg'),
    )
    filename = filedialog.askopenfilename(filetypes=filetypes)
    global filepath
    filepath = os.path.abspath(filename)
    try:
        imgtk = ImageTk.PhotoImage(file=filename)
    except PIL.UnidentifiedImageError:
        messagebox.showerror("Error", "Invalid File")
        upload_image()
    else:
        img_to_display = ImageTk.getimage(imgtk)
        width, height = img_to_display.size
        width_label = Label(text=f"Image Width : {width}")
        width_label.grid(row=5, column=0, padx=100)
        height_label = Label(text=f"Image Height : {height}")
        height_label.grid(row=6, column=0, padx=100)
        #img_to_display.show()
        img_resized = img_to_display.resize((500, 500), Image.Resampling.LANCZOS)
        img_resized = ImageTk.PhotoImage(img_resized)
        # canvas = Canvas(width=500,height=500, borderwidth=0, highlightthickness=0, bg="white")
        canvas.image = img_resized

        canvas.create_image(0, 0, anchor=NW, image=img_resized)


def add_watermark():
    global img
    img = Image.open(filepath)

    draw = ImageDraw.Draw(img)
    text = text_entry.get()
    font_choice = choice.get()
    color = clicked.get()
    x = int(x_entry.get())
    y = int(y_entry.get())
    text_size = int(size_entry.get())
    my_font = ImageFont.truetype(font_choice, text_size)
    # myFont = ImageFont.truetype('Arial Bold.ttf', 100)
    # draw.text((0, 0), text, fill=(255, 255, 255), font=myFont)
    draw.text((x, y), text, fill=color, font=my_font)
    #resize image to display it
    image_preview = img.copy()
    resized = image_preview.resize((500, 500), Image.Resampling.LANCZOS)
    prev = ImageTk.PhotoImage(resized)
    canvas.image = prev
    canvas.create_image(0, 0, anchor=NW, image=prev)

    #img.show()

def undo_changes():
    #reload image
    img =Image.open(filepath)
    resized = img.resize((500, 500), Image.Resampling.LANCZOS)
    prev = ImageTk.PhotoImage(resized)
    canvas.image = prev
    canvas.create_image(0, 0, anchor=NW, image=prev)



def save_image():
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    img.save(filename)


# ---------------------UI SETUP------------------------#
window = Tk()
window.title("Watermark an Image")
window.geometry("1250x900")

window.resizable(width=False, height=False)
title_label = Label(text="Watermark An Image", font='Courier 30 ', pady=20, padx=20)
title_label.grid(row=0, column=2)

upload_button = Button(text="Upload Image", fg="blue", bg="blue", command=upload_image)
upload_button.grid(row=1, column=2)
upload_button.config(height=2,width=10)

canvas = Canvas(width=400, height=500, borderwidth=0, highlightthickness=0, bg="white")
canvas.grid(row=2, column=0, padx=50, rowspan=3)
canvas_label =Label(text="Image Preview")
canvas_label.grid(row=1, column=0, padx=250)

watermark_text = Label(text="Watermark Text", padx=20)
watermark_text.grid(row=2, column=2)
text_entry = Entry()
text_entry.insert(0, "sample watermark")
text_entry.grid(row=2, column=3)

# dropdown menu options

font_options = ["Georgia.ttf", "Farisi.ttf", "Arial Bold.ttf", "Times New Roman.ttf", "Comic Sans MS.ttf", "Skia.ttf",
                "Impact.ttf", "Brush Script.ttf"]
choice = StringVar()
choice.set("Georgia.ttf")
select_font = Label(text="Select Font")
select_font.grid(row=3, column=2)
font_drop = OptionMenu(window, choice, *font_options)
font_drop.grid(row=3, column=3)
select_size = Label(text="Enter Font Size: ")
select_size.grid(row=4, column=2)
size_entry = Entry()
size_entry.insert(0, "100")
size_entry.grid(row=4, column=3)

select_color = Label(text="Select Font Color")
select_color.grid(row=5, column=2)
color_options = ["grey", "white", "black", "red", "green", "purple"]
clicked = StringVar()
clicked.set("grey")
color_drop = OptionMenu(window, clicked, *color_options)
color_drop.grid(row=5, column=3)

x_cor = Label(text="Enter X co-ordinate of text")
x_cor.grid(row=8, column=2)
x_entry = Entry()
x_entry.insert(0, "0")
x_entry.grid(row=8, column=3)

y_cor = Label(text="Enter Y co-ordinate of text")
y_cor.grid(row=9, column=2)
y_entry = Entry()
y_entry.insert(0, "0")
y_entry.grid(row=9, column=3)

watermark_button = Button(text="Add Watermark", fg="blue", command=add_watermark)
watermark_button.config(height=2,width=10)
watermark_button.grid(row=8, column=0)

undo_button = Button(text="Undo Changes", fg="blue", command=undo_changes)
undo_button.config(height=2,width=10)
undo_button.grid(row=9, column=0)

save_button = Button(text="Save Image", fg="blue", command=save_image)
save_button.config(height=2,width=10)
save_button.grid(row=10, column=0)

window.mainloop()
