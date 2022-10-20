"""°°°
#Importando bibliotecas úteis(numpy, pandas,math,matplotlib):
°°°"""
# |%%--%%| <j1LCf0B0fB|ZAFA9kUHdR>

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Importando o banco de dados como um DataFrame pandas

""" col_names_banana = ['At1', 'At2', 'Class']
banana=pd.read_csv('./data/banana.dat', names=col_names_banana)
print(banana) """

col_names_iris = ["SepalLength", "SepalWidth", "PetalLenght", "PetalWidth", "Class"]
iris = pd.read_csv("./data/iris.dat", names=col_names_iris)
print(iris)



# Separando as classes do Dataframe Banana e criando partições de treino e teste dos dados

bananaclass1 = banana[banana["Class"] == 1]
bananaclass2 = banana[banana["Class"] == -1]


# |%%--%%| <BqGFVjq3nL|NObPgNiu2V>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <NObPgNiu2V|TlgHSaYqJU>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <TlgHSaYqJU|jBhytwsOKD>

bananaclass1_train = bananaclass1.sample(frac=0.7)
bananaclass1_test = bananaclass1.drop(bananaclass1_train.index)
bananaclass1_train.reset_index(drop=True, inplace=True)
bananaclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <jBhytwsOKD|ryBcBMCqlf>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <ryBcBMCqlf|KwV5xWlq2S>

bananaclass2_train = bananaclass2.sample(frac=0.7)
bananaclass2_test = bananaclass2.drop(bananaclass2_train.index)
bananaclass2_train.reset_index(drop=True, inplace=True)
bananaclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <KwV5xWlq2S|aE3elkNBk5>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <aE3elkNBk5|Z8tGVMaSiI>

list_bananaclass1_train = []
for x in range(bananaclass1_train["At1"].size):
    temp_point = Point(bananaclass1_train["At1"][x], bananaclass1_train["At2"][x])
    list_bananaclass1_train.insert(1, temp_point)

list_bananaclass1_test = []
for x in range(bananaclass1_test["At1"].size):
    temp_point = Point(bananaclass1_test["At1"][x], bananaclass1_test["At2"][x])
    list_bananaclass1_test.insert(1, temp_point)

# |%%--%%| <Z8tGVMaSiI|Q8q8i9WZVr>

list_bananaclass2_train = []
for x in range(bananaclass2_train["At1"].size):
    temp_point = Point(bananaclass2_train["At1"][x], bananaclass2_train["At2"][x])
    list_bananaclass2_train.insert(1, temp_point)

list_bananaclass2_test = []
for x in range(bananaclass2_test["At1"].size):
    temp_point = Point(bananaclass2_test["At1"][x], bananaclass2_test["At2"][x])
    list_bananaclass2_test.insert(1, temp_point)

# |%%--%%| <Q8q8i9WZVr|IAXUVaAu5S>
"""°°°
# Separando as classes do Dataframe Haberman e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <IAXUVaAu5S|ASmU3ROz0r>

habermanclass1 = haberman[haberman[" Class"] == " positive"]
habermanclass2 = haberman[haberman[" Class"] == " negative"]
habermanclass1 = habermanclass1[["Age", " Positive"]]
habermanclass2 = habermanclass2[["Age", " Positive"]]

# |%%--%%| <ASmU3ROz0r|p2T0NGBGek>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <p2T0NGBGek|aWZUGSESDq>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <aWZUGSESDq|1Ioc8jC3Eu>

habermanclass1_train = habermanclass1.sample(frac=0.7)
habermanclass1_test = habermanclass1.drop(habermanclass1_train.index)
habermanclass1_train.reset_index(drop=True, inplace=True)
habermanclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <1Ioc8jC3Eu|3mRGd2NdCi>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <3mRGd2NdCi|9ZRO78d2go>

habermanclass2_train = habermanclass2.sample(frac=0.7)
habermanclass2_test = habermanclass2.drop(habermanclass2_train.index)
habermanclass2_train.reset_index(drop=True, inplace=True)
habermanclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <9ZRO78d2go|KASa0yHvj1>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <KASa0yHvj1|LhlKJYHbm6>

list_habermanclass1_train = []
for x in range(habermanclass1_train["Age"].size):
    temp_point = Point(
        habermanclass1_train["Age"][x], habermanclass1_train[" Positive"][x]
    )
    list_habermanclass1_train.insert(1, temp_point)

list_habermanclass1_test = []
for x in range(habermanclass1_test["Age"].size):
    temp_point = Point(
        habermanclass1_test["Age"][x], habermanclass1_test[" Positive"][x]
    )
    list_habermanclass1_test.insert(1, temp_point)

# |%%--%%| <LhlKJYHbm6|o5kxTbLZKk>

list_habermanclass2_train = []
for x in range(habermanclass2_train["Age"].size):
    temp_point = Point(
        habermanclass2_train["Age"][x], habermanclass2_train[" Positive"][x]
    )
    list_habermanclass2_train.insert(1, temp_point)

list_habermanclass2_test = []
for x in range(habermanclass2_test["Age"].size):
    temp_point = Point(
        habermanclass2_test["Age"][x], habermanclass2_test[" Positive"][x]
    )
    list_habermanclass2_test.insert(1, temp_point)

# |%%--%%| <o5kxTbLZKk|UCnUL3hF9H>
"""°°°
# Separando as classes do Dataframe Adult e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <UCnUL3hF9H|SwRHrFUldB>


