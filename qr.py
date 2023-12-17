import tkinter as tk
from PIL import ImageTk
import qrcode
from tkinter import ttk


class VCardApp:
    def __init__(self, base):
        self.label_image = None
        self.setting_frame = None
        self.entries = None
        self.root = base
        self.root.title("vCard QR Code Creator")
        self.root.resizable(True, True)

        self.setup_widgets()

    def setup_widgets(self):
        self.setting_frame = tk.LabelFrame(self.root, text="vCard Settings")
        self.setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.entries = {}
        fields = [
            "First Name", "Last Name", "Mobile",
            "Phone", "Email", "Company",
            "Job Title", "Street", "City",
            "State", "ZIP", "Country", "Website"
        ]
        for idx, field in enumerate(fields):
            row = idx // 2
            col = idx % 2
            label = tk.Label(self.setting_frame, text=f"{field}:")
            label.grid(row=row, column=col*2, sticky="w")
            entry_var = tk.StringVar(value=field)
            entry = ttk.Entry(self.setting_frame, textvariable=entry_var)
            entry.grid(row=row, column=col*2+1, padx=5, pady=2, sticky="ew")
            self.entries[field] = entry_var

        generate_button = tk.Button(
            self.root,
            text="Generate QR Code",
            command=self.create_qrcode_label
        )
        generate_button.grid(row=1, column=0, pady=10)

    def create_qrcode_label(self):
        img = self.vcard_create()
        img = ImageTk.PhotoImage(img)
        if hasattr(self, 'label_image'):
            self.label_image.configure(image=img)
        else:
            self.label_image = tk.Label(self.root, image=img)
            self.label_image.grid(row=2, column=0, padx=10)
        self.label_image.image = img

    def vcard_create(self):
        data = self.generate_vcard_data()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def generate_vcard_data(self):
        data = "BEGIN:VCARD\nVERSION:3.0\n"
        data += f"FN:{self.entries['First Name'].get()}" \
                f" {self.entries['Last Name'].get()}\n"
        data += f"TEL;TYPE=CELL:{self.entries['Mobile'].get()}\n"
        data += f"TEL;TYPE=WORK:{self.entries['Phone'].get()}\n"
        data += f"EMAIL:{self.entries['Email'].get()}\n"
        data += f"ORG:{self.entries['Company'].get()}\n"
        data += f"TITLE:{self.entries['Job Title'].get()}\n"
        data += f"ADR:;;{self.entries['Street'].get()};" \
                f"{self.entries['City'].get()};" \
                f"{self.entries['State'].get()};" \
                f"{self.entries['ZIP'].get()};" \
                f"{self.entries['Country'].get()}\n"
        data += f"URL:{self.entries['Website'].get()}\n"
        data += "END:VCARD"
        return data


if __name__ == "__main__":
    root = tk.Tk()
    app = VCardApp(root)
    root.mainloop()
