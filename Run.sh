python -c "from messenger import text_notification; text_notification('Starting Runs')"

#for i in {1..20}
#do
#    ./CL_Heuristic.sh M
#done

#python -c "from messenger import text_notification; text_notification('Finished M')"

for i in {1..10}
do
   ./CL_PMaster.sh P
done

python -c "from messenger import text_notification; text_notification('Finished P')"

for i in {1..10}
do
  ./CL_PMaster.sh S
done

python -c "from messenger import text_notification; text_notification('Finished S')"
