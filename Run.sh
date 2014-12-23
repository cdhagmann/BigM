for i in {1..10}
do
    ./CL_PMaster.sh S
done

#for i in {1..10}
#do
#    ./CL_PMaster.sh P
#done

for i in {1..5}
do
    ./CL_Heuristic.sh M
done

./CL_Heuristic.sh L
