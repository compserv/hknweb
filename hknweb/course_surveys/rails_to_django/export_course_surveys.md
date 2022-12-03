# Rails course surveys db export notes

Sandbox production database command

`bundle exec rails console -e production --sandbox`

Export output file to local machine
`scp hkn@apphost.ocf.berkeley.edu:/home/h/hk/hkn/hkn-rails/prod/current/course_surveys_data.json .`

Code links
- [course surveys upload](https://github.com/compserv/hkn-rails/blob/master/app/helpers/admin/csec_admin_helper.rb)
- [Instructor creation](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L89)
- [Dept find](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L102)
- [Question find](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L120)
- [Course creation](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L138)
- [Klass (Course-Semester relation) creation](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L142)
- [Instructorship (Instructor-Course-Semester relation) creation](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L150)
- [SurveyAnswer (Rating) creation](https://github.com/compserv/hkn-rails/blob/ca7707185d1e796ead12bfa7923ea8b39c3c3280/app/helpers/admin/csec_admin_helper.rb#L158)

Notes
- There isn't a semester model, just a string.
