import tkinter as tk
from PIL import Image, ImageTk
import qrcode
from tkinter import ttk
from tkinter import filedialog
import os


def valid_entry(input):
    if input in reserved_names:
        return ""
    else:
        return input


def vcard_create():
    data = f"""BEGIN:VCARD
    VERSION:3.0
    FN;CHARSET=UTF-8:
    {valid_entry(first_name.get())} {valid_entry(last_name.get())}
    N;CHARSET=UTF-8:{valid_entry(first_name.get())};{valid_entry(last_name.get())};;;
    TEL;TYPE=HOME,VOICE:{valid_entry(home_phone.get())}
    TEL;TYPE=WORK,VOICE:{valid_entry(work_phone.get())}
    EMAIL:{valid_entry(email.get())}
    ORG;CHARSET=UTF-8:{valid_entry(company_name.get())}
    TITLE;CHARSET=UTF-8:{valid_entry(job_title.get())}
    URL:{valid_entry(website.get())}
    ADR:;;{street.get()};{city.get()};{state.get()};{valid_entry(zip_code.get())};{country.get()}
    END:VCARD"""
    data = data.replace(" ", "")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    qr.border = 0
    qr.box_size = 20
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(back_color=(240, 240, 240))
    return img


def ask_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        save_folder = folder_path + "/qr_code.jpg"
        qr_img = vcard_create()
        qr_img.save(save_folder)


def create_qrcode_label():
    img = vcard_create()
    img.save("temp.jpg")
    img = Image.open("temp.jpg")
    img_size = setting_frame.winfo_height()
    img = img.resize((img_size, img_size))
    img = ImageTk.PhotoImage(img)

    label_image = tk.Label(root)
    label_image.grid(row=1, column=2, padx=10)
    label_image.configure(image=img)
    label_image.image = img
    os.remove("temp.jpg")

    tk.Button(
        root,
        text="Save to the folder",
        command=ask_folder
    ).grid(row=2, column=2)


def out_click(entry_var, entry, def_name):
    if len(entry_var.get()) == 0:
        entry_var.set(def_name)
        entry.config(foreground="gray")


def on_click(event, entry_var, entry, def_name):
    if entry_var.get() == def_name:
        event.widget.delete(0, tk.END)
        entry.config(foreground="black")


root = tk.Tk()
root.title("vCard QR code creator")
root.resizable(False, False)

reserved_names = [
    "First name",
    "Last name",
    "Mobile",
    "Phone",
    "your@email.com",
    "Company",
    "Your job",
    "ZIP",
    "www.your-website.com",
]

first_name = tk.StringVar()
first_name.set("First name")
last_name = tk.StringVar()
last_name.set("Last name")
home_phone = tk.StringVar()
home_phone.set("Mobile")
work_phone = tk.StringVar()
work_phone.set("Phone")
email = tk.StringVar()
email.set("your@email.com")
company_name = tk.StringVar()
company_name.set("Company")
job_title = tk.StringVar()
job_title.set("Your job")
street = tk.StringVar()
city = tk.StringVar()
zip_code = tk.StringVar()
zip_code.set("ZIP")
state = tk.StringVar()
country = tk.StringVar()
website = tk.StringVar()
website.set("www.your-website.com")

setting_frame = tk.LabelFrame(root, text="vCArd settings")

tk.Label(setting_frame, text="Your Name:").grid(row=1, column=1, sticky="w")
first_name_entry = ttk.Entry(
    setting_frame,
    textvariable=first_name,
    foreground="gray"
)
first_name_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, first_name, first_name_entry, "First name"),
)
first_name_entry.bind(
    "<FocusOut>",
    lambda event: out_click(first_name, first_name_entry, "First name")
)
first_name_entry.grid(row=1, column=2, padx=5)

last_name_entry = tk.Entry(
    setting_frame,
    textvariable=last_name,
    foreground="gray"
)
last_name_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, last_name, last_name_entry, "Last name")
)
last_name_entry.bind(
    "<FocusOut>",
    lambda event: out_click(last_name, last_name_entry, "Last name")
)
last_name_entry.grid(row=1, column=3, padx=5)

