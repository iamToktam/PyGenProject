import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from controller.main import EduLangInterpreter

class EduLangIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("EduLang Code Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        self.interpreter = EduLangInterpreter()

        self.editor_bg = "#252526"
        self.fg_color = "#d4d4d4"
        self.console_bg = "#1e1e1e"
        self.console_fg = "#9cdcfe"

        # Editor
        self.editor = tk.Text(root, font=("Consolas", 12),
                              bg=self.editor_bg, fg=self.fg_color,
                              insertbackground="white")
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Run button
        self.btn_run = tk.Button(root, text="▶ Run Code", command=self.run_code,
                                 bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"))
        self.btn_run.pack(pady=5)

        # Console
        tk.Label(root, text="CONSOLE OUTPUT", bg="#1e1e1e", fg="#569cd6",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10)
        self.console = scrolledtext.ScrolledText(root, height=10, font=("Consolas", 11),
                                                 bg=self.console_bg, fg=self.console_fg)
        self.console.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        self.console.insert(tk.END, "System Ready...\n")
        self.console.configure(state='disabled')

    def run_code(self):
        code_content = self.editor.get("1.0", tk.END).strip()
        if not code_content:
            return

        self.console.configure(state='normal')
        self.console.delete("1.0", tk.END)

        def input_dialog(var_name):
            return simpledialog.askstring("Input", f"Enter value for {var_name}:", parent=self.root)

        interpreter = EduLangInterpreter(input_callback=input_dialog)

        # اجرای خط به خط
        for line in code_content.splitlines():
            interpreter.execute_line(line)

        # نمایش خروجی‌ها در کنسول
        for out in interpreter.output:
            if "Error" in out:
                self.console.insert(tk.END, out + "\n", "error")
            else:
                self.console.insert(tk.END, out + "\n")

        # تعریف تگ رنگ قرمز برای خطاها
        self.console.tag_config("error", foreground="#ff5555")
        self.console.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = EduLangIDE(root)
    root.mainloop()
