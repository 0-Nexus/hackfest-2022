from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

content="Air pollution is contamination of the indoor or outdoor environment by any chemical, physical or biological agent that modifies the natural characteristics of the atmosphere. Household combustion devices, motor vehicles, industrial facilities and forest fires are common sources of air pollution. Pollutants of major public health concern include particulate matter, carbon monoxide, ozone, nitrogen dioxide and sulfur dioxide. Outdoor and indoor air pollution cause respiratory and other diseases and are important sources of morbidity and mortality. WHO data show that almost all of the global population (99%) breathe air that exceeds WHO guideline limits and contains high levels of pollutants, with low- and middle-income countries suffering from the highest exposures. Air quality is closely linked to the earth’s climate and ecosystems globally. Many of the drivers of air pollution (i.e. combustion of fossil fuels) are also sources of greenhouse gas emissions. Policies to reduce air pollution, therefore, offer a win-win strategy for both climate and health, lowering the burden of disease attributable to air pollution, as well as contributing to the near- and long-term mitigation of climate change."

stopWords=set(stopwords.words("english"))
words=word_tokenize(content)

freq=dict()
for word in words:
    word=word.lower()
    if word in stopWords:
        continue
    if word in freq:
        freq[word]+=1
    else:
        freq[word]=1

sentences=sent_tokenize(content)
sentVal=dict()
for sent in sentences:
    for word,frequency in freq.items():
        if word in sent.lower():
            if sent in sentVal:
                sentVal[sent]+=frequency
            else:
                sentVal[sent]=frequency

sumVal=0
for sent in sentVal:
    sumVal+=sentVal[sent]

avg=int(sumVal/len(sentVal))

summary=""
for sent in sentences:
    if (sent in sentVal) and (sentVal[sent]>(1.2*avg)):
        summary+=" "+sent

print(summary)
