# Databricks notebook source
# MAGIC %sh
# MAGIC 
# MAGIC echo "#!/bin/bash" > /tmp/hail-init.sh
# MAGIC echo "apt-get install -y libopenblas-dev libopenblas-base liblapack3" >> /tmp/hail-init.sh
# MAGIC mkdir -p /dbfs/scripts
# MAGIC cp -f /tmp/hail-init.sh /dbfs/scripts/hail-init.sh

# COMMAND ----------

cat /dbfs/scripts/hail-init.sh
