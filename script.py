import os

from scraper import Scraper, MyJSON
from content import Content
from converter import Converter


course_name = 'FEWDR'

if __name__ == '__main__':
    if not os.path.exists(course_name):
        os.makedirs(course_name)

    with open(os.path.join(course_name, 'README.md'), 'a') as tmp:
        tmp.write('''
# Frontend Web Development 🎉🎈🎂🍾🎊🍻💃

## Table of Contents
Here are all the lectures for this course. This section will be updated with notes as we make our way through the curriculum.

        ''')

    for i in range(1, 19):
        print('------------ Starting Lecture {} task ------------'.format(i))
        url = Scraper.assemble(('fewd627_{}'.format(i)))
        res = Scraper.run(url)
        c = Content(res)
        cvt = Converter(c.content)
        k = MyJSON.post(cvt.exportable)
        curr_path = "{}/Lecture_{}".format(course_name, i)

        if not os.path.exists(curr_path):
            os.makedirs(curr_path)

        with open(os.path.join(course_name, 'README.md'), 'a') as tmp:
            tmp.write('''
### [Lecture {num}: {title}](Lecture_{num}) | [Slides]({uri})
        	'''.format(num=i, title=c.title, uri=k))

        with open(os.path.join(curr_path, 'README.md'), 'w') as tmp:
            tmp.write(cvt.exportable)

        print('------------ DONE with Lecture {} task ------------'.format(i))
