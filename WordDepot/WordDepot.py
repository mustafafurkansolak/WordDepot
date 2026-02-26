import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import math
import webbrowser

# === WORDLIST GLOBAL ===
wordlist_words = []

# === BANNER ===
def banner():
    print(r"""
       🔥  WordDepot !
    """)

# === LEETSPEAK & VARYASYONLAR ===
def leetspeak(word):
    leet_dict = {'a': '@', 'e': '3', 'i': '1', 's': '$', 'o': '0', 'b': '8'}
    return ''.join(leet_dict.get(c.lower(), c) for c in word)

def generate_smart_variations(keyword, numbers, symbols, extra_words):
    variations = set()
    base = [keyword, keyword.lower(), keyword.upper(),
            keyword.capitalize(), leetspeak(keyword), keyword[::-1]]

    numbers = [n.strip() for n in numbers.split(',') if n.strip()]
    symbols = list(symbols)
    extras = [e.strip() for e in extra_words.split(',') if e.strip()]

    for b in base:
        variations.add(b)
        for num in numbers:
            variations.update([f"{b}{num}", f"{num}{b}"])
        for sym in symbols:
            variations.update([f"{b}{sym}", f"{sym}{b}"])
        for ext in extras:
            variations.update([f"{b}{ext}", f"{ext}{b}"])
        for num in numbers:
            for sym in symbols:
                variations.update([f"{b}{sym}{num}", f"{sym}{b}{num}", f"{num}{b}{sym}"])
    return variations

# === PASSWORD STRENGTH ANALYSIS ===
def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(not c.isalnum() for c in password): charset += 32
    if charset == 0:
        return 0
    return len(password) * math.log2(charset)

def strength_label(entropy):
    if entropy < 28:
        return "Kolay"
    elif entropy < 50:
        return "Orta"
    else:
        return "Zor"

# === WORDLIST SEÇME ===
def select_wordlist():
    global wordlist_words
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, "r", encoding="utf-8") as f:
            wordlist_words = [line.strip() for line in f if line.strip()]
        messagebox.showinfo("Yüklendi", f"{len(wordlist_words)} kelime yüklendi.")

# === MOD TOGGLE ===
def toggle_mode():
    if mode_var.get() == "wordlist":
        keyword_entry.config(state="disabled")
        wordlist_button.config(state="normal")
    else:
        keyword_entry.config(state="normal")
        wordlist_button.config(state="disabled")

# === TXT KAYDET SEÇENEKLERİ (GÜNCELLENDİ) ===
def save_to_file_table():
    options = ["Sadece Kolay", "Sadece Orta", "Sadece Zor", "Hepsi", "İptal"]
    choice_win = tk.Toplevel(root)
    choice_win.title("Kaydetme Seçeneği")
    choice_win.geometry("350x300") 
    choice_win.configure(bg="#0f0f0f")
    choice_win.resizable(False, False)

    tk.Label(choice_win, text="Hangi şifreleri kaydetmek istersiniz?", 
             fg="#39FF14", bg="#0f0f0f", font=("Courier New", 12, "bold")).pack(pady=20)

    def save_choice(option):
        if option == "İptal":
            choice_win.destroy()
            return
        if option == "Sadece Kolay":
            data = [kolay_table.item(i)["values"][0] for i in kolay_table.get_children()]
        elif option == "Sadece Orta":
            data = [orta_table.item(i)["values"][0] for i in orta_table.get_children()]
        elif option == "Sadece Zor":
            data = [zor_table.item(i)["values"][0] for i in zor_table.get_children()]
        else:
            data = [kolay_table.item(i)["values"][0] for i in kolay_table.get_children()] + \
                   [orta_table.item(i)["values"][0] for i in orta_table.get_children()] + \
                   [zor_table.item(i)["values"][0] for i in zor_table.get_children()]

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="WordDepot_Wordlist.txt",
            filetypes=[("Metin Dosyası", "*.txt")]
        )
        if filepath:
            with open(filepath, 'w', encoding="utf-8") as f:
                for item in data:
                    f.write(item + "\n")
            messagebox.showinfo("Kaydedildi", f"Wordlist kaydedildi:\n{filepath}")
        choice_win.destroy()

    for opt in options:
        tk.Button(choice_win, text=opt, width=25, 
                  command=lambda o=opt: save_choice(o),
                  bg="#0f0f0f", fg="#39FF14", activebackground="#39FF14",
                  activeforeground="black", font=("Courier New", 11, "bold"), bd=2).pack(pady=5)

