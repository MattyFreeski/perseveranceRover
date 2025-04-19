# Perseverance rover - SOFTWARE


## Contents


1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)  
   2.1. [Arduino](#arduino)   
   2.2. [Python](#python)


## Prerequisites 
   1. Download and install [Arduino IDE](https://www.arduino.cc/en/software/)

   2. Download and install [Anaconda3](https://www.anaconda.com/download)



## Getting Started

Clone the repository by opening your termimal and typing:
```bash
git clone https://github.com/MattyFreeski/perseveranceRover.git
```


### Arduino

The Arduino software part is very simple:
1. Connect your Arduino to the PC via USB
2. Open `standardFirmata.ino` file in your Arduino IDE
3. Select the board from the dropdown menu
4. Click the `Upload` button

### Python
1. **Install the dependencies**

   The `makefile` creates a conda environment by running in your terminal:

   ```bash
   make install
   ```

3. **Launch the controller application**
   
   The `makefile` can also run the python script of the controller application by:
      ```bash
   make run
   ```

   You can control the rover either using the app or your keyboard:
   - **W**: Forward
   - **S**: Stop
   - **X**: Backward
   - **Q**: Rotate counterclockwise
   - **E**: Rotate clockwise






