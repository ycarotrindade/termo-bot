from textual.app import App
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input,Footer,Label,ListItem,ListView
from textual import on
from textual.validation import Function
from textual.containers import Vertical,Horizontal
from sieve import Filter,Letter

titulo = """
 ######   #######  ######   ##   ##   #####            ######    #####   ######
 # ## #    ##   #   ##  ##  ### ###  ##   ##            ##  ##  ##   ##  # ## #
   ##      ## #     ##  ##  #######  ##   ##            ##  ##  ##   ##    ##
   ##      ####     #####   #######  ##   ##  ######    #####   ##   ##    ##
   ##      ## #     ## ##   ## # ##  ##   ##            ##  ##  ##   ##    ##
   ##      ##   #   ##  ##  ##   ##  ##   ##            ##  ##  ##   ##    ##
  ####    #######  #### ##  ##   ##   #####            ######    #####    ####

"""

with open('palavras.txt','r') as file:
    ALL_WORDS = file.readlines()
    ALL_WORDS = list(map(lambda x:x.removesuffix("\n"),ALL_WORDS))

def is_five_words(word:str):
    if len(word) == 5:
        return True
    else:
        return False
    
class Pharse(Widget):
    text_var = reactive("")
    cursor_index = reactive(0)
    letter_changed = reactive(False)
    colored_text = ""
    list_of_chars = []
    
    def watch_letter_changed(self):
        self.change_color_text(self.cursor_index)
        self.letter_changed = False
    
    def watch_text_var(self):
        self.list_of_chars.clear()
        for letter in self.text_var:
            self.list_of_chars.append(Letter(letter,'white'))
    
    def watch_cursor_index(self):
        self.change_color_text(self.cursor_index)
    
    def change_color_text(self,cursor_index:int):
        self.colored_text = ""
        for index,letter in enumerate(self.list_of_chars):
            if index == self.cursor_index:
                self.colored_text += f"[bold reverse {letter.type}]{letter.char}[/]"
            else:
                self.colored_text += f"[{letter.type}]{letter.char}[/]"      
    
    def render(self):
        self.change_color_text(self.cursor_index)
        return f"{self.colored_text}"

class TermoBot(App):
    titulo = """[yellow]
 ######   #######  ######   ##   ##   #####            ######    #####   ######
 # ## #    ##   #   ##  ##  ### ###  ##   ##            ##  ##  ##   ##  # ## #
   ##      ## #     ##  ##  #######  ##   ##            ##  ##  ##   ##    ##
   ##      ####     #####   #######  ##   ##  ######    #####   ##   ##    ##
   ##      ## #     ## ##   ## # ##  ##   ##            ##  ##  ##   ##    ##
   ##      ##   #   ##  ##  ##   ##  ##   ##            ##  ##  ##   ##    ##
  ####    #######  #### ##  ##   ##   #####            ######    #####    ####
[/]
"""
    CSS_PATH = "global.tcss"
    pharse = Pharse()
    filter_object = Filter(ALL_WORDS)
    BINDINGS = [
        ('ctrl+z','enable_input','enable input back'),
        ('ctrl+a',"save_word",'save word and calc best outputs'),
        ('right','move_cursor_right','move cursor to right'),
        ('left','move_cursor_left','move cursor to left'),
        ("up","move_color","Change the letter color"),
        ("backspace","restart","Restart rounds"),
    ]
    
    def on_input_submitted(self,event:Input.Submitted):
        if event.validation_result.is_valid:
            self.query_one(Pharse).text_var = event.value
            event.input.disabled = True
            event.input.value = ""
        
    def compose(self):
        yield Label(self.titulo)
        yield Vertical(
         Input(id="pharse_input",placeholder="Insert words here",max_length=5,validators=[Function(is_five_words,"Thai is not a valid word")]),
         Pharse(id="phrase_label"),
         id="first_container"
        )
        yield ListView(id="wordlist")
        yield Footer()
    
    def action_enable_input(self):
      phrase_input = self.query_one("#pharse_input")
      phrase_label = self.query_one("#phrase_label")
      if phrase_input.disabled == True:
          phrase_input.disabled = False
          phrase_label.text_var = ""
          phrase_input.focus()
    
    def action_move_cursor_right(self):
        phrase_label = self.query_one("#phrase_label")
        if phrase_label.cursor_index < 4:
            phrase_label.cursor_index += 1
    
    def action_move_cursor_left(self):
        phrase_label = self.query_one("#phrase_label")
        if phrase_label.cursor_index > 0:
            phrase_label.cursor_index -= 1
    
    def action_move_color(self):
        phrase_label = self.query_one("#phrase_label")
        if len(phrase_label.text_var) == 5:
            cursor_index = phrase_label.cursor_index
            actual_letter = phrase_label.list_of_chars[cursor_index]
            if actual_letter.get_type_index() < len(actual_letter.TYPES_LIST) -1 :
                actual_letter.change_type(actual_letter.get_type_index()+1)
            else:
                actual_letter.change_type(0)
            phrase_label.letter_changed = True
    
    def action_save_word(self):
        list_view = self.query_one("#wordlist")
        list_view.clear()
        word = self.query_one("#phrase_label").list_of_chars
        calc_words = self.filter_object.process_word(word).sieve()
        for i in calc_words[:5]:
            list_view.append(ListItem(Label(f"{i}")))
    
    def action_restart(self):
        self.filter_object.reset_values()
        self.query_one("#wordlist").clear()
        phrase_input = self.query_one("#pharse_input")
        phrase_label = self.query_one("#phrase_label")
        if phrase_input.disabled == True:
            phrase_input.disabled = False
            phrase_label.text_var = ""
            phrase_input.focus()
        
    
        
if __name__ == "__main__":
    app = TermoBot()
    app.run()