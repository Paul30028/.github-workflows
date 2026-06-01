import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import csv

def scrape_data(url, output_file):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 简单示例：采集页面所有标题 (h1, h2, h3)
        data = []
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            data.append([tag.name, tag.get_text(strip=True)])
            
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Tag', 'Content'])
            writer.writerows(data)
        return True
    except Exception as e:
        return str(e)

def start_scrape():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        error = scrape_data(url, file_path)
        if error is True:
            messagebox.showinfo("Success", "Data collected successfully!")
        else:
            messagebox.showerror("Error", f"Scraping failed: {error}")

root = tk.Tk()
root.title("WebPulse Scraper")
root.geometry("400x200")

tk.Label(root, text="Enter Website URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

btn = tk.Button(root, text="Scrape & Save CSV", command=start_scrape, bg="#FF6B6B", fg="white")
btn.pack(pady=20)

root.mainloop()