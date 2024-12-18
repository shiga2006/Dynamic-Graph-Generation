DYNAMIC GRAPH GENERATOR

AIM - The application allows users to specify the type of analysis or visualization they require through natural language input and displays the corresponding charts dynamically

Project Structure:

![image](https://github.com/user-attachments/assets/b892e3ca-1f16-4cb3-aa73-b0fc74a4567f)


Tech Stack :

     1) Flask
     
     2) HTML
     
     3) CSS
     
     4) Voiceflow (Codeless chatbot)
     
     5) LLM(Hugging Face’s GPT-2 model)

     6) Javascript

     7) Emailjs
Screen shots of the website:
![Screenshot 2024-12-02 193542](https://github.com/user-attachments/assets/cb2d8810-ecbf-4d77-bc72-0f45abb87ace)
![Screenshot 2024-11-30 212954](https://github.com/user-attachments/assets/d990d50b-8c61-4f87-823b-7402c9bec850)
![Screenshot 2024-11-30 203842](https://github.com/user-attachments/assets/50b6ec97-ffde-4f91-9499-6f43bb2f329b)
![Screenshot 2024-11-30 203859](https://github.com/user-attachments/assets/66c6c095-b27a-4c86-906d-2a65f815ed7d)
![image](https://github.com/user-attachments/assets/d618f481-c75c-40ce-82f5-2746ba2387aa)
![Screenshot 2024-12-02 214017](https://github.com/user-attachments/assets/a48e5e2e-ef40-46f7-9d98-a41abb8b1f5c)
![Screenshot 2024-11-30 211704](https://github.com/user-attachments/assets/6d20102d-4ab9-43c6-a941-5c92e45d2eaa)



Graph generated in the website:
![Screenshot 2024-11-30 214519](https://github.com/user-attachments/assets/7f6a032f-ff2e-4220-8b48-f0ef38f0a3c7)
![Screenshot 2024-11-30 215009](https://github.com/user-attachments/assets/78166866-59d1-4380-958d-189b7460f616)


Youtube video link -[ https://youtu.be/2rJbAFookGg](https://www.youtube.com/watch?v=2rJbAFookGg&list=PL1Zw2iWy4ih9kuO9z0q3GstqW-d2sjsua)
I have published the demo video(working of the website) in youtube check it to know the working of this website


Challenges Faced and Solutions
1) Challenge: Deployment Environment Compatibility
   
Description: The application behaved differently across development and production environments.

Solution: Utilized Docker to create consistent containerized environments. This ensured compatibility and smooth deployment across different platforms.


2) Challenge: Dynamic Graph Generation in Web Application
   
Description: Integrating user-defined graph descriptions with backend rendering was complex.

Solution: Utilized the matplotlib and Plotly libraries in Python to dynamically generate graphs based on user input. Implemented input validation and error handling to ensure the system was robust.


3) Challenge: Security Concerns with User Authentication
   
Description: Handling sensitive data during user authentication raised concerns about security vulnerabilities.

Solution: Used HTTPS for secure communication, encrypted user passwords with bcrypt, and implemented token-based authentication (JWT).


4) Challenge: Compatibility Issue Between matplotlib and tkinter
   
Description: During the implementation of graphical features, a compatibility issue arose between matplotlib and tkinter, causing errors in rendering the graphs in a GUI environment.

Solution: Resolved the issue by explicitly setting the matplotlib backend to TkAgg in the code. Additionally, updated all dependencies to their latest compatible versions to prevent similar issues in the future.


5) Challenge: Integrating Voiceflow with Flask
   
Description: Initially, the integration was attempted using only the version ID and user ID. This approach was insufficient for handling dynamic user inputs and providing context-specific responses, leading to incomplete interaction capabilities.

Solution: To address this limitation, the full Voiceflow API was integrated into the Flask application. This allowed for better interaction handling by enabling dynamic requests and responses, leveraging Voiceflow's state management and context features effectively.
