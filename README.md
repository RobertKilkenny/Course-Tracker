# Course Tracker

Created by Robert Kilkenny using Python 3.10.11

## Background

For years, I had used an Excel spreadsheet to track my classes and current plans for each semester. It was originally a document that the Wertheim College of Engineering at the University of Florida gave me, but I found it too simple to be useful. As such, I made many revisions to it over the years, to the point that barely any part of the original document remains. While it was an excellent opportunity to learn the advanced features of Excel (like XLOOKUP), iterating on the document has become more and more tedious. I had planned on making a program for this several different times but up until now had just dealt with using the somewhat jury-rigged spreadsheet due to the amount of time I had spent working on it.

## Methodology

I wanted to use Python as my frontend for this application because I find PySide2 (or rather QT in general) as a easy library to quickly iterate on to make a clean looking application. Also, I had assignments in the past where I used Python and PySide2 as my frontend while wrapping C++ code to help with the heavier work. Since I wanted to implement a CSV file structure to save the different class data and the user's data, I thought it would be interesting to make some C++ code to handle reading the data (to hopefully speed up the application during runtime).

## Features List

### Completed

### In Testing

### Planned

- Reading a CSV file to add a batch of classes to the master list
- Manual single / batch additions to the master list in the app
- Creating and tracking different tags for classes (ex. "Critical Tracking", "For Minor", etc.)
- Planning feature for future semesters
  - Checks for time-sensitive classes (ex. if Calculus 1 has to be done before the 3rd semester, it will force the user to have it within the first two semesters)
  - Reads a JSON file of rules for a major completion
    - When planning is done, will reference the JSON to see if any rules are not completed
- Overview page for degree completion including:
  - Current GPA (Total, For Major, Towards Honors [optional])
  - Current semester
  - Overview of Critical Tracking classes with grades and credits
- Custom pages for each semester where classes have been completed
- List of classes that have been failed and **must** be retaken
- "Check if on track" button
- Ability to add on other majors, minors, and certificates both with JSON files or by user input in app

# Notes

As the license says, feel free to use this repository to create your own Course Tracker (once it is working of course!). I would perfer if you credited me if you do alter it, especially if it is for a personal project!! Feel free to message me here if you have questions on how this works.

To get started, just make a virtual environment (using `python -m venv env`)and then install all the packages using 