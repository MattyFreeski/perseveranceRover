# Define names and versions
ENV_NAME := rover-env
PYTHON_VERSION := 3.12

.PHONY: install conda uninstall activate 

all: install run

###############################################################################
###				  Environment and dependencies installation  				###
###############################################################################
install: conda poetry

conda:
	@echo "\n 🚀 Creating Conda environment & installing dependencies 📦 \n"
	conda env create -n $(ENV_NAME) -f environment.yml
	bash -i -c "conda activate $(ENV_NAME) && pip install pyfirmata2"
	@echo "✅ Conda environment created.\n\n"

uninstall:
	@echo "\n 🧹 Removing Conda environment"
	conda remove -y --name $(ENV_NAME) --all

activate:
	@echo "\n\n 🔧 To activate the environment, use \n"
	@echo "	conda activate $(ENV_NAME)\n\n"


###############################################################################
###				  				Code execution  							###
###############################################################################
run:
run:
	@echo "\n\n 🎮 Starting the controller app 🎮 \n"
	bash -c "source $(shell conda info --base)/etc/profile.d/conda.sh && \
			 conda activate $(ENV_NAME) && \
			 python3 roverCode.py"

