# session_staff
reporting tool for PyCon session staff

This started as the gist, bit.ly/PyConSessionStaff


In the works:
- [ ] merge flow, and item extraction from the gist fork (branch here);
  - [ ] rewrite to BeautifulSoup (not faster, but more forgiving);
  - [ ] parameterize extraction items; add into Session class in master;
- [ ] add vcrpy - to avoid hitting the server repeatedly when generating reports;  for testing in "non-pycon times";
  - [ ] for starters, have plain summary report update, others use vcr;
  - [ ] add flag to force update of vcr;
  - [ ] include pycon-year in name (for testing/training dev);
- [ ] merge master -> branch;
  - [ ] add formatter abc;  and formatters for existing output(s);
  - [ ] maybe add options to specify what to output;
  - [ ] add some basic output formats (text, json, yaml, csv)
  - [ ] add iCal as a formatter option (for volunteers);
  - [ ] add ability to filter by volunteer name;
  - [ ] add "None" as user to Session class, to output needs;
- [ ] add some training so code doesn't need to change w/ PyCon years / template changes;
