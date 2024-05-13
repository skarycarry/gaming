import tkinter as tk
import pandas as pd
import yaml
import os
import numpy as np

class GameGUI:
    def __init__(self, master, fields, range_type, title):
        self.master = master
        self.fields = fields
        self.range_type = range_type
        self.title = title
        self.results = None
        self.setup_gui()

    def setup_gui(self):
        self.master.title(self.title)
        scrollbar = tk.Scrollbar(self.master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.master, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.entries = {}
        vcmd = self.master.register(self.validate_entry), '%P'
        for field in self.fields:
            frame_row = tk.Frame(self.frame)
            frame_row.pack(padx=10, pady=5, fill=tk.X)
            label = tk.Label(frame_row, text=field)
            label.pack(side=tk.LEFT)
            entry_text = '0.' if self.range_type == 'float0-1' else ''
            entry = tk.Entry(frame_row, validate='key', validatecommand=vcmd, justify=tk.LEFT)
            entry.insert(0, entry_text)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.entries[field] = entry

            entry.bind("<FocusIn>", self.on_focus_in)

        submit_button = tk.Button(self.frame, text='Submit', command=self.submit)
        submit_button.pack(side=tk.BOTTOM, pady=5)
        self.label_result = tk.Label(self.frame, text='')
        self.label_result.pack(side=tk.BOTTOM, fill=tk.X)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def on_focus_in(self, event):
        self.canvas.update_idletasks()
        
        # Get the widget's absolute position within the frame
        widget = event.widget
        widget_y = widget.winfo_y()
        
        # Include the y-coordinates of all parent widgets up to the frame that is directly placed on the canvas
        parent = widget.master
        while parent != self.frame:
            widget_y += parent.winfo_y()
            parent = parent.master
        
        # Calculate the new position to scroll to, by considering the top of the widget
        # should align with the top of the canvas
        canvas_height = self.canvas.winfo_height()
        total_scrollable_height = self.canvas.bbox("all")[3]
        
        # Calculating the fraction of the total scrollable height
        # The goal is to position the widget at the top of the canvas
        fraction = widget_y / total_scrollable_height
        
        # Applying the calculated fraction to the canvas's vertical scroll
        self.canvas.yview_moveto(fraction)


    def validate_entry(self, new_value):
        if not new_value.strip():
            return True
        if self.range_type == 'int1-10':
            try:
                value = int(new_value)
                return 1 <= value <= 10
            except ValueError:
                return False
        elif self.range_type == 'float0-1':
            try:
                value = float(new_value)
                return 0 <= value <= 1
            except ValueError:
                return False

    def submit(self):
        if self.range_type == 'int1-10':
            self.results = [int(self.entries[field].get().strip() or '0') for field in self.fields]
        elif self.range_type == 'float0-1':
            self.results = [float(self.entries[field].get().strip() or '0.0') for field in self.fields]
        self.label_result.config(text=str(self.results))
        self.master.destroy()
        return self.results

def load_axes():
    with open('../game_type_descriptions/game_factors.yaml', 'r') as file:
        data = yaml.safe_load(file)['Video_Game_Genres']
    axes = []
    for g in data:
        genre = data[g]
        axes.extend(genre['Key_Factors'])
        for s in genre['Subgenres']:
            axes.extend(genre['Subgenres'][s]['Factors'])
    return axes

def comparison(game_name):
    df = pd.read_csv('comparisons.csv', index_col=0) if os.path.exists('comparisons.csv') else pd.DataFrame(index=[], columns=[])
    if game_name not in df.columns:
        root = tk.Tk()
        fields = df.columns.tolist() if not df.empty else None
        if fields:
            app = GameGUI(root, fields, 'float0-1', f'Comparing to {game_name}')
            root.mainloop()
            scores = app.results
            s = df.columns.append(pd.Index([game_name]))
            new_row = pd.Series(scores + [1], index=s, name=game_name)
    
            # Add the new row to the DataFrame
            df = pd.concat([df, pd.DataFrame([new_row])], axis=0)
            
            # Add a new column for the same game_name
            df[game_name] = scores + [1]
        else:
            df[game_name] = [1]

    df.to_csv('comparisons.csv')

def new_game(game_name):
    if os.path.exists(f'{game_name}.yaml'):
        return
    fields = load_axes()
    root = tk.Tk()
    app = GameGUI(root, fields, 'int1-10', f'{game_name} Rating')
    root.mainloop()
    output = app.results
    output = {fields[i]: output[i] for i in range(len(fields))}
    if output:
        filename = f'../data/{game_name}.yaml'
        with open(filename, 'w') as file:
            yaml.dump(output, file, default_flow_style=False)

def main():
    games = [game.strip() for game in open('../data/games.txt').readlines()]

    for game_name in games:
        new_game(game_name)
        comparison(game_name)

if __name__ == "__main__":
    main()