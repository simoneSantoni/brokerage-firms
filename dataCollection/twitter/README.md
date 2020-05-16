Twitter data collection - README
================================


```{bash}
FROM: Toni Narciss
DATE: 11/27/2019

Hi Gianvito and Simone,

I have uploaded the indices (1,2 and 3) to a google drive folder, they can be
found in the “Pout”
folder(https://drive.google.com/open?id=1QrFz14to6JGye1UDCrR66g3U9NwMUWLG).

Some notes about the indices:

For the sentiment analysis and hot locations index the 2 figures cover AI and DL
respectively and range from 2013-01 till 2019-06. Updating the figures can be
done using code also available in the drive on a monthly basis.  For the Top
companies index I only was able to  complete 2018 and 2019 and that is because
of 2 reasons: collecting google data for the logistic model took a lot of time
due to google blocking excessive activity. (however we now have all the data
back till 2013) even after the logistic model the data still needed manual
cleaning and this took the bulk of the time (cleaning the lists we have to reach
2013 could take weeks) the lists uploaded are mostly top 100 lists, however for
DL tables in 2018 due to the large amount of noise in that year, the lists are
top 60 sometimes. We can fix this in 2 ways: either we trim the lists and use
the top 50(this takes no time at all), or we expand google scrapes for that year
to reach top 100 (this would take almost a week to scrape and manually clean the
new data).
 
The google folder attached above also contains the project codes, twitter data
collected and other data used.

All the best,

Toni
```
