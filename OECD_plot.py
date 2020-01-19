def plotme(dataframes, choice):
    
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
