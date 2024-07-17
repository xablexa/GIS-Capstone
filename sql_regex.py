import re
import pandas as pd
geo_tags = open(r'enwiki-20240601-geo_tags2.txt', 'r+', encoding='utf-8')
list_to_df = []

lineList = geo_tags.readlines()
'''
#print(lineList[0])
lineList[0] = re.sub("\(", "", lineList[0], 1)
lineList[0] = re.sub("\);", "", lineList[0], 1)
pageList = re.split("\),\(", lineList[0])
print(pageList[0])
page = re.split(",", pageList[0])
print(page)
#append to list_to_df'''

for line in lineList:
    line = re.sub("INSERT INTO `geo_tags` VALUES", "", line) #remove SQL at beginning of line
    line = re.sub(" \(", "", line, 1) #remove leading parentheses
    line = re.sub("\);", "", line) #remove end parentheses
    #line = re.sub("('[^',]+),([^',]+),([^']+')", "-", line) #19 #replace commas inside quotes with dashes
    #line = re.sub("(?<=[^')L0-9]),(?=[^N])", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    line = re.sub(",(?=[^',]+')", "-", line)
    #line = re.sub("('[^',]+),([^']*')", "-", line) #22
    #line = re.sub(",(?=[^']*'[^']*(?:'[^']*'[^']*)*$)", "-", line) #times out
    #line = re.sub(",(?!(([^']*'){2})*[^']*$)", "-", line) #times out
    pageList = re.split("\),\(", line)

    for page in pageList:
        article = re.split(",", page)
        list_to_df.append(article)
geo_tags.close()

print(len(list_to_df))
print(list_to_df[:9])
#print(list_to_df[-5:-1])

columns = ['gt_id', 'gt_page_id', 'gt_globe', 'gt_primary', 'gt_lat', 'gt_lon', 'gt_dim', 'gt_type', 'gt_name', 'gt_country', 'gt_region', 'gt_lat_int', 'gt_lon_int']

#print(zip(columns, list_to_df))
df = pd.DataFrame.from_records(list_to_df)
print(df.head())

df.to_csv('raw_articles_geo.csv')

#df.drop(columns=['13','14','15,','16','17','18','19','20','21','22','23'], inplace=True)
df = df.drop(df.columns[[13,14,15,16,17,18,19,20,21,22,23]], axis=1)
print(df.head())
df.columns = columns
#df = df.rename(columns={'0': columns[0], '1': columns[1], '2': columns[2], '3': columns[3], '4':columns[4], '5': columns[5],
                   #'6': columns[6], '7': columns[7], '8': columns[8], '9': columns[9], '10': columns[10], '11': columns[11],
                   #'12': columns[12]}, inplace=True)
print(df.head())
df = df[df['gt_name'] != "NULL"]
#df = df.iloc[(df.index != 'NULL'), 8]

df.to_csv('articles_wName_geo.csv')
#for line in geo_tags:
    #print(line)
#geo_tags.close()