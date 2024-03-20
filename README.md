# Term Project
 Group 18's Term Project
 
 Christopher Ng, Dylan Featherson, Edward Eyre


# Introduction
This project introduces an autonomous turret system designed to display enhanced target acquisition and firing capabilities for Nerf or similar projectile launchers. The primary purpose of this device is to autonomously locate the centroid of heat in a designated area through a thermal camera and adjust the yaw of the Nerf gun to aim precisely at the detected target. While the pitch remains fixed, our turret system ensures accurate horizontal alignment for firing at the identified heat source. The device is primarily intended for recreational use, targeting enthusiasts of Nerf or similar foam projectile launchers who seek an enhanced and automated shooting experience. Additionally, our turret system can be of interest to hobbyists, makers, and engineering students interested in exploring mechatronics, automation, and robotics applications. With its autonomous targeting capabilities, the device offers a unique and engaging way to enjoy Nerf battles while showcasing advancements in technology integration and automation.

# Final Product
![20240315_135635](https://github.com/Cadre1/Term-Project/assets/55156855/13e64ac5-0520-4c69-b7a5-7084ba4032b9)
![20240315_135642](https://github.com/Cadre1/Term-Project/assets/55156855/f875bbc5-17c6-4bc6-b902-88512c888c7d)
![20240312_233611](https://github.com/Cadre1/Term-Project/assets/55156855/3b1dd39f-36ef-4f7a-80c1-1240762ae399)


The Project in Action - https://youtu.be/ceA77QBQG_Y?si=SO-bap_1HtrvdEz_

# Hardware Design
Using the CAD model shown here and parts provided in the CAD folder, we developed laser printed wood parts for the main structural design of the turret along with specific 3D printed parts for components such as electronic fixtures, gears, and other small parts with sizings measured for the actual products. 

![image](https://github.com/Cadre1/Term-Project/assets/156386309/14a63418-f225-4f98-84ee-75bd75f43966)


# Electronic Schematic
Using the electronic schematic shown here, we wired the STM32 Nucleo to its corresponding electronic components with extended wires and external power sources.

![image](https://github.com/Cadre1/Term-Project/assets/156386309/85fd8def-7f5e-48b9-8cd7-d34d9cd2ef06)

# Software Design
Using the finite state machines shown here, we programmed our system accordingly to produce our controlled results. 

The program documentation can be found here - https://cadre1.github.io/Term-Project/

![image](https://github.com/Cadre1/Term-Project/assets/55156855/35797bbd-3ab6-4ab8-95d5-6899b830bee7)
![image](https://github.com/Cadre1/Term-Project/assets/55156855/cc1501a2-59ac-47d4-a599-750216bdc687)

# Results
Our system underwent rigorous testing on the designated battle table, which spanned 8 feet in length. During these tests, we evaluated its performance in various scenarios by setting up targets at different positions, heat levels, and time settings. Provided enough testing for general settings, the system demonstrated accurate target acquisition and aiming, proving its reliability under simulated battle conditions. With proper calibration of the IR sensor and a functional Nerf gun, the turret successfully located and fired at targets with precision, showcasing its effectiveness in autonomous operation.

# Challenges and Lessons Learned
Despite its overall success, we encountered challenges primarily related to mechanical components, particularly the undersized 3D printed spur gear teeth, and some detection of hotspots. Issues with too shallow of gear teeth depth and wear due to material choice and sizing resulted in occasional slipping and improper meshing of gears, necessitating slow and careful adjustments to ensure smooth turret rotation. This mainly showed to our lack in experience in developing gears for situations under medium amounts of play between moving parts. Provided more time, this issue could have been remedied by recutting wood and moving the motor location to better contact the annular gear, increasing gear teeth sizes, and/or altering our gear type to be spur gears to be able to mesh the two and have more room for error. In addition, maintaining proper calibration of the IR sensor and addressing potential jams in the Nerf gun were critical for optimal performance. Further adjustments for higher mounting of the thermal camera or a more sophisticated algorithim for horizontal hotspot calculation could have helped in aiming. From these challenges, we learned the importance of meticulous component sizing and compatibility checks, as well as the significance of thorough calibration procedures for sensor-based systems.

![20240315_133732](https://github.com/Cadre1/Term-Project/assets/55156855/f9f6561b-2345-45d2-a90d-2498befd2129)

# Recomendations
For those seeking to build upon our work, we recommend prioritizing careful sizing and compatibility checks of mechanical components to prevent issues such as gear slipping. Additionally, implementing regular maintenance checks and calibration procedures for sensors and actuators is essential for consistent performance. Exploring alternative materials or manufacturing methods for gears could improve durability and reliability. Furthermore, integrating additional sensors or advanced algorithms for target tracking could enhance the system's accuracy and adaptability in dynamic environments. Overall, these recommendations aim to address challenges encountered during our project and offer avenues for further refinement and improvement in future iterations.

# References
Inspiration for the project: 

Vinnie San’s automatic turret - https://www.youtube.com/watch?v=dkEc3wjEfYc

<br>

Hardware and software manuals and support documents:

Helpful Code for ME 405 - https://github.com/spluttflob/ME405-Support

STM32L476 Nucleo User Manual - https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf

MLX90640 Thermal Camera Datasheet - https://www.melexis.com/en/documents/documentation/datasheets/datasheet-mlx90640

HEXFLY 25kg Metal Gear Servo Specifications - https://www.redcatracing.com/products/rer11856?variant=30993858625626

IRLB8721PbF MOSFET Datasheet - https://www.infineon.com/dgdl/irlb8721pbf.pdf?fileId=5546d462533600a40153566056732591

L7805CV Voltage Regulator Datasheet - https://www.mouser.com/datasheet/2/389/l78-1849632.pdf

Nerf Gun - https://www.amazon.com/NERF-Motorized-Blaster-6-Dart-Compatible/dp/B08HSRQ1QV?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A2WM0OF2NX07WG