adultclass1 = adult[adult[" Class"] == ">50K"]
adultclass2 = adult[adult[" Class"] == "<=50K"]
adultclass1 = adultclass1[["Age", " Education-num"]]
adultclass2 = adultclass2[["Age", " Education-num"]]

# |%%--%%| <SwRHrFUldB|FQPeDMPMWG>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <FQPeDMPMWG|ALtyPHDmLP>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <ALtyPHDmLP|UJuIJellnM>

adultclass1_train = adultclass1.sample(frac=0.7)
adultclass1_test = adultclass1.drop(adultclass1_train.index)
adultclass1_train.reset_index(drop=True, inplace=True)
adultclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <UJuIJellnM|wLTfRUuWe7>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <wLTfRUuWe7|Fny3rYUPhl>

adultclass2_train = adultclass2.sample(frac=0.7)
adultclass2_test = adultclass2.drop(adultclass2_train.index)
adultclass2_train.reset_index(drop=True, inplace=True)
adultclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <Fny3rYUPhl|q1qjnbymf4>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <q1qjnbymf4|zwF53EbNvt>

list_adultclass1_train = []
for x in range(adultclass1_train["Age"].size):
    temp_point = Point(
        adultclass1_train["Age"][x], adultclass1_train[" Education-num"][x]
    )
    list_adultclass1_train.insert(1, temp_point)

list_adultclass1_test = []
for x in range(adultclass1_test["Age"].size):
    temp_point = Point(
        adultclass1_test["Age"][x], adultclass1_test[" Education-num"][x]
    )
    list_adultclass1_test.insert(1, temp_point)

# |%%--%%| <zwF53EbNvt|DPMwSCsRKL>

list_adultclass2_train = []
for x in range(adultclass2_train["Age"].size):
    temp_point = Point(
        adultclass2_train["Age"][x], adultclass2_train[" Education-num"][x]
    )
    list_adultclass2_train.insert(1, temp_point)

list_adultclass2_test = []
for x in range(adultclass2_test["Age"].size):
    temp_point = Point(
        adultclass2_test["Age"][x], adultclass2_test[" Education-num"][x]
    )
    list_adultclass2_test.insert(1, temp_point)

