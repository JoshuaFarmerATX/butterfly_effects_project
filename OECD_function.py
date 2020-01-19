import pandas as pd
import numpy as np
import os
import pprint as pp
import matplotlib.pyplot as plt


path = os.path.join("OECD_data", "broadband.csv")

with open(path) as csv_file:
    og_broadband_df = pd.read_csv(csv_file)
og_bb_df = og_broadband_df[["Country", "VAR", "Time", "Value", "Unit"]]

path = os.path.join("OECD_data", "GERD.csv")

with open(path) as csv_file:
    GERD = pd.read_csv(csv_file)

GERD = GERD[["Country", 'ï»¿"MSTI_VAR"', "MSTI Variables", "Year", "Value"]]

path = os.path.join("OECD_data", "economic_outlook.csv")

with open(path) as csv_file:
    econ_df = pd.read_csv(csv_file)

econ_df = econ_df[["Country", "VARIABLE", "Variable", "Time", "Value"]]
fixed100_bb_df = get_var(og_bb_df, "BB-P100-TOT")
mob100_bb_df = get_var(og_bb_df, "BBW-P100-TOT")
fixed100_df = get_values(fixed100_bb_df[fixed100_bb_df["Time"].str.startswith("2")])
mobile100_df = get_values(mob100_bb_df[mob100_bb_df["Time"].str.startswith("2")])

fixed_bb_df = get_var(og_bb_df, "BB-SUBS-TOT")
mob_bb_df = get_var(og_bb_df, "BBW-SUBS-TOT")
fixed_df = get_values(fixed_bb_df[fixed_bb_df["Time"].str.startswith("2")])
mobile_df = get_values(mob_bb_df[mob_bb_df["Time"].str.startswith("2")])

POP = get_var(econ_df, "POP")
population = get_values(POP)

##fixed+mobile in persons
total_bb_df = pd.DataFrame()
for col in fixed_df.columns:
    total_bb_df[col] = fixed_df[col] + mobile_df[col]

total100_df = pd.DataFrame()
for col in total_bb_df.columns:
    total100_df[col] = (total_bb_df[col] / population[col]) * 100

total100_df = total100_df.dropna(axis=0)

##Research and Development
gdpRD = get_var(GERD, "G_XGDP")
gdpRD_df = get_values(gdpRD)

VA_PPP = get_var(GERD, "VA_PPP")
val_addedPPP = get_values(VA_PPP)

##economic_indicators
GDP_PPP = get_var(GERD, "GDP_PPP")
gdp_ppp = get_values(GDP_PPP)

def plotitfunc(choice):
    dataframes = [
    gdp_pcapita_PPP,
    unemployment_rate,
    gdpRD_df,
    val_addedPPP,
    ]
    
    colors = [    
        "b","g","r","c","m","y","k","b","g","r", "c","m","y", "k", "b",\
        "g", "y", "k", "b", "g", "r", "c",  "m",  "r",  "c",  "m",  "y",\
        "k",  "b",  "m",  "y",  "k","b",  "g","r",  "c",  "m", "y", "k",\
        "b", "g", "r", "c", "m", "y", "k",
        ]
    units = [
        '$USD',
        '%',
        '%',
        '$USD'
        ]
    
    titles = [
        'gdp_pcapita_PPP',
        "unemployment rate",
        "gdp % spent on R&D sector",
        "value added PPP R&D sector"]

    ind = 0
    for df in dataframes:
        cc = 0
        fig, axs = plt.subplots(1, 4, figsize=(20, 8))

        head = choice.sort_values("2018", ascending=False).head()
        lab_head = list(choice.sort_values("2018", ascending=False).head().index)

        tail = choice.sort_values("2018", ascending=False).tail()
        lab_tail = list(choice.sort_values("2018", ascending=False).tail().index)
        
        for c in list(head.index):
            try:
                idk = axs[0].plot(sorted(choice.columns), choice.loc[c], color=colors[cc], label=c)
            except:
                pass
            try:
                idk3 = axs[1].plot(sorted(df.columns), df.loc[c], color=colors[cc], label=c)
            except:
                pass
            axs[0].legend()
            axs[0].set_title('total broadband subs \n top 5')
            axs[1].legend()
            axs[1].set_title(str(titles[ind]) +'\n' + units[ind])
            cc += 1

        for c in list(tail.index):
            try:
                idk2 = axs[2].plot(sorted(choice.columns), choice.loc[c], color=colors[cc + 5], label=c)
            except:
                pass
            try:
                idk4 = axs[3].plot(sorted(df.columns), df.loc[c], color=colors[cc + 5], label=c)
            except:
                pass

            axs[2].legend()
            axs[2].set_title('total broadband subs \n bottom 5')
            axs[3].legend()
            axs[3].set_title(str(titles[ind]) +'\n' + units[ind])
            cc += 1
            
        plt.setp(axs[0].xaxis.get_majorticklabels(), rotation=45)
        plt.setp(axs[1].xaxis.get_majorticklabels(), rotation=45)
        plt.setp(axs[2].xaxis.get_majorticklabels(), rotation=45)
        plt.setp(axs[3].xaxis.get_majorticklabels(), rotation=45)
        ind += 1

        plt.show()
