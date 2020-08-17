from __future__ import annotations
from abc import ABC, abstractmethod
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import importlib.util

class SingletonMeta(type):

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Plugin(ABC):
    
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getDescription(self):
        pass

    @abstractmethod
    def execute(self, *args):
        pass


class CursorSubject(ABC):

    @abstractmethod
    def cursor_attach(self, observer):
        pass

    @abstractmethod
    def cursor_detach(self, observer):
        pass

    @abstractmethod
    def cursor_notify(self):
        pass


class CursorObserver(ABC):

    @abstractmethod
    def updateCursorLocation(self, cursorLocation):
        pass


class TextSubject(ABC):

    @abstractmethod
    def text_attach(self, observer):
        pass

    @abstractmethod
    def text_detach(self, observer):
        pass

    @abstractmethod
    def text_notify(self):
        pass


class TextObserver(ABC):

    @abstractmethod
    def updateText(self):
        pass


class ClipboardSubject(ABC):

    @abstractmethod
    def clip_attach(self, observer):
        pass

    @abstractmethod
    def clip_detach(self, observer):
        pass

    @abstractmethod
    def clip_notify(self):
        pass


class ClipboardObserver(ABC):

    @abstractmethod
    def updateClipboard(self):
        pass


class UndoStackSubject(ABC):

    @abstractmethod
    def undo_attach(self, observer):
        pass

    @abstractmethod
    def undo_detach(self, observer):
        pass

    @abstractmethod
    def undo_notify(self):
        pass


class UndoStackObserver(ABC):
    
    @abstractmethod
    def updateUndo(self):
        pass


class Action(ABC):

    @abstractmethod
    def execute_do(self):
        pass
    
    @abstractmethod
    def execute_undo(self):
        pass


class EditAction():
    def __init__(self, restore_command, command, past_state, args):
        self.restore_command = restore_command
        self.past_state = past_state
        self.command = command
        self.args = args
    
    def execute_do(self):
        if self.args is not None:
            self.command(self.args)
        else:
            self.command()

    def execute_undo(self):
        self.restore_command(self.past_state)


class UndoManager(UndoStackSubject):

    __metaclass__ = SingletonMeta

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self._undo_observers = []
    
    def empty_undo(self):
        if len(self.undo_stack):
            return False
        return True
    
    def empty_redo(self):
        if len(self.redo_stack):
            return False
        return True

    def undo(self):
        if not self.empty_undo():
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            action.execute_undo()
        self.undo_notify()

    def redo(self):
        if not self.empty_redo():
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            action.execute_do()
        self.undo_notify()
    
    def push(self, editAction):
        self.undo_stack.append(editAction)
        self.undo_notify()

    def undo_attach(self, observer):
        self._undo_observers.append(observer)

    def undo_detach(self, observer):
        self._undo_observers.remove(observer)

    def undo_notify(self):
        for o in self._undo_observers:
            o.updateUndo()
        

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class LocationRange:
    def __init__(self, location1, location2):
        self.location1 = location1
        self.location2 = location2


class ClipboardStack(ClipboardSubject):
    def __init__(self):
        self.texts = []
        self._clip_observers = []
    
    def push(self, text):
        self.texts.append(text)
        self.clip_notify()

    def pop(self):
        if self.empty():
            return -1
        ret_val = self.texts.pop()
        self.clip_notify()
        return ret_val
    
    def read(self):
        if self.empty():
            return -1
        return self.texts[-1]
    
    def empty(self):
        if len(self.texts):
            return False
        return True
    
    def delete(self):
        self.texts = []

    def clip_attach(self, observer):
        self._clip_observers.append(observer)

    def clip_detach(self, observer):
        self._clip_observers.remove(observer)

    def clip_notify(self):
        for o in self._clip_observers:
            o.updateClipboard()


