ARG ARCH=

FROM ${ARCH}rust:1.62.1 as builder
WORKDIR /root
RUN rustup component add rustfmt
RUN git clone https://github.com/dtn7/dtn7-rs  && cd dtn7-rs && \
    cargo install --locked --bins --examples --root /usr/local --path examples && \
    cargo install --locked --bins --examples --root /usr/local --path core/dtn7


FROM ${ARCH}golang:1.19 as gobuilder

ARG wtfversion=v0.41.0

RUN git clone https://github.com/wtfutil/wtf.git $GOPATH/src/github.com/wtfutil/wtf && \
    cd $GOPATH/src/github.com/wtfutil/wtf && \
    git checkout $wtfversion

ENV GOPROXY=https://proxy.golang.org,direct
ENV GO111MODULE=on
ENV GOSUMDB=off

WORKDIR $GOPATH/src/github.com/wtfutil/wtf

ENV PATH=$PATH:./bin

RUN make build && \
    cp bin/wtfutil /usr/local/bin/


FROM ${ARCH}gh0st42/coreemu-lab

COPY --from=builder /usr/local/bin/* /usr/local/bin/
COPY --from=gobuilder /usr/local/bin/* /usr/local/bin/

COPY scripts/dtn7-* /usr/local/bin/

RUN mkdir -p /root/.core/myservices && mkdir -p /root/.coregui/custom_services && mkdir -p /root/.coregui/icons
COPY core_services/* /root/.core/myservices/
COPY coregui/config.yaml /root/.coregui/
COPY coregui/icons/* /root/.coregui/icons/
COPY configs/dtn7.yml /root/

COPY scripts/entrypoint.sh /entrypoint.sh

# Base on https://github.com/dusty-nv/jetson-containers/blob/e8a040/Dockerfile.ros.humble

# Install ROS2 Humble
ARG ROS_PKG=ros_base
ENV ROS_DISTRO=humble
ENV ROS_ROOT=/opt/ros/${ROS_DISTRO}
ENV ROS_PYTHON_VERSION=3

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL /bin/bash
SHELL ["/bin/bash", "-c"] 

WORKDIR /tmp


# set Python3 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

#
# add the ROS deb repo to the apt sources list
#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        gnupg2 \
        lsb-release \
        ca-certificates \
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# change the locale from POSIX to UTF-8
RUN locale-gen en_US en_US.UTF-8 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

#
# install development packages
#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        libbullet-dev \
        libpython3-dev \
        python3-colcon-common-extensions \
        python3-flake8 \
        python3-pip \
        python3-numpy \
        python3-pytest-cov \
        python3-rosdep \
        python3-setuptools \
        python3-vcstool \
        python3-rosinstall-generator \
        libasio-dev \
        libtinyxml2-dev \
        libcunit1-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# install some pip packages needed for testing
RUN python3 -m pip install -U \
        argcomplete \
        flake8-blind-except \
        flake8-builtins \
        flake8-class-newline \
        flake8-comprehensions \
        flake8-deprecated \
        flake8-docstrings \
        flake8-import-order \
        flake8-quotes \
        pytest-repeat \
        pytest-rerunfailures \
        pytest

#
# upgrade cmake - this is needed to build some of the ROS2 packages
#
RUN pip3 install --upgrade --no-cache-dir --verbose cmake && cmake --version

#
# download/build ROS from source
#
ENV RTI_NC_LICENSE_ACCEPTED=yes
RUN mkdir -p ${ROS_ROOT}/src && \
    cd ${ROS_ROOT} && \
    
    # https://answers.ros.org/question/325245/minimal-ros2-installation/?answer=325249#post-id-325249
    rosinstall_generator --deps --rosdistro ${ROS_DISTRO} ${ROS_PKG} \
    rosbag2_storage_mcap \
    > ros2.${ROS_DISTRO}.${ROS_PKG}.rosinstall && \
    cat ros2.${ROS_DISTRO}.${ROS_PKG}.rosinstall && \
    vcs import src < ros2.${ROS_DISTRO}.${ROS_PKG}.rosinstall && \
    
    # https://github.com/dusty-nv/jetson-containers/issues/181
    rm -r ${ROS_ROOT}/src/ament_cmake && \
    git -C ${ROS_ROOT}/src/ clone https://github.com/ament/ament_cmake -b ${ROS_DISTRO} && \

    # add foxglove-bridge
    git -C ${ROS_ROOT}/src/ clone https://github.com/foxglove/ros-foxglove-bridge.git &&\

    # install dependencies using rosdep
    apt-get update && \
    cd ${ROS_ROOT} && \
    rosdep init && \
    rosdep update && \
    rosdep install -y \
        --ignore-src \
        --from-paths src \
        --rosdistro ${ROS_DISTRO} \
        --skip-keys "libopencv-dev libopencv-contrib-dev libopencv-imgproc-dev python-opencv python3-opencv" && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \

    # build it!
    colcon build \
        --merge-install \
        --packages-skip foxglove_bridge \
        --cmake-args -DCMAKE_BUILD_TYPE=Release && \

    # build foxglove_bridge as rclcpp is built now
    source ${ROS_ROOT}/install/setup.bash && \
    colcon build \
        --merge-install \
        --packages-select foxglove_bridge \
        --cmake-args -DCMAKE_BUILD_TYPE=Release && \

    # remove build files
    rm -rf ${ROS_ROOT}/src && \
    rm -rf ${ROS_ROOT}/logs && \
    rm -rf ${ROS_ROOT}/build && \
    rm ${ROS_ROOT}/*.rosinstall


EXPOSE 22
EXPOSE 8765
EXPOSE 50051

WORKDIR /shared

ENTRYPOINT [ "/entrypoint.sh" ]
