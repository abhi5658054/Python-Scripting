"""
Project for Week 3 of "Python Data Analysis".
Read and write CSV files using a dictionary of dictionaries.
Be sure to read the project description page for further information
about the expected behavior of the program.
"""
import csv
def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Ouput:
      A list of strings corresponding to the field names in
      the given CSV file.
    """
    table = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile,
                               delimiter = separator,
                               quotechar = quote)
        for row in csvreader:
            table.append(row)
    return table[0]

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile,
                               delimiter = separator,
                               quotechar = quote)
        for row in csvreader:
            table.append(row)
    field_name = read_csv_fieldnames(filename, separator, quote)
    table2 = table[1:]
    new_table = []
    index = 0
    for index in range(len(table2)):
        the_dic = {}
        index2 = 0
        new_table.append(the_dic)
        while index2 < len(table2[index]):
            the_dic[field_name[index2]] = table2[index][index2]
            index2 += 1
    return new_table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table ={}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   delimiter=separator,
                                   quotechar=quote)
        for row in csvreader:
            table[row[keyfield]] = row
    return table

def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames.  The CSV file should use the given separator and
      quote characters.  All non-numeric fields will be quoted.
    """

    with open(filename , 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter = separator,
                                quotechar = quote,
                                quoting = csv.QUOTE_NONNUMERIC)
        spamwriter.writerow(fieldnames)
        index = 0
        while index < len(table):
            key = table[index].values()
            value = table[index].values()
            if key == fieldnames:
                spamwriter.writerow(value)
            else:
                the_list = []
                for index2 in range(len(fieldnames)):
                    the_list.append(table[index][fieldnames[index2]])
                spamwriter.writerow(the_list)
            index += 1