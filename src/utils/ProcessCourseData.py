import os
import pandas as pd


class CourseList():
  def __init__(self, course_csv_location: str):
    if os.path.exists(course_csv_location):
      temp = pd.read_csv(course_csv_location)
      if all(column in temp.columns for column in ["name", "credits"]):
        self.df = temp[["name", "credits"]].copy()
        self.df.set_index("name", inplace=True)
        if "tags" in temp.columns:
          self.df = pd.merge(self.df, temp[["name", "tags"]], on="name")
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

      columns = ['name', 'credits', 'tags']
      data_types = {'name': str, 'credits': int, 'tags': TagList}
      self.df = pd.DataFrame(columns=columns)
      self.df.to_csv(course_csv_location, index=False)
    print(self.df.head())


  def search_by_tag(tag: str):
    pass

class TagList():
  def __init__():
    pass

  def __len__(self):
    return 1