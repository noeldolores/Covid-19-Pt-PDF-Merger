As Covid-19 vaccinations begin, there are a two handouts that patients must be given [Pfizer EUA, V-Safe info sheet]. 
The handouts are only 8 pages in total, but printing and organizing packets for thousands of patients is not ideal. 
After running through this process with several stacks of these handouts myself, I realized that it would be easier 
if the two PDF files were merged into one, allowing for a more streamlined and option-versatile printing process, 
that also reduces paper waste. 

Issue: The source file for these packets must be kept up-to-date as the 
Pfizer EUA handout for patients has been receiving regular updates. 

Solution: An automated web-scraper that emails out a new combined PDF file 
whenever an update is detected.

This script does several things:
1) Scrapes a single FDA website to check for the current version date of the Pfizer Emergency Use Authorization letter
2) Compares this date with the date we have stored in a text file, representing the previously known update
  (if the version date is new)
3) Updates the version date text file
4) Downloads the new PDF file
5) Creates a blank PDF file, where the new file and V-Safe info sheet are merged
<<<<<<< HEAD
6) Emails the updated version to listed parties
=======
6) Emails the updated version to listed parties
>>>>>>> 825f86cd539bc4ee9589db688e9b41e7cbe555b1
