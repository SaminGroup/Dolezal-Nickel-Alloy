#!/bin/csh
#PBS -A WPPAFITO44063OPS
#PBS -q debug
#PBS -l select=2:ncpus=48:mpiprocs=48
#PBS -l walltime=1:00:00
#PBS -N nbcl3-P4-test
#PBS -o OUT-nbcl3-P4-test
#PBS -e ERROR
#PBS -j oe
#PBS -m be
##PBS -M dolezal127@gmail.com

cd $HOME/relax-1

source $MODULESHOME/init/csh

module load cseinit
module load cse/python3
module load VASP

setenv VASP_NPROCS 96

vasp
