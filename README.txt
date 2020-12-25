My first extracurricular project that I have put together in order to save time and paper.

As Covid-19 vaccinations begin, there are a couple handouts that patients must be given. The handouts are only 8 pages in
total, but printing and organizing packets for thousands of patients is not ideal. After printing and organizing several 
stacks of these handouts myself, I realized that it would be easier if the two PDF files were merged into one, allowing for 
a more streamlined and option-versatile printing process, that also reduces paper waste.

This script does several things:
1) Scrapes a single FDA website to check for the current version date of the Pfizer Emergency Use Authorization letter
2) Compares this date with the date we have stored in a text file, representing the previously known update
  (if the version date is different/new)
3) Updates the version date text file
4) Downloads the new PDF file
5) Creates a blank PDF file, where we copy the new file with the CDCs V-Safe patient handout
6) Emails the updated version to my email