tk.Label(setting_frame, text="Contact:").grid(row=2, column=1, sticky="w")
home_phone_entry = tk.Entry(
    setting_frame,
    textvariable=home_phone,
    foreground="gray"
)
home_phone_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, home_phone, home_phone_entry, "Mobile")
)
home_phone_entry.bind(
    "<FocusOut>",
    lambda event: out_click(home_phone, home_phone_entry, "Mobile")
)
home_phone_entry.grid(row=2, column=2, columnspan=3, sticky="we", padx=5)

work_phone_entry = tk.Entry(
    setting_frame,
    textvariable=work_phone,
    foreground="gray"
)
work_phone_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, work_phone, work_phone_entry, "Phone")
)
work_phone_entry.bind(
    "<FocusOut>",
    lambda event: out_click(work_phone, work_phone_entry, "Phone")
)
work_phone_entry.grid(row=3, column=2, columnspan=3, sticky="we", padx=5)

tk.Label(setting_frame, text="Email:").grid(row=4, column=1, sticky="w")
email_entry = tk.Entry(setting_frame, textvariable=email, foreground="gray")
email_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, email, email_entry, "your@email.com")
)
email_entry.bind(
    "<FocusOut>",
    lambda event: out_click(email, email_entry, "your@email.com")
)
email_entry.grid(row=4, column=2, columnspan=3, sticky="we", padx=5)

tk.Label(setting_frame, text="Company:").grid(row=5, column=1, sticky="w")
company_name_entry = tk.Entry(
    setting_frame, textvariable=company_name, foreground="gray"
)
company_name_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, company_name, company_name_entry, "Company"),
)
company_name_entry.bind(
    "<FocusOut>",
    lambda event: out_click(company_name, company_name_entry, "Company")
)
company_name_entry.grid(row=5, column=2, padx=5)

job_title_entry = tk.Entry(
    setting_frame,
    textvariable=job_title,
    foreground="gray"
)
job_title_entry.bind(
    "<FocusIn>",
    lambda event: on_click(event, job_title, job_title_entry, "Your job")
)
job_title_entry.bind(
    "<FocusOut>",
    lambda event: out_click(job_title, job_title_entry, "Your job")
)
job_title_entry.grid(row=5, column=3, padx=5)

tk.Label(setting_frame, text="Street:").grid(row=6, column=1, sticky="w")
tk.Entry(setting_frame, textvariable=street).grid(
    row=6, column=2, columnspan=3, sticky="we", padx=5
)
tk.Label(setting_frame, text="City:").grid(row=7, column=1, sticky="w")
tk.Entry(setting_frame, textvariable=city).grid(
    row=7, column=2, columnspan=3, sticky="we", padx=5
)

zip_code_entry = tk.Entry(
    setting_frame, width=10, textvariable=zip_code, foreground="gray"
)
zip_code_entry.bind(
    "<FocusIn>", lambda event: on_click(event, zip_code, zip_code_entry, "ZIP")
)
zip_code_entry.bind(
    "<FocusOut>", lambda event: out_click(zip_code, zip_code_entry, "ZIP")
)
zip_code_entry.grid(row=7, column=3, sticky="e", padx=5)

tk.Label(setting_frame, text="State:").grid(row=8, column=1, sticky="w")
tk.Entry(setting_frame, textvariable=state).grid(
    row=8, column=2, columnspan=3, sticky="we", padx=5
)
tk.Label(setting_frame, text="Country:").grid(row=9, column=1, sticky="w")
tk.Entry(setting_frame, textvariable=country).grid(
    row=9, column=2, columnspan=3, sticky="we", padx=5
)
tk.Label(setting_frame, text="Website:").grid(row=10, column=1, sticky="w")

website_entry = tk.Entry(
    setting_frame,
    textvariable=website,
    foreground="gray"
)
website_entry.bind(
    "<FocusIn>",
    lambda event: on_click(
        event,
        website,
        website_entry,
        "www.your-website.com"
    ),
)
website_entry.bind(
    "<FocusOut>",
    lambda event: out_click(website, website_entry, "www.your-website.com"),
)
website_entry.grid(row=10, column=2, columnspan=3, sticky="we", padx=5)

tk.Button(root, text="Generate QR code", command=create_qrcode_label).grid(
    row=2, column=1, pady=10
)

setting_frame.grid(row=1, column=1)
root.mainloop()
