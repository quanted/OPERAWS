# 11/04/20 - latest OPERA version supports 3.6 
FROM python:3.6-slim
# FROM python:2.7-slim

# Install requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# ENV OPERA_EXE_PATH=/usr/local/bin/OPERA/application/run_OPERA.sh
# ENV MATLAB_RUNTIME_PATH=/usr/local/MATLAB/MATLAB_Runtime/v94
# ENV LD_LIBRARY_PATH=.:/usr/local/MATLAB/MATLAB_Runtime/v94/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/sys/opengl/lib/glnxa64
# ENV XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Runtime/v94/X11/app-defaults
# ENV IS_LINUX=True

# ENV OPERA_EXE_PATH=/usr/OPERA/application/run_OPERA.sh
ENV OPERA_EXE_PATH=/usr/local/bin/OPERA/application/run_OPERA.sh
ENV MATLAB_RUNTIME_PATH=/usr/local/MATLAB/MATLAB_Runtime/v99
ENV LD_LIBRARY_PATH=.:/usr/local/MATLAB/MATLAB_Runtime/v99/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v99/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v99/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v99/sys/opengl/lib/glnxa64
ENV XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Runtime/v99/X11/app-defaults
ENV IS_LINUX=True

RUN	mkdir -p /usr/share/man/man1 && \
	apt-get update && \
	apt-get install -y openjdk-11-jre unzip wget

# # Installs Matlab MCR:
# RUN mkdir -p /src/matlab && \
# 	cd /src/matlab/ && \
# 	wget https://ssd.mathworks.com/supportfiles/downloads/R2018a/deployment_files/R2018a/installers/glnxa64/MCR_R2018a_glnxa64_installer.zip && \
# 	unzip MCR_R2018a_glnxa64_installer.zip && \
# 	./install -mode silent -agreeToLicense yes

# Installs OPERA Python module:
# RUN cd /src/
RUN	wget https://github.com/kmansouri/OPERA/releases/download/v2.8.2/libOPERA2.8_Py.tar.gz
RUN	tar xzf libOPERA2.8_Py.tar.gz
RUN	rm libOPERA2.8_Py.tar.gz
RUN cd libOPERA2_Py/ && \
	./OPERA2.8_Py_mcr.install -mode silent -agreeToLicense yes
RUN cd /usr/local/bin/OPERA/application/ && \
	python setup.py install

# RUN	python setup.py install







# # Installs OPERA
# # RUN cd /src/
# RUN	wget https://github.com/kmansouri/OPERA/releases/download/v2.8.2/OPERA2.8_CL_mcr.tar.gz
# RUN	tar -xvzf OPERA2.8_CL_mcr.tar.gz
# RUN	rm OPERA2.8_CL_mcr.tar.gz
# RUN	cd OPERA2_CL_mcr/ && \
# 	./OPERA2.8_mcr_Installer.install -mode silent -agreeToLicense yes
# RUN cd / && \
# 	$OPERA_EXE_PATH $MATLAB_RUNTIME_PATH
# RUN mkdir -p /root/.mcrCache9.9/OPERA_0/
# RUN echo "/usr/OPERA/application" > /root/.mcrCache9.9/OPERA_0/OPERA_installdir.txt
# RUN echo "/usr/OPERA/application" > /root/.mcrCache9.9/OPERA_installdir.txt
# RUN rm -rf OPERA2_CL_mcr/
# # RUN apt-get autoremove
# # RUN apt-get clean
# RUN rm -rf /var/lib/apt/lists/*

# # TODO: Non-root user

COPY . /src/operaws

# # # Fix for running OPERA first time throwing "missing/wrong path in OPERA_installdir.txt" error.
# # # Running OPERA once then creating the file with the path fixes this issue.
# # RUN	mkdir -p /root/.mcrCache9.4/libOPE0/ && \
# # 	python /src/operaws/opera_cli.py init && \
# # 	echo "/src/libOPERA2_Py" > /root/.mcrCache9.4/libOPE0/OPERA_installdir.txt

WORKDIR /src/operaws

CMD ["waitress-serve", "--port=3344", "opera_flask:app"]