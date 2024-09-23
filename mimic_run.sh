
#!/bin/bash

command=$1

# Activate the virtual environment
source iv/bin/activate

# Step 1: Install torch first
pip install torch>=2.2.2 || { echo "Failed to install torch"; exit 1; }

# Step 2: Install the rest of the dependencies
pip install -r requirements.txt || { echo "Failed to install dependencies from requirements.txt"; exit 1; }

# Step 3: Install signatory
#pip install signatory==1.2.3.1.6.0 || { echo "Failed to install signatory"; exit 1; }

echo "BUILD MODELS"
echo "Using MIMIC dataset directory: ai_clinician/modeling/mimic_inputs"
echo "Using model output directory: ai_clinician/implementation/mimic/outputs"
echo

echo "GENERATE DATASETS"
python ai_clinician/modeling/01_generate_datasets.py ai_clinician/modeling/mimic_inputs ai_clinician/implementation/mimic/outputs || exit 1

echo "TRAIN MODELS"
python ai_clinician/modeling/02_train_models.py ai_clinician/implementation/mimic/outputs --n-models 100 || exit 1

echo "DONE"

# Deactivate the virtual environment
deactivate