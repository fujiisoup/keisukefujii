import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MaxNLocator
import seaborn as sns

matplotlib.rc('font', size=14)


# Events
positions = [
    # until year, until month, height, name
    (2012, 3, 6, 'PhD. candidate'),
    (2022, 3, 8.2, 'Kyoto Univ'),
    (None, None, 8.2, 'ORNL'),
]

#----------------------------------------------------------------
# papers
# analyzing publications/index.md
#----------------------------------------------------------------

with open('publications/index.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# first authored papers
first = []
first_years = []
coaut = []
coaut_years = []

for i, line in enumerate(lines):
    if "# List of papers (first- and corresponding-author)" in line:
        lines = lines[i+1:]
        break

papers = first
years = first_years
offset = 0
for i in range(0, len(lines) - 5, 5):
    if "# List of published papers" in lines[i]:
        papers = coaut
        years = coaut_years
        offset = 1
    journal = lines[i + 2 + offset].strip()
    year = int(journal[-5:-1])
    #journal = journal[journal.find('*') + 1:]
    #journal = journal[: journal.find('*')]
    years.append(year)
    papers.append(1)
years = np.concatenate([first_years, coaut_years])

bins = np.arange(np.min(years), np.max(years) + 1)

plt.figure(figsize=(15, 5))
plt.hist(first_years, bins=bins, color='C0', width=0.9, label='first authored', zorder=3)
plt.hist(years, bins=bins, color='0.8', width=0.9, label='all', zorder=1,)
plt.xticks(bins - 0.55, ['{}'.format(b) for b in bins]) 
plt.gca().yaxis.grid(color='0.8', alpha=0.8)
plt.xlabel('year')
plt.ylabel('number of papers / year')

start = 2008 + 3 / 12
for y, m, height, position in positions:
    if y is None:
        now = datetime.datetime.now()
        now = now.year + now.month / 12 + 1
    else:
        now = y + m / 12
        plt.axvline(now - 1, color='0.5', ls='--')
    plt.text((start + now) / 2 - 1, height, position, color='k', ha='center')
    start = now
    
plt.legend(loc='upper left')
sns.despine()
plt.savefig('publication_history.png', bbox_inches='tight')


#----------------------------------------------------------------
# talks
# analyzing data/international_conferences.csv
#----------------------------------------------------------------

with open('data/international_conferences.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# first authored papers
years = []
talk_types = []

for line in lines[1:]:
    talk_type = line.split(',')[0].strip()
    year = line.split(',')[-2].strip()
    year = year[:year.find('/')]
    years.append(int(year))
    talk_types.append(talk_type)

plt.figure(figsize=(15, 5))
plt.hist(years, bins=bins, color='0.8', width=0.9, label='poster', zorder=1)
plt.hist([y for y, t in zip(years, talk_types) if t in ['oral', 'invited']], bins=bins, color='C0', width=0.9, label='oral', zorder=2)
plt.hist([y for y, t in zip(years, talk_types) if t == 'invited'], bins=bins, color='C1', width=0.9, label='invited', zorder=3)
plt.xticks(bins - 0.55, ['{}'.format(b) for b in bins]) 
plt.gca().yaxis.grid(color='0.8', alpha=0.8)
plt.xlabel('year')
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.ylabel('number of talks / year')

start = 2008 + 3 / 12
for y, m, height, position in positions:
    if y is None:
        now = datetime.datetime.now()
        now = now.year + now.month / 12 + 1
    else:
        now = y + m / 12
        plt.axvline(now - 1, color='0.5', ls='--')
    start = now

plt.legend(loc='upper left')
sns.despine()
plt.savefig('talk_history.png', bbox_inches='tight')


#----------------------------------------------------------------
# reviews
#----------------------------------------------------------------

with open('data/private_reviewing.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# first authored papers
years = []

for line in lines[1:]:
    if line[0] == '#':
        continue
    year = line.split(',')[-1].strip()
    year = year[:year.find('/')]
    years.append(int(year))

plt.figure(figsize=(15, 5))
plt.hist(years, bins=bins, color='C0', width=0.9)
plt.xticks(bins - 0.55, ['{}'.format(b) for b in bins]) 
plt.gca().yaxis.grid(color='0.8', alpha=0.8)
plt.xlabel('year')
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.ylabel('number of paper reviewing / year')

start = 2008 + 3 / 12
for y, m, height, position in positions:
    if y is None:
        now = datetime.datetime.now()
        now = now.year + now.month / 12 + 1
    else:
        now = y + m / 12
        plt.axvline(now - 1, color='0.5', ls='--')
    start = now

sns.despine()
plt.savefig('reviewing_history.png', bbox_inches='tight')

