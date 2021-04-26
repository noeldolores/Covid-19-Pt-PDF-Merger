A Python script that checks for updates to the Pfizer Emergency Use Authorization. If detected, the script will
download the new version, combine the PDF file with the CDC V-Safe PDF file, and email it to appropriate parties.<br/><br/>

Problem:<br/>
<ol>
<li>The source files for the Covid Vaccine patient handout are updated randomly and frequently.</li>
<li>Printing and assembling the handouts is time and paper inefficient.</li>
</ol>

Solution:<br/>
<ol>
<li>Automate the process of checking the date of the current Pfizer EUA using a web-scraping script.</li>
<li>Email a single PDF that contains both the new Pfizer EUA and V-Safe files when new versions are available.</li>
</ol><br/>

Requirements:<br/>
<ol>
<li>PyPDF2: https://pypi.org/project/PyPDF2/</li>
<li>GMAIL API: https://developers.google.com/gmail/api/quickstart/python</li>
<li>'email.txt' file that contains line-seperated email addresses to notify.</li>
</ol>