class TextEditorModel(CursorSubject, TextSubject):

    def __init__(self, text):
        self.text = text.split('\n')
        self.selectionRange = None
        self.cursorLocation = Location(len(self.text[-1]), len(self.text) - 1)
        self.undoManager = UndoManager()
        self._cursor_observers = []
        self._text_observers = []

    def allLines(self):
        return iter(self.text)

    def linesRange(self, index1, index2):
        return iter(self.text[index1:index2])

    def moveCursorLeft(self):
        if self.cursorLocation.x == 0:
            if self.cursorLocation.y == 0:
                pass
            else:
                self.cursorLocation.y -= 1
                self.cursorLocation.x = len(self.text[self.cursorLocation.y])
        else:
            self.cursorLocation.x -= 1
        self.cursor_notify()

    def moveCursorRight(self):
        if self.cursorLocation.y == len(self.text):
            pass
        elif self.cursorLocation.x == len(self.text[self.cursorLocation.y]):
            if self.cursorLocation.y < len(self.text) - 1:
                self.cursorLocation.x = 0
                self.cursorLocation.y += 1
        else:
            self.cursorLocation.x += 1
        self.cursor_notify()

    def moveCursorUp(self):
        if self.cursorLocation.y == 0:
                pass
        else:
            self.cursorLocation.y -= 1
            if self.cursorLocation.x > len(self.text[self.cursorLocation.y]):
                self.cursorLocation.x = len(self.text[self.cursorLocation.y])
        self.cursor_notify()

    def moveCursorDown(self):
        if self.cursorLocation.y < len(self.text) - 1:
            self.cursorLocation.y += 1
            if self.cursorLocation.x > len(self.text[self.cursorLocation.y]):
                self.cursorLocation.x = len(self.text[self.cursorLocation.y])
            self.cursor_notify()

    def restore(self, state):
        self.cursorLocation = state[0]
        self.text = state[1]
        self.selectionRange = state[2]
        try:
            self.cursor_notify()
        except IndexError:
            pass
        self.text_notify()


    def deleteBefore(self):
        if self.cursorLocation.y != 0 or self.cursorLocation.x != 0:
            editAction = EditAction(self.restore, self.deleteBefore, 
            [Location(self.cursorLocation.x, self.cursorLocation.y), self.text.copy(), self.selectionRange], None)
            self.undoManager.push(editAction)
            if self.cursorLocation.x != 0:
                self.text[self.cursorLocation.y] = self.text[self.cursorLocation.y][:self.cursorLocation.x - 1] + \
                                                   self.text[self.cursorLocation.y][self.cursorLocation.x:]
            else:
                self.text[self.cursorLocation.y - 1] =  self.text[self.cursorLocation.y - 1] +  self.text[self.cursorLocation.y]
                self.text.pop(self.cursorLocation.y)
            self.text_notify()
            self.moveCursorLeft()
            

    def deleteAfter(self):
        if self.cursorLocation.y != len(self.text) - 1 or self.cursorLocation.x != len(self.text[self.cursorLocation.y]):
            editAction = EditAction(self.restore, self.deleteAfter, 
            [Location(self.cursorLocation.x, self.cursorLocation.y), self.text.copy(), self.selectionRange], None)
            self.undoManager.push(editAction)
            if self.cursorLocation.x != len(self.text[self.cursorLocation.y]):
                self.text[self.cursorLocation.y] = self.text[self.cursorLocation.y][:self.cursorLocation.x] + \
                                                   self.text[self.cursorLocation.y][self.cursorLocation.x + 1:]
            else:
                self.text[self.cursorLocation.y]=  self.text[self.cursorLocation.y] +  self.text[self.cursorLocation.y + 1]
                self.text.pop(self.cursorLocation.y + 1)
            self.text_notify()
            self.cursor_notify()

    def _get_selection_range(self, location_range):
        if location_range.location1.x == location_range.location2.x and location_range.location1.y == location_range.location2.y:
            self.selectionRange = None
            self.text_notify()
            self.cursor_notify()
            return
        #from loc_start to loc_end
        if location_range.location1.y > location_range.location2.y:
            loc_start = location_range.location2
            loc_end = location_range.location1
        elif location_range.location1.y < location_range.location2.y:
            loc_start = location_range.location1
            loc_end = location_range.location2
        else:
            if location_range.location1.x > location_range.location2.x:
                loc_start = location_range.location2
                loc_end = location_range.location1
            elif location_range.location1.x <= location_range.location2.x:
                loc_start = location_range.location1
                loc_end = location_range.location2
        return [loc_start, loc_end]

    
    def get_selection_text(self, location_range):
        selectionRange = self._get_selection_range(location_range)
        if selectionRange is None:
            return ''
        loc_start, loc_end = self._get_selection_range(location_range)
        if loc_start.y == loc_end.y:
            return self.text[loc_start.y][loc_start.x:loc_end.x]
        else:
            text = ''
            text += self.text[loc_start.y][loc_start.x:] + '\n'
            for y in range(loc_start.y + 1, loc_end.y):
                text += self.text[y] + '\n'
            text += self.text[loc_end.y][:loc_end.x]
            return text
        

    def deleteRange(self, location_range):

        editAction = EditAction(self.restore, self.deleteRange,
         [Location(self.cursorLocation.x, self.cursorLocation.y), self.text.copy(), self.selectionRange], location_range)
        self.undoManager.push(editAction)
        selectionRange = self._get_selection_range(location_range)
        if selectionRange is None:
            return
        loc_start, loc_end = self._get_selection_range(location_range)
        if loc_start.y < loc_end.y:
            self.text[loc_start.y] = self.text[loc_start.y][:loc_start.x]
            removed_rows_counter = 0
            for i in range(loc_start.y + 1, loc_end.y):
                self.text.pop(i - removed_rows_counter)
                removed_rows_counter += 1
            line = self.text.pop(loc_end.y - removed_rows_counter)
            self.text[loc_start.y] += line[loc_end.x:]
        else:
            self.text[loc_start.y] = self.text[loc_start.y][:loc_start.x] + self.text[loc_end.y][loc_end.x:]
        self.selectionRange = None
        self.text_notify()
        self.cursorLocation = loc_start
        self.cursor_notify()

    def insert(self, chars):
        editAction = EditAction(self.restore, self.insert, [Location(self.cursorLocation.x, self.cursorLocation.y), self.text.copy(), self.selectionRange], chars)
        self.undoManager.push(editAction)
        if chars == '\r':
            index = self.cursorLocation.y
            line = self.text.pop(index)
            self.text.insert(index, line[self.cursorLocation.x:])
            self.text.insert(index, line[:self.cursorLocation.x])
            self.text_notify()
            self.cursorLocation.x = 0
            self.cursorLocation.y = index + 1
            self.cursor_notify()
            
        else:
            self.text[self.cursorLocation.y] = self.text[self.cursorLocation.y][:self.cursorLocation.x] + \
                                            chars + self.text[self.cursorLocation.y][self.cursorLocation.x:]
            if '\n' in self.text[self.cursorLocation.y]:
                split_text = self.text.pop(self.cursorLocation.y).split('\n')
                split_text.reverse()
                for split in split_text:
                    self.text.insert(self.cursorLocation.y, split)
            self.text_notify()
            for _ in chars:
                self.moveCursorRight()
        
    def getSelectionRange(self):
        return self.selectionRange

    def setSelectionRange(self, selectionRange):
        self.selectionRange = selectionRange
        self.text_notify()

    def cursor_attach(self, observer):
        self._cursor_observers.append(observer)

    def cursor_detach(self, observer):
        self._cursor_observers.remove(observer)

    def cursor_notify(self):
        for o in self._cursor_observers:
            o.updateCursorLocation(self.cursorLocation)

    def text_attach(self, observer):
        self._text_observers.append(observer)

    def text_detach(self, observer):
        self._text_observers.remove(observer)

    def text_notify(self):
        for o in self._text_observers:
            o.updateText()


