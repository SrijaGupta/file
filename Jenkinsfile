pipeline {
  agent any
  triggers {
    GenericTrigger(
     genericVariables: [[key: 'changed', value: '$.["commits"][*].modified[*]',  ,expressionType: 'JSONPath', regexpFilter: 'templates/'], 
                        [key: 'added',   value: '$.["commits"][*].added[*]',    expressionType: 'JSONPath', regexpFilter: 'templates/'],
                        ],
     token: 'sup3r_s3cr3t',
     printContributedVariables: true,
     printPostContent: true,
     silentResponse: false
    )
  }

  environment {
        ANSIBLE_BASE="./ansible"
        INVENTORY_FILE_PATH="${WORKSPACE}/ansible/inventory/cluster_inventory.inv"
        CONFIG_FRAGMENT_TEMPLATE_REPO_DIR="${WORKSPACE}"
        CONFIG_FRAGMENT_TEMPLATE_BASE_DIR="${CONFIG_FRAGMENT_TEMPLATE_REPO_DIR}/templates"
        ANSIBLE_HOST_KEY_CHECKING="False"
        COMMIT_DEVICE_INV_HOSTNAMES="${COMMIT_DEVICE_INV_HOSTNAMES}"
        NETDEV_DEVICE_IP_LIST="100.123.1.0 100.123.1.1 100.123.15.0 100.123.15.1 100.123.15.2 100.123.15.3"
        NETDEV_DEVICE_LOGIN_USERNAME="jcluser"
        NETDEV_DEVICE_CLI_USERNAME="jcluser"
        NETDEV_DEVICE_CLI_PASSWORD="Juniper!1"
        NETDEV_FABRIC_NAME="Fab1"
        ANSIBLE_CONFIG="/etc/ansible/ansible.cfg"
        DQNET_DEVICE_DATA_DIR="${WORKSPACE}/ansible" 
    }
  stages {
    stage('Group from Webhook Trigger ') {
      steps {
          script{
              catchError{
             // create .ssh dir if not present
             sh 'mkdir -p ${JENKINS_HOME}/.ssh'

             // generate rsa priv/publiv keys if not already there.
             sh(returnStdout: true, script: '''#!/bin/bash
                 if [ -e "${JENKINS_HOME}/.ssh/id_rsa" ];then
                    echo "ssh key present."
                 else
                     ssh-keygen -b 2048 -t rsa -N "" -q -f "${JENKINS_HOME}/.ssh/id_rsa" <<<y
                 fi
                 '''.stripIndent()
             )
             sh "export c=$changed"  
             sh "python -m pip install xlrd"
             sh "cd ${WORKSPACE}; touch file.txt"  
             sh "cd ${WORKSPACE};python resolving.py"
             groups = sh(returnStdout: true, script: 'cat file.txt')
                         
             sh "echo $groups"
             sh " echo changed files: + $changed + ' ' + added files : + $added "

                }
                }
            }  
        }
        
    stage('Keys Upload'){
        when {   expression { !fileExists("${WORKSPACE}/Keys_Uploaded.txt")} }
            steps{
                sh "cd ${WORKSPACE}/ansible;./run_netdev_junos_device_upload_authorized_keys.sh"
                sh "cd ${WORKSPACE}; touch Keys_Uploaded.txt"
                sh "cd ${WORKSPACE}; echo 'Successful' >> Keys_Uploaded.txt"
                
            }
        }

    stage('Inventory Generate'){

        when {  expression { fileExists("${WORKSPACE}/Keys_Uploaded.txt") } }
            steps{
                //sh "echo ---------skipped Upload Keys-------------- "
                sh "ansible --version"
                sh "cd ${WORKSPACE}/ansible;./run_netdev_junos_inventory_gen.sh"
                sh " touch ${WORKSPACE}/ansible/result.txt"
            }
        }

    stage('Config Check Scripts') {
            steps{  
                script {
                    def stepsForParallel = [:]
                    def branches = [:]
                    branches = groups.split()
                    branches.each {
                        def stepName = "${it}"
                        stepsForParallel[stepName] = { ->           
                            sh "echo ansible-playbook -i host ${it}"
                            sh "export DEVICE_GROUP_NAME=${it};cd ${WORKSPACE}/ansible; ./run_netdev_junos_config_gen_commitcheck.sh"
                            sh "export DEVICE_GROUP_NAME=${it};cd ${WORKSPACE}/ansible; ./run_netdev_junos_config_diff_report.sh"
                            sh "cat ${WORKSPACE}/ansible/junos_config_diff/${it}/${it}_config_diff_report.yml >> ${WORKSPACE}/ansible/result.txt"
                            archiveArtifacts '**/result.txt'
                         }
                    }
                    parallel stepsForParallel
                }
            }
                    
            }
    stage("Enter Devices:") {
            steps {
                script {
                    def inputConfig
                    def userInput = input(
                            id: 'userInput', message: 'Enter the Devices:?',
                            parameters: [

                                    string(defaultValue: 'None',
                                            description: 'Enter the COMMIT_DEVICE_INV_HOSTNAME ',
                                            name: 'Config'),
                            ])
                    inputConfig = userInput?:''
                    sh "cd ${WORKSPACE};touch inputData.txt"
                    writeFile file: "inputData.txt", text: "${inputConfig}"
                    COMMIT_DEVICE_INV_HOSTNAME = sh(returnStdout: true, script: 'cat inputData.txt')
                   }
               }
            }
    stage("Config Deploy"){ 
            steps{
                script{
                sh "export COMMIT_DEVICE_INV_HOSTNAMES=${COMMIT_DEVICE_INV_HOSTNAME};cd ${WORKSPACE}/ansible; ./run_netdev_junos_config_gen_commit.sh --device-group-name vmx ${COMMIT_DEVICE_INV_HOSTNAMES} "
                 }
                }
           }
        } 
    }
