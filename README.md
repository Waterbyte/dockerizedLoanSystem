The backend is made with Python Flask and the default development server. Webargs are used for argument parsing and Flask_restful for routing.

Mongodb is used as a database.

Features:
1. List, view and edit users -  this can only be done by "agent" and "admin" roles
2. Create a loan request on behalf of the user -  This can only be done by "agent" role. Inputs would be tenure selected (in months) and interest to be charged every month. Loan can have 3 states - "NEW", "REJECTED", "APPROVED".
3. Approval of loan request - This can only be done by an "admin" role.
4. Edit a loan (but not after it has been approved) -  This can be done only by "agent" role. But cannot be done if loan is in "Approved" state.
5. Ability to list and view loans (approved) or loan requests based on the filter applied. "customer" can only see his own loans...while "agent" and "admin" can see everyone's loans. 
 