class TextEditor(tk.Tk, CursorObserver, TextObserver, ClipboardObserver, UndoStackObserver):

    def __init__(self, textEditorModel, clipboardStack):
        super().__init__()
        self.clipboardStack = clipboardStack
        self.textEditorModel = textEditorModel
        self.clipboardStack.clip_attach(self)
        self.textEditorModel.cursor_attach(self)
        self.textEditorModel.text_attach(self)
        self.textEditorModel.undoManager.undo_attach(self)
        self.plugins = {}
        self.filepath = None
        self.textChars = []
        self.cursor = None
        self.highlight = []
        self._initUI()
        self.mainloop()

    def _initUI(self):
        self.geometry('860x600')
        self.title("Grafičko sučelje za uređivač teksta.")
        self.initMenubar()
        self.initToolbar()
        self.initStatusBar()
        self.bind('<Key>', self.insert)
        self.bind('<Up>', self.moveCursor)
        self.bind('<Down>', self.moveCursor)
        self.bind('<Left>', self.moveCursor)
        self.bind('<Right>', self.moveCursor)
        self.bind('<BackSpace>', self.delete)
        self.bind('<Delete>', self.delete)
        self.bind('<Shift-Left>', self.textHighlighting)
        self.bind('<Shift-Right>', self.textHighlighting)
        self.bind('<Shift-Up>', self.textHighlighting)
        self.bind('<Shift-Down>', self.textHighlighting)
        self.bind('<Control-c>', self.clipboardAction)
        self.bind('<Control-v>', self.clipboardAction)
        self.bind('<Control-x>', self.clipboardAction)
        self.bind('<Control-V>', self.clipboardAction)
        self.bind('<Control-z>', self.undoAction)
        self.bind('<Control-y>', self.undoAction)
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self._show_text()
        self._draw_cursor(self.textEditorModel.cursorLocation.x, self.textEditorModel.cursorLocation.y)

    def initStatusBar(self):
        self.status_label = tk.Label(self, text="Cursor position: ({}, {}), Number of lines: {}"
                            .format(self.textEditorModel.cursorLocation.x + 1, self.textEditorModel.cursorLocation.y + 1, len(self.textEditorModel.text)),
                            borderwidth=2, relief="groove")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def initToolbar(self):
        # Undo, Redo, Cut, Copy, Paste
        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.paste_button = tk.Button(self.toolbar, relief=tk.FLAT, text="Paste", command=self.paste, state='disabled')
        self.copy_button = tk.Button(self.toolbar, relief=tk.FLAT, text="Copy", command=self.copy, state='disabled')
        self.cut_button = tk.Button(self.toolbar, relief=tk.FLAT, text="Cut", command=self.cut, state='disabled')
        self.redo_button = tk.Button(self.toolbar, relief=tk.FLAT, text="Redo", command=self.textEditorModel.undoManager.redo, state='disabled')
        self.undo_button = tk.Button(self.toolbar, relief=tk.FLAT, text="Undo", command=self.textEditorModel.undoManager.undo, state='disabled')
        self.paste_button.pack(side=tk.LEFT)
        self.copy_button.pack(side=tk.LEFT)
        self.cut_button.pack(side=tk.LEFT)
        self.redo_button.pack(side=tk.LEFT)
        self.undo_button.pack(side=tk.LEFT)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def initMenubar(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Open', command=self._open)
        self.filemenu.add_command(label='Save', command=self._save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self._close_window)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label='Undo', command=self.textEditorModel.undoManager.undo, state='disabled')
        self.edit_menu.add_command(label='Redo', command=self.textEditorModel.undoManager.redo, state='disabled')
        self.edit_menu.add_command(label='Cut', command=self.cut, state='disabled')
        self.edit_menu.add_command(label='Copy', command=self.copy, state='disabled')
        self.edit_menu.add_command(label='Paste', command=self.paste, state='disabled')
        self.edit_menu.add_command(label='Paste and Take', command=self.paste_and_take, state='disabled')
        self.edit_menu.add_command(label='Delete selection', command=self.delete_selection, state='disabled')
        self.edit_menu.add_command(label='Clear document', command=self.clear_document)
        self.menubar.add_cascade(label='Edit', menu=self.edit_menu)
        self.move_menu = tk.Menu(self.menubar, tearoff=0)
        self.move_menu.add_command(label='Cursor to document start', command=lambda : self.move_cursor('start'))
        self.move_menu.add_command(label='Cursor to document end', command=lambda : self.move_cursor('end'))
        self.menubar.add_cascade(label='Move', menu=self.move_menu)
        self.plugin_menu = tk.Menu(self.menubar, tearoff=0)
        self.plugin_menu.add_command(label='Add plugin', command=self.find_plugins)
        self.plugin_menu.add_separator()
        self.menubar.add_cascade(label='Plugins', menu=self.plugin_menu)
        self.config(menu=self.menubar)

    def find_plugins(self):
        ftypes = [('Python files', '*.py')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            plugin = self.load_plugin(fl)
            self.plugin_menu.add_command(label=plugin.getName(),
            command=lambda: plugin.execute(self.textEditorModel, self.textEditorModel.undoManager, self.clipboardStack))

    def load_plugin(self, fl):
        spec = importlib.util.spec_from_file_location("module.name", fl)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return getattr(foo, os.path.split(fl)[-1].replace('.py', ''))()

    def _open(self):
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            with open(fl, 'r') as inp:
                inp_content = inp.read()
                self.textEditorModel.cursor_detach(self)
                self.textEditorModel.text_detach(self)
                self.textEditorModel.undoManager.undo_detach(self)
                self.clipboardStack.clip_detach(self)

                self.textEditorModel = TextEditorModel(inp_content)
                self.clipboardStack.clip_attach(self)
                self.textEditorModel.cursor_attach(self)
                self.textEditorModel.text_attach(self)
                self.textEditorModel.undoManager.undo_attach(self)
                self.filepath = None
                self.textChars = []
                self.cursor = None
                self.highlight = []
                self._show_text()
                self._draw_cursor(self.textEditorModel.cursorLocation.x, self.textEditorModel.cursorLocation.y)

    def _save(self):
        if self.filepath is None:
            formats = [('Text file', '*.txt'), ('Python script', '*.py'), ('All', '.*')]
            filename = tk.filedialog.asksaveasfilename(filetypes=formats)
            if filename:
                with open(filename, 'w') as out:
                    out.write('\n'.join(self.textEditorModel.text))
                self.filepath = filename
        else:
            with open(self.filename, 'w') as out:
                out.write('\n'.join(self.textEditorModel.text))

    def move_cursor(self, position):
        if position == 'start':
            self.textEditorModel.cursorLocation = Location(0, 0)
        else:
            self.textEditorModel.cursorLocation = Location(len(self.textEditorModel.text[-1]), len(self.textEditorModel.text) - 1)
        self.updateCursorLocation(self.textEditorModel.cursorLocation)

    def undoAction(self, event):
        if event.keysym == 'z':
            self.textEditorModel.undoManager.undo()
        else:
            self.textEditorModel.undoManager.redo()

    def clipboardAction(self, event):
        if event.keysym == 'c':
            self.copy()
        elif event.keysym == 'v':
            self.paste()
        elif event.keysym == 'x':
            self.cut()
        else:
            self.paste_and_take()

    def clear_document(self):
        self.textEditorModel.cursor_detach(self)
        self.textEditorModel.text_detach(self)
        self.textEditorModel.undoManager.undo_detach(self)
        self.clipboardStack.clip_detach(self)

        self.textEditorModel = TextEditorModel("")
        self.clipboardStack.clip_attach(self)
        self.textEditorModel.cursor_attach(self)
        self.textEditorModel.text_attach(self)
        self.textEditorModel.undoManager.undo_attach(self)
        self.filepath = None
        self.textChars = []
        self.cursor = None
        self.highlight = []
        self._show_text()
        self._draw_cursor(self.textEditorModel.cursorLocation.x, self.textEditorModel.cursorLocation.y)

    def cut(self):
        if self.textEditorModel.getSelectionRange() is not None:
                self.clipboardStack.push(self.textEditorModel.get_selection_text(self.textEditorModel.getSelectionRange()))
                self.textEditorModel.deleteRange(self.textEditorModel.getSelectionRange())
                for hl in self.highlight:
                    self.canvas.delete(hl)
    
    def copy(self):
        if self.textEditorModel.getSelectionRange() is not None:
                self.clipboardStack.push(self.textEditorModel.get_selection_text(self.textEditorModel.getSelectionRange()))

    def paste(self):
        if self.textEditorModel.getSelectionRange() is not None:
            self.textEditorModel.deleteRange(self.textEditorModel.getSelectionRange())
            for hl in self.highlight:
                self.canvas.delete(hl)
        text = self.clipboardStack.read()
        if text != -1:
            self.textEditorModel.insert(text)

    def paste_and_take(self):
        if self.textEditorModel.getSelectionRange() is not None:
                self.textEditorModel.deleteRange(self.textEditorModel.getSelectionRange())
                for hl in self.highlight:
                    self.canvas.delete(hl)
        text = self.clipboardStack.pop()
        if text != -1:
            self.textEditorModel.insert(text)

    def insert(self, event):
        if 'Control' in event.keysym:
            return
        if self.textEditorModel.getSelectionRange() is not None:
            self.textEditorModel.deleteRange(self.textEditorModel.getSelectionRange())
            for hl in self.highlight:
                self.canvas.delete(hl)
        self.textEditorModel.insert(event.char)

    def moveCursor(self, event):
        self.textEditorModel.setSelectionRange(None)
        for hl in self.highlight:
            self.canvas.delete(hl)
        if event.keysym == 'Up':
            self.textEditorModel.moveCursorUp()
        elif event.keysym == 'Down':
            self.textEditorModel.moveCursorDown()
        elif event.keysym == 'Right':
            self.textEditorModel.moveCursorRight()
        else:
            self.textEditorModel.moveCursorLeft()

    def delete(self, event):
        if self.textEditorModel.selectionRange is not None:
            self.textEditorModel.deleteRange(self.textEditorModel.getSelectionRange())
        else:
            if event.keysym == 'Delete':
                self.textEditorModel.deleteAfter()
            else:
                self.textEditorModel.deleteBefore()

    def delete_selection(self):
        if self.textEditorModel.selectionRange is not None:
            self.textEditorModel.deleteRange(self.textEditorModel.getSelectionRange())

    def textHighlighting(self, event):
        if self.textEditorModel.selectionRange is None:
                location1 = [self.textEditorModel.cursorLocation.x, self.textEditorModel.cursorLocation.y]
                if event.keysym == 'Right': 
                    self.textEditorModel.moveCursorRight()
                elif event.keysym == 'Left':
                    self.textEditorModel.moveCursorLeft()
                elif event.keysym == 'Up':
                    self.textEditorModel.moveCursorUp()
                else:
                    self.textEditorModel.moveCursorDown()
                location2 = self.textEditorModel.cursorLocation
                self.textEditorModel.setSelectionRange(LocationRange(Location(location1[0], location1[1]), location2))
        else:
            if event.keysym == 'Right': 
                self.textEditorModel.moveCursorRight()
            elif event.keysym == 'Left':
                self.textEditorModel.moveCursorLeft()
            elif event.keysym == 'Up':
                self.textEditorModel.moveCursorUp()
            else:
                self.textEditorModel.moveCursorDown()
            location2 = self.textEditorModel.cursorLocation
            self.textEditorModel.setSelectionRange(LocationRange(self.textEditorModel.getSelectionRange().location1, location2))
        self._draw_highlight(self.textEditorModel.getSelectionRange().location1, self.textEditorModel.getSelectionRange().location2)
    
    def _draw_highlight(self, location1, location2):
        for hl in self.highlight:
            self.canvas.delete(hl)
        if location1.y == location2.y:
            hl = self.canvas.create_rectangle(self.textChars[location1.y][location1.x][0], self.textChars[location1.y][location1.x][1],
                                        self.textChars[location2.y][location2.x][0], self.textChars[location2.y][location2.x][1] + 20,
                                        stipple="gray12", fill = 'blue', outline='blue')
            self.highlight.append(hl)
        else:
            #from loc_start to loc_end
            if location1.y > location2.y:
                loc_start = location2
                loc_end = location1
            else:
                loc_start = location1
                loc_end = location2
            for y in range(loc_start.y, loc_end.y + 1):
                #Row is equal to start and highlight goes from loc_start.x
                if y == loc_start.y:
                    hl = self.canvas.create_rectangle(self.textChars[y][loc_start.x][0], self.textChars[y][loc_start.x][1],
                                        self.textChars[y][-1][0], self.textChars[y][-1][1] + 20,
                                        stipple="gray12", fill = 'blue', outline='blue')
                    self.highlight.append(hl)
                #Row is equal to end and highlight goes to loc_end.x
                elif y == loc_end.y:
                    hl = self.canvas.create_rectangle(self.textChars[y][0][0], self.textChars[y][0][1],
                                        self.textChars[y][loc_end.x][0], self.textChars[y][loc_end.x][1] + 20,
                                        stipple="gray12", fill = 'blue', outline='blue')
                    self.highlight.append(hl)
                #Row is between start and end and highlight goes through whole row
                else:
                    hl = self.canvas.create_rectangle(self.textChars[y][0][0], self.textChars[y][0][1],
                                        self.textChars[y][-1][0], self.textChars[y][-1][1] + 20,
                                        stipple="gray12", fill = 'blue', outline='blue')
                    self.highlight.append(hl)       
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def updateCursorLocation(self, cursorLocation):
        self._draw_cursor(cursorLocation.x, cursorLocation.y)
        self.status_label.config(text="Cursor position: ({}, {}), Number of lines: {}"
                            .format(self.textEditorModel.cursorLocation.x + 1, self.textEditorModel.cursorLocation.y + 1, len(self.textEditorModel.text)))

    def updateClipboard(self):
        if self.clipboardStack.empty():
            self.edit_menu.entryconfig("Paste", state="disabled")
            self.edit_menu.entryconfig("Paste and Take", state="disabled")
            self.paste_button.config(state=tk.DISABLED)
        else:
            self.edit_menu.entryconfig("Paste", state="normal")
            self.edit_menu.entryconfig("Paste and Take", state="normal")
            self.paste_button.config(state=tk.NORMAL)

    def updateText(self):
        if self.textEditorModel.getSelectionRange() is None:
            self.edit_menu.entryconfig("Cut", state="disabled")
            self.edit_menu.entryconfig("Copy", state="disabled")
            self.edit_menu.entryconfig("Delete selection", state="disabled")
            self.copy_button.config(state=tk.DISABLED)
        else:
            self.edit_menu.entryconfig("Cut", state="normal")
            self.edit_menu.entryconfig("Copy", state="normal")
            self.edit_menu.entryconfig("Delete selection", state="normal")
            self.copy_button.config(state=tk.NORMAL)
        self._show_text()
        self.status_label.config(text="Cursor position: ({}, {}), Number of lines: {}"
                                .format(self.textEditorModel.cursorLocation.x + 1, self.textEditorModel.cursorLocation.y + 1, len(self.textEditorModel.text)))

    def updateUndo(self):
        if self.textEditorModel.undoManager.empty_undo():
            self.edit_menu.entryconfig("Undo", state="disabled")
            self.undo_button.config(state=tk.DISABLED)
        else:
            self.edit_menu.entryconfig("Undo", state="normal")
            self.undo_button.config(state=tk.NORMAL)
        if self.textEditorModel.undoManager.empty_redo():
            self.edit_menu.entryconfig("Redo", state="disabled")
            self.redo_button.config(state=tk.DISABLED)
        else:
            self.edit_menu.entryconfig("Redo", state="normal")
            self.redo_button.config(state=tk.NORMAL)

    def _draw_cursor(self, x, y):
        self.canvas.delete(self.cursor)
        self.cursor = self.canvas.create_line(self.textChars[y][x][0], self.textChars[y][x][1],
                                              self.textChars[y][x][0], self.textChars[y][x][1] + 15, fill="#000")
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def _show_text(self):
        self.canvas.delete("all")
        self.textChars = []
        y = 10
        for i, line in enumerate(self.textEditorModel.allLines()):
            self.textChars.append([])
            x = 10
            for char in line:
                text = self.canvas.create_text(x, y, anchor=tk.NW, text=char)
                self.textChars[i].append([x, y])
                x += (self.canvas.bbox(text)[2] - self.canvas.bbox(text)[0])
            self.textChars[i].append([x, y])
            y += 20
        self.canvas.pack(fill=tk.BOTH, expand=1)
            
    def _close_window(self):
        self.destroy()
    

if __name__ == "__main__":
    textEditorModel = TextEditorModel("")
    clipboardStack = ClipboardStack()
    TextEditor(textEditorModel, clipboardStack)
