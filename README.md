# Term Project
 Group 18's Term Project
Christopher Ng, Dylan Featherson, Edward Eyre


# Introduction
Our project introduces an autonomous turret system designed to enhance target acquisition and firing capabilities for Nerf or similar projectile launchers. The primary purpose of our device is to autonomously locate the centroid of heat in a designated area and adjust the yaw of the Nerf gun to aim precisely at the detected target. While the pitch remains fixed, our turret system ensures accurate horizontal alignment for firing at the identified heat source. The device is primarily intended for recreational use, targeting enthusiasts of Nerf or similar foam projectile launchers who seek an enhanced and automated shooting experience. Additionally, our turret system can be of interest to hobbyists, makers, and engineering students interested in exploring mechatronics, automation, and robotics applications. With its autonomous targeting capabilities, the device offers a unique and engaging way to enjoy Nerf battles while showcasing advancements in technology integration and automation.

# Hardware Design
![20240315_135635](https://github.com/Cadre1/Term-Project/assets/55156855/13e64ac5-0520-4c69-b7a5-7084ba4032b9)
![20240315_135642](https://github.com/Cadre1/Term-Project/assets/55156855/f875bbc5-17c6-4bc6-b902-88512c888c7d)

" Ned would you be able to put a screen shot of the CAD here"


# Software Design
![image](https://github.com/Cadre1/Term-Project/assets/55156855/35797bbd-3ab6-4ab8-95d5-6899b830bee7)
![image](https://github.com/Cadre1/Term-Project/assets/55156855/cc1501a2-59ac-47d4-a599-750216bdc687)

# Results
Our system underwent rigorous testing on the designated battle table, which spanned 8 feet in length. During these tests, we evaluated its performance in various scenarios by setting up targets at different distances and heat levels. The system consistently demonstrated accurate target acquisition and aiming, proving its reliability under simulated battle conditions. With proper calibration of the IR sensor and a functional Nerf gun, the turret successfully located and fired at targets with precision, showcasing its effectiveness in autonomous operation.

# Challenges and Lessons Learned
Despite its overall success, we encountered challenges primarily related to mechanical components, particularly the undersized 3D printed gear teeth. This issue resulted in occasional slipping and improper meshing of gears, necessitating careful adjustments to ensure smooth turret rotation. Additionally, maintaining proper calibration of the IR sensor and addressing potential jams in the Nerf gun were critical for optimal performance. From these challenges, we learned the importance of meticulous component sizing and compatibility checks, as well as the significance of thorough calibration procedures for sensor-based systems.

# Reccomendations
For those seeking to build upon our work, we recommend prioritizing careful sizing and compatibility checks of mechanical components to prevent issues such as gear slipping. Additionally, implementing regular maintenance checks and calibration procedures for sensors and actuators is essential for consistent performance. Exploring alternative materials or manufacturing methods for gears could improve durability and reliability. Furthermore, integrating additional sensors or advanced algorithms for target tracking could enhance the system's accuracy and adaptability in dynamic environments. Overall, these recommendations aim to address challenges encountered during our project and offer avenues for further refinement and improvement in future iterations.

# References
Inspiration for the project: 

Vinnie San’s automatic turret - https://www.youtube.com/watch?v=dkEc3wjEfYc

Hardware and software manuals and support documents:

Helpful Code for ME 405 - https://github.com/spluttflob/ME405-Support

The STM32L476 Nucleo User Manual - https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf

The MLX90640 Thermal Camera Datasheet - https://www.melexis.com/en/documents/documentation/datasheets/datasheet-mlx90640

The ___ Servo Motor Datasheet - <INSERT DATASHEET>

The Project in Action - https://youtu.be/ceA77QBQG_Y?si=SO-bap_1HtrvdEz_
