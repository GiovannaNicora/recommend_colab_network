# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:56:32 2024

@author: evabr
"""
 
import pandas as pd
import csv
#%%Programming
data=pd.read_csv("full_network_for_python.csv")
#Definition of variables that will be used after
dict_list={}
list_new_links={}
dict_dataframe={}
#Creation of a list containing all the source nodes available in the data
list_nodes=list(pd.value_counts(data['Source']).index)
list_target=list(pd.value_counts(data['Target']).index)
for i in range(len(list_target)):
    if list_target[i] not in list_nodes: 
        list_nodes.append(list_target[i])
#Creation of a list containing all the keywords available in nodes  
list_keywords=[]
data_keywords=pd.read_excel('gephi_edges_tables_keywords.xlsx')
for i in data_keywords['Source']: 
    if i.lower() not in list_keywords: 
        list_keywords.append(i.lower())
        
#%%
#for each node, creation of a list, in the dictionnary dict_list, of the nodes it is linked to.
for j in range(len(list_nodes)):
    print(j)
    var2=list_nodes[j]
    dict_list[var2] = []
    for i in range(len(data['Target'])):
        if data['Source'][i]==list_nodes[j]: 
            dict_list[var2].append([data['Target'][i],data['Weight'][i]])
    for i in range(len(data['Source'])):
        if data['Target'][i]==list_nodes[j]: 
            dict_list[var2].append([data['Source'][i],data['Weight'][i]])
#%%
#Create a dataframe that contains the existing links between to nodes connected to a same nodes 
#Considering 3 nodes, A,B,C. A is connected to B and A is connected to C. If B and C are connected together
#this will be encoded by a 1, otherwise by 0. 
#Construction of the dataframe
for j in range(len(list_nodes)):
    print(j)
    var2=list_nodes[j]
    list_index_columns=[]
    for i in range(len(dict_list[var2])):
        list_index_columns.append(dict_list[var2][i][0])
    dict_dataframe['%s%s' % ('data', var2)]=pd.DataFrame(index=list_index_columns,columns=list_index_columns)
#%%

for j in range(len(list_nodes)):
    print(j)
    var2=list_nodes[j]
    for index in dict_dataframe['%s%s' % ('data', var2)].index: 
        for column in dict_dataframe['%s%s' % ('data', var2)].columns:
            for i in range(len(dict_list[index])):
                    if column in dict_list[index][i]:
                        dict_dataframe['%s%s' % ('data', var2)].loc[index,column]=dict_list[index][i][1]
    dict_dataframe['%s%s' % ('data', var2)]=dict_dataframe['%s%s' % ('data', var2)].fillna(value=0)
    
#%%
#Create a list of possible new links for each nodes, according to the data collected before
#Regarding the dataframe for each node, if the value of a cell egals 0, the name of the line
#and the name of the columns (which are two nodes) are added to a list of new possible links

print('NOUVEAUX LIENS')
for j in range(len(list_nodes)):
    print(j)
    var2=list_nodes[j]
    list_new_links['%s%s' % ('New_from_', var2)]=[]
    for index in range(len(dict_dataframe['%s%s' % ('data', var2)].index)): 
        for column in range(len(dict_dataframe['%s%s' % ('data', var2)].columns)):
            if (index+column)<len(dict_dataframe['%s%s' % ('data', var2)].columns):
                if dict_dataframe['%s%s' % ('data', var2)].iat[index,column+index]==0:
                    if list(dict_dataframe['%s%s' % ('data', var2)].columns)[index]!=list(dict_dataframe['%s%s' % ('data', var2)].columns)[column+index]: 
                       if ([list(dict_dataframe['%s%s' % ('data', var2)].columns)[index],list(dict_dataframe['%s%s' % ('data', var2)].columns)[index+column]] not in list_new_links['%s%s' % ('New_from_', var2)]) and ([list(dict_dataframe['%s%s' % ('data', var2)].columns)[index+column],list(dict_dataframe['%s%s' % ('data', var2)].columns)[index]] not in list_new_links['%s%s' % ('New_from_', var2)]):
                           list_new_links['%s%s' % ('New_from_', var2)].append([list(dict_dataframe['%s%s' % ('data', var2)].columns)[index],list(dict_dataframe['%s%s' % ('data', var2)].columns)[index+column]])



    
#%% Remove links that are not relevant and saving the relevant ones in a dictionnary
list_suggestions={}
for j in range(len(list_nodes)):
    print(j)
    var2=list_nodes[j]
    name=str('New_from_'+var2)
    list_suggestions[name]=[]
    for i in list_new_links[name]:
        if (i[0] not in list_keywords) and (i[1] not in list_keywords):
            if i not in list_suggestions[name]:
                list_suggestions[name].append(i)
        else:
            print(i)
#%% 
#Remove the nodes for which no new links are suggested
for j in range(len(list_nodes)):
    print(j)
    var2=list_nodes[j]
    name=str('New_from_'+var2)
    if len(list_suggestions[name])==0:
        del list_suggestions[name]
        
#%% research


node = input('From which center or keywork would you like to have suggestions of new links ?')
if node in list_nodes:
    name=str('New_from_'+node)
    print(list_suggestions[name])
else: 
    print("The name wanted is not in list of centers or keywords available")
export= input('Do you want to export the data in a CSV file ?')
if export == 'yes': 
    with open(str('Suggestion_from_'+name+'.csv'), 'w', encoding='utf-8') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(list_suggestions[name])
        
#%% Fit4Med group of disease of interest 

list_new_link_from_amputation=[]
for i in list_suggestions['New_from_lower-limb amputation']:
    list_new_link_from_amputation.append(i)
for i in list_suggestions['New_from_transfemoral amputation']: 
    if i not in list_new_link_from_amputation: 
        list_new_link_from_amputation.append(i)
with open(str('Suggestion_from_amputation.csv'), 'w', encoding='utf-8') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(list_new_link_from_amputation)
        
#%% Analysis 

list_fit4_centers= ['fondazione don carlo gnocchi-milan','fondazione don carlo gnocchi-florence',
               'irccs fondazione mondino-pavia','fondazione policlinico universitario campus bio-medico-rome',
               'istituto giannina gaslini-genoa','centro protesi inail-bologna','inail centro di riabilitazione motoria-volterra',
               'inail centro di protesi-vigorso di budrio','inail-monte porzio catone','istituto nazionale assicurazione infortuni sul lavoro (inail)-bologna',
               "istituto nazionale per l'assicurazione contro gli infortuni sul lavoro (inail)-volterra",'istituto scientifico fondazion s. maugeri-pavia',
               'irccs san martino polyclinic hospital-genoa','universitÃ  degli studi di modena e reggio emilia-modena',
               'universitÃ  degli studi di napoli federico ii-naples','ospedale valduce-como', 
               'irccs eugenio medea-bosisio parini','universitÃ  di pisa-pisa']

list_fit4_diseases=['stroke','multiple sclerosis','parkinson disease','neuropathy','spinal cord injury','acquired brain injury','lower-limb amputation', 'transfemoral amputation']


list_index=[]
for i in list_suggestions: 
    for j in list_suggestions[i]: 
        if (j[0] in list_fit4_centers) or (j[1] in list_fit4_centers): 
            if sorted(j) not in list_index:
                list_index.append(sorted(j))
index=[]
for i in list_index: 
    name = str(i[0]+'/'+i[1])
    index.append(name)
suggest_nb=pd.DataFrame(index=index,columns=['number of time','number of time on a subject of Fit4']) 

suggest_nb=suggest_nb.fillna(0)
for i in list_suggestions: 
    for j in list_suggestions[i]: 
        if sorted(j) in list_index:
            list_j=sorted(j)
            name=str(list_j[0]+'/'+list_j[1])
            suggest_nb.loc[[name],["number of time"]]+=1

for i in list_suggestions: 
    if i[9:] in list_fit4_diseases: 
        for j in list_suggestions[i]: 
            if sorted(j) in list_index: 
                list_j=sorted(j)
                name=str(list_j[0]+'/'+list_j[1])
                suggest_nb.loc[[name],["number of time on a subject of Fit4"]]+=1

suggest_nb.to_csv("Suggest_nb.csv")
            


#%%
#Exportation of the new links in a csv file
filename = 'mon_dict.csv'

# Sauvegarder le dictionnaire dans un fichier CSV
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
#     for key, value in list_new_links.items():
#         writer.writerow([key, value])

# print(f"The dictionnary have been saved as {filename}")
