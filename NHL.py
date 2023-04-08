import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

dic_abv = {'V': "victoire",
           'D': "defaite",
           'DP': "defaite par prolongation",
           'PTS': "points",
           'BP': "buts marquer",
           'BC': "buts encaisser",
           'DIFF': "difference de buts"}

division = ["Atlantic","Metropolitan","Central","Pacific"]

def lire_classement():
    classement = {}

    with open("Projet_2_NHL-main\database\classement2019.txt") as file :
        raw = file.readlines()

    leagues = []

    i = -1

    while i < len(raw)-1 :
        i += 1
        j = i
        while raw[i] != "\n" and i < len(raw)-1 :
            i+=1
        if i == 40 :
            i += 1
        leagues.append(raw[j:i])

    for league in leagues:
        league_name = league[0].split()[1]
        league_teams = []
        for team in league[1:]:
            dic = {"Name" : team.split()[0]} | dict(zip(league[0].split()[2:],team.split()[1:])) | {"DIV" : league_name}
            for key in dic:
                try:
                    dic[key] = int(dic[key])
                except Exception:
                    pass
            league_teams.append(dic)
        classement[league_name] = league_teams

    return classement

ligue_classement = lire_classement()

def creer_df(ligue_classement):
    # To-Do: Vous devez creer votre dataframe a partir d'un dictionnaire
    # To-Do: Pour cela commencer par regrouper toute les equipe dans un seul dictionnaire
    # To-Do: Que vous allez convertir en dataframe. la fonction retourne un dataframe
    # Lien utile: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html

    data = {}
    for dic in ligue_classement :
        for team in ligue_classement[dic] :
            data[team["Name"]] = {key:team[key] for key in team if key != "Name"}

    df = pd.DataFrame.from_dict(data, orient = "index")

    return df

df = creer_df(ligue_classement)

def df_extraite_division(df_f, division):

    filtre=(df["DIV"]==division)
    df_func = df_f.copy()
    df_func.drop("DIV", inplace=True, axis=1)

    return df_func[filtre]

def df_sort_type(df_f,colonne,ordre):

    df_func = df_f.copy()
    df_func.sort_values(by=colonne, ascending= ordre ,inplace=True)

    return df_func


def df_summary_inf(nhl_df):
    #ToDo: la fonction affiche les stats des equipes
    noms_statistique = ["Victoire", "defaite", "defaite par prolongation", "points", "buts marqués", "buts encaissés", "difference de but"]
    indice = [2,3,4,5,7,8,9]#Indices utilisé pour avoir les bonnes colonnes dans le dataframe panda : nhl_df.column()[indice[0]] ---> "V"

    for division in nhl_df.drop_duplicates(subset=['DIV'])["DIV"]:#Boucle pour visiter toute les divisions (les 4 divisions)
        print(f"Stats division {division}:")

        division_df = df_extraite_division(nhl_df, division)#Avoir seulement les equipes de la division en question
        for i in range(len(noms_statistique)):#Pour pouvoir avoir toute les analyses qu'il faut avoir, i.e la longueur de la liste des noms des statistiques
            division_trie_df = df_sort_type(division_df, division_df.columns[indice[i]], False)#dataframe de la division triee en fonction de la statistique 
            statistique = division_trie_df[division_df.columns[indice[i]]][0]#Récupère la valeur de la statistique de la meilleur équipe 
            equipe = division_trie_df.index[0]#récupère le nom de ladit equipe
            print(f"\tL'équipe qui a le plus de {noms_statistique[i]} est {equipe} avec {statistique} {noms_statistique[i]} \n")

    print("Stats ligue:")
    for i in range(len(noms_statistique)):#Pour pouvoir avoir toute les analyses qu'il faut avoir, i.e les élements de la liste noms_statistique
        nhl_trie_df = df_sort_type(nhl_df, nhl_df.columns[indice[i]], False)#dataframe en parametre triee en fonction de la statistique

        statistique = nhl_trie_df[nhl_df.columns[indice[i]]][0]#Récupère la valeur de la statistique de la meilleur équipe
        equipe = nhl_trie_df.index[0]#récupère le nom de ladit equipe
        print(f"\tL'équipe qui a le plus de {noms_statistique[i]} est {equipe} avec {statistique} {noms_statistique[i]} \n")
    
    print("Stats ligue:")
    for i in range(len(noms_statistique)):#Pour pouvoir avoir toute les analyses qu'il faut avoir, i.e les élements de la liste noms_statistique
        nhl_trie_df = df_sort_type(nhl_df, nhl_df.columns[indice[i]], False)#dataframe en parametre triee en fonction de la statistique

        statistique = nhl_trie_df[nhl_df.columns[indice[i]]][0]#Récupère la valeur de la statistique de la meilleur équipe
        equipe = nhl_trie_df.index[0]#récupère le nom de ladit equipe
        print(f"\tL'équipe qui a le plus de {noms_statistique[i]} est {equipe} avec {statistique} {noms_statistique[i]} \n")


