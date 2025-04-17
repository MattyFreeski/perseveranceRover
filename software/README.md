# stocksPredictor
Neural Network algorithm to predict the stocks market

## Contents

1. [Getting Started](#getting-started)  
2. [Running the code](#running-the-code)  

   2.1. [Database generation only](#database-generation-only)  
   2.2. [Machine Learning only](#machine-learning-only)  




## Getting Started

1. **Clone the repository:**
   ```bash
   git clone 
   ```


1. **Download and install [Poetry](https://install.python-poetry.org)** if not already present:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   
2. **Install dependencies inside a virtual environment:**
   Install dependencies using poetry in a virtual environment
   using Python3.9 (if not present in the system install it before):
   ```bash
   conda env create -f environment.yml
   conda activate stocksPredictor

   ```
   if not done automatically activate the virtual environment you just created:
   ```bash
   source $(poetry env info --path)/bin/activate
   ```

   **Optional packages**: 
   ```bash
   python -m ipykernel install --user --name=stocksPredictor-conda_env --display-name "stocksPredictor-conda_env"
   ```



## Running the entire code

  The `makefile` in the main folder of the repo the code creates the syntetic database, trains the neural network and postprocesses the data obtained:

   ```bash
   make all
   ```



## Database generation only




## Machine Learning only





