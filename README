Copyright Russell Ferriday 2010 
russf@topia.com 
First release May 2010

This file is part of ATTUsageAnalysis.

ATTUsageAnalysis is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ATTUsageAnalysis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ATTUsageAnalysis.  If not, see <http://www.gnu.org/licenses/>.


Purpose
-------

This program allows quick analysis of the call and text records on your
ATT wireless account. It can help identify frequent conversations by
voice or text, and can determine who initiates those conversations.


Usage
-----

Log in to your ATT Wireless account at http://wireless.att.com/ .
You should be placed on the Account Overview page.

In the Bill and Payments Box, click View Bill Summary

Under the Wireless Statement heading click the USAGE DETAILS tab

Click Download Usage Details 

Select the period of interest in the drop-down

Select CSV and click Submit

You will receive a csv file that covers your whole account, including
all the users in your group. 

You can repeat this for a number of separate periods. On the Mac, these 
all download with the same file name (your account number), but with an 
additional (1), (2), etc appended. So you may need or wish to rename the files
with the starting date of the period. I'd recommend the format 

  20100401.csv
  
for example.

Put this file/ these files in the same directory as this program.  

Do   

  python run.py 2010*.csv 
  
to create a report for all the files starting with 2010

If you take a few minutes to add well known phone numbers to a file
in the format shown in testdir.dir, these will be added to the report
to make interpretation easier.  There is no fuzzy matching; you need
to make the number look just like those in the report.

Interpretation
--------------

Most of the output is self-explanatory. The purpose is to summarize traffic
to each 'party', meaning each phone number.  

If you want to know which kids your child texts most, the result is in 
the Texts/To column alongside the number. 

If you want to know if there are conversations between your child and another
(more than just a single message), Compare the values in the Texts column
with those in the Text Sessions column. The ratio of the values here is 
the average number of messages in an exchange of file minutes or less. 

If the In number is higher, then the OTHER party has initiated more of those 
exchanges. If the Out is higher, then your child has initiated. 

This is useful information, if you are concerned about predation, or bullying.


Thanks for using this program. I appreciate comments by email. 
Russ Ferriday
russf@topia.com


