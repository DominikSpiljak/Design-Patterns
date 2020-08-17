import tkinter as tk

class Statistika:

    def __init__(self):
        self.name = 'Statistika'
        self.description = 'Displays statistics for given text'

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def execute(self, textEditorModel, undoManager, clipboardStack):
        number_of_lines = len(textEditorModel.text)
        number_of_words = sum([len(line.split()) for line in textEditorModel.text])
        number_of_letters = 0
        for line in textEditorModel.text:
            for word in line.split():
                number_of_letters += len(word)
        tk.messagebox.showinfo('Statistika', 'Number of lines: {}\nNumber of words: {}\nNumber of letters: {}'
        .format(number_of_lines, number_of_words, number_of_letters))