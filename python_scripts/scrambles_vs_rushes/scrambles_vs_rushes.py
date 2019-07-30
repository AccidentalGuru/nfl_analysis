import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Ignore chained assignment warning
pd.options.mode.chained_assignment = None

data = pd.read_csv('https://raw.githubusercontent.com/ryurko/nflscrapR-data/master/play_by_play_data/regular_season/reg_pbp_2018.csv')

#Get rid of quarters ending and other events
data = data.loc[
    (data['epa'].notnull()) &
    ((data['play_type'] == 'no_play') |
    (data['play_type'] == 'pass') |
    (data['play_type'] == 'run'))
]

#Remove timeouts
data.drop(data[(data['replay_or_challenge'] == 0) & (data['desc'].str.contains('Timeout'))].index, inplace=True)

#Classify running plays with penalities as runs
data.loc[data.desc.str.contains('left end|left tackle|left guard|up the middle|right guard|right tackle|right end|rushes'), 'play_type'] = 'run'

#Classify scrambles, sacks, and incomplete/complete with penalty as pass plays instead of runs/no play
data.loc[data.desc.str.contains('scrambles|sacked|pass'), 'play_type'] = 'pass'

#Remove kneels and spikes
#Kneels and spikes with penalties are classified as no_play, thus not removed in above cell
data = data.loc[data.desc.str.contains('kneels|spiked') == False]

#Reindex data dataframe
data.reset_index(drop=True, inplace=True)

#Create a smaller dataframe with plays where rusher_player_name is null
rusher_nan = data.loc[(data['play_type'] == 'run') &
         (data['rusher_player_name'].isnull())]

#Create a list of the indexes/indices for the plays where rusher_player_name is null
rusher_nan_indices = list(rusher_nan.index)

for i in rusher_nan_indices:
    #Split the description on the blank spaces, isolating each word
    desc = data['desc'].iloc[i].split()
    
    #For each word in the play description
    for j in range(0,len(desc)):
        #If a word is right, up, or left
        if desc[j] == 'right' or desc[j] == 'up' or desc[j] == 'left':
            #Set rusher_player_name for that play to the word just before the direction
            data['rusher_player_name'].iloc[i] = desc[j-1]
            
        else:
            pass

 passer_nan = data.loc[(data['play_type'] == 'pass') &
         (data['passer_player_name'].isnull())]

passer_nan_indices = list(passer_nan.index)

for i in passer_nan_indices:
    desc = data['desc'].iloc[i].split()
    
    for j in range(0,len(desc)):
        if desc[j] == 'pass':
            data['passer_player_name'].iloc[i] = desc[j-1]
            
        else:
            pass
        
data.loc[data['passer_player_name'] == 'Backward', 'passer_player_name'] = float('NaN')

data.insert(69, 'success', 0)
data.loc[data['epa'] > 0, 'success'] = 1

epa_running = data['epa'].loc[data['play_type']=='run']
epa_scrambles = data['epa'].loc[data['desc'].str.contains('scrambles')]

#Neutral situation runs and scrambles
neutral_epa_running = data['epa'].loc[(data['play_type']=='run') & (data['qtr']<=2) & (data['down']<=2)]
neutral_epa_scrambles = data['epa'].loc[(data['desc'].str.contains('scrambles')) & (data['qtr']<=2) & (data['down']<=2)]

#Non redzone runs and scrambles
non_rz_epa_running = data['epa'].loc[(data['play_type']=='run') & (data['yardline_100'] > 20)]
non_rz_epa_scrambles = data['epa'].loc[(data['desc'].str.contains('scrambles')) & (data['yardline_100'] > 20)]

#Chart all runs and scrambles
fig, ax = plt.subplots(figsize=(10,6))

ax.hist(epa_running, label='Designed Runs', bins=20, color='slategrey')
ax.hist(epa_scrambles, label='Scrambles', bins=20, color='springgreen')

ax.set_yscale('log')
ax.set_yticks([1, 10, 100, 1000, 10000])
ax.set_ylabel('Number of Plays (log scale)')
ax.set_xticks(np.linspace(-9,9,19))
ax.set_xlabel('Expected Points Added')
ax.set_title('EPA on Designed Runs vs Scrambles - 2018')
ax.text(5.8, 2000, 'Data from nflscrapR', alpha=.7)
ax.legend()

plt.savefig('epa_runs_vs_scrambles.png', dpi=400)

#Chart neutral situation runs and scrambles
fig, ax = plt.subplots(figsize=(10,6))

ax.hist(neutral_epa_running, label='Neutral Designed Runs', bins=20, color='slategrey')
ax.hist(neutral_epa_scrambles, label='Neutral Scrambles', bins=20, color='springgreen')

ax.set_yscale('log')
ax.set_yticks([1, 10, 100, 1000, 10000])
ax.set_ylabel('Number of Plays (log scale)')
ax.set_xticks(np.linspace(-9,9,19))
ax.set_xlabel('Expected Points Added')
ax.set_title('EPA on Designed Runs vs Scrambles (Neutral Situations) - 2018')
ax.text(5.8, 2000, 'Data from nflscrapR', alpha=.7)
ax.legend()

plt.savefig('neutral_epa_runs_vs_scrambles.png', dpi=400)

#Chart non redzone runs and scrambles
fig, ax = plt.subplots(figsize=(10,6))

ax.hist(non_rz_epa_running, label='Non-Redzone Designed Runs', bins=20, color='slategrey')
ax.hist(non_rz_epa_scrambles, label='Non-Redzone Scrambles', bins=20, color='springgreen')

ax.set_yscale('log')
ax.set_yticks([1, 10, 100, 1000, 10000])
ax.set_ylabel('Number of Plays (log scale)')
ax.set_xticks(np.linspace(-9,9,19))
ax.set_xlabel('Expected Points Added')
ax.set_title('EPA on Designed Runs vs Scrambles (Non-Redzone) - 2018')
ax.text(5.8, 2000, 'Data from nflscrapR', alpha=.7)
ax.legend()

plt.savefig('non_rz_epa_runs_vs_scrambles.png', dpi=400)

#Success rates from designed runs and scrambles
run_success = data['success'].loc[data['play_type']=='run'].mean()
scramble_success = data['success'].loc[data['desc'].str.contains('scrambles')].mean()

#Create a summary dataframe
df = pd.DataFrame(index=['Designed Runs','Scrambles'],columns=['Mean EPA', 'St. Dev', 'Success Rate', 'Attempts'])
df.loc['Designed Runs'] = [epa_running.mean(), epa_running.std(), run_success, len(epa_running)]
df.loc['Scrambles'] = [epa_scrambles.mean(), epa_scrambles.std(), scramble_success, len(epa_scrambles)]

df['Mean EPA'] = df['Mean EPA'].astype(float).round(3)
df['St. Dev'] = df['St. Dev'].astype(float).round(3)
df['Success Rate'] = df['Success Rate'].astype(float).round(2)