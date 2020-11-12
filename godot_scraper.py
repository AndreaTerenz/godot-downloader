from PyColorText import PyCT as ct
from bs4 import BeautifulSoup
from pathlib import Path
import requests, re, zipfile, os

def get_page_links(url):
    output = []

    r = requests.get(url, allow_redirects=True)
    
    if (r.status_code == 200):
        a = r.content #read the page

        soup = BeautifulSoup(a, 'html.parser')
        links = (soup.find_all('a')) #filter out everything that isn't a hyperlink
        for i in links: #i is an html tag
            
            file_name = i.extract().get_text() #extract the actual link text from the tag
            url_new = (url + file_name).replace(" ","%20") #replace whitespaces

            output.append(url_new)

    return output

def get_filtered_urls(url, regex):
    return list(filter(lambda u : re.search(regex, u), get_page_links(url)))

def print_array(arr):
    for a in arr:
        print(a)

def get_output_dir():
    if (d := input("Output location (Enter to use current folder) >> ")) == "":
        d = str(Path.cwd())
    elif not(Path.is_absolute(Path(d))):
        home = str(Path.home())
        home_as_root = input(f"Path isn't absolute - use home directory {home} as path root [Y/n]? ")

        if (home_as_root != "n"):
            d = home + "/" + d  
        
    return d

if __name__ == '__main__':

    #PHASE 1: Get the link to the last version's directory

    urls = get_filtered_urls("https://downloads.tuxfamily.org/godotengine/", r".*/(\d\.*)+$")
    last_stable_url = urls[-2]+"/"
    last_url = urls[-1]+"/"

    last_stable = last_stable_url.split("/")[-2]
    last = last_url.split("/")[-2]

    #PHASE 2: Check if the last version has a stable release (aka if its page contains a link to a zip file)

    archive_regex = r"x11\.64\.zip$"
    all_urls = get_filtered_urls(last_url, "")
    urls = get_filtered_urls(last_url, archive_regex)

    if len(urls) == 0:
        proceed = input(ct("This version doesn't have a stable release yet - download anyway [Y/n]? ", "yellow")).lower()

        if (proceed in ["", "y"]):        
            #PASE 2b: if the latest version is not stable yet, get the link to the latest beta/rc
            urls = get_filtered_urls(all_urls[-1]+"/", archive_regex)
            print(ct(f"Selected version: {last}", "green"))
        else:
            proceed = input(ct(f"Download latest stable version ({last_stable}) instead [Y/n]? ", "yellow")).lower()

            if (proceed == "n"):
                exit(-1)
            
            urls = get_filtered_urls(last_stable_url, archive_regex)
            print(ct(f"Selected version: {last_stable}", "green"))
    
    #PHASE 3: Download the zip file

    out_dir = get_output_dir()
    print(ct(f"Output directory: {out_dir}", "green"))

    print("Downloading file...")

    archive_url = urls[0]
    archive_name = "tmp.zip"
    r = requests.get(archive_url, allow_redirects=True)

    with open(archive_name, 'wb') as f:
        f.write(r.content)

    #PHASE 4 : Unzip the file

    print("Unzipping archive...")

    with zipfile.ZipFile(archive_name, 'r') as zip_ref:
        zip_ref.extractall(out_dir)
    
    os.remove(archive_name)

    print(ct("Done", "green"))