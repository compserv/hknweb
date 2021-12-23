### Editing course surveys transparency information
1. Head to the [admin for markdown pages](https://dev-hkn.eecs.berkeley.edu/admin/markdown_pages/markdownpage/)
2. Copy the appropriate path name from the [constants.py](https://github.com/compserv/hknweb/blob/1328bc2be34280cde6ff7b7b2756e144cc835aa7/hknweb/course_surveys/constants.py#L7) file
3. The name and description are "Course surveys {{path_name}}"
4. Go to the appropriate Google doc and use the "Docs to Markdown" Google Docs add-on to export the document to markdown
5. Clean up the resulting markdown and copy it into the "Body" section of the admin panel

For example:
1. ...
2. `course_surveys_authentication`
3. `Course surveys Authentication`
4. ...
5. ...
