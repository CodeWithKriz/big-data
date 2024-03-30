# Install Apache Hadoop on Windows Subsystem for Linux (WSL) Ubuntu-22.04
Deploying Apache Hadoop on Windows Subsystem for Linux (WSL) Ubuntu-22.04 involves setting up the Hadoop ecosystem on a Linux environment that is running within the Windows operating system.

Below is a detailed guide on how to accomplish this

![wsl2](https://github.com/CodeWithKriz/data-engineering/assets/66562899/0978b7b8-b03b-4e68-8a02-3aa30bb1b25b)

# Setup Guide
## Step 1: Setup WSL & Install Ubuntu-22.04
Firstly, ensure that Windows Subsystem for Linux (WSL) is enabled on your Windows system. You can enable it through the Windows Features settings.

Once WSL is enabled, you need to install the Ubuntu-22.04 distribution from the Microsoft Store. This will provide you with a Linux environment to work with.

After installing Ubuntu-22.04, launch it and update the system packages to ensure you have the latest software versions <pre>sudo apt update
sudo apt upgrade</pre>

## Step 2: Install Java Development Kit
Once linux system is setup and all system packages are updated, run the following commands to setup Open JDK 11
1. install openjdk-11 for linux (debian) by running following command: <pre>sudo apt install openjdk-11-jdk</pre>
2. To verify java is installed successfully, run following command: <pre>java --version</pre>
![java-version](https://github.com/CodeWithKriz/data-engineering/assets/66562899/8396ae3a-fba5-436e-a64f-0c275d1543ec)
3. To get JAVA_HOME location, run following command: <pre>dirname $(dirname $(readlink -f $(which java)))</pre>
![java-home-location](https://github.com/CodeWithKriz/data-engineering/assets/66562899/92db4efd-05d3-4056-be1d-5651e2d5c4fe)

## Step 3: Create User for Hadoop
The user you create for Apache Hadoop will be utilized for running all Hadoop components, as well as for logging into Hadoop's web interface.
Run the following commands to create new user 
1. create new user named <strong>hadoop</strong>: <pre>sudo adduser hadoop</pre>
![new-user-hadoop](https://github.com/CodeWithKriz/data-engineering/assets/66562899/fd84e96e-27fe-4c72-ad37-d60e61b00a9c)
2. switch to new user <strong>hadoop</strong>: <pre>su - hadoop</pre>
![switch-user](https://github.com/CodeWithKriz/data-engineering/assets/66562899/cb3913ec-84ae-4679-a96c-c1d8243fba6a)
3. Generate SSH keypair to configure password-less SSH access for the newly created user: <pre>ssh-keygen -t rsa</pre>
4. Copy generated public key to the authorized key file and set the proper permissions: <pre>cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 640 ~/.ssh/authorized_keys</pre>
5. To test SSH access to localhost: <pre>ssh localhost</pre>
![ssh-localhost](https://github.com/CodeWithKriz/data-engineering/assets/66562899/f4e4dd0c-cb81-4a59-9a8b-67a6668a7598)

### Troubleshooting
You might experience SSH access issue "Connection refused" when attempting to connect to localhost port 22 through Windows Subsystem for Linux (WSL) using a new user for Hadoop <pre>ssh: connect to host localhost port 22: Connection refused</pre>

WSL does not start <strong>sshd</strong> automatically. To start ssh server try running the following commands:
1. remove ssh server: <pre>sudo apt remove openssh-server</pre>
2. install it again: <pre>sudo apt install openssh-server</pre>
3. start the server: <pre>sudo service ssh start</pre>
4. check the server status: <pre>sudo service ssh status</pre>

## Step 4: Install Hadoop on Ubuntu
After setting up Java and establishing a new user, proceed to obtain Apache Hadoop alongside its associated components like Hive, Pig, Sqoop, etc. The most recent version can be sourced from the official Hadoop download page. Ensure to acquire the binary archive, not the source code: https://hadoop.apache.org/

Run the following commands to setup hadoop
1. download hadoop binary archive from official page: <pre>wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz</pre>
2. move downloaded binary archive to $HOME location and extract archive: <pre>mv hadoop-3.3.6.tar.gz $HOME/
cd $HOME/
tar -xvzf hadoop-3.3.6.tar.gz</pre>
3. next, configure Hadoop and Java environment variables in .profile file. export following variables: <pre>export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=$HOME/hadoop-3.3.6
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"</pre>
4. load the above configuration in the current environment: <pre>source ~/.profile</pre>
5. JAVA_HOME variable needs to be configured in hadoop-env.sh file: <pre>nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh</pre>
![java-home-hadoop-env](https://github.com/CodeWithKriz/data-engineering/assets/66562899/6fdb556c-d331-455c-8be0-854f9a5d02bd)

In this demonstration, Hadoop version 3.3.6 is utilized. However, you have the flexibility to configure the setup according to your specific needs.

## Step 5: Configure Hadoop
Next step is to configure Hadoop configuration files available under etc directory.
1. first, create the <strong>namenode</strong> and <strong>datanode</strong> directories inside the Hadoop user home directory: <pre>cd $HOME
mkdir -p ~/hadoopdata/hdfs/namenode
mkdir -p ~/hadoopdata/hdfs/datanode</pre>
2. edit the core-site.xml file and update with your system hostname. Open the file in editor <pre>nano $HADOOP_HOME/etc/hadoop/core-site.xml</pre> Change the following name as per your system hostname: <pre>&lt;configuration&gt;
    &lt;property&gt;
        &lt;name&gt;fs.defaultFS&lt;/name&gt;
        &lt;value&gt;hdfs://localhost:9000</value&gt;
    &lt;/property&gt;
&lt;/configuration&gt;</pre> Save and close the file.
3. edit hdfs-site.xml file and change <strong>NameNode</strong> and <strong>DataNode</strong> directory paths as shown below: <pre>nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml</pre> Update the following directory paths: <pre>&lt;configuration&gt;
    &lt;property&gt;
        &lt;name&gt;dfs.replication&lt;/name&gt;
        &lt;value&gt;1&lt;/value&gt;
    &lt;/property&gt;
    &lt;property&gt;
        &lt;name&gt;dfs.namenode.name.dir&lt;/name&gt;
        &lt;value&gt;file:///home/hadoop/hadoopdata/hdfs/namenode&lt;/value&gt;
    &lt;/property&gt;
    &lt;property&gt;
        &lt;name&gt;dfs.datanode.data.dir&lt;/name&gt;
        &lt;value&gt;file:///home/hadoop/hadoopdata/hdfs/datanode&lt;/value&gt;
    &lt;/property&gt;
&lt;/configuration&gt;</pre> Save and close the file.
4. edit mapred-site.xml file: <pre>nano $HADOOP_HOME/etc/hadoop/mapred-site.xml</pre> Add the following changes: <pre>&lt;configuration&gt;
    &lt;property&gt;
        &lt;name&gt;mapreduce.framework.name&lt;/name&gt;
        &lt;value&gt;yarn&lt;/value&gt;
    &lt;/property&gt;
&lt;/configuration&gt;</pre> Save and close the file.
5. edit yarn-site.xml file: <pre>nano $HADOOP_HOME/etc/hadoop/yarn-site.xml</pre> Add the following changes: <pre>&lt;configuration&gt;
    &lt;property&gt;
        &lt;name&gt;yarn.nodemanager.aux-services&lt;/name&gt;
        &lt;value&gt;mapreduce_shuffle&lt;/value&gt;
    &lt;/property&gt;
&lt;/configuration&gt;</pre> Save and close the file.

## Step 6: Start Hadoop Cluster
Prior to initiating the Hadoop cluster, it's necessary to format the Namenode under the <strong>hadoop</strong> user.

1. Execute the command below to format the namenode: <pre>hdfs namenode -format</pre>
2. Upon successful formatting of the Namenode directory with the HDFS file system, you'll receive the confirmation message: "Storage directory /home/hadoop/hadoopdata/hdfs/namenode has been successfully formatted."
![hdfs-namenode-format](https://github.com/CodeWithKriz/data-engineering/assets/66562899/6266e402-da80-42b2-81f3-6e1c349ac060)
3. Subsequently, commence the Hadoop cluster by executing the following command: <pre>start-all.sh</pre>. You can verify the cluster processes by running <code>jps</code> command 
![hadoop-start-all](https://github.com/CodeWithKriz/data-engineering/assets/66562899/6f2a90f1-7436-472f-a4ee-231524e81025)
4. Once all the services have been initiated, you can access Hadoop at the following URL: http://localhost:9870.
![hadoop-cluster-url](https://github.com/CodeWithKriz/data-engineering/assets/66562899/10977436-8ca4-4909-aa3e-8f182d3bc2c2)
5. Additionally, the Hadoop application page is accessible at: http://localhost:8088.
![hadoop-application-url](https://github.com/CodeWithKriz/data-engineering/assets/66562899/55ba5cf2-e7c4-477b-9b17-87316f719e10)

To stop the Hadoop cluster just run the command: <pre>stop-all.sh</pre>

# Conclusion
Setting up Apache Hadoop on Windows Subsystem for Linux (WSL) might pose challenges for beginners, especially if they solely rely on the documentation. Fortunately, this article offers a comprehensive, step-by-step guide to simplify the process of installing Apache Hadoop on WSL. By following the instructions outlined here, you can ensure a smooth and hassle-free installation of Hadoop on your system.
