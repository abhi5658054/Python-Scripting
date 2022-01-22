"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.
Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv

##
## Provided code from Week 3 Project
##

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
    field_name = table[0]
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


##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500

def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0

def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0

def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """
    the_filtter_list = []
    for item in statistics:
        if int(item[yearid]) == year:
            #print(int(item[yearid]) >= year)
            #print(int(item[yearid]))
            the_filtter_list.append(item)

    return the_filtter_list
    #newtups = list(filter(lambda pair: pair[1] < pair[0], tups))
    #print("filtered:", newtups)




def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    the_list = []
    for item in statistics:
        tup = ()
        player_id = item[info['playerid']]
        #print(player_id)
        result = formula(info,item)
        #print(result)
        tup = (player_id,result)
        the_list.append(tup)

    the_list.sort(key = lambda pair: pair[1],reverse=True)
    #print(the_list)
    the_filtter_list = the_list[0:numplayers]


    return the_filtter_list


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    table = read_csv_as_list_dict(info['masterfile'], info['separator'], info['quote'])
    the_name_list = []
    for item in top_ids_and_stats:
        for item2 in table:
            value = item2.get(info['playerid'])
            if value != 'None':
                if item[0] == value:
                    firstname = item2[info['firstname']]
                    lastname = item2[info['lastname']]
                    score = item[1]
                    score_s_f = "{0:.3f}".format(score)
                    new_item = score_s_f + " " + "---" + " " + firstname + " " + lastname
                    the_name_list.append(new_item)

    return the_name_list

def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """

    the_list = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])
    the_filtter_list = filter_by_year( the_list , year, info['yearid'])
    top_player_list = top_player_ids(info, the_filtter_list, formula, numplayers)
    the_name_list = lookup_player_names(info, top_player_list)


    return the_name_list




##
## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    the_dic = {}

    for item in statistics:
        #print(item)
        player_id = item[playerid]
        #print("the playerid",player_id)
        value = the_dic.get(player_id,-1)
        #print("the value",value)
        the_value = {}
        if value == -1:
            for index in range(len(fields)):
                the_value[fields[index]] = int(item[fields[index]])
                #print("the dic with -1 " ,fields[index],the_value[fields[index]])
            the_value[playerid] = player_id
            the_dic[player_id] = the_value
            #print(the_dic)
        else:
            for index in range(len(fields)):
                #print(fields[index])
                #print(int(item[fields[index]]))
                #print(int(value[fields[index]]))
                the_value[fields[index]] = int(item[fields[index]]) + int(value[fields[index]])
                #print("the dic with " ,fields[index],the_value[fields[index]])
            the_value[playerid] = player_id
            the_dic[player_id] = the_value
            #print(the_dic)
    return the_dic



def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    the_list = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])
    the_new_dic = aggregate_by_player_id(the_list, info['playerid'],info['battingfields'])
    the_new_list = the_new_dic.values()
    top_player_list = top_player_ids(info, the_new_list, formula, numplayers)
    the_name_list = lookup_player_names(info, top_player_list)

    return the_name_list

##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")