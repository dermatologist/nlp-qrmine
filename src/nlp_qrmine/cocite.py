import sys
import time

from Bio import Entrez


def main():

    print("Finding Articles citing the given reference.....")

    for var in sys.argv:
        time.sleep(3)
        articles = []
        print("Processing ", var)
        Entrez.email = 'cocite_application@gulfdoctor.net'
        pmids = ','.join(Entrez.read(Entrez.esearch(db='pubmed', term=var)))
        pmids = ','.join(Entrez.read(Entrez.elink(dbfrom="pubmed", id=pmids, linkname="pubmed_pubmed_citedin")))
        handle = Entrez.efetch(db="pubmed", retmode="xml")
        records = Entrez.parse(handle)
        for record in records:
            articles.append(record['PMID'])

        # Remove duplicates: SO 7961363
        articles = list(set(articles)) 
        article_no = len(articles)

    print("Finding Co-citations. This may take several hours...........")

    for article in articles:
        time.sleep(3)

    print("_________________________________________")
    print("CoCite - QRMine.\n\n")
    print("Cocitation finder\n")
    print("-----------------------------------------")

    print("-----------------------------------------")



if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
