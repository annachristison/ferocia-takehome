## About
This project includes a term deposit class, some helper functions, and tests.  
An instance of a term deposit has one external facing method which is `get_balance_at_maturity`.
The helper functions (`financial_tools`) are split into those which operate annually, 
and those concerned with monthly based calculations. These functions are for manipulating interest rates and 
calculating the interest earned over various periods. 

## To run the tests
1. From the project root, run: `pytest`
1. To run all tests which match a string run `pytest -k test_correctly_calculates_balance_at_maturity_`

## To run locally as a script
#### To install the dependencies and set up the repo, run the following from the project root:
   1. Create the virtual environment to isolate dependencies: `python3 -m venv venv`
   1. Activate the virtual env: `source venv/bin/activate`
   1. Install the dependencies: `pip install -r requirements.txt` *(includes dev and test)*

#### Run the main module with custom input:

   
   * From the project root, run:`python3 -m term_deposit 1000 1.1 3 0 annually`
   
   * From the project root, run: `python3 -m term_deposit 10000 2.5 4 2 at_maturity`

*The arguments are all required, in order:*
1. initial deposit
1. interest rate
1. term - years
1. term - months
1. frequency
   
## Roadmap
* Bundle the input validation for term deposit class.