def df_summary_division(df, sort_by, ascending=True):

    divisions = df.groupby('DIV', group_keys=True)

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 7),)

    for (division, data), ax in zip(divisions, axs.flatten()):
        sns.barplot(data=data.sort_values(sort_by, ascending= ascending), y ='ABV', x = sort_by, ax=ax, palette="Spectral")
        ax.set(title=f"Division {division}")

    plt.show()


def df_summary_league(df, type_sort, ascending):
    # Tri du dataframe en fonction du critère et de l'ordre
    df_sorted = df.sort_values(by=type_sort, ascending= ascending)
    df_top10 = df_sorted.head(10)
    
    # Créer un histogramme 
    ax = sns.barplot(x=type_sort, y=df_top10.index, data=df_top10, palette="Spectral")
    ax.set_title("Top 10 de la ligue trié par {}".format(type_sort))

    plt.show()

def df_groupby_div(df_f):
    # To-Do: la fonction regroupe le dataframe par division
    # Lien utile: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
    nouveau_df = df_f.copy().groupby(['DIV']).sum(numeric_only=True)
    print(nouveau_df)
    return nouveau_df


def df_secteur_div(nhl_df, type_statistique, bool):
    dix_meilleures = df_sort_type(nhl_df, type_statistique,bool).head(10) # trier le df par rapport au critère demandé et récupère les 10 premiers
    print(dix_meilleures)
    divisions_somme = df_groupby_div(dix_meilleures) # regrouper par division
    divisions_pourcentage = (100. * divisions_somme / divisions_somme.sum()).round(1) # creer un dataframe avec les pourcentage (rapport critère / somme de la colonne)
    pourcentages = divisions_pourcentage[type_statistique] # on recupère la colonne qui nous interesse
    fig, ax = plt.subplots()
    ax.pie(pourcentages, labels=[pourcentage for pourcentage in pourcentages if pourcentage != "DIV"]) # cree le pie chart 
    hole = plt.Circle((0, 0), 0.65, facecolor='white') # fait le trou au milieu
    ax.set(title=f'Statistiques de {dic_abv[type_statistique]}')

    ax.legend(labels=divisions_pourcentage.index, bbox_to_anchor=(.9, .5)) # ajouter la légende

    plt.gcf().gca().add_artist(hole)
    plt.show()

if __name__ == '__main__':
    # 1.1
    ligue_classement = lire_classement()
    
    # 1.2
    nhl_df = creer_df(ligue_classement)
    print(nhl_df)
    # 1.3
    for div in division:
        print(df_extraite_division(nhl_df, div))
        print("\n")
        
    # 1.4.a
    nhl_df_sort_by_pts = df_sort_type(nhl_df, "PTS", False)
    print(nhl_df_sort_by_pts)
    print("\n")
    
    # 1.4.b
    nhl_div_df = df_extraite_division(nhl_df, "Atlantic")
    nhl_div_df_sort_by_v = df_sort_type(nhl_div_df, "V", True)
    print(nhl_div_df_sort_by_v)
    
    # 1.5
    df_summary_inf(nhl_df)
    
    # 2.1
    df_summary_division(nhl_df,"PTS", False)
    df_summary_division(nhl_df,"V", False)
    df_summary_division(nhl_df,"BP", False)
    
    # 2.2
    df_summary_league(nhl_df,"PTS", False)
    df_summary_league(nhl_df,"V", False)
    df_summary_league(nhl_df,"DIFF", False)
    df_summary_league(nhl_df,"DIFF", True)
    
    # 2.3.a
    df_secteur_div(nhl_df, "PTS", False)
    df_secteur_div(nhl_df, "PTS", True)
    
    # 2.3.a
    df_secteur_div(nhl_df, "V", False)
    df_secteur_div(nhl_df, "V", True)