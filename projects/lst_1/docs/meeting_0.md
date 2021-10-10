---
marp: true
---

# From book chapter 2 article

## Project update and research design 

_Last edit:_ Thu Aug 19 02:01:19 PM BST 2021

---

# Table of contents
- [From book chapter 2 article](#from-book-chapter-2-article)
	- [Project update and research design](#project-update-and-research-design)
- [Table of contents](#table-of-contents)
- [Project update](#project-update)
- [Population of companies](#population-of-companies)
- [Name ambiguity issues](#name-ambiguity-issues)
- [Data: domains & sources](#data-domains--sources)
- [Analytical strategy & tools:](#analytical-strategy--tools)

---

# Project update

![bg left](images/doh.png)

- MSc students collected tons of data from Bloomberg
- But the acquired data aren't research quality
  - there are some gaps and consistency issues
  - and Bloomberg isn't the best data source (reports come in .pdf format)
- Too bad, I had to do the data gathering from scratch

---

# Population of companies

- However, I had the opportunity to expand the data
- Our population: 95 'banks' traded in the NYSE
  - We adopt BvD's Orbis definition of 'bank'
  - The population of companies traverses the following NACE codes:
    - 64.19, 'other monetary intermediation'
    - 64.20, 'activities of holding'
    - 64.92, 'other credit granting'
    - 66.19, 'other activities auxiliary to financial services'
  - Get a closer look at the individual companies [here](https://docs.google.com/spreadsheets/d/1sNdpN4ueY40UIjzrmxVqd333wYrNkIYM/edit?usp=sharing&ouid=111993737706152551300&rtpof=true&sd=true)
  
---

# Name ambiguity issues

One __issue__, three manifestations:

- Oftentimes, panel data present name ambiguity issues. E.g.:
  - M&As might produce new entities
  - Legal entities can change over time
- Parent-subsidiary relationships
- Public companies' trusts 

[SEC's Edgar website](https://www.sec.gov/edgar/searchedgar/companysearch.html) provides us with the solution to the name ambiguity issue 

---

# Data: domains & sources

| Domain                    | Source            | Status      |
| ------------------------- | ----------------- | ----------- |
| 10-k                      | SEC               | In progress        |
| Proxy                     | SEC               | In progress        |
| Financial analyst reports | Mergent Online    | In progress        |
| Company news              | Eikon (Refinitiv) | To start |
| Investor presentations | Filing expert | To start |

Get a closer look at the data: [BlackRock example](https://drive.google.com/drive/folders/136x33ysZg7XNseGZJDZSo0v_H15eWB0t?usp=sharing).

---

# Analytical strategy & tools: 

- Topic modeling?
- Semantic network analysis?
- Discourse analysis?
- Formal analysis of meanings?
