import unittest
import connection

class validateMethods(unittest.TestCase):
    def testvalueCheck(self):
        none = "None"
        self.assertEqual(none, str(connection.valueCheck(1)))
        self.assertEqual(none, str(connection.valueCheck(500)))
        
    def testconnectionTest(self):
        self.assertEqual("working", connection.connectionTest())
    #    self.assertRaises(connection.connectionWithDatabaseFailure, connection.connectionTest(), 2)

if(__name__=='__main__'):
    unittest.main()