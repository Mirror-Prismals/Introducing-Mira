corpus = r"""corpus"""
import random
import re
import tkinter as tk



# Corpus preprocessing
ngram = {}
corpus = corpus.replace('\\', '\\\\')  # Escape backslashes
corpus = re.sub(r'\\[Uu][0-9A-Fa-f]{8}', '', corpus)  # Remove invalid \UXXXXXXXX sequences
corpus = re.sub(r'\\[xX][0-9A-Fa-f]{2}', '', corpus)  # Remove \xXX sequences
corpus = re.sub(r'\\.', '', corpus)  # Remove any remaining backslash escape sequences
corpus = corpus.lower().replace('"', '').replace('\\', '').replace("'", '').replace('\n', '')
corpus = corpus.replace(')', '').replace('(', '').replace('[', '').replace(']', '')
corpus = corpus.replace('’', '').replace("“", '').replace("”", '')

# Build the n-gram model
for sentence in corpus.split('.'):
    words = sentence.split(' ')
    for i in range(2, len(words)):
        word_pair = (words[i - 2], words[i - 1])
        if '' in word_pair:
            continue
        if word_pair not in ngram:
            ngram[word_pair] = []
        ngram[word_pair].append(words[i])

# Function to generate output banter
def generate_banter():
    if not ngram:
        return "Error: n-gram model is empty."
    word_pair = random.choice(list(ngram.keys()))
    output = word_pair[0] + ' ' + word_pair[1] + ' '
    while word_pair in ngram:
        third = random.choice(ngram[word_pair])
        output += third + ' '
        word_pair = (word_pair[1], third)
    return output.strip()

# Function to update text on the screen
def update_text():
    new_banter = generate_banter()
    text_widget.config(text=new_banter)
    root.after(30000, update_text)  # Schedule next update (5 seconds)

# Initialize Tkinter app
root = tk.Tk()
root.attributes('-fullscreen', True)  # Fullscreen mode
root.configure(bg="black")

# Create a label to display the banter
text_widget = tk.Label(root, text="", font=("Arial", 24), fg="white", bg="black", wraplength=root.winfo_screenwidth(), justify="center")
text_widget.pack(expand=True)

# Start the timer to update text
update_text()

# Bind Escape key to exit the app
root.bind("<Escape>", lambda e: root.destroy())

# Run the app
root.mainloop()
