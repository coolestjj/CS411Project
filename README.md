In the previous stages, we designed all the database components for our application. Now it is time to connect your database to the front-end application. For this stage, your team is expected to build a simple user interface that interacts with the database you developed in Stage 3. Please note that we do not grade based on how fancy your user interface is. We grade based on the functionality of your interface and how it connects to the database.

For this stage, your team is expected to develop advanced database functions and add a creative component to your application. You are expected to continue working on the same (or an improved version of the) database you developed in Stage 3. You will also use this time to complete your application interface. 

Your web application should be designed for your users, not for the teaching staff. So, make sure that your application functionality matches your intended application description (usefulness, realness, uniqueness,...).

Each team will demo to their project TA by signing up on the demo signup sheet. More details will be posted as the demos approach. All team members are required to be present at the demo. Please keep track of your demo time. The project TA can cut you off when the time is up and not give you grades for components not presented during your demo.  Missing your demo slot will result in a grade of 0 for the entire team. Other accommodations follow the course syllabus.

The requirements are as follows:

A complete application with basic CRUD operations described in your proposal.  
Search the database using a keyword search. Your application should allow the user to input their search keyword and return the result to the interface.  
Implement an advanced database program that is related to your application. An advanced database program should include a transaction + trigger OR a stored procedure + trigger.    
Integrate your advanced database program with the application.   
This advanced database application must be triggered by some front-end interface/interaction.  
Definition of the previous requirement:   
Transaction requirements: A complete and functioning transaction with the correct and justified isolation level, involves at least two advanced queries, involves looping and control (e.g., IF statements) structures, and provides useful functionality to the application.  
Stored procedure requirements: A complete and functioning stored procedure, involves at least two advanced queries, uses cursors, involves looping and control (e.g., IF statements) structures, and provides useful functionality to the application.   
Trigger requirements: A complete and functioning trigger, involving an event, condition (IF statement), and action (Update, Insert or Delete), provides useful functionality to the application.   
Transactions, stored procedures, and triggers do not need to be related as long as they are relevant and real to the application.  
Transactions, stored procedures, and triggers need to be implemented in SQL, not through Object-relational Mappers (ORMs).  
The conditions (i.e., the If statements) and the advanced database program need to make sense to your application.   
Extra Credit (1% of the entire project grade): The entire application including frontend and backend should be hosted on GCP and connected to a MySQL instance on GCP.  
Extra Credit (up to 2% of the entire project grade): We would like your team to develop a creative component (function) that complements your project. This creative function can use existing libraries and/or APIs. It could be as simple as an interactive visualization tool or as complex as a machine learning recommendation system.  
A complete application demo. Think about what is the objective of your application. How would the user use the application? Discuss your system design choices (index selection, transaction, advance query, creative component). Discuss future improvements or extensions.   
Rubric: This stage is worth 35%. The entire stage would be graded during the demo. You are graded by completeness and correctness. The rubric is as follows:  

Your project TA will set up a meeting with you between 11/6 and 11/13. During the meeting, you are expected to discuss your plans for the application and any changes to your initial design. The goal of this meeting is to ensure your application is useful and viable to implement. Any team member who does not attend this meeting will get a penalty to their grade. (-5%)  
Arriving on time and completing the presentation within the given time frame (details will come at a later time on CampusWire). (+1%)  
A clear demo featuring a user's end-to-end process interacting with the system that involves presenting the CRUD operations, the advanced database program, and the (optional) creative function (10%)  
Ability to insert, update, and delete rows from the database and reflect the change on the frontend interface (7%):  
 0% if no interface for this operation is present  
+1% for having the code connecting the interface with the database  
+3% for having the interface for CRUD  
+3% for successfully changing the database and showing the change via an interface  
Search the database using a keyword search. Your application should allow the user to input their search keyword and return the result to the interface (5%):  
0% if no interface for this operation is present  
+0.5% for having the code connecting the interface with the database  
+1.5 % for having a textbox for entering the search keyword  
+3% for the successful execution of the query and the returning the result to the interface  
The advanced database program contains at least a sophisticated transaction+trigger or a stored procedure+trigger (+12%)  
Project TAs may deduct up to 50% of this component if the transaction and/or trigger does not make sense to the application.  

If you implemented transaction+trigger (12%):  
Transaction requirements (8%): A complete and functioning transaction with the correct and justified isolation level (2%), involves at least two advanced queries (2%, 1% each), involves control (e.g., IF statements) structures (2%), and provides useful functionality to the application (2%).   
Trigger requirements (4%): A complete and functioning trigger (1.5%), involves event, condition (IF statement), and action (Update, Insert or Delete) (1.5%), provides useful functionality to the application (1%).  
If you implemented stored procedure+trigger (12%):  
Stored procedure requirements (8%): A complete and functioning stored procedure (2%), involves at least two advanced queries (2%, 1% each), uses cursors, involves looping and control (e.g., IF statements) structures (2%), provides useful functionality to the application (2%).   
Trigger requirements (4%): A complete and functioning trigger (1.5%), involves event, condition (IF statement), and action (Update, Insert or Delete) (1.5%), provides useful functionality to the application (1%).  
Extra credit: The entire application is hosted on GCP AND connected to a MySQL database hosted on GCP. (+1% for hosting both application and database on GCP. Hosting both the application and database on other platforms, including but not limited to Azure and AWS, will receive this extra credit upon the project TA’s approval.)   
Extra Credit: A functioning and interesting creative component that is relevant to your application (up to +2% of the entire project grade)  
Extra Credit: The final application is well functioning, and the database consists of a TA-proposed dataset (+1% of the entire project grade)  
During the demo, the team should also discuss the following points: (-1% for any missing point or incorrect response)  
Explain your choice for the advanced database program and how it is suitable for your application. For example, if you chose a stored procedure+trigger, explain how this choice is suitable for your application.  
How did the creative element add extra value to your application?  
How would you want to further improve your application? In terms of database design and system optimization?  
What were the challenges you faced when implementing and designing the application? How was it the same/different from the original design?  
If you were to include a NoSQL database, how would you incorporate it into your application?  
You must submit your code to the repository in order to receive the grade. You should also tag your release and submit it on canvas. Failure to tag your release will result in a 3% deduction.  
All members must be present at the demo. Members who did not attend the entire duration of the demo will receive a 0.  
Using ORMs will result in a 0 for this stage!  