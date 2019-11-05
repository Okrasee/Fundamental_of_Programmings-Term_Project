# 15-112 Term Project - Physics Game
This is a physics-based game empowered by a 2D physics library called PyMunk. <http://www.pymunk.org/en/latest/installation.html> 

The main scenario of the game is to send the main character, an electron, to its destination which is an atom. The player wins the game If he/she passes all three levels of the game.

### Level 1:
The player could move the electron along levers and create a path by two bars to make sure it does not fall into the lake. 

### Level 2:
The player could place three (at max) balls on the pulley joints so that the joints move in ways which push the electron toward the destination. 

### Level 3:
The player could build a path for the electron to follow. The gateways send the electron for one block to another as it is not possible to traverse through the blocks. The destination is a curve on which there are stars for the electron to hit. More stars it hits, the higher score.

### Multiplayer Mode
There is a multiplayer mode in which two players could play simultaneously and compete against each other through the use of Socket. Messages containing information about the movement of electrons and construction of new paths will be sent back and forth between server and client.

