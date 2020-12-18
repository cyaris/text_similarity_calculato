# text_similarity_calculator

Run main.py and you will be prompted to enter two texts.
<br/>
<br/>
Once provided, the file will return an overall score on on text similarity.
<br/>
<br/>
Text similarity will be calculated as follows:
<br/>
- The numerator is the summation of the total words in each exact match phrase squared.
<br/>
- The denominator is the total words between both lists squared. 
  - This includes single word phrases (regular overlapping words). The idea here is that the same words in a totally different order should get credit, but nowhere near as much credit as the same words in the same order.
<br/>
<br/>
See the code inside main.py for further explanation.
