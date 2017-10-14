from bs4 import BeautifulSoup
import unittest
import requests
from collections import defaultdict
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
def part0():
    try:
        with open("kitty_html", "r") as k:
            html_data = k.read()
    except:
        html_data = requests.get("http://newmantaylor.com/gallery.html").text
        with open("kitty_html", "w", encoding = "utf-8") as k:
            k.write(html_data)

    soup = BeautifulSoup(html_data, "html.parser")
    img_ls = soup.find_all("img")
    for img in img_ls:
        alt = img.get("alt")
        if alt:
            print(alt)
        else:
            print("No alternative text provided!")

part0()
######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, 
# but if you prefer to build up the code to do this scraping and caching yourself, that is OK.






# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" 
# -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.
try:
    with open("nps_gov_data.html", "r") as index:
        index_page = index.read()
    with open("arkansas_data.html", "r") as ark:
        ark_page = ark.read()
    with open("california_data.html", "r") as ca:
        ca_page = ca.read()
    with open("michigan_data.html", "r") as mi:
        mi_page = mi.read()

except:
    index_page = requests.get("https://www.nps.gov/index.htm").text
    with open("nps_gov_data.html", "w", encoding = "utf-8") as index:
        index.write(index_page)
    soup_index = BeautifulSoup(index_page, "html.parser")
    dropdown = soup_index.find("ul", {"class":"dropdown-menu SearchBar-keywordSearch"})
    li_ls = dropdown.find_all("li")
    # print(li_ls)
    state_links = defaultdict(lambda: "http://www.nps.gov")
    for li_ele in li_ls:
        if li_ele.text == "Arkansas" or li_ele.text == "California" or li_ele.text == "Michigan":
            state_links[li_ele.text] += li_ele.a.get("href")
    # print(state_links)
    ark_page = requests.get(state_links["Arkansas"]).text
    ca_page = requests.get(state_links["California"]).text
    mi_page = requests.get(state_links["Michigan"]).text
    with open("arkansas_data.html", "w", encoding = "utf-8") as ark:
        ark.write(ark_page)
    with open("california_data.html", "w", encoding = "utf-8") as ca:
        ca.write(ca_page)
    with open("michigan_data.html", "w", encoding = "utf-8") as mi:
        mi.write(mi_page)




######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. 
# However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...





## Define your class NationalSite here:
class NationalSite(object):
    def __init__(self, soup):
        self.location = soup.find("h4").text
        self.name = soup.find("h3").a.text
        typeSite = soup.find("h2").text
        if typeSite == "":
            self.type = None
        else:
            self.type = typeSite
        self.description = soup.find("p").text
        right_list_soup = soup.find("ul")
        self.rt_ls = right_list_soup.find_all("li")
    
    def __str__(self):
        res = self.name + " | " + self.location
        return res

    def get_basic_info_url(self):
        for row in self.rt_ls:
            if "Basic Information" in row.a.text:
                res_url = row.a.get("href")
                break
        return res_url
    
    def get_mailing_address(self):
        basic_url = self.get_basic_info_url()
        basic_info_page = requests.get(basic_url).text
        basic_soup = BeautifulSoup(basic_info_page, "html.parser")
        address = basic_soup.find("div", itemprop = "address").text
        addr_ls = address.strip().split('\n')
        addr_ls = list(filter(lambda x: x != '', addr_ls))
        addr_oneline = "/".join(addr_ls)
        return addr_oneline

    def __contains__(self, input):
        return input in self.name


## Recommendation: to test the class, at various points,
# uncomment the following code and invoke some of the methods / 
# check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.




##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- 
# so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, 
# you might run into some problems and have to debug for where you need to put in some None value / error handling!

def create_ls(state_page):
    soup_state = BeautifulSoup(state_page, "html.parser")
    park_ls = soup_state.find("ul", id = "list_parks")
    soup_park_ls = park_ls.find_all("li", {"class": "clearfix"})
    # for soup_park in soup_park_ls:
    #     print(soup_park.prettify())
    sites_ls = [NationalSite(soup_park) for soup_park in soup_park_ls]
    return sites_ls
# create_ls(ark_page)

arkansas_natl_sites = create_ls(ark_page)
california_natl_sites = create_ls(ca_page)
michigan_natl_sites = create_ls(mi_page)


# for p in california_natl_sites:
#   print(p)
# for a in arkansas_natl_sites:
#   print(a)
# for m in michigan_natl_sites:
#   print(m)

def write_csv(sites_ls, filename):
    with open(filename, "w", newline = '') as csvfile:
        colnames = ["Name", "Location", "Type", "Address", "Description"]
        writer = csv.DictWriter(csvfile, colnames)
        writer.writeheader()
        for one_site in sites_ls:
            if one_site.type == None:
                one_site.type = "None"
            writer.writerow({"Name": one_site.name, "Location": one_site.location, "Type": one_site.type, 
                "Address": one_site.get_mailing_address(), "Description": one_site.description})

write_csv(arkansas_natl_sites, "arkansas.csv")
write_csv(california_natl_sites, "california.csv")
write_csv(michigan_natl_sites, "michigan.csv")