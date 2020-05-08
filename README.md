# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/search.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Mycroft Confluence Search


## About
This skill is hosted on [Gitlab](https://gitlab.com/stratus-ss/mycroft-confluence-search-skill)and mirrored to GitHub
.The main purpose of this skill is to be able to search an Atlassian Confluence Wiki and return the results to a Telegram group of channel. It will
send results in groups of two and after the first 2 are displayed ask the user if more results should be returne.

You can as for a general title search, or if you know the page you want is nested, ask Mycroft to narrow the results based on a parent page.
This skill uses fuzzy searching so it is unlikely that only 1 match will be returned.

## Examples
find pages with computer stuff in confluence
find all the pages with chicken under dinner in confluence

find (pages with| all the pages with | ) {Page} (under {ParentPage} |) in confluence


## Credits
stratus-ss

## Category
**Information**

## Tags
#Confluence
#Search
#Telegram

