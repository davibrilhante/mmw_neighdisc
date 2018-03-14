#!/bin/bash

#Qual sera meu dir?
#Localmente:
#NS_DIR="/root/repos/ns-3-allinone/ns-3-dev"
#Remotamente:
NS_DIR="/homesim/dbrilhante/svn/ns-allinone-3.24/ns-3.24"
PREFIX="sector-norelief"

#Qual sera meu dir?
#Localmente:
#DIR="/home/davi/Documents/Mestrado/codes"
#Remotamente
DIR="/homesim/dbrilhante/outputs/power_eff_nodes"

WAF_COMMAND="./waf --run"

#Trocar pelo nome do seu script
SCRIPT_COMMAND="python ../triangulation/relay.py"

#N_BEAMS=(4 8 16 32)
NNODES=`seq 5 5 25` #`seq -f%02.f 5 5 25`

BEAMS=(4 8 16 32)

MEAND=(0 2 5) #`seq 0 1 5` #(-1 0 0.75 1.5 2.25 3) #`seq 0 0.75 3`  #(-1 0 0.4 0.8 1.2 1.6) #`seq 0 0.4 1.6`
MEANA=(0 2 4) #`seq 0 1 4` #(-1 0 45 90 135 180) #`seq 0 45 180` #(-1 0 5 10 15 20) #`seq 0 5 20`

RELIEF=0

RUNS=`seq 1 1 30`

DATE=`date +%H-%M-%S-%d-%m-%y`
touch /home/davi/log-$DATE
mkdir /home/davi/outputs/$DATE
OUTDIR="/home/davi/outputs/$DATE"
if [ $1 == "SUBMIT" ]
then
	#cd $NS_DIR
	#for i in `seq 1 1 $N_PROTOCOLS`
	#do
		#protocol_nsname=`echo $PROTOCOL_NSNAMES | awk '{print $'$i'}'`
		#protocol_name=`echo $PROTOCOL_NAMES | awk '{print $'$i'}'`

		#for j in `seq 1 1 $N_RATE_MANAGERS`
		#do
		#	rate_manager_nsname=`echo $RATE_MANAGER_NSNAMES | awk '{print $'$j'}'`
		#	rate_manager_name=`echo $RATE_MANAGER_NAMES | awk '{print $'$j'}'`
			#echo $rate_nsname $rate_name

			# adaptive relay
			#for n_beams in $N_BEAMS
			#do
				for nnodes in $NNODES
				do
					for nbeams in ${BEAMS[@]}
					do
						for meand in ${MEAND[@]} #$MEAND
						do
							for meana in ${MEANA[@]} #$MEANA
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
									$SCRIPT_COMMAND $nnodes $nbeams $meand $meana $RELIEF $runs > $OUTDIR/$nnodes-$nbeams-$meand-$meana-$runs

									#echo "$WAF_COMMAND \"$SCRIPT_COMMAND --experiment_duration=$EXPERIMENT_DURATION --protocol=$protocol_nsname --rate_manager=$rate_manager_nsname --prim_dist=$dist --sec_dist=$sec_dist --enable_relay=1 --enable_adaptive=1 --relay_eval_duration=$eval_duration --relay_eval_interval=$EVAL_INTERVAL --run=$run\""
									#qsub -o $OUT_FILENAME -e /dev/null -V -b y -cwd -shell n $WAF_COMMAND "$SCRIPT_COMMAND --experiment_duration=$EXPERIMENT_DURATION --protocol=$protocol_nsname --rate_manager=$rate_manager_nsname --prim_dist=$dist --sec_dist=$sec_dist --enable_relay=1 --enable_adaptive=1 --relay_eval_duration=$eval_duration --relay_eval_interval=$EVAL_INTERVAL --run=$run --verbose=0"
								done
							done
						done
					done
				done
			#done
		#done
	#done
fi
