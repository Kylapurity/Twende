import os
from safari_learning.models import SafariCourse, images_path, Interest

"""
utilty error class
"""
class SafariCourseExistError(Exception):
    def __init__(self, message):
        super().__init__(message)

def run():
    # create a dictionary with a key whose value is an array
    # to store the profession for that course links
    while True:
        profession_list, course_tags_list  = [], []
        profession_json, course_tags_json = {}, {}

        file_name = input(f"\nAdd a file name from path {images_path()}: ")
        if not os.path.exists(os.path.join(images_path(), file_name)):
            print(f"file {file_name} doesn't exist in the directory {images_path()}")
            print(f"Hint: first upload the file to this directory {images_path()}")
            outcome = input("Do you want to quit application, yes or no: ")
            if outcome.lower() == "yes":
                break
            else:
                continue
        while True:
            profession = input("\nAdd a profession suitable for this course: ")
            profession_list.append(profession)
            outcome = input("Do you still want to add more profession for that course, yes or no: ")
            if outcome.lower() == "yes":
                continue
            else:
                break
        while True:
            course_tag = input("\nAdd a course tag suitable for this course")
            course_tags_list.append(course_tag.lower())
            # then check if the Interest table doesn't have this course tag inorder to prevent
            # unecessary duplication
            check_course_tag = Interest.objects.filter(
                interest__icontains=course_tag.lower(),
            )
            if check_course_tag.exists():
                pass
            else:
                # add course tag if it doesn't exist
                Interest.objects.create(
                    interest=course_tag.lower(),
                )
            outcome = input("Do you still want to add more tags for this course, yes or no: ")
            if outcome.lower() == "yes":
                continue
            else:
                break
        try:
            course_name = input("\nPlease give me a course name: ")
            course_link = input("Please give me a valid course url link: ")
            # now create the safari course using course_link, file_name, and profession json
            profession_json["profession"] = profession_list
            course_tags_json["course_tags"] = course_tags_list
            safari_course_exist = SafariCourse.objects.filter(
                course_link=course_link,
            ).exists()
            if safari_course_exist:
                SafariCourseExistError(f"This course with course link {course_link} with image {file_name} already exist.")
        except SafariCourseExistError as error:
            print(error)
            outcome = input("Do you still want to create a new course, yes or no: ")
            if outcome.lower() == "yes":
                continue
            else:
                break            
        except Exception as error:
            print(error)
            outcome = input("Do you still want to create a new course, yes or no: ")
            if outcome.lower() == "yes":
                continue
            else:
                break     
        else:
            safari_course = SafariCourse.objects.create(
                course_link=course_link,
                file_name=file_name,
                profession_json=profession_json,
                course_name=course_name,
                course_tags=course_tags_json,
            )
            print(safari_course)
        outcome = input("Do you still want to create a new course, yes or no: ")
        if outcome.lower() == "yes":
            continue
        else:
            break
    print("\nQuitting scripts...")



        
    