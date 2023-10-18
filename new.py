import pandas as pd 
import re

# https://stackoverflow.com/a/41516221
transl_table = dict( [ (ord(x), ord(y)) for x,y in zip( u"‘’´“”–-",  u"'''\"\"--") ] ) 

def format_text(line):
    line = line.replace("%", "\%")
    line = line.replace("_", "\_")
    line = line.replace("&", "\&")
    line = line.translate(transl_table)
    return line 

def format_authors(line):
    try:
        authors = line.split(", ")
        simple_authors = authors.copy()
        for i, _ in enumerate(authors):
            author = authors[i].strip()
            try:
                idx = re.search(r'[^a-zA-Z .$]', author).end()
                simple_authors[i] = author[:idx-1]
                authors[i] = author[:idx-1] + f'$^{{{author[idx-1:]}}}$'
            except:
                simple_authors[i] = author
                authors[i] = author            
        line = ', '.join(authors)
        for j, simple_author in enumerate(simple_authors):
            simple_authors[j] = simple_author.split(" ")[-1].strip() + "!" + ' '.join(simple_author.split(" ")[:-1])
        author_idx = ", ".join(simple_authors)
    except:
        pass
    return line, author_idx 

def format_affiliation(line):
    try:
        line = line.replace("&", "\&")
        schools = line.split("|")
        for i, school in enumerate(schools):
            school = school.replace(";", ",").strip()
            if school[0].isnumeric():
                idx = school.find(next(filter(str.isalpha, school)))
                school = f'$^{{{school[:idx].strip()}}}$' + school[idx:].strip()
            schools[i] = school.strip()
        line = ' $\\bullet$ '.join(schools)
    except:
        line = ""
        pass
    return line 

def format_emails(line):
    try:
        line = line.replace(" ", "")
        emails = line.split(",")
        line = ', '.join(emails)
    except:
        line = ""
        pass
    return line

def create_abstract(row):
    # if row.name > 0:
    #     return
    try:
        id = row['Paper id']
        title = format_text(row['Title'])
        authors, author_idx = format_authors(row["Authors"])
        affiliation = format_affiliation(row["Affiliation"])
        keywords = row['Keyword']
        emails = format_emails(row["Email id"])
        text = format_text(row["Abstract"])
        print(author_idx)
        s = f'''
    \\begin{{conf-abstract}}[]
        {{\\textbf{{{title}}}}}
        {{\\textit{{{authors}}}}}
        {{{affiliation}}}
        {{\\texttt{{{emails}}}}}
        \indexauthors{{{author_idx}}}
        {{{text}}}
    \\end{{conf-abstract}}
        '''
        f = open(f"abstracts/Paper_{id}.tex", "w")
        f.write(s)
        f.close() 
    except Exception as e:
        print(id, e)
        pass

df = pd.read_csv("comsys 2022 Abstract_50_updated.tsv", sep="\t", encoding='utf-8')
df.apply(create_abstract, axis = 1)