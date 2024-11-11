ifeq ($(OS),Windows_NT)
    PYTHON = python
    PIP = pip
else
    PYTHON = python3
    PIP = pip3
endif

REQUIREMENTS = requirements.txt
MAIN_SCRIPT = main.py

all: install run

install:
	$(PIP) install -r $(REQUIREMENTS)

# Target to run the main script
run:
	$(PYTHON) $(MAIN_SCRIPT)

clean:
	@echo "No files to clean in this setup."