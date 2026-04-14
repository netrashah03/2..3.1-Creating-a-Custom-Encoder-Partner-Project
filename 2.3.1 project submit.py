import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw

#configuration
#use similar shades for "security"
color_0 = (30, 30, 30) #near black
color_1 = (35, 35, 35) #slightly lighter
threshold = 33 #halfway between 30 and 35
img_width = 200 #width of the barcode strip

#encoder logic
def text_to_bits(text):
    bits = ""
    for char in text:
        #convert char to 8-bit binary
        bits += bin(ord(char))[2:].zfill(8)
    return bits

def encode_action():
    message = entry_input.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Error", "Please enter a message!")
        return
    
    bit_sequence = text_to_bits(message)
    img_height = len(bit_sequence)

    #create the image
    img = Image.new("RGB", (img_width, img_height))
    draw = ImageDraw.Draw(img)

    for y, bit in enumerate(bit_sequence):
        color = color_0 if bit == '0' else color_1
        draw.line([(0, y), (img_width, y)], fill=color)

    save_path = "secret_barcode.png"
    img.save(save_path)
    messagebox.showinfo("Success", f"Encoded {len(message)} chars into {save_path}")


#Decoder Logic
def decode_action():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if not file_path:
        return
    
    try:
        img = Image.open(file_path)
        pixels = img.load()
        width, height = img.size

        bits = ""
        #scan the center column of the image
        for y in range(height):
            r, g, b = pixels[width // 2, y]
            bits += '0' if r < threshold else '1'

        #converts bits back to text
        decoded_text = ""
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                decoded_text += chr(int(byte, 2))

        text_result.config(state=tk.NORMAL)
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, decoded_text)
        text_result.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode: {e}")


# --- GUI LAYOUT ---
root = tk.Tk()
root.title("Barcode Gradient Messenger")
root.geometry("600x400")

# Left Frame (Sender)
frame_left = tk.LabelFrame(root, text="Sender (Encoder)", padx=10, pady=10)
frame_left.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

tk.Label(frame_left, text="Enter Secret Message:").pack()
entry_input = tk.Text(frame_left, height=10, width=30)
entry_input.pack(pady=5)

btn_encode = tk.Button(frame_left, text="Generate Image", command=encode_action, bg="lightblue")
btn_encode.pack(fill=tk.X)

# Right Frame (Receiver)
frame_right = tk.LabelFrame(root, text="Receiver (Decoder)", padx=10, pady=10)
frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

btn_decode = tk.Button(frame_right, text="Open & Decode Image", command=decode_action, bg="lightgreen")
btn_decode.pack(fill=tk.X, pady=5)

tk.Label(frame_right, text="Decoded Result:").pack()
text_result = tk.Text(frame_right, height=10, width=30, state=tk.DISABLED)
text_result.pack(pady=5)

root.mainloop()
