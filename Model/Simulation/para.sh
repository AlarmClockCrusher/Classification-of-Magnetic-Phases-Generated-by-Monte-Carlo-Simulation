#PBS -N paraGen
#PBS -l walltime=10:00:00
#PBS -l nodes=1:ppn=11
#PBS -l mem=55000MB
#PBS -j oe

module load python/3.6-conda5.2
python -u /users/PAS1495/gsdbuilder/FinalProject/Paragenerate.py 11 > /users/PAS1495/gsdbuilder/FinalProject/PhaseDiagram_2.log
