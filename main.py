from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000
WHITE = '#fbfbfb'
BLUE = '#b9e1dc'
ORANGE = '#f38181'
PURPLE = '#756c83'
FONT_NAME = "Montserrat"
FONT_TYPES = ["arial", "times", "cour"]
FONT_TYPE = "arial"
FONT_SIZES = ["20", "40", "60", "80", "100", "120", "140"]
FONT_SIZE = 80
OPACITY = 125
H_POSITION = 50
V_POSITION = 50
text = ""
file_location = ""
image_resize = None
canvas_image = None
canvas_imagetk = None
watermarked_image = None
test = None
resized_width = CANVAS_WIDTH
resized_height = CANVAS_HEIGHT


def browsefiles():
    global image_resize, test, resized_width, resized_height

    rotate_button.grid_forget()
    watermark_button.grid_forget()
    edit_button.grid_forget()
    save_button.grid_forget()

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select an image file",
                                          filetypes=[("Image files", ".jpg .png")])

    # Upload image
    if filename:
        image1 = Image.open(filename).convert("RGBA")

        # Resize image
        img_width, img_height = image1.size
        resize_factor = min(CANVAS_WIDTH / img_width, CANVAS_HEIGHT / img_height)
        resized_width = int(img_width * resize_factor)
        resized_height = int(img_height * resize_factor)
        image_resize = image1.resize((resized_width, resized_height), Image.ANTIALIAS)
        display_image(image_resize)


def display_image(current_image):
    global canvas_image, canvas_imagetk

    canvas_image = current_image
    canvas_imagetk = ImageTk.PhotoImage(canvas_image)
    canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=canvas_imagetk)
    canvas.grid(row=1, column=0)
    rotate_button.grid(column=1, row=4, padx=10, pady=10)
    watermark_button.grid(column=1, row=5, padx=10, pady=10)


def rotate_img():
    global image_resize

    edit_button.grid_forget()
    save_button.grid_forget()
    image_resize = image_resize.rotate(90, expand=True)
    display_image(image_resize)


def watermarktext_function():

    text_window = Toplevel()
    text_window.title("Add watermark text")
    text_window.config(padx=20, pady=20, bg=WHITE)

    label = Label(text_window, text="Please enter watermark text:",
                  justify=LEFT, width=60, bg=WHITE, fg=PURPLE,
                  font=(FONT_NAME, 10, "normal"))
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    text_input = Entry(text_window, width=60, font=(FONT_NAME, 10, "normal"))
    text_input.grid(row=1, column=0, columnspan=2, pady=5)

    ok_button = Button(text_window, text="OK", bg=ORANGE, fg=WHITE, width=15, font=(FONT_NAME, 10, "bold"),
                       command=lambda: [text_callback(), text_window.destroy()])
    cancel_button = Button(text_window, text="Cancel", bg=ORANGE, fg=WHITE, width=15,
                           font=(FONT_NAME, 10, "bold"), command=text_window.destroy)
    ok_button.grid(row=2, column=0, pady=5)
    cancel_button.grid(row=2, column=1, pady=5)

    def text_callback():
        global text
        text = text_input.get()
        apply_watermark(image_resize)


def apply_watermark(current_image):
    global watermarked_image

    img_width, img_height = current_image.size

    # Add text over image
    watermark_text = Image.new('RGBA', current_image.size, (255, 255, 255, 0))
    font = ImageFont.truetype(FONT_TYPE+".ttf", FONT_SIZE)
    d = ImageDraw.Draw(watermark_text)
    textwidth, textheight = d.textsize(text, font)
    x = img_width/(100/H_POSITION) - textwidth/2
    y = img_height/(100/V_POSITION) - textheight/2
    d.text((x, y), text, fill=(255, 255, 255, OPACITY), font=font)

    watermarked_image = Image.alpha_composite(current_image, watermark_text)
    display_image(watermarked_image)
    edit_button.grid(column=1, row=6, padx=10, pady=10)
    save_button.grid(column=1, row=7, padx=10, pady=10)


