# Factiva data collection - README

- [Factiva data collection - README](#factiva-data-collection---readme)
  - [Overview of the scripts/procedures included in the current folder](#overview-of-the-scriptsprocedures-included-in-the-current-folder)
  - [Eikon data](#eikon-data)
  - [Factiva data](#factiva-data)
    - [Article search](#article-search)
    - [Outcome of the query](#outcome-of-the-query)
      - [Query 0](#query-0)
      - [Query 1](#query-1)
      - [Query 2](#query-2)
      - [Query 3](#query-3)
## Overview of the scripts/procedures included in the current folder

| Script   | Task                               | Status | Warnings |
| :------- | :--------------------------------- | :----- | :------- |
| eikon.py | parse .rtf downloaded from Factiva | run    | none     |

The Factiva data collection sticks to a hand-curated workflow ― summarized 
below.
## Eikon data 

__!! TO DO !!__
## Factiva data
### Article search

Keywords have been derived from the Google Knowledge Graph:

+ Computer Software
+ Internet of Things
+ Machine Learning
+ Robotics
+ Technology
+ Computer Science
+ Computers
+ Automation
+ Augmented Reality
+ Big Data
+ Deep Learning
+ Cloud Computing
+ Natural Language Processing
+ Pattern Recognition
+ Analytics
+ Computing

### Outcome of the query

#### Query 0

| Attribute | Value                                                    |
| :-------- | :------------------------------------------------------- |
| Text      | ("artificial intelligence" or "deep learning")           |
|           | and (rst=sfft or rst=sfwsj or rst=sfeco) and (in=ifinal) |
| Date      | 01/01/2000 to 28/02/2019                                 |
| Source    | All Sources                                              |
| Author    | All Authors                                              |
| Company   | All Companies                                            |
| Subject   | All Subjects                                             |
| Industry  | Financial services                                       |
| Region    | All Regions                                              |
| Language  | English                                                  |
| Results   | Found 2,951                                              |
| Timestamp | 6 March 2019 21:52                                       |
| Status    | NOT TO CARRY OUT                                         |

#### Query 1

| Attribute  | Value                                                                    |
| :--------- | :----------------------------------------------------------------------- |
| Text       | ("artificial intelligence" or "deep learning" or                         |
|            | "machine learning" or "big data" or "natural language processing"        |
|            | or "analytics") and (rst=sfft or rst=sfwsj or rst=sfeco) and (in=ifinal) |
| Date       | 01/01/2000 to 31/03/2019                                                 |
| Source     | All Sources                                                              |
| Author     | All Authors                                                              |
| Company    | All Companies                                                            |
| Subject    | All Subjects                                                             |
| Industry   | Financial Services                                                       |
| Region     | All Regions                                                              |
| Language   | English                                                                  |
| Results    | Found 11,200 (english only publications  = 9,767)                        |
| Timestamp  | 11 April 2019 22:12                                                      |
| Duplicates | Similar                                                                  |
| Status     | COMPLETED                                                                |

#### Query 2

| Attribute  | Value                                                                    |
| :--------- | :----------------------------------------------------------------------- |
| Text       | ("artificial intelligence" or "deep learning" or                         |
|            | "machine learning" or "big data" or "natural language processing"        |
|            | or "analytics") and (rst=sfft or rst=sfwsj or rst=sfeco) and (in=ifinal) |
| Date       | 01/01/2000 to 31/03/2019                                                 |
| Source     | All Sources                                                              |
| Author     | All Authors                                                              |
| Company    | All Companies                                                            |
| Subject    | All Subjects                                                             |
| Industry   | All Industries                                                           |
| Region     | All Regions                                                              |
| Language   | English                                                                  |
| Results    | Found 11,200 (english only publications  = 9,767)                        |
| Timestamp  | 11 April 2019 22:12                                                      |
| Duplicates | Identical                                                                |
| Status     | NOT TO CARRY OUT                                                         |
|            |                                                                          |

#### Query 3

| Attribute                         | Value                                                                                                                              |
|:-------------------------------- -|:-----------------------------------------------------------------------------------------------------------------------------------|
| Text                              | ("artificial intelligence" or "deep learning" or "machine learning" or "big data" or "natural language processing" or "analytics") |
| Date                              | 01/04/2019 to 31/12/2019                                                                                                           |
| Source                            | Financial Times (Available through Third Party Subscription Services) - All sources Or The Wall Street Journal - All sources       |
| Author                            | All Authors                                                                                                                        |
| Company                           | All Companies                                                                                                                      |
| Subject                           | All Subjects                                                                                                                       |
| Industry                          | Financial Services                                                                                                                 |
| Region                            | All Regions                                                                                                                        |
| Language                          | English                                                                                                                            |
| News Filters	Industry:           | Financial Services                                                                                                                 |
| Results Found                     | 2,056                                                                                                                              |
| Timestamp                       	| 20 September 2020 10:06                                                                                                            |

__Notes__: Factiva has stopped to index FT items ― thus, it is not possible
to retrieve data on FT items from Factiva; a different source, such as Nexis,
has to be used.
