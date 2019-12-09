FROM python:3.7-slim

# Install requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ENV OPERA_EXE_PATH=/usr/local/bin/OPERA/application/run_OPERA.sh
ENV MATLAB_RUNTIME_PATH=/usr/local/MATLAB/MATLAB_Runtime/v94
ENV LD_LIBRARY_PATH=.:/usr/local/MATLAB/MATLAB_Runtime/v94/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v94/sys/opengl/lib/glnxa64
ENV IS_LINUX=True

COPY . /src
WORKDIR /src

RUN	mkdir -p /usr/share/man/man1 && \
	apt-get update && \
	apt-get install -y openjdk-11-jre unzip && \
	# apt-get install -y openjdk-11-jdk-headless wget unzip && \
	# update-alternatives --config java && \
	# wget https://github.com/kmansouri/OPERA/releases/download/v2.3-beta2/OPERA2.3_CL_mcr.tar.gz && \
	tar -xvzf OPERA2.3_CL_mcr.tar.gz && \
	rm OPERA2.3_CL_mcr.tar.gz && \
	cd OPERA2_CL_mcr/ && \
	./OPERA2.3_CL_mcr.install -mode silent -agreeToLicense yes && \
	cd / && \
	$OPERA_EXE_PATH $MATLAB_RUNTIME_PATH && \
	mkdir -p /root/.mcrCache9.4/OPERA_0/ && \
	echo "/usr/local/bin/OPERA/application" > /root/.mcrCache9.4/OPERA_0/OPERA_installdir.txt && \
	rm -rf OPERA2_CL_mcr/ && \
	rm -rf OPERA2.3_CL_mcr.tar.gz && \
	apt-get autoremove && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

EXPOSE 3344

CMD ["waitress-serve", "--port=3344", "wsgi_flask:app"]