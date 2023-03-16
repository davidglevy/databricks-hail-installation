# Databricks notebook source
import hail as hl

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initialize Hail
# MAGIC 
# MAGIC We need to initialize Hail. As we already have a SparkContext, we must reference that. In addition, if we are running this Notebook from a Repo we must specify an alternate log directory and tmp directory for hail.

# COMMAND ----------

hl.init(sc=sc,log="/var/log/hail",tmp_dir="/tmp")

# COMMAND ----------

mt = hl.balding_nichols_model(n_populations=3,
    n_samples=500,
    n_variants=500_000,
    n_partitions=32)
mt = mt.annotate_cols(drinks_coffee = hl.rand_bool(0.33))
gwas = hl.linear_regression_rows(y=mt.drinks_coffee,
       x=mt.GT.n_alt_alleles(),
       covariates=[1.0])
gwas.order_by(gwas.p_value).show(25)
