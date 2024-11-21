
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tree Menu Executor")
        self.root.configure(bg="black")
        
        # Menu principal
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Botão para carregar o arquivo .tree
        self.load_button = tk.Button(
            root,
            text="Load .tree File",
            bg="black",
            fg="white",
            command=self.load_tree_file
        )
        self.load_button.pack(pady=10)

    def load_tree_file(self):
        tree_path = filedialog.askopenfilename(filetypes=[("Tree Files", "*.tree")])
        if not tree_path:
            return

        try:
            with open(tree_path, "r") as file:
                lines = file.readlines()

            if not lines:
                messagebox.showerror("Error", "The .tree file is empty!")
                return

            # Clear the menu bar
            self.menu_bar.delete(0, tk.END)

            current_menu = None

            for line in lines:
                line = line.rstrip("\n")
                if not line.strip():
                    continue

                # Detect menu titles (no leading space)
                if not line.startswith(" "):
                    current_menu = tk.Menu(self.menu_bar, tearoff=0)
                    self.menu_bar.add_cascade(label=line, menu=current_menu)
                else:
                    # Detect submenus (leading space)
                    if current_menu is not None:
                        parts = line.strip().split(",", 1)
                        if len(parts) == 2:
                            submenu_name, command = parts
                            current_menu.add_command(
                                label=submenu_name.strip(),
                                command=lambda cmd=command.strip(): self.execute_command(cmd)
                            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load .tree file: {e}")

    def execute_command(self, command):
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute command: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()
