MADE BY Fré Leys
VERSION: 0.1

How to run this code
Copy Paste folder (fork)
open folder in visual studio code
open Terminal and run: 
1) python -m venv env  (this creates virtual environment)
2) .\env\Scripts\activate (activates virtual environment)
3) pip install -r requirements.txt (installs all the required packages)
(4) when adding requirements: pip freeze > requirements.txt (before sharing)



Key words

-------
'USES': keeps/removes everything within the pair of equaly named {USES_...}

Example: 
  {USES_GROEF_X6}L X{GROEF_X6} F500
  L Z-0.95 F1000
  L Y+17.1 F200
  L Z-1.05 F50
  L Y+20 F200 {USES_GROEF_X6}

  if USES_GROEF_X6 = YES this gives:
  L X{GROEF_X6} F500
  L Z-0.95 F1000
  L Y+17.1 F200
  L Z-1.05 F50
  L Y+20 F200

  if USES_GROEF_X6 = NO this removes everything

-------
  'SELECTS' only used for labels: the python script searches for the filename defined by the parameter and inserts it at the place where 'SELECTS' is used

-------
  'FOR': takes list [a,b,c]


-------



  TODOS
  * FOR Loop voor Groeven