def edit_watermark():

    edit_window = Toplevel()
    edit_window.title("Edit watermark text")
    edit_window.config(padx=20, pady=20, bg=WHITE)

    font_type_label = Label(edit_window, text="Font Type:", width=20, anchor='w', bg=WHITE, fg=PURPLE,
                            font=(FONT_NAME, 10, "normal"))
    font_size_label = Label(edit_window, text="Font Size:", width=20, anchor='w', bg=WHITE, fg=PURPLE,
                            font=(FONT_NAME, 10, "normal"))
    opacity_label = Label(edit_window, text="Opacity:", width=20, anchor='w', bg=WHITE, fg=PURPLE,
                          font=(FONT_NAME, 10, "normal"))
    horizontal_position_label = Label(edit_window, text="Horizontal Position:", width=20, anchor='w',
                                      bg=WHITE, fg=PURPLE, font=(FONT_NAME, 10, "normal"))
    vertical_position_label = Label(edit_window, text="Vertical Position:", width=20, anchor='w',
                                    bg=WHITE, fg=PURPLE, font=(FONT_NAME, 10, "normal"))
    font_type_label.grid(row=0, column=0, padx=5, pady=5)
    font_size_label.grid(row=1, column=0, padx=5, pady=5)
    opacity_label.grid(row=2, column=0, padx=5, pady=5)
    horizontal_position_label.grid(row=3, column=0, padx=5, pady=5)
    vertical_position_label.grid(row=3, column=1, padx=5, pady=5)

    font_dropbox = ttk.Combobox(edit_window, values=FONT_TYPES)
    font_dropbox.grid(row=0, column=1, padx=5, pady=5)

    size_dropbox = ttk.Combobox(edit_window, values=FONT_SIZES)
    size_dropbox.grid(row=1, column=1, padx=5, pady=5)

    opacity_slider = Scale(edit_window, from_=1, to=255, sliderrelief='flat', highlightthickness=0,
                           troughcolor=BLUE, activebackground=ORANGE, background=WHITE, fg=PURPLE, orient=HORIZONTAL)
    opacity_slider.grid(row=2, column=1, padx=5, pady=5)

    horizontal_slider = Scale(edit_window, from_=1, to=100, sliderrelief='flat', highlightthickness=0,
                              troughcolor=BLUE, activebackground=ORANGE, background=WHITE, fg=PURPLE, orient=HORIZONTAL)
    horizontal_slider.grid(row=4, column=0, padx=5, pady=5)

    vertical_slider = Scale(edit_window, from_=1, to=100, sliderrelief='flat', highlightthickness=0,
                            troughcolor=BLUE, activebackground=ORANGE, background=WHITE, fg=PURPLE)
    vertical_slider.grid(row=4, column=1, padx=5, pady=5)

    font_dropbox.set(FONT_TYPE)
    size_dropbox.set(FONT_SIZE)
    opacity_slider.set(OPACITY)
    horizontal_slider.set(H_POSITION)
    vertical_slider.set(V_POSITION)

    apply_button = Button(edit_window, text="Apply", bg=ORANGE, fg=WHITE, width=20, font=(FONT_NAME, 10, "bold"),
                          command=lambda: [edit_callback()])
    close_button = Button(edit_window, text="Close", bg=ORANGE, fg=WHITE, width=20, font=(FONT_NAME, 10, "bold"),
                          command=edit_window.destroy)

    apply_button.grid(row=5, column=0, padx=5, pady=5)
    close_button.grid(row=5, column=1, padx=5, pady=5)

    def edit_callback():
        global FONT_TYPE, FONT_SIZE, OPACITY, H_POSITION, V_POSITION

        FONT_TYPE = font_dropbox.get()
        FONT_SIZE = int(size_dropbox.get())
        OPACITY = int(opacity_slider.get())
        H_POSITION = int(horizontal_slider.get())
        V_POSITION = int(vertical_slider.get())

        apply_watermark(image_resize)


def save_as():
    filename = filedialog.asksaveasfilename(initialdir="/",
                                            title="Save image as PNG",
                                            filetypes=[("Image files", "*.png")],
                                            defaultextension=".png")

    if filename:
        watermarked_image.save(filename)
        messagebox.showinfo(title="Save Complete",
                            message=f"Your file has been saved in the following location:\n{filename}")


def exit_function():
    msgbox = messagebox.askquestion(title="Exit Application",
                                    message="Are you sure you want to exit the application?",
                                    icon='warning')
    if msgbox == 'yes':
        window.destroy()


window = Tk()
window.title("Image Watermarking App")
window.config(padx=50, pady=50, bg=WHITE)

title_label = Label(text="Watermarking App", fg=PURPLE, bg=WHITE, font=(FONT_NAME, 40, "bold"))
title_label.grid(row=0, column=0)
canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WHITE, highlightthickness=0)
canvas.grid(row=1, column=0, rowspan=16, padx=20, pady=20)

upload_button = Button(text="Upload Image", highlightthickness=0, width=25, height=3,
                       bg=ORANGE, fg=WHITE, font=(FONT_NAME, 15, "bold"), command=browsefiles)
upload_button.grid(column=1, row=3, padx=10, pady=10)

rotate_button = Button(text="Rotate Image", highlightthickness=0, width=25, height=3,
                       bg=ORANGE, fg=WHITE, font=(FONT_NAME, 15, "bold"), command=rotate_img)
watermark_button = Button(text="Add Watermark Text", highlightthickness=0, width=25, height=3,
                          bg=ORANGE, fg=WHITE, font=(FONT_NAME, 15, "bold"), command=watermarktext_function)
edit_button = Button(text="Edit Watermark", highlightthickness=0, width=25, height=3,
                     bg=ORANGE, fg=WHITE, font=(FONT_NAME, 15, "bold"), command=edit_watermark)
save_button = Button(text="Save Image", highlightthickness=0, width=25, height=3,
                     bg=ORANGE, fg=WHITE, font=(FONT_NAME, 15, "bold"), command=save_as)


exit_button = Button(text="Exit", highlightthickness=0, width=25, height=3,
                     bg=ORANGE, fg=WHITE, font=(FONT_NAME, 15, "bold"), command=exit_function)
exit_button.grid(column=1, row=14, padx=10, pady=10)


window.mainloop()
