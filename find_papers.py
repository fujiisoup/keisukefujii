"""
Find details of papers and export as necessary formats
Need to install crossref library,
>>> pip install crossref
"""
from crossref.restful import Works
import numpy as np
import json


def download_details(doi_list):
    works = Works()
    details = []
    for j, doi in enumerate(doi_list):
        doi = doi.strip()
        if doi[0] == '#':
            continue
        if ',' in doi:
            doi, tag = doi.split(',')
        else:
            tag = ''

        try:
            work = works.doi(doi)
        except json.decoder.JSONDecodeError:
            continue
        work['doi'] = doi
        detail = standarize(work)
        # add tag here
        detail['webpage_tag'] = tag.strip()
        details.append(detail)
    return details


def get_firstauthor(details):
    firstauthors = []
    for detail in details:
        if detail['author'][0].get('family', None).lower() == 'fujii':
            firstauthors.append(detail)
    return firstauthors


def standarize(detail):
    if 'journal-issue' not in detail:
        detail['journal-issue'] = {}
    if 'published-print' not in detail['journal-issue']:
        detail['journal-issue']['published-print'] = {}
        detail['journal-issue']['published-print']['date-parts'] = detail['issued']['date-parts']
    if len(detail['journal-issue']['published-print']['date-parts'][0]) < 2:
        if isinstance(detail['journal-issue']['published-print']['date-parts'][0][0], list):
            detail['journal-issue']['published-print']['date-parts'][0] = detail['journal-issue']['published-print']['date-parts'][0][0]
        if len(detail['journal-issue']['published-print']['date-parts'][0]) == 1:
            detail['journal-issue']['published-print']['date-parts'][0].append(0)  # month not available

    if 'container-title' in detail:
        if len(detail['container-title']) == 0:
            print(detail['doi'])
            print(detail)

    for author in detail['author']:
        if 'family' not in author:
            author['family'] = author['name']
        if 'given' not in author:
            author['given'] = ''
    return detail


def sort_by_date(details, newest_first=True):
    dates = []
    for detail in details:
        y = detail['journal-issue']['published-print']['date-parts'][0][0]
        m = detail['journal-issue']['published-print']['date-parts'][0][1]
            
        dates.append(int('{0:d}{1:02d}'.format(y, m)))
    idx = np.argsort(dates)
    if newest_first:
        idx = idx[::-1]
    return [details[i] for i in idx]


def save_markdown(details, outname):
    """
    Save as a markdown format
    """
    details = sort_by_date(details)
    header = [
        "---",
        "layout: publications ",
        "---",
        "",
    ]
    selected_papers = [
        "# List of selected papers",
    ]
    first_corresponding_papers = [
        "# List of papers (first- and corresponding-author)"
    ]
    other_papers = [
        "# List of published papers"
    ] 
    i_selected = 0
    i_first = 0
    i_other = 0
    for i, detail in enumerate(details):
        lines = []
        lines.append('**{}**  '.format(detail['title'][0]))
        authors = ''
        for author in detail['author']:
            if author['family'].lower() == 'fujii':
                authors += '**<u>{} {}</u>**, '.format(author['given'], author['family'])
            else:
                authors += '{} {}, '.format(author['given'], author['family'])
        lines.append(' {}  '.format(authors[:-2]))  # remove the last comma
        # journal
        articlenumber = detail.get('article-number', detail.get('page'))
        lines.append(' *{}* **{},** {} ({})  '.format(
            detail['container-title'][0], 
            detail['volume'],
            articlenumber, 
            detail['journal-issue']['published-print']['date-parts'][0][0]
        ))
        lines.append('<a href="https://doi.org/{0:s}">{0:s}</a>  \n'.format(detail['doi']))
        
        if 'corresponding' in detail.get('webpage_tag', ''):
            i_first += 1
            first_corresponding_papers += [
                '{}. {}'.format(i_first, l) if i == 0 else l for i, l in enumerate(lines)
            ]
            if '*' in detail['webpage_tag']:
                i_selected += 1
                selected_papers += [
                    '{}. {}'.format(i_selected, l) if i == 0 else l for i, l in enumerate(lines)
                ]
        else:
            i_other += 1
            other_papers += [
                '{}. {}'.format(i_other, l) if i == 0 else l for i, l in enumerate(lines)
            ]
    with open(outname, 'w') as f:
        for line in (
            header + selected_papers + first_corresponding_papers + other_papers
        ):
            f.write(line + '\n')


if __name__ == '__main__':
    with open('./data/papers.csv', 'r') as f:
        doi_list = f.readlines()
    details = download_details(doi_list)
    with open('./data/selected_papers.csv', 'r') as f:
        selected_doi_list = f.readlines()
    selected_details = download_details(selected_doi_list)
    # with open('dois.txt', 'w') as f:
    #     for detail in details:
    #         f.write('{}\n'.format(detail))
    save_markdown(details, 'publications/index.md')
    # save_cv1(details, 'private_papers.md')