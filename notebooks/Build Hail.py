# Databricks notebook source
# MAGIC %md
# MAGIC ## Build Hail
# MAGIC 
# MAGIC Hail does not have a pre-built version which is compatible for Databricks LTS 11.3 but we can adapt the instructions on the Hail website to build it.
# MAGIC 
# MAGIC We found the following changes to the base instructions
# MAGIC 
# MAGIC * Numerous apt-get packages had name changes
# MAGIC * Installing the JDK on Ubuntu was non-trivial
# MAGIC     * Dependencies missing 
# MAGIC     * Ubuntu package not found
# MAGIC     * Need to change default java

# COMMAND ----------

# MAGIC %md
# MAGIC ### Install Dependencies
# MAGIC We install dependencies for the build here:
# MAGIC 
# MAGIC * First run an apt update
# MAGIC * Download listed dependencies: libopenblas-dev liblz4-dev
# MAGIC * Download additional dependencies for OpenJDK: ca-certificates-java libpcsclite1

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get update

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y libopenblas-dev liblz4-dev

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y ca-certificates-java libpcsclite1

# COMMAND ----------

# MAGIC %md
# MAGIC ## Manually Install OpenJDK 8 jre/jdk
# MAGIC 
# MAGIC There's some issue at the moment installing OpenJDK 8 headless so I've manually downloaded the deb packages and install them like so. Hopefully in future this "just works" once Ubuntu 20.04 has fixed up whatever issue is preventing it.

# COMMAND ----------

# MAGIC %sh
# MAGIC wget http://security.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jre-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb
# MAGIC wget http://security.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jdk-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb

# COMMAND ----------

# MAGIC %sh
# MAGIC dpkg -i 'openjdk-8-jre-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb'
# MAGIC dpkg -i 'openjdk-8-jdk-headless_8u362-ga-0ubuntu1~20.04.1_amd64.deb'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Switch Version of Java
# MAGIC 
# MAGIC We also need to change the version of Java via the alternatives command to one which will enable our Hail build.

# COMMAND ----------

# MAGIC %sh
# MAGIC readlink -f `which java`

# COMMAND ----------

# MAGIC %sh
# MAGIC update-alternatives --set java $(update-alternatives --list java | grep java-8-openjdk)

# COMMAND ----------

# MAGIC %sh
# MAGIC update-alternatives --list java | grep java-8-openjdk

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build Hail
# MAGIC 
# MAGIC Now that our system is setup with dependencies, we can build Hail.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp
# MAGIC git clone https://github.com/hail-is/hail.git

# COMMAND ----------

# MAGIC %sh
# MAGIC JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# MAGIC PATH=$JAVA_HOME/bin/java:$PATH
# MAGIC C_INCLUDE_PATH=$JAVA_HOME/include
# MAGIC export JAVA_HOME PATH C_INCLUDE_PATH
# MAGIC cd /tmp/hail/hail
# MAGIC make install-on-cluster HAIL_COMPILE_NATIVES=1 SCALA_VERSION=2.12.13 SPARK_VERSION=3.3.2

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp/hail
# MAGIC cp ./hail/build/libs/hail-all-spark.jar /dbfs/hail/hail-all-spark.jar
# MAGIC cp ./hail/build/deploy/dist/hail-0.2.112-py3-none-any.whl /dbfs/hail/hail-0.2.111-py3-none-any.whl
