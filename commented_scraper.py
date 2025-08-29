```python
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import lxml
#variable to hold the website URL
url = 'https://quotes.toscrape.com/'

#send request to the website
response = requests.get(url)
print(f"Response Status Code: {response.status_code}")

# Create a BeautifulSoup object from the response text.
soup = BeautifulSoup(response.text, 'lxml')
# Find all 'a' tags with class 'tag'.
tags = soup.find_all('a', class_='tag')

for tag in tags:
    # Print the text of each tag.
    print(tag.text)
    #Fetch: We used requests to download the HTML. Parse: We gave the HTML to BeautifulSoup to create a searchable soup object. Find: We used our browser's Inspector to find the right tag (a) and class (tag). Extract: We used soup.find_all() to get a list of all matching tags. Loop & Clean: We looped through the list and printed the .text of each tag to get the final result.
    #analyzing the tags
tag_counts = {}
for tag in tags:
    # Get the text from the current tag.
    tag_text = tag.text
    # Increment the count for the tag in the dictionary.
    if tag_text in tag_counts:
        # Increment count if tag already exists.
        tag_counts[tag_text] += 1
    else:
        # Add tag to dictionary if it's new.
        tag_counts[tag_text] = 1

print(tag_counts)

#visualizing the tags
list(tag_counts.keys())
list(tag_counts.values())
# Create a bar chart of tag counts.
plt.bar(list(tag_counts.keys()), list(tag_counts.values()))
# Set the title of the chart.
plt.title('Tag Counts from Quotes to Scrape')
# Rotate x-axis labels for better readability.
plt.xticks(rotation=45)
# Set the x-axis label.
plt.xlabel('Tags')
# Set the y-axis label.
plt.ylabel('Counts')
# Display the chart.
plt.show()
# Save the chart as a PNG file.
plt.savefig('tag_counts.png')
#We created an empty dictionary tag_counts to hold the counts of each tag. We looped through the tags list, updating the count for each tag in the dictionary. Finally, we printed the tag_counts dictionary to see the results.
    
```
