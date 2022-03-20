#!/bin/csh
#PBS -A WPPAFITO44063OPS
#PBS -q debug
#PBS -l select=2:ncpus=48:mpiprocs=48
#PBS -l walltime=1:00:00
#PBS -N nbcl2-P1
#PBS -o OUT-nbcl2-P1
#PBS -e ERROR
#PBS -j oe
#PBS -m be
##PBS -M dolezal127@gmail.com

cd $HOME/relax-2

source $MODULESHOME/init/csh

module load cseinit
module load cse/python3
module load VASP

setenv VASP_NPROCS 96

vasp
