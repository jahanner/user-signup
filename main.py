
import webapp2
import re
import cgi


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):

    def make_function(self, username='', user_error='', pass_error='', verify_error='', email='', email_error=''):
        signup = '''<!DOCTYPE>
            <html>
            <head>
            </head>
            <body>
            <h1>Signup</h1>
                <form method="post">
                    <table>
                        <tr>
                            <td><label for="username">Username</label></td>
                            <td>
                                <input name="username" type="text" value={username}>
                                {error1}
                            </td>
                        </tr>
                        <tr>
                            <td><label for="password">Password</label></td>
                            <td>
                                <input name="password" type="password">
                                {error2}
                            </td>
                        </tr>
                        <tr>
                            <td><label for="verify">Verify Password</label></td>
                            <td>
                                <input name="verify" type="password">
                                {error3}
                            </td>
                        </tr>
                        <tr>
                            <td><label for="email">Email (optional)</label></td>
                            <td>
                                <input name="email" type="email" value={email}>
                                {error4}
                            </td>
                        </tr>
                    </table>
                    <input type="submit">
                </form>
            </body>
        </html>'''
        return signup.format(username=username, email=email, error1=user_error, error2=pass_error, error3=verify_error, error4=email_error)

    def get(self):
        self.response.out.write(self.make_function())

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username):
            user_error = "<span>That's not a valid username.</span>"
            have_error = True
        else:
            user_error = ''

        if not valid_password(password):
            pass_error = "<span>That wasn't a valid password.</span>"
            have_error = True
        else:
            pass_error = ''

        if password != verify_password:
            verify_error = "<span>Your passwords didn't match.</span>"
            have_error = True
        else:
            verify_error = ''

        if email == '':
            email_error = ''
        elif not valid_email(email):
            email_error = "<span>That's not a valid email.</span>"
        else:
            email_error = ''

        if have_error:
            self.response.out.write(self.make_function(username, user_error, pass_error, verify_error, email, email_error))
        else:
            self.redirect('/welcome?username=' + username)



class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.reponse.out.write("Welcome, " + username + "!")
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