# |%%--%%| <DPMwSCsRKL|YMfkl7N6dY>
"""°°°
# Separando as classes do Dataframe Glass e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <YMfkl7N6dY|yriWuTDcEX>

glassclass1 = glass[glass[" Class"] == 2]
glassclass2 = glass[glass[" Class"] != 2]
glassclass1 = glassclass1[[" Al", " Si"]]
glassclass2 = glassclass2[[" Al", " Si"]]

# |%%--%%| <yriWuTDcEX|r73u5D8eoN>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <r73u5D8eoN|ymSDUJ1BE4>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <ymSDUJ1BE4|YM0BOsHeWu>

glassclass1_train = glassclass1.sample(frac=0.7)
glassclass1_test = glassclass1.drop(glassclass1_train.index)
glassclass1_train.reset_index(drop=True, inplace=True)
glassclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <YM0BOsHeWu|8Hfyj28NgP>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <8Hfyj28NgP|aipcXCbYQe>

glassclass2_train = glassclass2.sample(frac=0.7)
glassclass2_test = glassclass2.drop(glassclass2_train.index)
glassclass2_train.reset_index(drop=True, inplace=True)
glassclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <aipcXCbYQe|pFM5KRxGEw>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <pFM5KRxGEw|Igfoa8fZnV>

list_glassclass1_train = []
for x in range(glassclass1_train[" Al"].size):
    temp_point = Point(glassclass1_train[" Al"][x], glassclass1_train[" Si"][x])
    list_glassclass1_train.insert(1, temp_point)

list_glassclass1_test = []
for x in range(glassclass1_test[" Al"].size):
    temp_point = Point(glassclass1_test[" Al"][x], glassclass1_test[" Si"][x])
    list_glassclass1_test.insert(1, temp_point)

# |%%--%%| <Igfoa8fZnV|fk4jE14S2H>

list_glassclass2_train = []
for x in range(glassclass2_train[" Al"].size):
    temp_point = Point(glassclass2_train[" Al"][x], glassclass2_train[" Si"][x])
    list_glassclass2_train.insert(1, temp_point)

list_glassclass2_test = []
for x in range(glassclass2_test[" Al"].size):
    temp_point = Point(glassclass2_test[" Al"][x], glassclass2_test[" Si"][x])
    list_glassclass2_test.insert(1, temp_point)

# |%%--%%| <fk4jE14S2H|wLvGH7lNu2>
"""°°°
# Separando as classes do Dataframe Iris e criando partições de treino e teste dos dados


°°°"""
# |%%--%%| <wLvGH7lNu2|Sa8q4uPaij>

irisclass1 = iris[iris["Class"] != " Iris-setosa"]
irisclass2 = iris[iris["Class"] == " Iris-setosa"]
irisclass1 = irisclass1[["SepalLength", "SepalWidth"]]
irisclass2 = irisclass2[["SepalLength", "SepalWidth"]]

# |%%--%%| <Sa8q4uPaij|Za56fcLdWD>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <Za56fcLdWD|rqKGloHpFN>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <rqKGloHpFN|yXSkMXhdZk>

irisclass1_train = irisclass1.sample(frac=0.7)
irisclass1_test = irisclass1.drop(irisclass1_train.index)
irisclass1_train.reset_index(drop=True, inplace=True)
irisclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <yXSkMXhdZk|zcDamzVudt>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <zcDamzVudt|Qyd2I8ibS6>

irisclass2_train = irisclass2.sample(frac=0.7)
irisclass2_test = irisclass2.drop(irisclass2_train.index)
irisclass2_train.reset_index(drop=True, inplace=True)
irisclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <Qyd2I8ibS6|NiDc8yzq1K>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <NiDc8yzq1K|eeTTjNJIPT>

list_irisclass1_train = []
for x in range(irisclass1_train["SepalLength"].size):
    temp_point = Point(
        irisclass1_train["SepalLength"][x], irisclass1_train["SepalWidth"][x]
    )
    list_irisclass1_train.insert(1, temp_point)

list_irisclass1_test = []
for x in range(irisclass1_test["SepalLength"].size):
    temp_point = Point(
        irisclass1_test["SepalLength"][x], irisclass1_test["SepalWidth"][x]
    )
    list_irisclass1_test.insert(1, temp_point)

# |%%--%%| <eeTTjNJIPT|aJlZYuDx6y>

list_irisclass2_train = []
for x in range(irisclass2_train["SepalLength"].size):
    temp_point = Point(
        irisclass2_train["SepalLength"][x], irisclass2_train["SepalWidth"][x]
    )
    list_irisclass2_train.insert(1, temp_point)

list_irisclass2_test = []
for x in range(irisclass2_test["SepalLength"].size):
    temp_point = Point(
        irisclass2_test["SepalLength"][x], irisclass2_test["SepalWidth"][x]
    )
    list_irisclass2_test.insert(1, temp_point)

# |%%--%%| <aJlZYuDx6y|mJKY58uENV>

x1 = [float(p.x) for p in list_irisclass1_train]
y1 = [float(p.y) for p in list_irisclass1_train]
x2 = [float(p.x) for p in list_irisclass2_train]
y2 = [float(p.y) for p in list_irisclass2_train]
plt.xlim(min(min(x1), min(x2)), max(max(x1), max(x2)))
plt.ylim(min(min(y1), min(y2)), max(max(y1), max(y2)))
plt.scatter(x1, y1, color="black", s=0.8)
plt.scatter(x2, y2, color="green", s=0.8)
plt.show()

# |%%--%%| <mJKY58uENV|2cz8XkVzBQ>
"""°°°
# Separando as classes do Dataframe Magic e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <2cz8XkVzBQ|xR1i6R4QUE>

