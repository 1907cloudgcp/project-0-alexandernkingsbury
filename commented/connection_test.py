import unittest
import connection

class validateMethods(unittest.TestCase):
    def testvalueCheck(self):
        none = "None"
        #these are the min and max ranges of the database
        self.assertEqual(none, str(connection.valueCheck(0)))
        self.assertEqual(none, str(connection.valueCheck(999.99)))
        
    def testconnectionTest(self):
        self.assertEqual("working", connection.connectionTest())
    #    self.assertRaises(connection.connectionWithDatabaseFailure, connection.connectionTest(), 2)

if(__name__=='__main__'):
    unittest.main()