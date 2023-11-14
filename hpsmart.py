import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class ChangeConfigWindow(tk.Toplevel):
    def __init__(self, parent, current_config, main_app):
        super().__init__(parent)

        self.title("Change Config")

        self.main_app = main_app  # Reference to the main application

        # Calculate the position to center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400  # Adjust the width as needed
        window_height = 550  # Adjust the height as needed
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the geometry of the Change Config window
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add margins
        self.margin_frame = tk.Frame(self)
        self.margin_frame.pack(pady=10, padx=10)

        self.current_config = current_config

        self.smtp_server_label = tk.Label(self.margin_frame, text="SMTP Server:")
        self.smtp_server_label.pack(pady=5)

        self.smtp_server_entry = tk.Entry(self.margin_frame, width=30)
        self.smtp_server_entry.insert(0, current_config.get("smtp_server", ""))
        self.smtp_server_entry.pack(pady=5)

        self.smtp_port_label = tk.Label(self.margin_frame, text="SMTP Port:")
        self.smtp_port_label.pack(pady=5)

        self.smtp_port_entry = tk.Entry(self.margin_frame, width=30)
        self.smtp_port_entry.insert(0, current_config.get("smtp_port", ""))
        self.smtp_port_entry.pack(pady=5)

        self.smtp_username_label = tk.Label(self.margin_frame, text="SMTP Username:")
        self.smtp_username_label.pack(pady=5)

        self.smtp_username_entry = tk.Entry(self.margin_frame, width=30)
        self.smtp_username_entry.insert(0, current_config.get("smtp_username", ""))
        self.smtp_username_entry.pack(pady=5)

        self.smtp_password_label = tk.Label(self.margin_frame, text="SMTP Password:")
        self.smtp_password_label.pack(pady=5)

        self.smtp_password_entry = tk.Entry(self.margin_frame, width=30, show="*")
        self.smtp_password_entry.insert(0, current_config.get("smtp_password", ""))
        self.smtp_password_entry.pack(pady=5)

        self.sender_email_label = tk.Label(self.margin_frame, text="Sender Email:")
        self.sender_email_label.pack(pady=5)

        self.sender_email_entry = tk.Entry(self.margin_frame, width=30)
        self.sender_email_entry.insert(0, current_config.get("sender_email", ""))
        self.sender_email_entry.pack(pady=5)

        self.allowed_domain_label = tk.Label(self.margin_frame, text="Allowed Domain:")
        self.allowed_domain_label.pack(pady=5)

        self.allowed_domain_entry = tk.Entry(self.margin_frame, width=30)
        self.allowed_domain_entry.insert(0, current_config.get("allowed_domain", ""))
        self.allowed_domain_entry.pack(pady=5)

        self.default_recipient_label = tk.Label(self.margin_frame, text="Default Printer Email:")
        self.default_recipient_label.pack(pady=5)

        self.default_recipient_entry = tk.Entry(self.margin_frame, width=30)
        self.default_recipient_entry.insert(0, current_config.get("default_printer_email", ""))
        self.default_recipient_entry.pack(pady=5)

        self.save_button = tk.Button(self.margin_frame, text="Save", command=self.save_config)
        self.save_button.pack(pady=10)

    def save_config(self):
        new_config = {
            "smtp_server": self.smtp_server_entry.get(),
            "smtp_port": int(self.smtp_port_entry.get()),
            "smtp_username": self.smtp_username_entry.get(),
            "smtp_password": self.smtp_password_entry.get(),
            "sender_email": self.sender_email_entry.get(),
            "allowed_domain": self.allowed_domain_entry.get(),
            "default_printer_email": self.default_recipient_entry.get()
        }

        with open("config.json", "w") as config_file:
            json.dump(new_config, config_file, indent=4)

        # Close the Change Config window
        self.destroy()

        # Reload the configuration in the main app
        self.main_app.load_config()

        # Update the recipient email field in the main window
        self.main_app.email_entry.delete(0, tk.END)
        self.main_app.email_entry.insert(0, self.main_app.default_printer_email)

        # Notify the user that the application needs to be restarted
        messagebox.showinfo("Restart Required", "The application needs to be restarted for the changes to take effect.")

class EmailSenderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HP Smart")

        # Calculate the position to center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400  # Adjust the width as needed
        window_height = 300  # Adjust the height as needed
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the geometry of the main window
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add margins
        self.margin_frame = tk.Frame(self)
        self.margin_frame.pack(pady=10, padx=10)

        # Add header
        self.header_label = tk.Label(self.margin_frame, text="Remote Printing App", font=("Helvetica", 16))
        self.header_label.pack(pady=10)

        # Add content frame
        self.content_frame = tk.Frame(self.margin_frame)
        self.content_frame.pack()

        self.email_label = tk.Label(self.content_frame, text="Printer Email:")
        self.email_label.pack(pady=5)

        self.email_entry = tk.Entry(self.content_frame, width=30)
        self.email_entry.pack(pady=5)

        self.load_button = tk.Button(self.content_frame, text="Load PDF", command=self.load_pdf)
        self.load_button.pack(pady=5)

        self.send_button = tk.Button(self.content_frame, text="Send Email", command=self.send_email)
        self.send_button.pack(pady=5)

        self.change_config_button = tk.Button(self.content_frame, text="Change Config", command=self.open_change_config_window)
        self.change_config_button.pack(pady=5)

        self.load_config()
        self.email_entry.insert(0, self.default_printer_email)

        # Add footer
        self.footer_label = tk.Label(self.margin_frame, text="© 2023 drcoccodrillus")
        self.footer_label.pack(pady=10)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_path = file_path
            self.load_button.config(text=f"Loaded: {file_path}")

    def send_email(self):
        recipient_email = self.email_entry.get()
        if not recipient_email or (self.allowed_domain and not recipient_email.endswith(f"@{self.allowed_domain}")):
            tk.messagebox.showwarning("Invalid Email", f"Please enter a valid printer email ending with @{self.allowed_domain}")
            return

        if not hasattr(self, 'file_path'):
            tk.messagebox.showwarning("No File", "Please load a PDF file to send.")
            return

        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "PDF File Attachment"

            # Attach the PDF file
            with open(self.file_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), _subtype="pdf")
                attachment.add_header('Content-Disposition', f'attachment; filename="{file.name}"')
                msg.attach(attachment)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())

            tk.messagebox.showinfo("PDF Sent to printer", "Your PDF has been sent successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while sending the PDF to the printer:\n{str(e)}")


    def open_change_config_window(self):
        # Ensure the "Modify Settings" window is in front of the main window
        self.attributes("-topmost", True)
        ChangeConfigWindow(self, {
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "smtp_username": self.smtp_username,
            "smtp_password": self.smtp_password,
            "sender_email": self.sender_email,
            "allowed_domain": self.allowed_domain,
            "default_printer_email": self.default_printer_email
        }, self)
        # Reset the topmost attribute after the window is closed
        self.attributes("-topmost", False)

    def load_config(self):
        try:
            with open("config.json", "r") as config_file:
                config_data = json.load(config_file)
                self.smtp_server = config_data.get("smtp_server", "")
                self.smtp_port = config_data.get("smtp_port", 587)
                self.smtp_username = config_data.get("smtp_username", "")
                self.smtp_password = config_data.get("smtp_password", "")
                self.sender_email = config_data.get("sender_email", "")
                self.allowed_domain = config_data.get("allowed_domain", "")
                self.default_printer_email = config_data.get("default_printer_email", "")
        except FileNotFoundError:
            tk.messagebox.showerror("Config Error", "Config file not found. Please create a 'config.json' file.")
            self.destroy()

    def restart(self):
        # Destroy the current window and restart the application
        self.destroy()
        EmailSenderApp().mainloop()

if __name__ == "__main__":
    app = EmailSenderApp()
    app.mainloop()