magicclass1 = magic[magic[" Class"] == "g"]
magicclass2 = magic[magic[" Class"] == "h"]
magicclass1 = magicclass1[["FLength", " FWidth"]]
magicclass2 = magicclass2[["FLength", " FWidth"]]

# |%%--%%| <xR1i6R4QUE|ggvt6HhPBf>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <ggvt6HhPBf|gpg0D35yR5>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <gpg0D35yR5|Ijh6ETyc97>

magicclass1_train = magicclass1.sample(frac=0.7)
magicclass1_test = magicclass1.drop(magicclass1_train.index)
magicclass1_train.reset_index(drop=True, inplace=True)
magicclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <Ijh6ETyc97|YdGiuySimM>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <YdGiuySimM|6UMx36B7Yc>

magicclass2_train = magicclass2.sample(frac=0.7)
magicclass2_test = magicclass2.drop(magicclass2_train.index)
magicclass2_train.reset_index(drop=True, inplace=True)
magicclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <6UMx36B7Yc|ad5fD08mRC>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <ad5fD08mRC|aHrd7zbFyP>

list_magicclass1_train = []
for x in range(magicclass1_train["FLength"].size):
    temp_point = Point(magicclass1_train["FLength"][x], magicclass1_train[" FWidth"][x])
    list_magicclass1_train.insert(1, temp_point)

list_magicclass1_test = []
for x in range(magicclass1_test["FLength"].size):
    temp_point = Point(magicclass1_test["FLength"][x], magicclass1_test[" FWidth"][x])
    list_magicclass1_test.insert(1, temp_point)

# |%%--%%| <aHrd7zbFyP|o4cwN0zWT8>

list_magicclass2_train = []
for x in range(magicclass2_train["FLength"].size):
    temp_point = Point(magicclass2_train["FLength"][x], magicclass2_train[" FWidth"][x])
    list_magicclass2_train.insert(1, temp_point)

list_magicclass2_test = []
for x in range(magicclass2_test["FLength"].size):
    temp_point = Point(magicclass2_test["FLength"][x], magicclass2_test[" FWidth"][x])
    list_magicclass2_test.insert(1, temp_point)

# |%%--%%| <o4cwN0zWT8|0uCqAQmQGX>
"""°°°
# Separando as classes do Dataframe Pima e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <0uCqAQmQGX|5aoa5Qdodw>

pimaclass1 = pima[pima[" Class"] == "tested_positive"]
pimaclass2 = pima[pima[" Class"] == "tested_negative"]
pimaclass1 = pimaclass1[["Preg", " Plas"]]
pimaclass2 = pimaclass2[["Preg", " Plas"]]

# |%%--%%| <5aoa5Qdodw|4jjKrpvE4s>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <4jjKrpvE4s|0gQUzeIhWq>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <0gQUzeIhWq|RphetoZiw4>

pimaclass1_train = pimaclass1.sample(frac=0.7)
pimaclass1_test = pimaclass1.drop(pimaclass1_train.index)
pimaclass1_train.reset_index(drop=True, inplace=True)
pimaclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <RphetoZiw4|wV5YvVuKeN>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <wV5YvVuKeN|sgqmVgR9xi>

pimaclass2_train = pimaclass2.sample(frac=0.7)
pimaclass2_test = pimaclass2.drop(pimaclass2_train.index)
pimaclass2_train.reset_index(drop=True, inplace=True)
pimaclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <sgqmVgR9xi|x539iBnNFG>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <x539iBnNFG|S82FbEBfUM>

list_pimaclass1_train = []
for x in range(pimaclass1_train["Preg"].size):
    temp_point = Point(pimaclass1_train["Preg"][x], pimaclass1_train[" Plas"][x])
    list_pimaclass1_train.insert(1, temp_point)

list_pimaclass1_test = []
for x in range(pimaclass1_test["Preg"].size):
    temp_point = Point(pimaclass1_test["Preg"][x], pimaclass1_test[" Plas"][x])
    list_pimaclass1_test.insert(1, temp_point)

# |%%--%%| <S82FbEBfUM|Jbamn7m7GS>

list_pimaclass2_train = []
for x in range(pimaclass2_train["Preg"].size):
    temp_point = Point(pimaclass2_train["Preg"][x], pimaclass2_train[" Plas"][x])
    list_pimaclass2_train.insert(1, temp_point)

list_pimaclass2_test = []
for x in range(pimaclass2_test["Preg"].size):
    temp_point = Point(pimaclass2_test["Preg"][x], pimaclass2_test[" Plas"][x])
    list_pimaclass2_test.insert(1, temp_point)

# |%%--%%| <Jbamn7m7GS|5WacevZIMM>
"""°°°
# Separando as classes do Dataframe Sonar e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <5WacevZIMM|BZv4nofzVW>