# === LİNKLER ===
def my_github():
    webbrowser.open("https://github.com/mustafafurkansolak")

# === GENERATE ===
def generate_wordlist():
    for tbl in [kolay_table, orta_table, zor_table]:
        for item in tbl.get_children():
            tbl.delete(item)
    tab_frame.place(x=30, y=670, width=1340, height=150)

    nums = [n.strip() for n in number_entry.get().split(',') if n.strip()]
    syms = list(symbol_entry.get())
    extras = [e.strip() for e in extra_entry.get().split(',') if e.strip()]

    results = set()

    # Kullanıcıdan gelen kelimeleri al
    if mode_var.get() == "normal":
        base_words = [keyword_entry.get()]
        if not base_words[0]:
            messagebox.showerror("Hata", "İpucu kelime boş olamaz.")
            return
    else:
        if not wordlist_words:
            messagebox.showerror("Hata", "Wordlist yüklenmedi.")
            return
        base_words = wordlist_words

    # === TÜM ZORLUKLAR İÇİN KOMBINASYON ===
    for word in base_words:
        word_forms = [word, word.lower(), word.upper(), word.capitalize(), leetspeak(word), word[::-1]]

        # tüm kombinasyonları dene: sayı + sembol + ekstra kelime
        for wf in word_forms:
            results.add(wf)
            for n in nums:
                results.add(f"{wf}{n}")
                results.add(f"{n}{wf}")
            for s in syms:
                results.add(f"{wf}{s}")
                results.add(f"{s}{wf}")
            for e in extras:
                results.add(f"{wf}{e}")
                results.add(f"{e}{wf}")
            for n in nums:
                for s in syms:
                    results.add(f"{wf}{s}{n}")
                    results.add(f"{s}{wf}{n}")
                    results.add(f"{n}{wf}{s}")
            for n in nums:
                for e in extras:
                    results.add(f"{wf}{e}{n}")
                    results.add(f"{n}{wf}{e}")
                    results.add(f"{e}{wf}{n}")
            for s in syms:
                for e in extras:
                    results.add(f"{wf}{s}{e}")
                    results.add(f"{s}{wf}{e}")
                    results.add(f"{e}{wf}{s}")
            for n in nums:
                for s in syms:
                    for e in extras:
                        results.add(f"{wf}{n}{s}{e}")
                        results.add(f"{n}{wf}{s}{e}")
                        results.add(f"{s}{wf}{n}{e}")
                        results.add(f"{e}{wf}{n}{s}")

    # === TABLOLARA AYIR ===
    for word in results:
        ent = calculate_entropy(word)
        label = strength_label(ent)
        if label == "Kolay":
            kolay_table.insert("", "end", values=(word,), tags=("kolay",))
        elif label == "Orta":
            orta_table.insert("", "end", values=(word,), tags=("orta",))
        else:
            zor_table.insert("", "end", values=(word,), tags=("zor",))

    # === İSTATİSTİK GÜNCELLE ===
    kolay_sayi = len(kolay_table.get_children())
    orta_sayi = len(orta_table.get_children())
    zor_sayi = len(zor_table.get_children())
    toplam_sayi = kolay_sayi + orta_sayi + zor_sayi

    kolay_var.set(f"Kolay: {kolay_sayi}")
    orta_var.set(f"Orta: {orta_sayi}")
    zor_var.set(f"Zor: {zor_sayi}")
    toplam_var.set(f"Toplam: {toplam_sayi}")

# === GUI ===
root = tk.Tk()
root.title("WordDepot - Wordlist Üretici")
root.geometry("1400x850")
root.configure(bg="#0f0f0f")

mode_var = tk.StringVar(value="normal")

