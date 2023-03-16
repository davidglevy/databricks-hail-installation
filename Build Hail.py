# Databricks notebook source
# MAGIC %sh
# MAGIC apt-get update

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y ca-certificates-java libpcsclite1

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y libopenblas-dev liblz4-dev

# COMMAND ----------

# MAGIC %md
# MAGIC ## Manually Install OpenJDK 8 jre/jdk
# MAGIC 
# MAGIC There's some issue at the moment installing OpenJDK 8 headless so I've manually downloaded the deb packages and install them like so. Hopefully in future this "just works" once Ubuntu has fixed up whatever issue is preventing it.

# COMMAND ----------

# MAGIC %sh
# MAGIC wget http://security.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jre-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb
# MAGIC wget http://security.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jdk-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb

# COMMAND ----------

# MAGIC %sh
# MAGIC dpkg -i 'openjdk-8-jre-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb'
# MAGIC dpkg -i 'openjdk-8-jdk-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb'

# COMMAND ----------

# MAGIC %sh
# MAGIC git clone https://github.com/hail-is/hail.git

# COMMAND ----------

# MAGIC %sh

# COMMAND ----------

# MAGIC %sh
# MAGIC find /usr/lib/jvm/java-8-openjdk-amd64 | grep jni.h

# COMMAND ----------

# MAGIC %sh
# MAGIC update-alternatives --set java $(update-alternatives --list java | grep java-8-openjdk)

# COMMAND ----------

# MAGIC %sh
# MAGIC JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# MAGIC PATH=$JAVA_HOME/bin/java:$PATH
# MAGIC C_INCLUDE_PATH=$JAVA_HOME/include
# MAGIC export JAVA_HOME PATH C_INCLUDE_PATH
# MAGIC cd hail/hail
# MAGIC make install-on-cluster HAIL_COMPILE_NATIVES=1 SCALA_VERSION=2.12.13 SPARK_VERSION=3.3.2

# COMMAND ----------

# MAGIC %sh
# MAGIC cd hail
# MAGIC cp hail/build/libs/hail-all-spark.jar /dbfs/hail/hail-all-spark.jar

# COMMAND ----------

# MAGIC %sh
# MAGIC ls hail/hail/build/deploy

# COMMAND ----------

# MAGIC %sh
# MAGIC cd hail
# MAGIC tar czf /tmp/hail.tar.gz .

# COMMAND ----------

# MAGIC %sh
# MAGIC ls hail

# COMMAND ----------

# MAGIC %sh
# MAGIC mkdir -p /dbfs/hail
# MAGIC cp -f /tmp/hail.tar.gz /dbfs/hail

# COMMAND ----------

# MAGIC %sh
# MAGIC ls -la /dbfs/hail

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y libopenblas-base liblapack3

# COMMAND ----------

import hail as hl
mt = hl.balding_nichols_model(n_populations=3,
                              n_samples=500,
                              n_variants=500_000,
                              n_partitions=32)
mt = mt.annotate_cols(drinks_coffee = hl.rand_bool(0.33))
gwas = hl.linear_regression_rows(y=mt.drinks_coffee,
                                 x=mt.GT.n_alt_alleles(),
                                 covariates=[1.0])
gwas.order_by(gwas.p_value).show(25)

# COMMAND ----------

# MAGIC %sh
# MAGIC cd hail | grep hail-all-spark.jar