sonarclass1 = sonar[sonar[" Class"] == " R"]
sonarclass2 = sonar[sonar[" Class"] == " M"]
sonaclass1 = sonarclass1[["Band1", " Band2"]]
sonaclass2 = sonarclass2[["Band1", " Band2"]]

# |%%--%%| <BZv4nofzVW|RxWsuqLQ3H>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <RxWsuqLQ3H|8bnMXl7vAt>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <8bnMXl7vAt|XB4RiIYBHw>

sonarclass1_train = sonarclass1.sample(frac=0.7)
sonarclass1_test = sonarclass1.drop(sonarclass1_train.index)
sonarclass1_train.reset_index(drop=True, inplace=True)
sonarclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <XB4RiIYBHw|F4CSVEIBDl>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <F4CSVEIBDl|4WYkPr08t1>

sonarclass2_train = sonarclass2.sample(frac=0.7)
sonarclass2_test = sonarclass2.drop(sonarclass2_train.index)
sonarclass2_train.reset_index(drop=True, inplace=True)
sonarclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <4WYkPr08t1|EF7kBaQmLV>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <EF7kBaQmLV|DqcjpW2hQR>

list_sonarclass1_train = []
for x in range(sonarclass1_train["Band1"].size):
    temp_point = Point(sonarclass1_train["Band1"][x], sonarclass1_train[" Band2"][x])
    list_sonarclass1_train.insert(1, temp_point)

list_sonarclass1_test = []
for x in range(sonarclass1_test["Band1"].size):
    temp_point = Point(sonarclass1_test["Band1"][x], sonarclass1_test[" Band2"][x])
    list_sonarclass1_test.insert(1, temp_point)

# |%%--%%| <DqcjpW2hQR|OPk3NvyilD>

list_sonarclass2_train = []
for x in range(sonarclass2_train["Band1"].size):
    temp_point = Point(sonarclass2_train["Band1"][x], sonarclass2_train[" Band2"][x])
    list_sonarclass2_train.insert(1, temp_point)

list_sonarclass2_test = []
for x in range(sonarclass2_test["Band1"].size):
    temp_point = Point(sonarclass2_test["Band1"][x], sonarclass2_test[" Band2"][x])
    list_sonarclass2_test.insert(1, temp_point)

