
```
 python qrmine.py -i transcript.txt --codedict -n 5
 
 python qrmine.py -i transcript.txt --cat -n 20
  
 python qrmine.py -i transcript.txt --topics
 
 python qrmine.py -i transcript.txt --topics --assign -n 3

 python qrmine.py -i transcript.txt --codedict --cat -n 10

 python qrmine.py -i transcript.txt --sentiment

 python qrmine.py -i transcript.txt --summary


 
 python qrmine.py -i transcript.txt -t P7 --sentiment

 python qrmine.py -i transcript.txt -t P6 --cat -n 10

```

* Combine but not compare.

```
python qrmine.py -i transcript.txt -t P5 -t P7 --sentiment 

python qrmine.py -i transcript.txt -t P5 -t P7 --sentiment --sentence

python qrmine.py -i transcript.txt -t P5 -t P7 --sentiment --sentence --verbose

```


```

 python qrmine.py --csv diabetes.csv -t Index -t Exercise -t Obesity -t Stress -t Outcome --nnet

 python qrmine.py --csv diabetes.csv --nnet -n 10

 python qrmine.py --csv diabetes.csv --svm

 python qrmine.py --csv diabetes.csv --kmeans

 python qrmine.py --csv diabetes.csv --kmeans -n 2

 python qrmine.py --csv diabetes.csv --knn -n 5 -r 733

python qrmine.py --csv diabetes.csv --pca -n 2

```


* --assign can only be used with --topics. --assign takes -n as top_n documents/topics