import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import lxml
#variable to hold the website URL
url = 'https://quotes.toscrape.com/'

#send request to the website
response = requests.get(url)
print(f"Response Status Code: {response.status_code}")

soup = BeautifulSoup(response.text, 'lxml')
tags = soup.find_all('a', class_='tag')

for tag in tags:
    print(tag.text)
    #Fetch: We used requests to download the HTML. Parse: We gave the HTML to BeautifulSoup to create a searchable soup object. Find: We used our browser's Inspector to find the right tag (a) and class (tag). Extract: We used soup.find_all() to get a list of all matching tags. Loop & Clean: We looped through the list and printed the .text of each tag to get the final result.
    #analyzing the tags
tag_counts = {}
for tag in tags:
    tag_text = tag.text
    if tag_text in tag_counts:
        tag_counts[tag_text] += 1
    else:
        tag_counts[tag_text] = 1

print(tag_counts)

#visualizing the tags
list(tag_counts.keys())
list(tag_counts.values())
plt.bar(list(tag_counts.keys()), list(tag_counts.values())) #create a bar chart
plt.title('Tag Counts from Quotes to Scrape') #chart title
plt.xticks(rotation=45) #rotate x-axis labels for better readability
plt.xlabel('Tags')  #x-axis label
plt.ylabel('Counts')  #y-axis label
plt.show() #display the chart
plt.savefig('tag_counts.png') #save the chart as a PNG file
#We created an empty dictionary tag_counts to hold the counts of each tag. We looped through the tags list, updating the count for each tag in the dictionary. Finally, we printed the tag_counts dictionary to see the results.