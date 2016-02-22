import unittest
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join("..", os.path.dirname(__file__))))
import tmy

CONFIG_DIR = os.path.abspath(os.path.join("..", os.path.dirname(__file__)))

class TmyTests(unittest.TestCase):

    def test_has_data_works(self):
        args = {"config": os.path.join(CONFIG_DIR, "tmy-config.json"),
              "verbose": True,
              "plot_cdf": False,
              "bomfile": "melbourne.csv"}
        tmy.main(args)

    def test_missing_data_fails(self):
        args = {"config": os.path.join(CONFIG_DIR, "tmy-config.json"),
              "verbose": True,
              "plot_cdf": False,
              "bomfile": "cape_grim.csv"}
        with self.assertRaises(SystemExit):
            tmy.main(args)

    def test_remove_rows_with_nulls(self):
        test_csv_filepath = "test_csv.csv"
        expected_csv_filepath = "expected_csv.csv"
        # If we failed to clean up after the last test for some reason, do so now.
        if os.path.exists(test_csv_filepath):
           os.remove(test_csv_filepath)
        if os.path.exists(expected_csv_filepath):
           os.remove(expected_csv_filepath)

        with open(test_csv_filepath, 'w') as f:
           f.write("time,col1,col2,col3\n"\
                   "1998-01-01T10:00:00,,1,2\n"\
                   "1998-01-02T10:00:00,3,0,0\n"\
                   "1998-02-01T10:00:00,3,4,5\n"\
                   "1998-02-01T10:00:00,6,7,8\n"\
                   "1998-02-01T10:00:00,9,10,\n"\
                   "1998-03-01T10:00:00,11,12,13\n"\
                   "1998-04-01T10:00:00,14,15,14\n"\
                   "1998-04-01T10:00:00,16,17,18\n"\
                   "1998-04-01T10:00:00,19,20,21\n"\
                   "1999-05-01T10:00:00,19,20,21\n"\
                   "1999-05-01T10:00:00,19,20,21\n"\
                   "1998-05-01T10:00:00,,,\n")
        with open(expected_csv_filepath, 'w') as f:
           f.write("time,col1,col2,col3\n"\
                   "1998-03-01T10:00:00,11,12,13\n"\
                   "1998-04-01T10:00:00,14,15,14\n"\
                   "1998-04-01T10:00:00,16,17,18\n"\
                   "1998-04-01T10:00:00,19,20,21\n"\
                   "1999-05-01T10:00:00,19,20,21\n"\
                   "1999-05-01T10:00:00,19,20,21\n")
        d = pd.read_csv(test_csv_filepath, parse_dates=[0])
        d.set_index('time', inplace=True)
        col_names = ["col1", "col2", "col3"]

        d = tmy.removeMonthsWithNulls(col_names, d)
        print d
        expected_d = pd.read_csv(expected_csv_filepath, parse_dates=[0])
        expected_d.set_index('time', inplace=True)

        self.assertEqual(repr(d), repr(expected_d))

        # Clean up
        if os.path.exists(test_csv_filepath):
           os.remove(test_csv_filepath)
        if os.path.exists(expected_csv_filepath):
           os.remove(expected_csv_filepath)



if __name__ == '__main__':
    unittest.main()
