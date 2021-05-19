# požene 40 iteracij z multiprocessingom
# ostale argse nastaviš v args.py

#Files used:
# executeEpisode.py - požene epizode same s seboj na multiprocess
# learn.py - teach nn with data

# sprva mormo prpraut površino
echo "starting learning process.."
python3 load.py
for iteration in {1..100}
do
    echo "Iteration ($iteration)"
    python3 executeEpisodes.py -i $iteration
    echo "learning"
    python3 learn.py -i $iteration
done
echo "FINISHED"