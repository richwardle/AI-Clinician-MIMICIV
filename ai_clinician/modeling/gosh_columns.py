from ai_clinician.preprocessing.gosh_columns import *

C_OUTCOME = "outcome"
C_STATE = "state"
C_ACTION = "action"
C_REWARD = "reward"

C_SOFTENED_PHYSICIAN_PROBABILITY = "softened_physician_prob"
C_SOFTENED_MODEL_PROBABILITY = "softened_model_prob"
C_OPTIMAL_ACTION = "optimal_action"

"""
bloc,icustayid,charttime,gender,age,elixhauser,re_admission,died_in_hosp,died_within_48h_of_out_time,mortality_90d,delay_end_of_record_and_discharge_or_death,Weight_kg,GCS,HR,
SysBP,MeanBP,DiaBP,RR,SpO2,Temp_C,FiO2_1,Potassium,Sodium,Chloride,Glucose,BUN,Creatinine,Magnesium,Calcium,Ionised_Ca,CO2_mEqL,SGOT,SGPT,Total_bili,Albumin,Hb,WBC_count,
Platelets_count,PTT,PT,INR,Arterial_pH,paO2,paCO2,Arterial_BE,Arterial_lactate,HCO3,mechvent,Shock_Index,PaO2_FiO2,median_dose_vaso,max_dose_vaso,input_total,input_4hourly,
output_total,output_4hourly,cumulated_balance,SOFA,SIRS

"""

AS_IS_COLUMNS = [C_GENDER, C_MECHVENT, C_MAX_DOSE_VASO, C_RE_ADMISSION]
NORM_COLUMNS = [C_AGE, C_WEIGHT, C_GCS, C_HR, C_SYSBP, C_MEANBP, C_DIABP, C_RR, C_TEMP_C, C_FIO2_1,
            C_POTASSIUM, C_SODIUM, C_CHLORIDE, C_GLUCOSE, C_MAGNESIUM, C_CALCIUM,
            C_HB, C_WBC_COUNT, C_PLATELETS_COUNT, C_PTT, C_PT, C_ARTERIAL_PH, C_PAO2, C_PACO2,
            C_ARTERIAL_BE, C_HCO3, C_ARTERIAL_LACTATE, C_SOFA, C_SIRS, C_SHOCK_INDEX, C_PAO2_FIO2, C_CUMULATED_BALANCE]
LOG_NORM_COLUMNS = [C_SPO2, C_BUN, C_CREATININE, C_SGOT, C_SGPT, C_TOTAL_BILI, C_INR,
                    C_INPUT_TOTAL, C_INPUT_STEP, C_OUTPUT_TOTAL, C_OUTPUT_STEP]

ALL_FEATURE_COLUMNS = AS_IS_COLUMNS + NORM_COLUMNS + LOG_NORM_COLUMNS

STATE_COLUMNS = [C_GENDER, C_MECHVENT, C_RE_ADMISSION, C_AGE, C_WEIGHT,
                 C_GCS, C_HR, C_SYSBP, C_MEANBP, C_DIABP,
                 C_RR, C_TEMP_C, C_FIO2_1, C_POTASSIUM, C_SODIUM,
                 C_CHLORIDE, C_GLUCOSE, C_MAGNESIUM, C_CALCIUM, C_HB,
                 C_WBC_COUNT, C_PLATELETS_COUNT, C_PTT, C_PT, C_ARTERIAL_PH,
                 C_PAO2, C_PACO2, C_ARTERIAL_BE, C_HCO3, C_ARTERIAL_LACTATE,
                 C_SOFA, C_SIRS, C_SHOCK_INDEX, C_PAO2_FIO2, C_CUMULATED_BALANCE,
                 C_SPO2, C_BUN, C_CREATININE, C_SGOT, C_SGPT,
                 C_TOTAL_BILI, C_INR, C_INPUT_TOTAL, C_INPUT_STEP, C_OUTPUT_TOTAL,
                 C_OUTPUT_STEP]