./CL_Master.sh M

for i in {1..10}
do
./CL_Master.sh P
done

for i in {1..10}
do
    ./CL_Master.sh M
done

./CL_Master.sh L
