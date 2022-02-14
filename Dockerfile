# 11/04/20 - latest OPERA version supports 3.6 
FROM python:3.6-slim
# FROM python:2.7-slim

# Install requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ENV OPERA_EXE_PATH=/usr/local/bin/OPERA/application/run_OPERA.sh
ENV MATLAB_RUNTIME_PATH=/usr/local/MATLAB/MATLAB_Runtime/v94
ENV LD_LIBRARY_PATH=.:/usr/local/MATLAB/MATLAB_Runtime/v94/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/sys/opengl/lib/glnxa64
ENV XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Runtime/v94/X11/app-defaults
ENV IS_LINUX=True

RUN	mkdir -p /usr/share/man/man1 && \
	apt-get update && \
	apt-get install -y openjdk-11-jre unzip wget

# Installs Matlab MCR:
RUN mkdir -p /src/matlab && \
	cd /src/matlab/ && \
	wget https://ssd.mathworks.com/supportfiles/downloads/R2018a/deployment_files/R2018a/installers/glnxa64/MCR_R2018a_glnxa64_installer.zip && \
	unzip MCR_R2018a_glnxa64_installer.zip && \
	./install -mode silent -agreeToLicense yes

# Installs OPERA:
RUN cd /src/ && \
	wget https://github.com/kmansouri/OPERA/releases/download/v2.6-beta2/libOPERA2.6_Py.tar.gz && \
	tar xzf libOPERA2.6_Py.tar.gz && \
	rm libOPERA2.6_Py.tar.gz && \
	cd libOPERA2_Py/ && \
	python setup.py install

COPY . /src/operaws

# Fix for running OPERA first time throwing "missing/wrong path in OPERA_installdir.txt" error.
# Running OPERA once then creating the file with the path fixes this issue.
RUN	mkdir -p /root/.mcrCache9.4/libOPE0/ && \
	python /src/operaws/opera_cli.py init && \
	echo "/src/libOPERA2_Py" > /root/.mcrCache9.4/libOPE0/OPERA_installdir.txt

WORKDIR /src/operaws

CMD ["waitress-serve", "--port=3344", "opera_flask:app"]