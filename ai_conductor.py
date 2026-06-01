import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import re

class AIConductor:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Conductor: Data to Knowledge v1.0")
        self.root.geometry("500x450")
        self.root.configure(bg="#f3f4f6")

        # 界面元素
        self.label = tk.Label(root, text="AI 语境编排器", font=("Arial", 16, "bold"), bg="#f3f4f6", fg="#1e293b")
        self.label.pack(pady=20)

        self.info = tk.Label(root, text="将海量碎片文件一键转化为 AI 高质量知识库", bg="#f3f4f6", fg="#64748b")
        self.info.pack()

        self.btn_select = tk.Button(root, text="选择源资料文件夹", command=self.select_folder, 
                                   bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), height=2, width=30)
        self.btn_select.pack(pady=30)

        self.status_log = scrolledtext.ScrolledText(root, height=10, width=55, font=("Consolas", 9))
        self.status_log.pack(pady=10)
        self.status_log.insert(tk.END, "等待任务启动...\n系统就绪。\n")

    def log(self, message):
        self.status_log.insert(tk.END, f"> {message}\n")
        self.status_log.see(tk.END)
        self.root.update()

    def clean_text(self, text):
        # 移除多余空白和 HTML 残留
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def select_folder(self):
        src_dir = filedialog.askdirectory()
        if not src_dir:
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".md", 
                                                 filetypes=[("Markdown files", "*.md")],
                                                 initialfile="AI_Knowledge_Base.md")
        if not output_file:
            return

        self.process_files(src_dir, output_file)

    def process_files(self, src_dir, output_file):
        try:
            self.log(f"开始扫描目录: {src_dir}")
            files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
            
            with open(output_file, 'w', encoding='utf-8') as kb:
                # 写入 AI 引导指令 (System Prompt)
                kb.write("# AI 结构化知识库\n\n")
                kb.write("> **CONTEXT GUIDANCE**: 以下内容是经过结构化编排的原始资料。在回答问题时，请优先参考以下文档中的具体细节和事实。\n\n")
                kb.write("---\n\n")

                for i, filename in enumerate(files):
                    self.log(f"正在编排 ({i+1}/{len(files)}): {filename}")
                    full_path = os.path.join(src_dir, filename)
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            cleaned = self.clean_text(content)
                            
                            # 添加元数据和分块标记
                            kb.write(f"## 来源文档: {filename}\n")
                            kb.write(f"**INDEX**: REF-{i+1:03d}\n\n")
                            kb.write(cleaned)
                            kb.write("\n\n---\n\n")
                    except Exception as e:
                        self.log(f"跳过文件 {filename}: {str(e)}")

            self.log("知识库构建完成！")
            messagebox.showinfo("成功", f"知识库已生成于:\n{output_file}\n\n现在你可以将其上传给任何 AI 进行深度分析。")
            
        except Exception as e:
            self.log(f"错误: {str(e)}")
            messagebox.showerror("失败", f"处理过程中出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIConductor(root)
    root.mainloop()