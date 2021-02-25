import numpy as np


def domestic(csv_file):
    markdown = []
    with open(csv_file, 'r') as f:
        lines = f.readlines()[1:]

    lines = [line.split(',') for line in lines if line[0] != '#']
    dates = np.array(
        [np.datetime64('{0:d}-{1:02d}-{2:02d}'.format(
            int(line[-3]), int(line[-2]), int(line[-1])))
         for line in lines])
    index = np.argsort(dates)[::-1]
    markdown.append('# List of domestic conference presentation')
    
    for i, ind in enumerate(index):
        line = lines[ind]
        line = [l.strip() for l in line]
        markdown.append(
'''
## {}. {}  
**{}**  
{}  
*{}*  
{}/{} ({})  
'''.format(
    i + 1, line[0], 
    line[1], # title
    ','.join(line[3].split(';')),  # name
    line[2],  # conference
    line[5], line[6], line[4]
        ))
    
    with open('domestic_talks.md', 'w') as f:
        for line in markdown:
            f.write(line + '\n')


def international(csv_file):
    markdown = []
    with open(csv_file, 'r') as f:
        lines = f.readlines()[1:]

    lines = [line.split(',') for line in lines if line[0] != '#']
    dates = np.array(
        [np.datetime64('{0:d}-{1:02d}-{2:02d}'.format(
            int(line[-3]), int(line[-2]), int(line[-1])))
         for line in lines])
    index = np.argsort(dates)[::-1]
    markdown.append('# List of international conference presentation')
    
    for i, ind in enumerate(index):
        line = lines[ind]
        line = [l.strip() for l in line]
        markdown.append(
'''
## {0:d}. {1:s}  
**{2:s}**  
*{3:s}*  
{4:s}/{5:02d} {6:s} ({7:s})  
'''.format(
    i + 1, line[0], 
    line[1], # title
    line[2],  # conference
    line[5], int(line[6]), line[3], line[4]
        ))
    
    with open('international_talks.md', 'w') as f:
        for line in markdown:
            f.write(line + '\n')


if __name__ == '__main__':
    domestic('domestic_conferences.csv')
    international('international_conferences.csv')

