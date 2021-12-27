# Evolving-Soft-Robots
This project involved simulating and evolving soft robots using vpython (visual python)
The robots were made of spring-mass systems, where masses were spheres connected by springs (helixes)
By changing the spring constant k, and the spring's rest length as a function of 4 parameters, acceleration of the system was achieved
Soft robots were evolved by the magnitude of their velocity
At first, this involved only evolving the variable parameters a, b, c, and w in the equation Lo = a + b*sin(wt+c) 
Then, co-evolution between the spring parameters and the structure of the robot (positions and number of masses) was achieved
