= Installation =
== Nginx ==
 location / {
   rewrite ^/(downloads|about)$    /?p=$1 break;
 }

= Credits =
== Wikt2Dict ==
@InProceedings{acs-pajkossy-kornai:2013:BUCC,  
  author    = {Acs, Judit  and  Pajkossy, Katalin  and  Kornai, Andras},  
  title     = {Building basic vocabulary across 40 languages},  
  booktitle = {Proceedings of the Sixth Workshop on Building and Using Comparable Corpora},  
  month     = {August},  
  year      = {2013},  
  address   = {Sofia, Bulgaria},  
  publisher = {Association for Computational Linguistics},  
  pages     = {52--58},  
  url       = {http://www.aclweb.org/anthology/W13-2507}  
}  
