FROM python:3.9-slim

RUN	mkdir -p /usr/share/man/man1 && \
	apt-get update && \
	apt-get install -y \
		openjdk-17-jre \
		unzip \
		wget

# Install requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt



#############################################################
# What about another base image that copies the one above???
#############################################################



ENV OPERA_EXE_PATH=/usr/local/bin/OPERA/application/run_OPERA.sh
ENV MATLAB_RUNTIME_PATH=/usr/local/MATLAB/MATLAB_Runtime/v912
ENV LD_LIBRARY_PATH=.:/usr/local/MATLAB/MATLAB_Runtime/v912/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v912/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v912/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v912/sys/opengl/lib/glnxa64
ENV XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Runtime/v912/X11/app-defaults
ENV IS_LINUX=True

# Installs OPERA Python module:
RUN	wget https://github.com/kmansouri/OPERA/releases/download/v2.9.1/libOPERA2.9_Py.tar.gz
RUN	tar xzf libOPERA2.9_Py.tar.gz
RUN	rm libOPERA2.9_Py.tar.gz
RUN cd libOPERA2_Py/ && \
	./OPERA2.9_Py_mcr.install -mode silent -agreeToLicense yes
RUN cd /usr/local/bin/OPERA/application/ && \
	python setup.py install

RUN rm /usr/local/MATLAB/MATLAB_Runtime/v912/java/jarext/log4j.*

# # TODO: Non-root user

COPY . /src/operaws

WORKDIR /src/operaws

CMD ["waitress-serve", "--port=3344", "opera_flask:app"]
