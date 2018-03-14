#!/bin/bash

NS_DIR="/homesim/dbrilhante/svn/ns-allinone-3.24/ns-3.24"
PREFIX="sector-norelief"

DIR="/homesim/dbrilhante/outputs/power_eff_nodes"

WAF_COMMAND="./waf --run"

#Trocar pelo nome do seu script
SCRIPT_COMMAND="python ../triangulation/relay.py"

#N_BEAMS=(4 8 16 32)
NNODES=`seq 5 5 25` #`seq -f%02.f 5 5 25`

BEAMS=(4 8 16 32)

MEAND=2 #(0 2 5) #`seq 0 1 5` #(-1 0 0.75 1.5 2.25 3) #`seq 0 0.75 3`  #(-1 0 0.4 0.8 1.2 1.6) #`seq 0 0.4 1.6`
MEANA=2 #(0 2 4) #`seq 0 1 4` #(-1 0 45 90 135 180) #`seq 0 45 180` #(-1 0 5 10 15 20) #`seq 0 5 20`

RELIEF=0

NPEOPLE=`seq 5 1 10`

RUNS=`seq 1 1 30`



DATE=`date +%H-%M-%S-%d-%m-%y`
touch /home/davi/log-$DATE
mkdir /home/davi/outputs/$DATE
OUTDIR="/home/davi/outputs/$DATE"
if [ $1 == "SUBMIT" ]
then
	for nnodes in $NNODES
	do
		for nbeams in ${BEAMS[@]}
		do
			for meand in ${MEAND[@]} #$MEAND
			do
				for npeople in ${NPEOPLE[@]} #$MEANA
				do
					for runs in $RUNS
					do
						OUT_FILENAME="${DIR}/outl/${PREFIX}_roomside${room_side}_nnodes${n_nodes}_${alpha}_run${run}.out"

						if [ -f $OUT_FILENAME ]
						then
							continue
						fi
						echo "$SCRIPT_COMMAND $nnodes $nbeams $meand $MEANA $RELIEF $npeople $runs\""
						#$WAF_COMMAND "$SCRIPT_COMMAND --roomSide=$room_side --nNodes=$n_nodes --alpha=$alpha --seed=$runs"
						$SCRIPT_COMMAND $nnodes $nbeams $meand $MEANA $RELIEF $runs $npeople> $OUTDIR/$nnodes-$nbeams-$meand-$MEANA-$npeople-$runs

					done
				done
			done
		done
	done
fi
