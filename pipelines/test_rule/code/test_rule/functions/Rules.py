from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *

def Override_Housing_Purpose(
        secnd_purps_type_lbl: Column=col("Secnd_Purps_Type_Lbl"), 
        origination_system: Column=col("Origination_system"), 
        housing_purpose: Column=col("Housing_Purpose")
):
    return when(
          (
            (
              (secnd_purps_type_lbl == lit(231))
              & (origination_system == lit("MP-001"))
            )
            & (housing_purpose == lit("OO"))
          ),
          lit("IPL")
        )\
        .otherwise(col("housing_purpose"))\
        .alias("EFS_Housing_Purpose")

def Override_EFS_Rule_Id(residual_years: Column=col("Residual_years"), maturity_date: Column=col("Maturity_Date")):
    return when(((residual_years > lit(0)) & (residual_years <= lit(1))), lit(5))\
        .when((residual_years > lit(1)), lit(6))\
        .when((maturity_date == lit("")), lit(7))\
        .otherwise(lit(None))\
        .alias("EFS_Residual_Term_Rule_ID")
