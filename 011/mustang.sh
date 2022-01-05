#!/bin/csh
#PBS -A WPrAFITO44063OPS
#PBS -q standard
#PBS -l select=2:ncpus=48:mpiprocs=48
#PBS -l walltime=10:00:00
#PBS -N 011
#PBS -o OUT_011
#PBS -e ERROR
#PBS -j oe
#PBS -m be
##PBS -M dolezal127@gmail.com

cd $HOME/011

source $MODULESHOME/init/csh

module load cseinit
module load cse/python3
module load VASP

setenv VASP_NPROCS 96

vasp
