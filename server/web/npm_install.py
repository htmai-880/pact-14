import subprocess

###############INSTALL NVM#######################
command_line = "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash"
p = subprocess.Popen(command_line.split())
p.wait()
print(p)

##############INSTALL NODEJS ON SESSION######################
command_line = "nvm install 15"
p = subprocess.Popen(command_line.split())
p.wait()
print(p)
##############INSTALL NPM MODUILES###########################
command_line = "npm install"
p = subprocess.Popen(command_line.split())
p.wait()
print(p)
