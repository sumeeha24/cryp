def extract_message(self):
        stego_path = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("Image Files", "*.png")])
        if not stego_path:
            messagebox.showerror("Error", "Please select the stego image.")
            return

        # 🔐 Ask for password at time of extraction (not from entry box)
        pwd_popup = tk.Toplevel(self.master)
        pwd_popup.title("Enter Password")

        tk.Label(pwd_popup, text="Enter Password:").pack(pady=5)
        pwd_entry = tk.Entry(pwd_popup, show="*", width=30)
        pwd_entry.pack(pady=5)

        def on_submit():
            pwd = pwd_entry.get()
            if not pwd:
                messagebox.showerror("Error", "Password is required.")
                pwd_popup.destroy()
                return
            try:
                encrypted = extract_data_from_image(stego_path)
                decrypted = decrypt_message(encrypted, pwd)
                messagebox.showinfo("Message", f"Decrypted message:\n{decrypted.decode()}")
            except Exception as e:
                messagebox.showerror("Decryption Failed", str(e))
            pwd_popup.destroy()

        submit_btn = tk.Button(pwd_popup, text="Decrypt", command=on_submit)
        submit_btn.pack(pady=10)

        pwd_popup.grab_set()
