from regression_model.config import config
import pandas as pd

def validate_inputs(input_data: pd.DataFrame) -> pd.DataFrame:
    # check for numerical variables with NA not seen during training
    validated_data = input_data.copy()
    if input_data[config.FEATURES].isnull().any().any():
        validated_data = validated_data.dropna(
            axis=0, subset=config.FEATURES)

    return validated_data
