import requests
from lxml import html
import re


def get_a_tree(link):
    """
    Виймає html-дерево веб-сторінки за посиланням.
    :param link: посилання
    :return: дерево веб-сторінки
    """
    web_page = requests.get(link)
    return html.fromstring(web_page.content)


def get_tales(link: str, type_: str) -> True:
    """
    Автоматично вивантажує усі казки за посиланням (від першої до останньої сторінки), а тоді складає
    їх в окремі файли, а також усі разом в один великий файл.
    :param link: посилання на початкову сторінку казок
    :param type_: тип казок: (authors, folk)
    :return: True
    """
    all_titles = []
    all_links = []

    """Gets links and names of all tales"""
    tree = get_a_tree(link)
    tales_titles = tree.xpath('/html/body/div[2]/section[2]/div[3]/div/section/div[1]/ul/li/a/text()')
    all_titles.extend(tales_titles)

    tales_titles_ = []
    num = 1

    while tales_titles != tales_titles_:
        tales_titles = tales_titles_.copy()
        all_titles.extend(tales_titles_)
        all_links.extend(tree.xpath('/html/body/div[2]/section[2]/div[3]/div/section/div[1]/ul/li/a/@href'))
        num += 1
        print(num)
        tree = get_a_tree(link + f"next/{num}")
        tales_titles_ = tree.xpath('/html/body/div[2]/section[2]/div[3]/div/section/div[1]/ul/li/a/text()')

    print("Collected tales and links!")

    """Iterates through links to get tales"""
    all_texts = ""
    for title, link in zip(all_titles, all_links):
        print(title, link)
        tree = get_a_tree(link)
        tale = " ".join(tree.xpath("/html/body/div[2]/section[2]/div[3]/div/div[1]/article/div/p/text()"))
        all_texts += " " + tale

        title_ = re.sub(r"[\[\]\\/|:*?\"<>]", "", title).replace(" ", "_")+".txt"
        with open(f"sources\\tales_{type_}\\{title_}", "w", encoding="utf-8") as file1, \
                open(f"sources\\tales_{type_}.txt", "a", encoding="utf-8") as file2:
            print(tale, end="", file=file1)
            print(tale, end="\n\n", file=file2)

    print(f"Finished on {type_} tales!", end="\n\n")
    return True


if __name__ == "__main__":
    path_authors = "https://derevo-kazok.org/kazki-ukrayinskih-avtoriv/"
    get_tales(path_authors, "authors")
    path_folk = "https://derevo-kazok.org/ukrayinski-narodni-kazki/"
    get_tales(path_folk, "folk")
