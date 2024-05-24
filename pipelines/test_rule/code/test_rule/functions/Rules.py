from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *

def RiskAssetClassSegmentation(
        product_type_code: Column=col("PRODUCT_TYPE_CODE"), 
        con_bus_indc: Column=col("CON_BUS_INDC"), 
        reglt_counterparty_type_code: Column=col("REGLT_COUNTERPARTY_TYPE_CODE"), 
        lg_product_l08_key: Column=col("LG_PRODUCT_L08_KEY"), 
        tce: Column=col("TCE"), 
        month_key: Column=col("MONTH_KEY"), 
        basel_retail_corp_code: Column=col("BASEL_RETAIL_CORP_CODE"), 
        source_system_code: Column=col("SOURCE_SYSTEM_CODE"), 
        consol_annual_revenue: Column=col("CONSOL_ANNUAL_REVENUE"), 
        anzsic_code: Column=col("ANZSIC_CODE"), 
        owner_occupied_flg: Column=col("OWNER_OCCUPIED_FLG")
):
    return when((product_type_code.isin(lit("HL"), lit("IL"), lit("EA"), lit("PF")) & (con_bus_indc != lit("B"))), lit("MRTG"))\
        .when(
          (
            (
              (
                (con_bus_indc != lit("B"))
                & (reglt_counterparty_type_code == lit("540"))
              )
              & (lg_product_l08_key == lit("PFCRC"))
            )
            & (
              (tce <= lit(100000))
              & (month_key > lit("201304"))
            )
          ),
          lit("QRE")
        )\
        .when((basel_retail_corp_code == lit("SMERET")), lit("SMERET"))\
        .when(
          (
            (
              (con_bus_indc == lit("C"))
              & (reglt_counterparty_type_code == lit("540"))
            )
            & ~ source_system_code.isin(lit("CSH"), lit("GOE"), lit("CLS"), lit("ROS"))
          ),
          lit("OTHRETL")
        )\
        .when((reglt_counterparty_type_code == lit("510")), lit("SOV"))\
        .when((reglt_counterparty_type_code == lit("534")), lit("FI"))\
        .when(
          (
            (
              (basel_retail_corp_code == lit("SMECORP"))
              & (consol_annual_revenue <= lit(750000000))
            )
            & ~ anzsic_code.like("771%")
          ),
          lit("CORP-OTHER")
        )\
        .when(
          (
            (
              (reglt_counterparty_type_code == lit("538"))
              & (basel_retail_corp_code == lit("SMECORP"))
            )
            & (consol_annual_revenue > lit(750000000))
          ),
          lit("LRGCORP")
        )\
        .when(
          (
            (
              (basel_retail_corp_code == lit("SMECORP"))
              & (consol_annual_revenue > lit(750000000))
            )
            & (
              anzsic_code.like("771%")
              & (owner_occupied_flg != lit("Y"))
            )
          ),
          lit("IPRE_F")
        )\
        .when(
          (
            (
              (basel_retail_corp_code == lit("SMECORP"))
              & (consol_annual_revenue <= lit(750000000))
            )
            & (
              anzsic_code.like("771%")
              & (owner_occupied_flg != lit("Y"))
            )
          ),
          lit("IPRE_A_OTHER")
        )\
        .otherwise(lit(None))\
        .alias("Asset_Class")

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
