class VelikaSlova:

    def __init__(self):
        self.name = 'Velika Slova'
        self.description = 'Changes first letter of every word to upper'

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def execute(self, textEditorModel, undoManager, clipboardStack):
        for line in textEditorModel.text:
            line_buff = []
            for word in line.split():
                word = word[0].upper() + word[1:]
                line_buff.append(word)
            textEditorModel.text[textEditorModel.text.index(line)] = ' '.join(line_buff)
            textEditorModel.text_notify()