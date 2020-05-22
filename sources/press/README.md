Factiva data collection - README
================================

<!-- vim-toc-markdown -->

* [Overview of scripts](#overview-of-scripts)
* [Article search](#article-search)
* [Outcome of the query](#outcome-of-the-query)
  * [Query 0](#query-0)
  * [Query 1](#query-1)
  * [Query 2](#query-2)

<!-- vim-toc-markdown -->

Overview of scripts
===================

| Script   | Task                               | Status | Warnings |
|:---------|:-----------------------------------|:-------|:---------|
| _0.py    | parse .rtf downloaded from Factiva | run    | none     |
| _1.py    | assemble corpus of data            | run    | none     |
| _2.ipynb | topic modelling                    | run    | none     |
| _3.py    | semantic network analysis          | run    | none     |

Data collection procedures
==========================

Article search
--------------

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

Outcome of the query
--------------------

### Query 0

| Attribute | Value                                                    |
|:----------|:---------------------------------------------------------|
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

### Query 1

| Attribute  | Value                                                                    |
|:-----------|:-------------------------------------------------------------------------|
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
| Duplicates | Similar                                                                  |
| Status     | COMPLETED                                                                |

### Query 2

| Attribute  | Value                                                                    |
|:-----------|:-------------------------------------------------------------------------|
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
