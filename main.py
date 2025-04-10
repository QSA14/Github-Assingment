import requests
import webbrowser
from tkinter import Tk, Label, Entry, Button, Text, Toplevel, messagebox, END

API_KEY = 'pVWzxCuSJ8xc6lxaomnQZWDAEQsaR4BfSQVSYK2P'
BASE_URL = 'https://api.thenewsapi.com/v1/news/top'

//in the future we will upgrade it

def fetch_news(language='en', country=None, search=None):

    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'language': language,
        'country': country,
        'search': search,
        'limit': 10
    }
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch news: {e}")
        return []

def open_url(url):
    if url:
        webbrowser.open(url, new=2)
    else:
        messagebox.showerror("Error", "No URL available for this article.")

def display_news(articles):
    if not articles:
        messagebox.showinfo("No News", "No articles found!")
        return

    news_window = Toplevel(root)
    news_window.title("News Articles")
    news_window.geometry("800x600")

    text_widget = Text(news_window, wrap="word", font=("Arial", 12))
    text_widget.pack(expand=True, fill="both")

    for idx, article in enumerate(articles, start=1):
        title = f"{idx}. {article['title']}\n"
        description = f"{article.get('description', 'No description available')}\n"
        url = article.get('url', 'No URL available')

        text_widget.insert(END, title)
        text_widget.insert(END, description)

        if url and url != 'No URL available':
            text_widget.insert(END, f"Read more: {url}\n\n", (f"url{idx}",))
            text_widget.tag_config(f"url{idx}", foreground="blue", underline=1)
            text_widget.tag_bind(f"url{idx}", "<Button-1>", lambda e, link=url: open_url(link))
        else:
            text_widget.insert(END, "No URL available\n\n")

    text_widget.configure(state="disabled")

def search_by_country():
    country = country_entry.get().strip()
    articles = fetch_news(country=country)
    display_news(articles)

def search_by_keyword():
    keyword = keyword_entry.get().strip()
    articles = fetch_news(search=keyword)
    display_news(articles)

root = Tk()
root.title("News Aggregator")
root.geometry("400x300")

Label(root, text="Search by Country (e.g., 'us', 'ca')").pack(pady=5)
country_entry = Entry(root)
country_entry.pack(pady=5)
Button(root, text="Fetch News by Country", command=search_by_country).pack(pady=5)

Label(root, text="Search by Keyword").pack(pady=5)
keyword_entry = Entry(root)
keyword_entry.pack(pady=5)
Button(root, text="Search News by Keyword", command=search_by_keyword).pack(pady=5)

root.mainloop()

