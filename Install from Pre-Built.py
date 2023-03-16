# Databricks notebook source
# MAGIC %sh
# MAGIC mkdir /tmp/tar_temp
# MAGIC cp /dbfs/hail/hail.tar.gz /tmp/tar_temp

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp/tar_temp
# MAGIC tar xzf hail.tar.gz

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp/tar_temp/hail/build
# MAGIC find

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp/tar_temp/hail/build
# MAGIC cp ./deploy/dist/hail-0.2.111-py3-none-any.whl /dbfs/hail/hail-0.2.111-py3-none-any.whl

# COMMAND ----------

# MAGIC %sh
# MAGIC find /tmp/tar_temp | grep hail-all

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp
# MAGIC tar xzf hail.tar.gz

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp | grep 'hail-all'

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp
# MAGIC make install-on-cluster HAIL_COMPILE_NATIVES=1 SCALA_VERSION=2.12.13 SPARK_VERSION=3.3.2
