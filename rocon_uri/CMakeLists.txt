##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 2.8.3)
project(rocon_uri)

##############################################################################
# Catkin
##############################################################################

find_package(catkin REQUIRED)
catkin_package()

catkin_python_setup()

##############################################################################
# Installs
##############################################################################

install(DIRECTORY
  rules
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(
    PROGRAMS 
        scripts/rocon_uri
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )

##############################################################################
# Unit Tests
##############################################################################

if (CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(tests)
endif()
