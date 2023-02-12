import unittest
from methods import Token, Restricted
import werkzeug.exceptions
from methods import JWTDecodeError

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.convert = Token()
        self.validate = Restricted()

    def test_generate_token(self):
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI', self.convert.generate_token('admin', 'secret'))
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiZWRpdG9yIn0.4Km_GrMrTIX2xFMjQcrGP9VDhC9jFsnFCjxvBO8Wgio', self.convert.generate_token('noadmin', 'noPow3r'))
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidmlld2VyIn0.l7pxJXYHlJdtI9RME2UesMzuVjqf-RtzQeLTHomo_Ic', self.convert.generate_token('bob', 'thisIsNotAPasswordBob'))


    def test_user_does_not_exist(self):
            with self.assertRaises(werkzeug.exceptions.Forbidden):
                self.convert.generate_token('thisUserDoesNotExist', 'secret')


    def test_incorrect_password(self):
        with self.assertRaises(werkzeug.exceptions.Forbidden):
            self.convert.generate_token('admin', 'thisPasswordIsIncorrect')


    def test_access_data(self):
        self.assertEqual('You are under protected data', self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI'))
        self.assertEqual('You are under protected data', self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiZWRpdG9yIn0.4Km_GrMrTIX2xFMjQcrGP9VDhC9jFsnFCjxvBO8Wgio'))
        self.assertEqual('You are under protected data', self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidmlld2VyIn0.l7pxJXYHlJdtI9RME2UesMzuVjqf-RtzQeLTHomo_Ic'))


    def test_token_is_invalid(self):
        with self.assertRaises(JWTDecodeError):
            self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.BADTOKENpQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI')

        with self.assertRaises(JWTDecodeError):
            self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.BADTOKENIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI')

        with self.assertRaises(JWTDecodeError):
            self.validate.access_data('BADTOKENOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI')


if __name__ == '__main__':
    unittest.main()
