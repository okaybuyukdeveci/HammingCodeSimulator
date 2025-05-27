import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Hamming fonksiyonları (Aynı)
def calculate_parity_bits_length(m):
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    return r

def insert_parity_bits(data_bits, r):
    n = len(data_bits) + r
    j = 0
    k = 0
    res = ''
    for i in range(1, n + 1):
        if i == 2 ** j:
            res += '0'
            j += 1
        else:
            res += data_bits[k]
            k += 1
    return res

def calculate_parity_bits(hamming_code, r):
    n = len(hamming_code)
    hamming_code = list(hamming_code)
    for i in range(r):
        idx = (2 ** i) - 1
        parity = 0
        for j in range(1, n + 1):
            if j & (2 ** i) and j != (2 ** i):
                parity ^= int(hamming_code[j - 1])
        hamming_code[idx] = str(parity)
    return ''.join(hamming_code)

def add_error(hamming_code, bit_pos):
    code = list(hamming_code)
    bit_pos -= 1
    if 0 <= bit_pos < len(code):
        code[bit_pos] = '1' if code[bit_pos] == '0' else '0'
    return ''.join(code)

def detect_error(received_code, r):
    n = len(received_code)
    syndrome = 0
    for i in range(r):
        parity = 0
        for j in range(1, n + 1):
            if j & (2 ** i):
                parity ^= int(received_code[j - 1])
        syndrome += parity * (2 ** i)
    return syndrome

def correct_error(received_code, error_pos):
    if error_pos == 0:
        return received_code
    error_pos -= 1
    code = list(received_code)
    code[error_pos] = '1' if code[error_pos] == '0' else '0'
    return ''.join(code)

# GUI Fonksiyonları
def encode_data():
    data = entry_data.get()
    if not all(bit in '01' for bit in data):
        messagebox.showerror("Hata", "Sadece 0 ve 1 girin!")
        return
    m = len(data)
    r = calculate_parity_bits_length(m)
    code_with_parity = insert_parity_bits(data, r)
    hamming_code = calculate_parity_bits(code_with_parity, r)
    entry_code.config(state='normal')
    entry_code.delete(0, tk.END)
    entry_code.insert(0, hamming_code)
    entry_code.config(state='readonly')

def add_error_to_code():
    bit_pos = entry_error_bit.get()
    if not bit_pos.isdigit():
        messagebox.showerror("Hata", "Hata bit konumunu girin!")
        return
    bit_pos = int(bit_pos)
    code = entry_code.get()
    errored_code = add_error(code, bit_pos)
    entry_errored.config(state='normal')
    entry_errored.delete(0, tk.END)
    entry_errored.insert(0, errored_code)
    entry_errored.config(state='readonly')

def detect_and_correct():
    received_code = entry_errored.get()
    if not received_code:
        messagebox.showerror("Hata", "Hatalı kod yok!")
        return
    m = len(entry_data.get())
    r = calculate_parity_bits_length(m)
    syndrome = detect_error(received_code, r)
    entry_syndrome.config(state='normal')
    entry_syndrome.delete(0, tk.END)
    entry_syndrome.insert(0, str(syndrome))
    entry_syndrome.config(state='readonly')
    corrected = correct_error(received_code, syndrome)
    entry_corrected.config(state='normal')
    entry_corrected.delete(0, tk.END)
    entry_corrected.insert(0, corrected)
    entry_corrected.config(state='readonly')

# GUI Tasarımı
root = tk.Tk()
root.title("🔧 Hamming SEC-DED Simülatörü")
root.geometry("500x400")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")  # Modern tema

# Başlık
ttk.Label(root, text="Hamming SEC-DED Simülatörü", font=("Helvetica", 16, "bold")).pack(pady=10)

# Çerçeve: Veri Girişi ve Kodlama
frame_input = ttk.LabelFrame(root, text="Veri Girişi", padding=10)
frame_input.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_input, text="Veri (8/16/32 bit)").grid(row=0, column=0, sticky="w", pady=2)
entry_data = ttk.Entry(frame_input, width=40)
entry_data.grid(row=0, column=1, padx=5, pady=2)
ttk.Button(frame_input, text="Encode", command=encode_data).grid(row=0, column=2, padx=5)

ttk.Label(frame_input, text="Hamming Code").grid(row=1, column=0, sticky="w", pady=2)
entry_code = ttk.Entry(frame_input, width=40, state='readonly')
entry_code.grid(row=1, column=1, padx=5, pady=2)

# Çerçeve: Hata Ekleme
frame_error = ttk.LabelFrame(root, text="Hata Ekleme", padding=10)
frame_error.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_error, text="Hata Bit Pozisyonu (1-N)").grid(row=0, column=0, sticky="w", pady=2)
entry_error_bit = ttk.Entry(frame_error, width=10)
entry_error_bit.grid(row=0, column=1, sticky="w", padx=5, pady=2)
ttk.Button(frame_error, text="Hata Ekle", command=add_error_to_code).grid(row=0, column=2, padx=5)

ttk.Label(frame_error, text="Hatalı Kod").grid(row=1, column=0, sticky="w", pady=2)
entry_errored = ttk.Entry(frame_error, width=40, state='readonly')
entry_errored.grid(row=1, column=1, padx=5, pady=2)

# Çerçeve: Tespit ve Düzeltme
frame_correct = ttk.LabelFrame(root, text="Hata Tespiti ve Düzeltme", padding=10)
frame_correct.pack(fill="x", padx=10, pady=5)

ttk.Button(frame_correct, text="Tespit ve Düzelt", command=detect_and_correct).grid(row=0, column=0, padx=5, pady=5)

ttk.Label(frame_correct, text="Sendrom (Hata Poz.)").grid(row=1, column=0, sticky="w", pady=2)
entry_syndrome = ttk.Entry(frame_correct, width=40, state='readonly')
entry_syndrome.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(frame_correct, text="Düzeltilmiş Kod").grid(row=2, column=0, sticky="w", pady=2)
entry_corrected = ttk.Entry(frame_correct, width=40, state='readonly')
entry_corrected.grid(row=2, column=1, padx=5, pady=2)

root.mainloop()
