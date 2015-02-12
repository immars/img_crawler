#

textfile=$1

awk -F'\t' '{print $1;}' $textfile | sort | uniq > name.txt 
awk -F'\t' '{print $2;}' $textfile | sort | uniq > material.txt 
awk -F'\t' '{print $3;}' $textfile | sort | uniq > collar.txt
awk -F'\t' '{print $4;}' $textfile | sort | uniq > pattern.txt
awk -F'\t' '{print $5;}' $textfile | sort | uniq > thickness.txt
awk -F'\t' '{print $6;}' $textfile | sort | uniq > style.txt
awk -F'\t' '{print $7;}' $textfile | sort | uniq > brand.txt
awk -F'\t' '{print $8;}' $textfile | sort | uniq > sleeve.txt
awk -F'\t' '{print $9;}' $textfile | sort | uniq > zipper.txt
awk -F'\t' '{print $10;}' $textfile | sort | uniq > shoe_head.txt
awk -F'\t' '{print $11;}' $textfile | sort | uniq > hell.txt
awk -F'\t' '{print $11;}' $textfile | sort | uniq > heel.txt
awk -F'\t' '{print $12;}' $textfile | sort | uniq > handle.txt

