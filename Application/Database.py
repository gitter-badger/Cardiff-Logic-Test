#!/usr/bin/env python
# encoding: utf-8
# Created by Daniel Koehler - 15/03/2014

import os.path
import re
import sys
import cPickle as pickle

"""
"" @name: Database (Class)
"" @author: Daniel Koehler
"" @description: Class to wrap cPickle in a slightly relational manner
"""

class Database():

    """
    "" @name: Group Popover (Message Box)
    "" @author: Daniel Koehler  
    "" @description: Method to display a popup allowing a group to be added
    "" @prams: none
    "" @return: void
    """

    def __init__(self, relative_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "Data")), pragma_name = "pragma", table_prefix = ""):

        #Load data using tread/queue from flat file
        self.table_prefix = table_prefix
        # Tables list - in the form 'table_name' : {'1':{field_one: value, field_two: value}, '2':{field_one: value, field_two: value}}
        self.tables = {} 
        self.pragma_name = pragma_name
        self.pragma = dict()
        self.pragma['tables'] = {}

        # Set relative path to data files
        self.relative_path = relative_path

        # Load our pramga 
        self.load_pragma()
        # Load tables based on pragma
        self.load_tables()

    """
    "" @name: Select 
    "" @author: Daniel Koehler  
    "" @description: Method to select rows froma table, where clause is comma delimted, each condition in the form (`field_name` operator 'value') [AND] [OR]
    "" @prams: (String) Table Name, String (Where), (Integer) Limit
    "" @return: (List) Returned rows
    """

    def select(self, table_name, where="", limit=0):

        # Create empty matches list
        matches = []

        # If the table doesn't exist we can't query it.
        if not self.table_exists(table_name):
            return False

        # If we havn't got a limit it might as well be the upper bound of the table
        if not limit:
            limit = self.get_table_last_insert_id(table_name)

        # Clear counter
        count = 0
        # The number of rows currently in the table
        table_rows = self.get_table_row_count(table_name)
        # The tables ID field
        id_field = table_name + "_id"
        
        # If we're selecting all rows - we can do this a little faster.
        if where == "":
            for row_id in self.tables[table_name]:
                if len(matches) >= limit or count >= table_rows:
                    break

                matches.append(self.tables[table_name][row_id])
                count += 1

            return matches

        conditions = self.deserialise_where_clause(table_name, where)

        if conditions == False:
            return False
        for row_id in self.tables[table_name]:
            if len(matches) >= limit or count >= table_rows:
                break
            matches_query = False

            for condition in conditions:

                if eval("self.tables[table_name][row_id][condition['field']] " + condition['operator'] + " condition['value']"):
                    if "and" not in condition:
                        matches_query = True
                        break
                    else:
                        for subcondition in condition['and']:
                            if not eval("self.tables[table_name][row_id][subcondition['field']] " + condition['operator'] + " subcondition['value']"):
                                matches_query = False
                                break
                            else:
                                matches_query = True
                else:
                    matches_query = False

            if matches_query:
                matches.append(self.tables[table_name][row_id])

            self.tables[table_name][row_id]

            count +=1

        return matches

    """
    "" @name: Update 
    "" @author: Daniel Koehler  
    "" @description: Method to update rows in table, where clause is comma delimted, each condition in the form (`field_name` operator 'value') [AND] [OR]
    "" @prams: (String) Table Name, (List) Data to Update, String (Where), (Integer) Limit
    "" @return: (List) Returned rows
    """

    def update(self, table_name, data, where="", limit=0):

        if not self.table_exists(table_name):
            return False

        if not self.table_has_fields(table_name, data.keys()):
            return False

        if not len(data):
            self.error("No data to update where \"%s\" on table `%s`" % (where, table_name))

        if not limit:
            limit = self.get_table_last_insert_id(table_name)

        count = 0
        matches = 0

        table_rows = self.get_table_row_count(table_name)
        id_field = table_name + "_id"


        if where == "":
            for row_id in self.tables[table_name]:
                if len(matches) >= limit or count >= table_rows:
                    break

                self.tables[table_name][row_id][field] = data[field]
                matches += 1
                count += 1
            if matches:
                self.set_table_did_change_pragma(table_name)
            return matches

        conditions = self.deserialise_where_clause(table_name, where)

        if conditions == False:
            return False

        if table_name + "_id" in data:
            self.error("Can't UPDATE row id")

        for row_id in self.tables[table_name]:

            if matches >= limit or count >= table_rows:
                break

            matches_query = False

            for condition in conditions:
                if eval("self.tables[table_name][row_id][condition['field']] " + condition['operator'] + " condition['value']"):
                    if "and" not in condition:
                        matches_query = True
                        break
                    else:
                        for subcondition in condition['and']:
                            if not eval("self.tables[table_name][row_id][subcondition['field']] " + condition['operator'] + " subcondition['value']"):
                                matches_query = False
                                break
                            else:
                                matches_query = True
                else:
                    matches_query = False

            if matches_query:
                for field in data:
                    self.tables[table_name][row_id][field] = data[field]
                matches += 1

            if matches:
                self.set_table_did_change_pragma(table_name)

            self.tables[table_name][row_id]
            count +=1

        # Return affected rows
        return matches


    """
    "" @name: Delete 
    "" @author: Daniel Koehler  
    "" @description: Method to delete rows froma table, where clause is comma delimted, each condition in the form (`field_name` operator 'value') [AND] [OR]
    "" @prams: (String) Table Name, String (Where), (Integer) Limit
    "" @return: (List) Affected rows
    """

    def delete(self, table_name, where="", limit=0):

        if not self.table_exists(table_name):
            return False

        if not limit:
            limit = self.get_table_last_insert_id(table_name)

        count = 0
        matches = []
        
        table_rows = self.get_table_row_count(table_name)
        id_field = table_name + "_id"


        if where == "":
            for row_id in self.tables[table_name]:
                if len(matches) >= limit or count >= table_rows:
                    break

                matches.append(row_id)
                count += 1

            for match in matches:     
                del self.tables[table_name][match]
                self.decrement_table_row_count_pragma(table_name)

            return len(matches)

        conditions = self.deserialise_where_clause(table_name, where)

        if conditions == False:
            return False

        for row_id in self.tables[table_name]:

            if len(matches) >= limit or count >= table_rows:
                break

            matches_query = False

            for condition in conditions:
                if eval("self.tables[table_name][row_id][condition['field']] " + condition['operator'] + " condition['value']"):
                    if "and" not in condition:
                        matches_query = True
                        break
                    else:
                        for subcondition in condition['and']:
                            if not eval("self.tables[table_name][row_id][subcondition['field']] " + condition['operator'] + " subcondition['value']"):
                                matches_query = False
                                break
                            else:
                                matches_query = True
                else:
                    matches_query = False
            if matches_query:
                matches.append(row_id)
            count +=1
        
        if len(matches):
            self.set_table_did_change_pragma(table_name)
            for match in matches:     
                del self.tables[table_name][match]
                self.decrement_table_row_count_pragma(table_name)   
            return len(matches)
        # Return affected rows
        return False

    # Data = field, value pairs
    def insert(self, table_name, query_data={}):
        # Table exists?
        if not self.table_exists(table_name):
            return False

        # Table has fields?
        if not self.table_has_fields(table_name, query_data.keys()):
            return False
        # Get next safe ID

        insert_id = self.increment_next_id(table_name)
        query_data[table_name + "_id"] = str(insert_id)
        
        safe_query_data = dict()

        # Construct safe version of row.
        for default_field in self.pragma['tables'][table_name]['field']:
            if default_field in query_data:
                safe_query_data[default_field] = query_data[default_field]
            else:
                safe_query_data[default_field] = "null"

        # Add the actual row to TABLES, ID.equals(dict.key).
        self.tables[table_name][insert_id] = safe_query_data

        # Increment number of rows and the flag to tell the class to save data out on exit.
        self.increment_table_row_count_pragma(table_name)
        self.set_table_did_change_pragma(table_name)

        # Array in the form {'1':{key: value, key: value}, '2':{key: value, key: value}}
        return insert_id

    def deconstruct(self):
        # Always write out pragma
        i = 0
        for table_name in self.pragma['tables']:
            if self.get_table_did_change(table_name):
                self.save_file(table_name, self.tables[table_name])
                self.clear_table_did_change(table_name)
                i += 1
        self.save_file(self.pragma_name, self.pragma)

        self.notice("Changes to %s tables were saved" % i)
        # Check with hit 
        return True


    """
    "" @name: Select 
    "" @author: Daniel Koehler  
    "" @description: Method to select rows froma table, where clause is comma delimted, each condition in the form (`field_name` operator 'value') [AND] [OR]
    "" @prams: (String) Table Name, String (Where), (Integer) Limit
    "" @return: (List) Returned rows
    """

    def create_table(self, table_name):

        if self.pragma_exists() and table_name in self.pragma['tables']:
            self.error("Table discriptor exists for `%s`, cannot overwrite." % table_name)

        if self.pragma_exists() and table_name in self.tables:
            self.error("Table `%s` exists, cannot overwrite.")


        self.pragma['tables'][table_name] = {
                "field" : [], 
                "last_insert_id": 0, # NOT ZERO, Returning Insert ID would be ambiguous.
                "table_did_change": True, # Make sure this table is saved out.
                "row_count":0
            }

        self.tables[table_name] = {}
        self.create_field(table_name, table_name + '_id')

    def create_field(self, table_name, field_name, default="null"):
        if table_name not in self.pragma['tables']:
            self.error("Table `%s` not found" % table_name)
            return False

        if field_name in self.pragma['tables'][table_name]['field']:
            self.error("Field exists")
            return False

        self.pragma['tables'][table_name]['field'].append(field_name)
        
        # LOOP OVER ALL EXISTING ROWS IN SELF.TABLES ADDING field:default

        return True

    def save_file(self, filename, data):

        # Make sure user hasn't provided relative path or table prefix, we'll add these.
        filename = filename.replace(self.relative_path,"").replace(self.table_prefix,"")
        
        # Create full path
        filepath = os.path.normpath(os.path.join(self.relative_path, self.table_prefix + filename + ".cpickle"))

        # Open file
        data_file = open(filepath, 'wb')     
        
        # Load data
        pickle.dump(data, data_file, protocol=2)
        
        # Close data
        data_file.close()
        return data

    def load_file(self, filename):

        # Make sure user hasn't provided relative path or table prefix, we'll add these.
        filename = filename.replace(self.relative_path,"").replace(self.table_prefix,"")
        
        # Create full path
        filepath = os.path.normpath(os.path.join(self.relative_path, self.table_prefix + filename + ".cpickle"))

        # Ensure we have file or throw error
        if not os.path.isfile(filepath):
            self.error("Pagma file not found", serious=False)
            return False

        # Open file
        data_file = open(filepath, 'rb')   #  UnpicklingError: invalid load key, ''. 

        
        # Load data
        data = pickle.load(data_file)
        
        # Close data
        data_file.close()
        return data

    def load_pragma(self):

        # Load file detailing pragma
        pragma = self.load_file(self.pragma_name)

        # Is the DB pragma file populated?
        if not pragma:
            self.error("Pragma empty", serious=False)
            return False
        # Do we have tables?
        if not len(pragma['tables']):
            self.error("No tables in pragma - correct file path?", serious=False)
        
        self.pragma = pragma

    def load_tables(self):

        # Do we have a populated pramga array?
        if not len(self.pragma):
            self.error("Pragma empty", serious=False)

        # Do we have any tables to load? 
        if not len(self.pragma['tables']):
            # No. Let's throw an error and return to thread.
            self.error("No tables", serious=False)
            return False

        # For each table, find file and load rows.
        for table_name in self.pragma['tables']:
            table_data = self.load_file(table_name)    
            self.tables[table_name] = table_data # Array in the form {'1':{key: value, key: value}, '2':{key: value, key: value}}

    def drop_table(table_name):
        pass

    def error(self, error, serious=True):
        if serious:
            print "Database Error: %s." % error
            sys.exit()
        print "Database Notice: %s." % error

    def notice(self, notice):
        print "Database Notice: %s." % notice

    def table_exists(self, table_name):
        
        # Table exists and has been loaded.
        if not self.table_pragma_exists(table_name):
            return False
        if not table_name in self.tables:
            self.error("Table doesn't exist")
            return False
        return True
    
    def table_pragma_exists(self, table_name):
        
        if not table_name in self.pragma['tables']:
            self.error("Table pragma doesn't exist")
            return False
        return True

    def pragma_exists(self):
        return bool(len(self.pragma))

    def get_fields(self, table_name):
        if not self.table_pragma_exists(table_name):
            return False
        return self.pragma['tables'][table_name]['field']

    def table_has_fields(self, table_name, fields):

        if not self.table_pragma_exists(table_name):
            return False

        for field in fields:
            if field not in self.pragma['tables'][table_name]['field']:
                self.error("Table doesn't contain the field `%s`, this operation effected 0 rows." % field)
        return True

    def increment_table_row_count_pragma(self, table_name):
        self.pragma['tables'][table_name]['row_count'] += 1

    def decrement_table_row_count_pragma(self, table_name):
        self.pragma['tables'][table_name]['row_count'] -= 1
    
    def get_table_row_count(self, table_name):
        if table_name not in self.pragma['tables']:
            self.error("Table not found")
        return self.pragma['tables'][table_name]['row_count']

    def set_table_did_change_pragma(self, table_name):
        if not table_name in self.pragma['tables']:
            self.error("Can't set change pragma because table discriptor doesn't exist")

        self.pragma['tables'][table_name]['table_did_change'] = True

    def get_table_did_change(self, table_name):
        if not table_name in self.pragma['tables']:
            self.error("Can't return change pragma because table discriptor doesn't exist for %s" % table_name)
        return self.pragma['tables'][table_name]['table_did_change']

    def clear_table_did_change(self, table_name):
        if not table_name in self.pragma['tables']:
            self.error("Can't clear change pragma because table discriptor doesn't exist for %s" % table_name)
        self.pragma['tables'][table_name]['table_did_change'] = False

    def get_table_last_insert_id(self, table_name):
        if table_name not in self.pragma['tables']:
            self.error("Table not found")

        return self.pragma['tables'][table_name]['last_insert_id']


    """
    "" @name: Increment Next ID 
    "" @author: Daniel Koehler  
    "" @description: Method to increment the table ID
    "" @prams: (String) Table Name
    "" @return: New Insert ID
    """

    def increment_next_id(self, table_name):
        if table_name not in self.pragma['tables']:
            self.error("Table not found")
            return False

        # Increment id - currently points to last row on this table
        self.pragma['tables'][table_name]['last_insert_id'] += 1

        # Return the currently useable id
        return self.pragma['tables'][table_name]['last_insert_id'];

    """
    "" @name: Get Pragma 
    "" @author: Daniel Koehler  
    "" @description: Get Pragma array
    "" @prams: (String) Table Name, String (Where), (Integer) Limit
    "" @return: (List) Returned pragma
    """
    
    def get_pragma(self):
        if not len(self.pragma):
            self.error("Pragma unpopulated.")
        return self.pragma


    """
    "" @name: Deserialise Clause 
    "" @author: Daniel Koehler  
    "" @description: Method to select rows froma table, where clause is comma delimted, each condition in the form (`field_name` operator 'value') [AND] [OR]
    "" @prams: (String) Table Name, (String) clause
    "" @return: (List) Returned rows
    """

    def deserialise_clause(self, table_name, clause):

        valid_operators  = ['>', '>=', '<', '<=', '!=', '==']


        clause.lstrip() # Remove all whitespace on the left
    
        # Fetch out and validate Field.
        clause_field = clause.split("`")[1] # Get Field name   
    
        # Fetch out and validate Field.
        clause_field = clause.split("`")[1] # Get Field name         
        
        if clause_field not in self.get_fields(table_name):
            self.error("Invalid field in WHERE clause, `%s` does not exist in table `%s`" % (clause_field, table_name))

        clause = clause.strip("`")[len(clause_field):].lstrip("`").lstrip()

        # Fetch out and validate Operator.
        clause_operator = clause.split(" ")[0]

        if clause_operator not in valid_operators:
            self.error("Invalid operator in WHERE clause")

        clause = clause[len(clause_operator):].lstrip() # Remove operator and spaces

        # Fetch out and validate Value.

        clause_value = clause[1:-1]

        query_condition = {'field':clause_field,'operator':clause_operator, 'value': clause_value}

        return query_condition


    """
    "" @name: Deserialise Where Clause 
    "" @author: Daniel Koehler  
    "" @description: Method to convert part of where clause to usable array
    "" @prams: (String) Table Name, String (Where)
    "" @return: (List) Returned rows
    """

    def deserialise_where_clause(self, table_name, where ):
        
        conditions = list()

        # Split and re-format string segments. 

        clauses = where.split("') OR (`")
        clauses = [clause.lstrip("(").rstrip("')") for clause in clauses]
        clauses = ["`" + clause.lstrip("(`").rstrip("')") + "'" for clause in clauses]

        for clause in clauses:
            subclauses = clause.split("') AND (`")
            subclauses = ["`" + subclause.lstrip("(`").rstrip("')") + "'" for subclause in subclauses]

            if len(subclause) > 1: 
                clause = subclauses.pop(0)  

            query_condition = self.deserialise_clause(table_name, clause)

            if len(subclauses):
                subclauses = [self.deserialise_clause(table_name, subclause) for subclause in subclauses]     
                query_condition['and'] = subclauses 

            conditions.append(query_condition)

        return conditions

