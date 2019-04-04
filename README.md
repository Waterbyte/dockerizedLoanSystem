-------------------
 
You will be building a minimal loan management system. At RedCarpet everyone is a fullstack engineer with equal focus on front end and backend. We give full responsibility+ownership of products to our engineers. This interview is structured like that.
 
This is not a one sided interview - this allows you to interview us by giving you an idea of what a typical day looks like at RedCarpet. We hope you like it!
 
For the interview, you have the choice to build only API or UI+API. This interview question is written in a way that allows you to do both, since at RedCarpet, you will be expected to do both. This interview also throws some stuff that you may need to learn on the fly - we think thats a good thing to test for. At RedCarpet you will end up working on things that nobody has worked on - so an ability to learn quickly is highly valued here.
 
Arguing for your design:
 
At RedCarpet, we like to debate and argue over technology and architecture. There is no hierarchy or "boss" system. Even the juniormost intern has the power to argue with the CTO (politely).
Throughout this interview, you will be asked to think and make design choices and justify them. In addition to the code, we would like you to send a README file with reasons for each and every of the points mentioned in this interview. Commit this README file in your codebase itself.
 
Core infrastructure:
 
1. You can do this in any language. We dont care - language is just a tool. Work here is done primarily on python and reactjs (which you can learn if you join). At no point do we argue over the superiority of python over other languages. Its just a tool we ended up using and serves us well.
2. You will deliver your work as a Docker project. At RedCarpet we value seamless packaging of software to make it easy to develop and use. We expect you to do the same. Learning Docker isnt very hard. It takes an hour at most. Some examples are - https://nodejs.org/en/docs/guides/nodejs-docker-webapp/ , https://blog.codeship.com/building-minimal-docker-containers-for-go-applications/ , https://www.fullstackpython.com/blog/develop-flask-web-apps-docker-containers-macos.html, https://medium.com/@jhh3/all-the-small-things-86a8f2b3f67. You dont need to create an image and upload to a registry, just make sure the Dockerfiles work well. We will ONLY run your code through Docker. You should also specify how to run your testcases through Docker.
3.  Registration and Roles - Different users can have different roles. The three roles are "customer", "agent" and "admin". We want to see how you are creating/salting/hashing the passwords. Another question to think about is - how will you set the role of a user ? All of these are questions you should think about.
4. Your api needs to be protected by authentication.  For all the  API you will build, design an auth system. We want to see how you do this. Will you use a token? a username/password ?  Are you using JWT? remember that for API, you cant have cookies. How will you handle roles in an API? Will you only ask for authentication once or will every api call be authenticated. All of these are questions you should think about.
5. All data should be stored in a database. Ideally we would want this in Postgresql..but for purposes of interview, you can use any database (including Mongodb !)
 
Features:
1. List, view and edit users -  this can only be done by "agent" and "admin" roles
2. Create a loan request on behalf of the user -  This can only be done by "agent" role. Inputs would be tenure selected (in months) and interest to be charged every month. Loan can have 3 states - "NEW", "REJECTED", "APPROVED".
NOTE: we expect you to figure out what a "loan" object will look like. EMI, interest rates, duration, etc. This is domain knowledge that we expect our engineers to figure out by themeselves. Will you use reducing interest rates, etc ? Especially tricky question is how will you handle dates - we are especially interested to see this code, since date handling is one of the trickiest things here (is it needed to handle timezone information in your database ?)
3. Approval of loan request - This can only be done by an "admin" role.
4. Edit a loan (but not after it has been approved) -  This can be done only by "agent" role. But cannot be done if loan is in "Approved" state. IMPORTANT: We want to see how you design this. Can you save previous history ? In an extreme situation, can you "rollback" the changes ? Hint: the best designs here use "double safety" - logic in the code as well as database constraints.
5. Ability to list and view loans (approved) or loan requests based on the filter applied -  By "filter" we mean - select by date of creation, date of update, state of loan (NEW, REJECTED, APPROVED), etc. This action can be done by all : "customer", "agent" and "admin" roles. HOWEVER - "customer" can only see his own loans...while "agent" and "admin" can see everyone's loans. The way you design your data model above will allow you to do this. Make sure there are no security loopholes here. (P.S. you have to show us by writing the testcases to illustrate this)
 
Testcases:
Writing testcases are a cultural value and a hard requirement at RedCarpet. We wish to see the same. We prefer good testcases for less features, rather than no testcases and more features.
We dont expect you send a database dump for testing. All frameworks allow you to "mock" data (or fixtures).
Important: You should also specify how to run your testcases through Docker. This is the first thing we will try.
 
 
 
-----------------------------