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


def get_var(df, var):
    if "VAR" in df.columns:
        return df[df["VAR"] == var].fillna(value=0)
    elif 'ï»¿"MSTI_VAR"' in df.columns:
        return df[df['ï»¿"MSTI_VAR"'] == var].fillna(value=0)
    elif 'VARIABLE' in df.columns:
        return df[df['VARIABLE'] == var].fillna(0)
    

def get_values(df):
    countries = list(df.Country.unique())
    data = {}
    if "Time" in df.columns:
        years = list(df.Time.unique())
        for y in years:
            data[str(y)] = {}
            for c in countries:
                value = df.loc[(df["Country"] == c) & (df["Time"] == y)].Value.values
                if value.shape == (1,):
                    data[str(y)][c] = float(value)
                else:
                    data[str(y)][c] = np.nan

    elif "Year" in list(df.columns):
        years = list(df.Year.unique())
        for y in years:
            data[str(y)] = {}
            for c in countries:
                value = df.loc[(df["Country"] == c) & (df["Year"] == y)].Value.values
                if value.shape == (1,):
                    data[str(y)][c] = float(value)
                else:
                    data[str(y)][c] = np.nan

    return pd.DataFrame(data)



def plotitfunc(choice):
    dataframes = [
    gdpRD_df,
    val_addedPPP,
    gdp_ppp,
    unemployment_rate,
    gdp_percapita,
    gdp_pcapita_PPP
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
