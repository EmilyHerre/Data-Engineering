Analyzing Buildings S.A.'s requirements, the goal is to implement a system for daily monitoring of 
employees on each project. Below is a solution to carry out this control:

* Load the files and generate a data frame with the necessary data.
* Remove duplicate elements, if any.
* Group the elements by project to generate the corresponding tables.
* Evaluate if the table already exists in the database.
  * If it doesn't exist, create it and add the data.
  * If it exists, compare the table's elements with the new data to prevent the insertion of duplicate elements.

# Each project's table includes the following fields:

- Date
- Employee ID
- Employee's Name
- Employee's Surname
- Hours worked
- Specialty

This approach allows for greater control over employees and their work on each project. Including the specialty
facilitates salary calculation based on hours worked, as well as obtaining relevant information for the company,
such as the average hours worked on each project or the distribution of specialties by project over 
different periods (weekly, monthly, quarterly, etc.).
