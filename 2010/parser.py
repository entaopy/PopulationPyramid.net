# -*- coding: utf-8 -*-
import csv
import urllib
import json
from collections import defaultdict
files = {
    "male":
            {
            "old": "UN_POP/UN_POP_FEMALE/ESTIMATES-Table 1.csv",
            "prev": "UN_POP/UN_POP_FEMALE_PREV/MEDIUM-Table 1.csv"
        },
    "female":
            {
            "old": "UN_POP/UN_POP_MALE/ESTIMATES-Table 1.csv",
            "prev": "UN_POP/UN_POP_MALE_PREV/MEDIUM-Table 1.csv",
            }
}

f = lambda: defaultdict(f)
res_dict = defaultdict(f)
year_set = set()

countries_dict = {}
count =0
for sex in files:
    for typ in files[sex]:
        reader = csv.reader(open(files[sex][typ], 'rb'), delimiter=';')
        for row in reader:
            year = int(row[5])
            if (year % 5== 0):
                year_set.add(year)
                country = row[2]
                encoded_country =  urllib.quote_plus(country.decode('ascii','ignore'))
                countries_dict[encoded_country]=country
                i=0
                for v in row[6:]:
                    try:
                        res_dict[encoded_country][year][sex][i]=int(v)
                    except:
                        if v!="…":
                            print "failed on :'%s' " % v
                        res_dict[encoded_country][year][sex][i]=0
                    i = i+1
                    count = count +1


year_list = sorted(list(year_set))

#print year_list
#print countries_dict

encoded_countries_list= sorted(countries_dict.keys())
alphabet = map(chr, range(97, 123))

letters_to_countries_list_dict = defaultdict(list)

for c in encoded_countries_list:
    first_letter = c[0]
    letters_to_countries_list_dict[first_letter].append(c)

#print letters_to_countries_list_dict

pop_dict = defaultdict(f)
for encoded_country in encoded_countries_list:
    for year in year_list:
        for sex in ('male','female'):
            sum =0
            for i in res_dict[encoded_country][year][sex]:
                sum += res_dict[encoded_country][year][sex][i]
            pop_dict[encoded_country][year]=sum

#print pop_dict
def age_to_int(age):
    if not age.strip().startswith("100"):
        return int(age.split('-')[0])
    else:
        return 100

for encoded_country in encoded_countries_list:
    f = open("generated/%s.js" % encoded_country,'w')
    f.write(json.dumps(res_dict[encoded_country]))
    f.close()

age_labels = [' 0-4', ' 5-9', ' 10-14', ' 15-19', ' 20-24', ' 25-29', ' 30-34', ' 35-39', ' 40-44', ' 45-49', ' 50-54', ' 55-59', ' 60-64', ' 65-69', ' 70-74', ' 75-79', ' 80-84', ' 85-89', ' 90-94', ' 95-99', ' 100+'];


main_data_dict ={
    'alphabet':alphabet,
    'lettersToCountriesList':letters_to_countries_list_dict,
    'populations':pop_dict,
    'years':year_list,
    'countriesHumanNames': countries_dict,
    'ageLabels':age_labels

}

f = open('mainData.json','w')
f.write(json.dumps(main_data_dict))
f.close()