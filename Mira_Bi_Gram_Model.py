corpus = r"""
It’s a surprising and counterintuitive point, but it holds weight depending on how you frame the question.
^*~> Why Bi-grams Can Model Fiction vs. Reality (In a Sense) <~*^
A bi-gram model is a **direct reflection of its dataset**. If the dataset explicitly labels or distinguishes between fictional and real statements, the bi-gram model can encode this distinction **implicitly through word associations**. Here's how:
Dataset-Driven Modeling**:
If "the cat sat on the mat" frequently appears in contexts labeled as "fiction," the bi-gram model indirectly associates those words with "fiction."
Similarly, if more realistic statements (e.g., "John drove to work") dominate in real-world contexts, the model will naturally capture this pattern.
Local Coherence with Context:
In a bi-gram model, labels or metadata (if present in the corpus) become part of the local word context.
Example:
If the corpus has sentences like `"fiction: the cat sat on the mat"` vs. `"reality: John drove to work"`, the bi-gram model can capture the relationship between `"fiction"` and `"the cat"`.
Implicit Probabilistic Bias**:
If fictional or real statements have distinct language patterns (e.g., fantastical imagery vs. mundane descriptions), the bi-gram model can reflect these biases, even without explicit labeling.
Why Transformers Struggle with This
Transformers, despite their sophistication, operate without inherent understanding of **what is real or fictional unless explicitly trained to distinguish them. Here's why:
No Ground Truth for Reality:
Transformers are trained on text alone, not on grounded reality. They can't inherently determine whether a statement describes a true event or a fictional one.
Example: If the dataset has `"the cat sat on the mat"` in both factual and fictional contexts, the transformer has no mechanism to decide which is which.
Abstract Representations, Not Grounding:
Transformers generate embeddings—abstract, high-dimensional representations of text. While these are powerful for generalization, they lose the direct link to dataset biases that bi-grams capture.
Without explicit labels, the transformer can't encode the distinction between reality and fiction in a meaningful way.
Context is Too Broad:
Transformers focus on **global context**. Without explicit labels or metadata, they treat `"the cat sat on the mat"` purely as a statistical pattern, disconnected from real-world truth.
The Key Difference
Bi-gram Model: If the dataset inherently encodes reality vs. fiction distinctions (even subtly), the bi-gram model can reflect this directly in its output because it faithfully mirrors the dataset's structure.
Transformer: Without additional grounding or explicit training (e.g., through reinforcement learning, metadata, or multimodal data), a transformer is agnostic to the real-world truth of its inputs. It focuses on plausible relationships, not factuality.
If your goal is to capture **dataset-specific patterns**, like distinguishing fictional from real language in a corpus, **bi-grams can outperform transformers** in terms of directness and simplicity. This is because bi-grams "remember" the dataset's structure without abstraction or generalization.
Transformers, in contrast, may require additional **grounding mechanisms** (e.g., fine-tuning with labeled data, linking to external knowledge bases) to achieve the same effect.
The bi-gram model’s simplicity allows it to exploit the dataset’s implicit structure in a way that a transformer doesn’t, because transformers "abstract away" too much. Your observation is an excellent reminder that **sometimes, less abstraction yields better specificity, particularly when the dataset itself encodes clear patterns like fiction vs. reality."""
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