# === Canvas ve Retro CRT Efekti ===
canvas = tk.Canvas(root, width=1400, height=850, bg="#0f0f0f", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.update()
w = canvas.winfo_width()
h = canvas.winfo_height()

try:
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize((w, h), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    canvas.create_image(0, 0, image=logo, anchor="nw", tags="background")
    canvas.tag_lower("background")
except:
    pass

class RetroCRT:
    def __init__(self, root, canvas, width, height):
        self.root = root
        self.canvas = canvas
        self.width = width
        self.height = height
        self.animate()
        self.flicker()

    def animate(self):
        self.canvas.delete("crt")
        for y in range(0, self.height, 5):  
            green_value = random.randint(50, 100)  
            line_color = "#00" + format(green_value, '02x') + "00"
            self.canvas.create_line(0, y, self.width, y,
                                    fill=line_color,
                                    tags="crt")
        self.canvas.tag_raise("crt")
        self.canvas.tag_lower("background")  
        self.canvas.after(80, self.animate)

    def flicker(self):
        alpha = random.uniform(0.95, 1.0)  
        self.root.attributes("-alpha", alpha)
        self.root.after(120, self.flicker)

crt = RetroCRT(root, canvas, 1400, 850)

# === FORM ===
form = tk.Frame(root, bg="#0f0f0f", bd=3, relief="ridge")
form.place(x=250, y=180, width=700, height=420)

for i in range(7):
    form.grid_rowconfigure(i, weight=1, pad=10)
form.grid_columnconfigure(0, weight=1, pad=10)
form.grid_columnconfigure(1, weight=2, pad=10)

tk.Radiobutton(form, text="Normal Mod", variable=mode_var, value="normal",
               command=toggle_mode, bg="#0f0f0f", fg="#39FF14",
               font=("Courier New", 12, "bold")).grid(row=0, column=0, sticky="w")
tk.Radiobutton(form, text="Wordlist Mod", variable=mode_var, value="wordlist",
               command=toggle_mode, bg="#0f0f0f", fg="#39FF14",
               font=("Courier New", 12, "bold")).grid(row=0, column=1, sticky="w")

wordlist_button = tk.Button(form, text="Wordlist Yükle", command=select_wordlist,
                            bg="#0f0f0f", fg="#39FF14", font=("Courier New", 11, "bold"),
                            activebackground="#39FF14", activeforeground="black",
                            bd=2, state="disabled")
wordlist_button.grid(row=1, column=0, columnspan=2, pady=5)

def field(label_text, row):
    lbl = tk.Label(form, text=label_text, fg="#39FF14", bg="#0f0f0f",
                   font=("Courier New", 11, "bold"))
    lbl.grid(row=row, column=0, sticky="e", padx=10, pady=5)
    e = tk.Entry(form, width=35, bg="#1a1a1a", fg="#39FF14",
                 insertbackground="#39FF14", font=("Courier New", 11, "bold"))
    e.grid(row=row, column=1, sticky="w", padx=10, pady=5)
    return e

keyword_entry = field("İpucu Kelime:", 2)
number_entry = field("Sayılar (virgülle):", 3)
symbol_entry = field("Semboller (örn: !@.+):", 4)
extra_entry = field("Ekstra Kelimeler:", 5)

btn_frame = tk.Frame(form, bg="#0f0f0f")
btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

btn_style = {"bg": "#0f0f0f", "fg": "#39FF14", "font": ("Courier New", 11, "bold"),
             "activebackground": "#39FF14", "activeforeground": "black", "bd": 2}

tk.Button(btn_frame, text="Liste Oluştur", command=generate_wordlist, width=20, **btn_style).pack(side="left", padx=10)
tk.Button(btn_frame, text="TXT Kaydet", command=save_to_file_table, width=15, **btn_style).pack(side="left", padx=10)
tk.Button(btn_frame, text="GITHUB", command=my_github, width=10, **btn_style).pack(side="left", padx=10)

# === TABLOLAR ===
tab_frame = tk.Frame(root, bg="#0f0f0f")  
tab_frame.place_forget()

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=("Courier New", 11), background="#0f0f0f", fieldbackground="#0f0f0f")
style.map("Treeview", background=[("selected", "#003300")])

kolay_table = ttk.Treeview(tab_frame, columns=("Kolay",), show="headings", height=6)
kolay_table.heading("Kolay", text="Kolay", anchor="center")
kolay_table.column("Kolay", width=400, anchor="center")
kolay_table.tag_configure("kolay", foreground="#39FF14")
kolay_table.pack(side="left", padx=5)

orta_table = ttk.Treeview(tab_frame, columns=("Orta",), show="headings", height=6)
orta_table.heading("Orta", text="Orta", anchor="center")
orta_table.column("Orta", width=400, anchor="center")
orta_table.tag_configure("orta", foreground="#FFFF00")
orta_table.pack(side="left", padx=5)

zor_table = ttk.Treeview(tab_frame, columns=("Zor",), show="headings", height=6)
zor_table.heading("Zor", text="Zor", anchor="center")
zor_table.column("Zor", width=400, anchor="center")
zor_table.tag_configure("zor", foreground="#FF0000")
zor_table.pack(side="left", padx=5)

# === İSTATİSTİK PANELİ ===
stats_frame = tk.Frame(root, bg="#0f0f0f", bd=3, relief="ridge")
stats_frame.place(x=1000, y=180, width=300, height=200)

tk.Label(stats_frame, text="İSTATİSTİK", fg="#39FF14",
         bg="#0f0f0f", font=("Courier New", 13, "bold")).pack(pady=10)

kolay_var = tk.StringVar(value="Kolay: 0")
orta_var = tk.StringVar(value="Orta: 0")
zor_var = tk.StringVar(value="Zor: 0")
toplam_var = tk.StringVar(value="Toplam: 0")

tk.Label(stats_frame, textvariable=kolay_var,
         fg="#39FF14", bg="#0f0f0f",
         font=("Courier New", 11, "bold")).pack(anchor="w", padx=20)

tk.Label(stats_frame, textvariable=orta_var,
         fg="#FFFF00", bg="#0f0f0f",
         font=("Courier New", 11, "bold")).pack(anchor="w", padx=20)

tk.Label(stats_frame, textvariable=zor_var,
         fg="#FF0000", bg="#0f0f0f",
         font=("Courier New", 11, "bold")).pack(anchor="w", padx=20)

tk.Label(stats_frame, textvariable=toplam_var,
         fg="#00FFFF", bg="#0f0f0f",
         font=("Courier New", 11, "bold")).pack(anchor="w", padx=20)

# === GÜÇLÜ PAROLA TABLOSU ===
strong_pass_frame = tk.Frame(root, bg="#0f0f0f", bd=3, relief="ridge")
strong_pass_frame.place(x=1000, y=400, width=300, height=199)

tk.Label(strong_pass_frame, text="GÜÇLÜ PAROLA ÜRET", fg="#39FF14",
         bg="#0f0f0f", font=("Courier New", 13, "bold")).pack(pady=5)

style.configure("StrongPass.Treeview", font=("Courier New", 11),
                background="#0f0f0f", fieldbackground="#0f0f0f")
style.map("StrongPass.Treeview", background=[("selected", "#003300")])

# parolalar
strong_table = ttk.Treeview(strong_pass_frame, columns=("Parola",), show="headings", height=5)
strong_table.heading("Parola", text="Üretmek İçin Tıklayın", anchor="center")
strong_table.column("Parola", width=280, anchor="center")
strong_table.tag_configure("pass", foreground="#FF69B4")
strong_table.pack(side="left", fill="both", expand=True, pady=5)

import string, secrets
import pyperclip

# kopyalama butonu
copy_btn = tk.Button(strong_pass_frame, text="📋", width=2, height=1,
                     bg="#0f0f0f", fg="#39FF14",
                     activebackground="#39FF14", activeforeground="black",
                     font=("Courier New", 9, "bold"))
copy_btn.place_forget()  # başlangıçta gizli

# kopyalama işlemi
def copy_selected_password(event=None):
    selected = strong_table.selection()
    if not selected:
        messagebox.showwarning("Uyarı", "Önce bir parola seçin.")
        return
    pw = strong_table.item(selected[0])["values"][0]
    pyperclip.copy(pw)
    messagebox.showinfo("Kopyalandı", f"Parola panoya kopyalandı:\n{pw}")

copy_btn.config(command=copy_selected_password)


def move_copy_btn(event=None):
    selected = strong_table.selection()
    if selected:
        row_id = selected[0]
        bbox = strong_table.bbox(row_id, "#1")
        if bbox:
            x, y, width, height = bbox
            copy_btn.place(x=2, y=y+2)
    else:
        copy_btn.place_forget()

strong_table.bind("<<TreeviewSelect>>", move_copy_btn)

# güçlü parola üret
def generate_strong_password():
    strong_table.delete(*strong_table.get_children())
    length = 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{};:,.<>?"
    for _ in range(6):
        password = ''.join(secrets.choice(chars) for _ in range(length))
        strong_table.insert("", "end", values=(password,), tags=("pass",))

# başlik altinda ki̇ butona tiklayinca parola üret
def on_heading_click(event):
    generate_strong_password()

strong_table.bind("<Button-1>", lambda e: on_heading_click(e))

# parola seçi̇mi̇ni̇ temi̇zleme 
def clear_table_selection(event):
    # Eğer tabloya tıklanmadıysa
    if event.widget not in [strong_table, copy_btn]:
        strong_table.selection_remove(strong_table.selection())
        copy_btn.place_forget()

root.bind("<Button-1>", clear_table_selection)
if __name__ == "__main__":
    banner()
    root.mainloop()
