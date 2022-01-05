#!/bin/csh
#PBS -A WPrAFITO44063OPS
#PBS -q standard
#PBS -l select=2:ncpus=48:mpiprocs=48
#PBS -l walltime=48:00:00
#PBS -N 011-attack
#PBS -o OUT-011-attack
#PBS -e ERROR
#PBS -j oe
#PBS -m be
##PBS -M dolezal127@gmail.com

cd $HOME/attack-011-surface

source $MODULESHOME/init/csh

module load cseinit
module load cse/python3
module load VASP

setenv VASP_NPROCS 96

vasp
