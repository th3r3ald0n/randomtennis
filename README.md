TL;DR: Use random sampling to calculate probabililties of winning tennis matches based on constant and alternating probabilities of winning a (service) game. For example, what is the outcome of a match in which player 1 scores 60% of points during his serve and player 2 scores 55% of points during his serve? 

__New ideas, features, error spotting and improvements are all very much appreciated. 
Thank you!__
 

# How does a tennis player's probability of winning a single point affect his probability of winning the match?

Considering a simplified version of tennis with points, games and sets (no tie-break), 
and the players 1 and 2. 
For player 1, let $p$ be the probability of winning a single point which stays constant during the whole match. 

## What is the probability of winning a game? 

Tennis point count: 0, 15, 30, 40, (A), Game

Winning a game of tennis can be achieved by winning a game point after:
- 40-0
- 40-15
- 40-30
- A-40

Adding the probability for the four cases returns the overall probability of winning a game. 

- 40-0: Player 1 wins four points in a row. $p^4$
- 40-15: 
  - First, player 1 wins three points and player 2 wins one point. $\binom{4}{1} \cdot p^3 \cdot (1-p)$
  - Then, player 1 wins another point. $p$
  - Together, $\binom{4}{1} \cdot p^3 \cdot (1-p) \cdot p = 4 \cdot p^4 \cdot (1-p)$
- 40-30: $\binom{5}{2} \cdot p^3 \cdot (1-p)^2 \cdot p = 10 \cdot p^4 \cdot (1-p)^2$
- Deuce: 
  - First, player 1 and player 2 need to arrive at deuce. $\binom{6}{3} \cdot p^3 \cdot (1-p)^3$
  - To win, you have win two points in a row. $\frac{p^2}{p^2 + (1-p)^2}$
  - Together, $\binom{6}{3} \cdot p^3 \cdot (1-p)^3 \cdot \frac{p^2}{p^2 + (1-p)^2}$

Adding all cases is the overall probability of player 1 winning a game. 

## Why do we do this? 
Using this approach, we can calculate the winning chances for sets and the whole match, too. 
No random sampling needed. In fact, here is a nice [article](https://datagenetics.com/blog/august12018/index.html) (no affiliations) which goes in depth on that. 

However,...

## ...what about alternating probabilities of winning a game?
Now the interesting stuff. 
Probabilities of winning a game change with each service. 
When player 1 is serving, he might win points with 65% probability.
And when player 2 is serving, player 2 might win points with 60% probability.

How are the odds now? This is a simple task for random sampling. 

For more, see the Jupyter Notebook.
