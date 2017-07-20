#!/bin/bash

#Qual sera meu dir?
#Localmente:
#NS_DIR="/root/repos/ns-3-allinone/ns-3-dev"
#Remotamente:
NS_DIR="/homesim/dbrilhante/svn/ns-allinone-3.24/ns-3.24"
PREFIX="awgn-norelief"

#Qual sera meu dir?
#Localmente:
#DIR="/home/davi/Documents/Mestrado/codes"
#Remotamente
DIR="/homesim/dbrilhante/outputs/power_eff_nodes"

WAF_COMMAND="./waf --run"

#Trocar pelo nome do seu script
SCRIPT_COMMAND="python ../triangulation/triangulation_sector.py"

#N_BEAMS=(4 8 16 32)
NNODES=`seq -f%02.f 10 20 50`

BEAMS=(4 8 16 32)

MEAND=(0 5) 
MEANA=`seq 0 2 4`
DEV=`seq 0.05 0.01 0.1`

RELIEF=0

RUNS=`seq 1 1 20`

DATE=`date +%H-%M-%S-%d-%m-%y`
touch /homesim/dbrilhante/log/mmw/log-$DATE
mkdir /homesim/dbrilhante/outputs/$PREFIX-$DATE
OUTDIR="/homesim/dbrilhante/outputs/$DATE"
if [ $1 == "SUBMIT" ]
then
	for nnodes in $NNODES
	do
		for nbeams in ${BEAMS[@]}
		do
			for meand in ${MEAND[@]} #$MEAND
			do
				for meana in ${MEANA[@]} #$MEANA
				do
					for dev in $DEV
					do
						for runs in $RUNS
						do
							OUT_FILENAME="${DIR}/outl/${PREFIX}_roomside${room_side}_nnodes${n_nodes}_${alpha}_run${run}.out"
							#OUT_FILENAME="${DIR}/out/${PREFIX}_${protocol_name}_${rate_manager_name}_relay1_adaptive1_d${eval_duration}_sdist${sec_dist}_${dist}_run${run}.out"
							#LOG_FILENAME="${DIR}/out/${PREFIX}_${protocol_name}_${rate_manager_name}_relay1_adaptive1_d${eval_duration}_sdist${sec_dist}_${dist}_run${run}.log"
							#if [ $leader == $chosen ]
							#then
							#	break
							#fi

							if [ -f $OUT_FILENAME ]
							then
								continue
							fi
							echo "$SCRIPT_COMMAND $nnodes $nbeams $meand $meana $RELIEF $runs\""
							#$WAF_COMMAND "$SCRIPT_COMMAND --roomSide=$room_side --nNodes=$n_nodes --alpha=$alpha --seed=$runs"
							qsub -q all.q -e /homesim/dbrilhante/log/mmw/log-$DATE -o /homesim/dbrilhante/outputs/$PREFIX-$DATE/$nnodes-$nbeams-$meand-$meana-$dev-$runs -V -b y -cwd -shell n  $SCRIPT_COMMAND $nnodes $nbeams $meand $meana $RELIEF $dev $runs

						done
					done
				done
			done
		done
	done
fi
