## Mini-SQL-Engine
A Mini SQL Engine which runs a subset of queries using CLI.
It contains sample queries and the code.  
### The subset of queries which it can run:
- Select all records from one or more tables:
   - Select * from table_name;
- Aggregate functions on a single column like sum, average, max and min. 
   - Select sum(col1) from table1;
- Project columns from one or more tables:
  - Select col1, col2 from table1;
- Select with 'WHERE' condition from one or more tables:
  - Select col1, col2 from table1 where col1 = 10;
- Projecting columns from one or more tables with one JOIN condition:
   - Select col1,col2 from table1, table2 where table1.col1 = table2.col2
- Error handling is done wherever necessary.

### Steps to run the code:
python3 sql_engine.py <query>


 
