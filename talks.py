"""
Convert to a markdown for talks
"""
import numpy as np
from numpy.core.fromnumeric import sort
import pandas as pd
import json
"""
Find details of papers and export as necessary formats
Need to install crossref library,
>>> pip install crossref
"""
from crossref.restful import Works
import numpy as np
import json


def sort_by_date(conferences, newest_first=True):
    dates = conferences['start_date']
    idx = np.argsort(dates)
    if newest_first:
        idx = idx[::-1]

    return conferences.iloc[idx]


def save_markdown(international, domestic, outname):
    """
    Save as a markdown format
    """
    header = [
        "---",
        "layout: talks ",
        "---",
        "",
    ]
    current_type = None

    contents = ["# Talks in International Conferences\n"]
    second_header = {
        'invited': "## Invited talks\n",
        'oral': "## Oral talks\n",
        'poster': "## Posters\n",
    }

    for type_ in ['invited', 'oral', 'poster']:
        if current_type != type_:
            contents.append(second_header[type_])
        
        conf = international[international['type'] == type_]
        for i in range(len(conf)):
            c = conf.iloc[i]
            text = """{0:d}. **{1:s}**  \n*{2:s}*  \n{3:s}, {4:s}, {5:s}-{6:s}\n""".format(
                i + 1, c['title'], c['conference'], c['city'], c['country'],
                c['start_date'].strftime('%Y. %b. %d'), c['end_date'].strftime('%b. %d')
            )
            contents.append(text)

    contents += ["# Talks in Domestic Conferences\n"]
    for type_ in ['invited', 'oral', 'poster']:
        if current_type != type_:
            contents.append(second_header[type_])
        
        conf = domestic[domestic['type'] == type_]
        for i in range(len(conf)):
            c = conf.iloc[i]
            text = """{0:d}. **{1:s}**  \n""".format(
                i + 1, c['title'])
            text += ', '.join(c['authors'].split(';')) + '  \n'
            text += """*{0:s}*, {1:s}, {2:s}-{3:s}  \n""".format(
                c['conference'], c['city'],
                c['start_date'].strftime('%Y. %b. %d'), c['end_date'].strftime('%b. %d')
            )
            contents.append(text)
            
    with open(outname, 'w') as f:
        for line in (
            header + contents
        ):
            f.write(line + '\n')


if __name__ == '__main__':
    international = pd.read_csv(
        './data/international_conferences.csv',
        parse_dates=[5, 6], skipinitialspace=True, comment='#',
        index_col=False,
    )
    international = sort_by_date(international)

    domestic = pd.read_csv(
        './data/domestic_conferences.csv',
        parse_dates=[5, 6], 
        skipinitialspace=True, comment='#',
        index_col=False,
    )
    domestic = sort_by_date(domestic)
    save_markdown(international, domestic, 'talks/index.md')