import os
import pandas as pd


class CourseList():
  def __init__(self, course_csv_location: str):
    if os.path.exists(course_csv_location):
      temp = pd.read_csv(course_csv_location)
      if all(column in temp.columns for column in ["Course Code", "Credits"]):
        self.df = temp[["Course Code", "Credits"]].copy()

        if "Course Name" in temp.columns:
          self.df = pd.merge(self.df, temp[["Course Code", "Credits", "Course Name"]], on=["Course Code", "Credits"])
        else:
          self.df['Course Name'] = " "

        if "tags" in temp.columns:
          self.df = pd.merge(self.df, temp[["Course Code", "Credits", "tags"]], on=["Course Code", "Credits"])
        else:
          self.df['tags'] = " "
      else:
        print("invalid csv used")


    else:
      print("CSV did not exist")
      path_pieces = course_csv_location.split("/")
      print(path_pieces)
      path = path_pieces[0]
      for piece in path_pieces[1:-1]:
        path += "/" + piece
        if not os.path.exists(path):
          print("path:", path, "did not exist")
          os.makedirs(path)

      self.df = pd.DataFrame({'Course Code':["TMPXXXX"], 'Course Name':["Example Class"], 'Credits':[-1], 'tags': ["example, do not use"]})
      self.df.to_csv(course_csv_location)

    try:
      self.df.set_index(['Course Code', 'Credits'], inplace=True)
    except Exception as exception:
      print("Error with creating Pandas Dataframe.\nSee:", exception)


  def search_by_tag(tag: str):
    pass