# |%%--%%| <OPk3NvyilD|5jfi6aEcoF>
"""°°°
# Separando as classes do Dataframe Vehicle e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <5jfi6aEcoF|A4ypKXt1Fc>

vehicleclass1 = vehicle[vehicle[" Class"] == " bus "]
vehicleclass2 = vehicle[vehicle[" Class"] != " bus "]
vehicleclass1 = vehicleclass1[["Compactness", " Circularity"]]
vehicleclass2 = vehicleclass2[["Compactness", " Circularity"]]

# |%%--%%| <A4ypKXt1Fc|oJogkzph43>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <oJogkzph43|HvpHhFuftR>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <HvpHhFuftR|djoOiXvdU0>

vehicleclass1_train = vehicleclass1.sample(frac=0.7)
vehicleclass1_test = vehicleclass1.drop(vehicleclass1_train.index)
vehicleclass1_train.reset_index(drop=True, inplace=True)
vehicleclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <djoOiXvdU0|zAYN89GgLA>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <zAYN89GgLA|JQ3eeOlTgm>

vehicleclass2_train = vehicleclass2.sample(frac=0.7)
vehicleclass2_test = vehicleclass2.drop(vehicleclass2_train.index)
vehicleclass2_train.reset_index(drop=True, inplace=True)
vehicleclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <JQ3eeOlTgm|vRHhDMOF3Y>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <vRHhDMOF3Y|yDChGohHPu>

list_vehicleclass1_train = []
for x in range(vehicleclass1_train["Compactness"].size):
    temp_point = Point(
        vehicleclass1_train["Compactness"][x], vehicleclass1_train[" Circularity"][x]
    )
    list_vehicleclass1_train.insert(1, temp_point)

list_vehicleclass1_test = []
for x in range(vehicleclass1_test["Compactness"].size):
    temp_point = Point(
        vehicleclass1_test["Compactness"][x], vehicleclass1_test[" Circularity"][x]
    )
    list_vehicleclass1_test.insert(1, temp_point)

# |%%--%%| <yDChGohHPu|FcnPZ9NTSB>

list_vehicleclass2_train = []
for x in range(vehicleclass2_train["Compactness"].size):
    temp_point = Point(
        vehicleclass2_train["Compactness"][x], vehicleclass2_train[" Circularity"][x]
    )
    list_vehicleclass2_train.insert(1, temp_point)

list_vehicleclass2_test = []
for x in range(vehicleclass2_test["Compactness"].size):
    temp_point = Point(
        vehicleclass2_test["Compactness"][x], vehicleclass2_test[" Circularity"][x]
    )
    list_vehicleclass2_test.insert(1, temp_point)

# |%%--%%| <FcnPZ9NTSB|cBVtL8f9Z3>
"""°°°
# Separando as classes do Dataframe Vehicle e criando partições de treino e teste dos dados
°°°"""
# |%%--%%| <cBVtL8f9Z3|FNsFK1JHSx>

wineclass1 = wine[wine[" Class"] == 2]
wineclass2 = wine[wine[" Class"] != 2]
wineclass1 = wineclass1[["Alcohol", " MalicAcid"]]
wineclass2 = wineclass2[["Alcohol", " MalicAcid"]]

# |%%--%%| <FNsFK1JHSx|5smbMj10Sj>
"""°°°
Separando as classes em treino e teste
°°°"""
# |%%--%%| <5smbMj10Sj|FvEwxVWt4R>
"""°°°


> Classe 1:


°°°"""
# |%%--%%| <FvEwxVWt4R|fLpHMB13Hf>

wineclass1_train = wineclass1.sample(frac=0.7)
wineclass1_test = wineclass1.drop(wineclass1_train.index)
wineclass1_train.reset_index(drop=True, inplace=True)
wineclass1_test.reset_index(drop=True, inplace=True)


# |%%--%%| <fLpHMB13Hf|JGgysZnoAK>
"""°°°


> Classe 2:


°°°"""
# |%%--%%| <JGgysZnoAK|KF3oEVYxsb>

wineclass2_train = wineclass2.sample(frac=0.7)
wineclass2_test = wineclass2.drop(wineclass2_train.index)
wineclass2_train.reset_index(drop=True, inplace=True)
wineclass2_test.reset_index(drop=True, inplace=True)

# |%%--%%| <KF3oEVYxsb|P7pQd7OMic>
"""°°°
Passando os dados para o tipo Point:
°°°"""
# |%%--%%| <P7pQd7OMic|4UbUElHeiV>

list_wineclass1_train = []
for x in range(wineclass1_train["Alcohol"].size):
    temp_point = Point(
        wineclass1_train["Alcohol"][x], wineclass1_train[" MalicAcid"][x]
    )
    list_wineclass1_train.insert(1, temp_point)

list_wineclass1_test = []
for x in range(wineclass1_test["Alcohol"].size):
    temp_point = Point(wineclass1_test["Alcohol"][x], wineclass1_test[" MalicAcid"][x])
    list_wineclass1_test.insert(1, temp_point)

# |%%--%%| <4UbUElHeiV|uTbmG0AXfI>

list_wineclass2_train = []
for x in range(wineclass2_train["Alcohol"].size):
    temp_point = Point(
        wineclass2_train["Alcohol"][x], wineclass2_train[" MalicAcid"][x]
    )
    list_wineclass2_train.insert(1, temp_point)

list_wineclass2_test = []
for x in range(wineclass2_test["Alcohol"].size):
    temp_point = Point(wineclass2_test["Alcohol"][x], wineclass2_test[" MalicAcid"][x])
    list_wineclass2_test.insert(1, temp_point)
